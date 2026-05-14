---
type: technique
category: evergreen
derived_from_case: false
vuln_class: IDOR
source_url: X post technical tips (real hunter)
source_author: @theXSSrat (X hunter)
source_date: 2025-01
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: high
target_types:
  - SaaS API
---

# Second-Order IDOR via Profile Update Affecting High-Privilege Module

## 核心思路

Update username field triggers secondary module using it without re-check

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `IDOR` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Niche second-order IDOR in SaaS user flows bypasses initial validation
- 适用场景：SaaS API
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。
- 测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。
- 重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。

## 适用目标画像

- SaaS API

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Niche second-order IDOR in SaaS user flows bypasses initial validation

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

- X post technical tips (real hunter)

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

# 核心思路
通过更新用户 Profile 中的关键字段（如 username），触发下游高权限模块（通知、仪表盘、权限同步等）使用更新后的值，而下游模块未重新校验原始所有者，导致跨用户影响。

# 前置条件
- 存在 Profile 更新接口（通常 PUT /profile 或类似）。
- 更新字段会被高权限/后台模块二次使用（如邮件通知、管理员视图、搜索索引）。
- 已授权 Lab 或 scope 内测试。

# 完整技法细节
- 用低权限用户 A 更新自身 username 为目标用户 B 的 username（或构造冲突值）。
- 触发下游模块（如“更新成功通知”或“同步到高权限面板”）。
- 若下游模块直接使用新 username 进行查询/操作而无 ownership re-check，即实现 second-order IDOR。
- 常见触发点：Profile 更新后自动同步到 Admin 模块或通知服务。

# 适用目标画像
SaaS 用户管理系统，尤其是包含 Profile 自助更新 + 内部高权限工作流（管理员面板、审计日志、通知中心）的平台。

# 为什么有效
第一层 Profile 更新有 auth 检查，但下游异步/二次处理模块假设“更新字段已合法”而未重新绑定用户上下文，形成时序 IDOR。

# 手工验证流程（授权 / Lab only）
- Lab 中创建用户 A（低权）和 B（高权）。
- 用户 A 更新 Profile 中的 username/email 为 B 的值。
- 触发下游模块（如刷新 Admin 面板或发送通知）。
- 验证是否影响 B 的高权限资源（仅观察响应/日志）。
- 记录完整请求链作为 PoC。

# 可自动化部分
- 使用 Burp Macro 模拟 Profile 更新 + 后续触发请求。
- 脚本监控更新接口后轮询高权限模块变化。

# 误报/失败条件
- 下游模块始终使用原始用户 ID 或 session 上下文。
- Profile 更新有严格唯一性校验或二次确认。
- 模块使用事务锁或缓存隔离。

# 授权边界
严格限定授权测试账号。禁止实际修改生产用户数据，仅在 Lab 验证效果。

# 报告 impact 角度
- 第二序 IDOR 导致高权限模块数据泄露或污染。
- 可能演变为账户接管或管理员视图绕过。
- 强调“用户流中隐藏的时序漏洞”。

# 相关案例链接
X post technical tips (real hunter) by @theXSSrat

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/api.md -->

<!-- backlink: docs/checklists/cors_postmessage_websocket.md -->

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->

<!-- backlink: docs/checklists/prototype_pollution_xss_chain.md -->
