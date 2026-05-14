---
type: technique
category: new_method
derived_from_case: false
vuln_class: Query + Circular Fragments
source_url: https://medium.com/@mpjani294/graphql-pentesting-for-bug-bounty-hunters-from-endpoint-discovery-to-high-impact-exploits-821f64a953b5
source_author: MPGODMATCH
source_date: 2025-11-15
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: low
target_types:
  - GraphQL with complex relations
---

# Circular Fragment + Recursive Query Abuse for DoS

## 核心思路

Define circular fragment on bidirectional relations (author { posts { author { ... } } }) with batching

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Query + Circular Fragments` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Creates infinite AST loops or deep recursion for DoS testing in BB
- 适用场景：GraphQL with complex relations
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 使用授权域名、组织名、公开仓库、证书、ASN、存储命名规律建立资产图。
- 对公开暴露只证明可访问性和最小元数据；不要下载大批量文件或读取敏感内容。
- 把 findings 关联回业务资产、权限边界或可利用路径，避免只报低价值暴露。

## 适用目标画像

- GraphQL with complex relations

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Creates infinite AST loops or deep recursion for DoS testing in BB

## 手工验证流程（授权 / Lab only）

1. 确认 scope、禁止项、速率限制与是否允许该功能测试。
2. 准备至少两个自有测试账号；多租户场景准备两个 organization/workspace。
3. 先完整走通正常业务流，记录对象 ID、角色、状态、token、请求路径。
4. 只替换一个变量或一步状态，观察服务端响应和后续副作用。
5. 用最小必要数据证明影响；不读取、不导出第三方真实数据。
6. 使用授权域名、组织名、公开仓库、证书、ASN、存储命名规律建立资产图。
7. 对公开暴露只证明可访问性和最小元数据；不要下载大批量文件或读取敏感内容。
8. 把 findings 关联回业务资产、权限边界或可利用路径，避免只报低价值暴露。

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

- https://medium.com/@mpjani294/graphql-pentesting-for-bug-bounty-hunters-from-endpoint-discovery-to-high-impact-exploits-821f64a953b5

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://medium.com/@mpjani294/graphql-pentesting-for-bug-bounty-hunters-from-endpoint-discovery-to-high-impact-exploits-821f64a953b5](https://medium.com/@mpjani294/graphql-pentesting-for-bug-bounty-hunters-from-endpoint-discovery-to-high-impact-exploits-821f64a953b5)
vuln_class: Query + Circular Fragments target_type: GraphQL with complex relations confidence: high type: technique tags: [graphql, recursion, query-complexity, lab-validation]

# Circular Fragment + Recursive Query Abuse for DoS
- **核心思路**
构建有界递归 fragment 或深度嵌套查询，验证 GraphQL 服务器是否正确实施 recursion-depth、query-cost 或复杂度控制，仅用于 Lab 环境的安全性评估。
- **前置条件**
- GraphQL endpoint 支持 fragment，且 schema 存在双向/嵌套关系字段（e.g. __schema、types、fields）。
- 仅限授权 Lab 或自有测试环境，严禁生产环境测试。
- **完整技法细节**
使用 bounded recursive fragment 测试解析器行为（非无限循环）：
```text
query {
__schema {
types {
fields {
type {
fields {
type {
fields {
name
}
}
}
}
}
}
}
}
```
逐步增加嵌套层数（5→10→20），观察响应时间、错误或超时，验证服务器是否拒绝高复杂度查询。
- **适用目标画像**
GraphQL API 包含复杂对象关系、未启用 Apollo/Hasura 等 query complexity 插件的后端服务。
- **为什么有效**
GraphQL 允许 fragment 复用与深度嵌套，许多服务器仅在 resolver 执行前进行有限解析，未对 AST 深度或成本进行严格限制，导致可被用于控制验证。
- **手工验证流程（授权 / Lab only）**
- 在授权 Lab 环境中使用 GraphQL 客户端发送有界递归查询。
- 从浅层开始逐步加深，监控 CPU/内存使用和响应。
- 记录服务器返回的 depth/complexity 错误或超时点。
- 立即停止，绝不在生产环境重复执行。
- **可自动化部分**
自定义脚本生成不同深度的递归查询模板；结合 GraphQL fuzzer 批量测试复杂度边界。
- **误报/失败条件**
- 服务器已启用 query complexity analyzer 或最大 depth 限制。
- Parser 层已实现 fragment 循环检测。
- 查询被 rate limiting 拦截。
- **授权边界**
仅限授权 Lab 或 Bug Bounty 程序明确允许的 GraphQL 测试环境。严禁任何可能导致生产 DoS 的操作。
- **报告 impact 角度**
- 缺失查询复杂度防护可能导致拒绝服务风险
- 服务器资源耗尽隐患
- 需加强 GraphQL 安全配置建议
- **相关案例链接**
- [https://medium.com/@mpjani294/graphql-pentesting-for-bug-bounty-hunters-from-endpoint-discovery-to-high-impact-exploits-821f64a953b5](https://medium.com/@mpjani294/graphql-pentesting-for-bug-bounty-hunters-from-endpoint-discovery-to-high-impact-exploits-821f64a953b5)

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/graphql.md -->
