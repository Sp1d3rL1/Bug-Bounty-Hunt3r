---
type: technique
category: new_method
derived_from_case: false
vuln_class: BOLA/IDOR
source_url: https://www.bountieshub.com/case/88
source_author: Bounties Hub / Intigriti
source_date: 2025-08-12
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: high
target_types:
  - Async job API
---

# Second-Order IDOR via Scheduled Jobs / Async Processing

## 核心思路

Trigger job with victim projectID then poll results for leaked cross-project data

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `BOLA/IDOR` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Async/queued processing bypasses synchronous authz; niche 2025-26 edge case
- 适用场景：Async job API
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。
- 测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。
- 重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。

## 适用目标画像

- Async job API

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Async/queued processing bypasses synchronous authz; niche 2025-26 edge case

## 手工验证流程（授权 / Lab only）

1. 确认 scope、禁止项、速率限制与是否允许该功能测试。
2. 准备至少两个自有测试账号；多租户场景准备两个 organization/workspace。
3. 先完整走通正常业务流，记录对象 ID、角色、状态、token、请求路径。
4. 只替换一个变量或一步状态，观察服务端响应和后续副作用。
5. 用最小必要数据证明影响；不读取、不导出第三方真实数据。
6. 建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。
7. 测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。
8. 重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。

## 可自动化部分

- 可自动化收集 endpoint、参数、对象 ID 形态、历史 URL、JS 中的隐藏 API。
- 可自动化做“候选点标记”和“差异对比”，但越权、支付、账号状态影响必须手工确认。

## 误报/失败条件

- 只有客户端表现异常，没有服务端影响。
- 只能影响当前自有账号，无法证明跨权限、跨租户、财务、数据或流程影响。
- 目标业务前提不存在，或服务端已做完整对象归属/状态校验。
- 来源帖子/案例缺少可验证链接时，需降级为 review_queue 并二次确认。

## 授权边界

仅用于授权项目、靶场或自有环境。禁止无授权扫描、凭证滥用、爆破、DoS、真实支付损害、读取第三方真实隐私数据或绕过平台规则。

## 报告 impact 角度

- 说明攻击者前提、受影响对象、服务端缺失的校验，以及可造成的数据访问、权限提升、财务损失、业务流程绕过或租户隔离破坏。
- 证据只保留最小必要截图/请求响应，并打码 token、cookie、PII、支付信息。

## 相关案例链接

- https://www.bountieshub.com/case/88

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

id: 25 title: Second-Order IDOR via Scheduled Jobs / Async Processing type: technique vuln_class: BOLA/IDOR author_date: Bounties Hub / Intigriti / 2025-08-12 source_url:
- [https://www.bountieshub.com/case/88](https://www.bountieshub.com/case/88)
one_line_trick: Trigger job with victim projectID then poll results for leaked cross-project data target_type: Async job API confidence: high tags: [second-order-idor, async-job, scheduled-processing]

## 核心思路
异步/定时任务（如 scheduled jobs）在后台处理请求时，使用提交的 projectID 加载数据，但未在处理阶段重新校验所有权。攻击者触发 job 后轮询自身结果，即可获取 victim 项目数据，实现 second-order IDOR。

## 前置条件
- API 存在异步任务队列（e.g. project export、report generation）。
- job 使用提交的 ID 加载跨项目数据，未在 worker 层重新 authz。
- 授权 Lab 或程序中可触发 job 并轮询结果。

## 完整技法细节
- 用 victim projectID 提交 job 创建请求（e.g. /schedule/export）。
- job 进入队列，后台处理时加载 victim 数据。
- attacker 轮询自身 job 结果（/jobs/myjob），获得泄露的 cross-project 数据。
：仅在自建 async API Lab 中触发，确认泄露但不实际导出/存储第三方数据。

## 适用目标画像
- 使用队列系统（RabbitMQ、Celery、AWS SQS）的 SaaS 平台。
- 项目管理、报表生成、批量处理类应用。
- 2025-2026 新兴 async-first 架构。

## 为什么有效
同步请求时 authz 有效，但异步 worker 仅依赖初始提交 ID，未重新绑定当前用户上下文；常见于微服务解耦场景。

## 手工验证流程（授权 / Lab only）
- Lab 中创建多个 project（attacker + victim）。
- attacker 提交带 victim projectID 的 job。
- 轮询 attacker job 结果，确认包含 victim 数据。
：仅 lab 读取 job 输出；禁止任何真实数据处理或持久化。

## 可自动化部分
- Python 脚本自动提交 job + 轮询结果。
- 可集成 Burp 宏实现 job ID 替换自动化。

## 误报/失败条件
- job worker 层强制重新校验当前用户所有权。
- job 结果严格隔离（仅返回提交者数据）。
- 队列使用加密/访问令牌绑定。

## 授权边界
仅限授权 Bug Bounty 程序或完全自控 Lab。禁止触发生产环境真实 job。边界：测试账号项目间读取，立即清理 Lab 队列。

## 报告 impact 角度
：异步处理导致跨项目数据泄露（High）。
：破坏项目隔离，可能暴露商业机密。
：High，强调“second-order 异步 authz 缺失”。

## 相关案例链接
- [https://www.bountieshub.com/case/88](https://www.bountieshub.com/case/88)

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/api.md -->
