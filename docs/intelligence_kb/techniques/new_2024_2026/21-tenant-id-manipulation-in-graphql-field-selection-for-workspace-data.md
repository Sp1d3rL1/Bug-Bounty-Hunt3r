---
type: technique
category: new_method
derived_from_case: false
vuln_class: GraphQL + IDOR
source_url: https://medium.com/
source_author: GraphQL Hunter
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: high
target_types:
  - SaaS GraphQL APIs
---

# Tenant ID Manipulation in GraphQL Field Selection for Workspace Data

## 核心思路

Select fields with other tenant workspace IDs in queries

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `GraphQL + IDOR` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Bypasses RBAC in multi-tenant workspace queries without resolver checks
- 适用场景：SaaS GraphQL APIs
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。
- 测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。
- 重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。

## 适用目标画像

- SaaS GraphQL APIs

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Bypasses RBAC in multi-tenant workspace queries without resolver checks

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

- https://medium.com/

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

# 核心思路
在多租户 SaaS 的 GraphQL API 中，通过查询字段选择或变量中替换/注入其他租户的 workspace/tenant ID，绕过 Resolver 层面的 RBAC 检查，直接访问属于其他工作区的数据。核心在于 GraphQL 的字段选择集（Field Selection Set）机制允许客户端指定任意字段/嵌套对象，而后端若未在每个 Resolver 中强制校验当前认证上下文的 tenant ID，即可实现跨租户数据泄露或操作。
# 前置条件
- 目标 API 为 GraphQL 端点（通常 `/graphql` 或类似）。
- 业务采用多租户架构，每个 workspace/tenant 由唯一 ID 隔离。
- 存在 workspace 相关查询（如 `workspace(id: "...") { ... }` 或嵌套字段），且 Resolver 未严格绑定当前用户 session 的 tenant 上下文。
- 已授权测试环境或自建 Lab（生产环境仅限明确 scope 内）。
# 完整技法细节
1. 枚举当前用户可见的 workspace ID（通过正常查询获取）。
2. 构造 GraphQL 查询，将字段参数或嵌套选择中的 ID 替换为其他租户的 workspace ID。
3. 示例查询（安全 Lab 测试用）：
query { workspace(id: "victim-tenant-workspace-id") { id name members { email } sensitiveData } }
```text
4. 若后端仅在顶层 Query 校验而非字段级 Resolver 校验，即可返回其他租户数据。
5. 变体：使用别名（aliases）或批量查询多个 tenant ID 进行枚举。
# 适用目标画像
SaaS 平台 GraphQL API，尤其是协作工具、项目管理、CRM 等多工作区产品（Notion-like、Slack-like、内部企业工具）。常见于使用 Apollo Server、GraphQL Java、Hasura 等框架但 authorization middleware 不完善的场景。
# 为什么有效
GraphQL 的声明式字段选择设计让客户端控制返回数据结构，但许多实现仅在入口处进行粗粒度 auth 检查，未在每个字段 Resolver 中重新绑定 tenant 上下文。tenant ID 作为业务键值而非严格授权边界，导致 IDOR 与 GraphQL 结合形成高危绕过。
# 手工验证流程（授权 / Lab only）
1. 在授权 Lab 环境中创建两个测试租户 A 和 B。
2. 用租户 A 用户登录，正常查询自身 workspace。
3. 修改查询中 workspace ID 为租户 B 的 ID，提交请求。
4. 观察响应是否返回租户 B 数据（仅记录响应，不进行任何修改操作）。
5. 使用 Burp Repeater 或 GraphQL Playground 反复测试字段级操纵。
6. 始终限制在 scope 内，仅读操作验证。
# 可自动化部分
- 使用 GraphQL introspection + Burp Suite / GraphQL Voyager 枚举所有 workspace 相关字段。
- 自定义脚本（Python + gql）批量替换 tenant ID 参数进行 fuzz。
- 注意：自动化仅限 Lab 环境，且需 rate-limit 控制。
# 误报/失败条件
- Resolver 已实现字段级 `@auth` directive 或 tenant 上下文注入。
- 查询使用严格的 `viewer` / `currentTenant` 根字段，无法直接指定外部 ID。
- 后端使用 DataLoader + batching 强制 tenant 隔离。
# 授权边界
严格限定于程序规则允许的 Bug Bounty scope 或自建 Lab 环境。禁止对生产环境任何未授权租户进行实际数据访问或修改。测试后立即删除 Lab 数据。
# 报告 impact 角度
- 跨租户数据泄露（PII、商业机密）。
- 违反多租户隔离原则，可能导致合规问题（GDPR 等）。
- 高危：若结合其他漏洞可实现完整 workspace 接管。
# 相关案例链接
https://medium.com/ （GraphQL Hunter 原帖）
参考多租户 GraphQL 隔离失败案例（如 Thrive Global GraphQL IDOR 链）
```

<!-- GROK_EXPANSION_END -->
