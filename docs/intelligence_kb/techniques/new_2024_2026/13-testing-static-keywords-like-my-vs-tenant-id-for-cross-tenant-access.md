---
type: technique
category: new_method
derived_from_case: false
vuln_class: Broken Access Control
source_url: https://www.intigriti.com/researchers/blog/hacking-tools/exploiting-broken-access-control-vulnerabilities
source_author: Intigriti BugQuest Researchers
source_date: 2026-03
collected_at: 2026-05-05
freshness: 2026
confidence: high
risk_level: high
target_types:
  - SaaS multi-tenant apps
---

# Testing Static Keywords Like 'my' vs Tenant ID for Cross-Tenant Access

## 核心思路

Replace 'my' keyword in /api/workspaces/my with victim tenant ID

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Broken Access Control` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Exploits lazy tenant isolation in workspace APIs for cross-org leaks
- 适用场景：SaaS multi-tenant apps
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。
- 测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。
- 重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。

## 适用目标画像

- SaaS multi-tenant apps

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Exploits lazy tenant isolation in workspace APIs for cross-org leaks

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

- https://www.intigriti.com/researchers/blog/hacking-tools/exploiting-broken-access-control-vulnerabilities

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://www.intigriti.com/researchers/blog/hacking-tools/exploiting-broken-access-control-vulnerabilities](https://www.intigriti.com/researchers/blog/hacking-tools/exploiting-broken-access-control-vulnerabilities)
" vuln_class: "Broken Access Control" one_line_trick: "Replace 'my' keyword in /api/workspaces/my with 另一测试租户ID" why_useful: "Exploits lazy tenant isolation in workspace APIs for cross-org leaks" target_type: "SaaS multi-tenant apps" confidence: "high" type: "technique" tags: ["bac", "multi-tenant", "idor", "tenant-isolation", "saas"]

### 核心思路
SaaS多租户API常用静态关键字“my”指代当前用户租户，但服务器端未严格校验，导致替换为另一测试租户ID即可跨租户访问其他组织工作区数据。

### 前置条件
- 目标SaaS为多租户架构（企业/组织工作区）。
- 已认证当前租户会话。
- 发现使用“my”关键字的API端点（如/api/workspaces/my）。

### 完整技法细节
- 捕获正常请求：GET /api/workspaces/my 返回当前工作区。
- 将“my”替换为已知另一测试租户ID（可从其他用户响应、枚举或OSINT获取）。
- 重放请求：/api/workspaces/{victim-tenant-id}。
- 观察是否返回另一测试租户的合成数据，确认跨租户访问。
- 类似关键字：me、current也可测试。

### 适用目标画像
- 多租户SaaS协作平台、工作区管理工具（如项目管理、CRM）。
- API使用懒加载租户隔离，未在每个请求中强制校验当前认证用户租户。

### 为什么有效
服务器将“my”解析为当前用户租户但未执行额外授权检查，导致直接对象引用（IDOR-like）在租户层面失效。

### 手工验证流程（授权 / Lab only）
- 在授权BB程序或自建多租户Lab中创建两个独立租户。
- 使用Burp Repeater修改“my”为另一租户ID。
- 确认响应返回跨租户数据。
- 立即停止，删除测试记录。
- 仅读取metadata，不下载真实数据。

### 可自动化部分
- Burp Intruder批量替换“my”/“me”为枚举的tenant ID列表。
- 自定义脚本监控API响应中的租户关键字。

### 误报/失败条件
- 服务器强制校验tenant ID属于当前认证用户。
- API使用JWT claims严格绑定租户。
- “my”被服务器端重写忽略输入。

### 授权边界
仅限授权Bug Bounty多租户SaaS。禁止任何跨租户数据读取/修改真实生产数据；仅Lab环境验证隔离失效。

### 报告 impact 角度
- 严重信息泄露：跨组织访问其他租户工作区数据，违反租户隔离。
- 合规影响：破坏多租户数据隔离，潜在GDPR/隐私违规。
- 业务影响：竞争对手数据暴露或内部信息泄露风险。

### 相关案例链接
Intigriti官方博客：
- [https://www.intigriti.com/researchers/blog/hacking-tools/exploiting-broken-access-control-vulnerabilities](https://www.intigriti.com/researchers/blog/hacking-tools/exploiting-broken-access-control-vulnerabilities)

<!-- GROK_EXPANSION_END -->
