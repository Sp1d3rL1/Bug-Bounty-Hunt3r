---
type: technique
category: trick
derived_from_case: false
vuln_class: GraphQL
source_url: https://x.com/theXSSrat/status/1936360659949691029
source_author: theXSSrat
source_date: 2025-06-21
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: medium
target_types:
  - GraphQL APIs
---

# GraphQL Introspection Batching for Data Leak/Abuse

## 核心思路

Enable": - /url: https://x.com/theXSSrat/status/1936360659949691029§GraphQL§Enable - text: introspection then batch queries or abuse authorization flaws

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `GraphQL` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Exposes excessive data or bypasses per-query auth in GraphQL endpoints
- 适用场景：GraphQL APIs
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 收集 schema、operation name、variables、node/id 解析路径和批量查询能力。
- 对同一对象分别测试 query、mutation、nested resolver、batching、alias 场景。
- 关注“列表受限但 node 直取未校验”“mutation 校验弱于 query”的差异。

## 适用目标画像

- GraphQL APIs

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Exposes excessive data or bypasses per-query auth in GraphQL endpoints

## 手工验证流程（授权 / Lab only）

1. 确认 scope、禁止项、速率限制与是否允许该功能测试。
2. 准备至少两个自有测试账号；多租户场景准备两个 organization/workspace。
3. 先完整走通正常业务流，记录对象 ID、角色、状态、token、请求路径。
4. 只替换一个变量或一步状态，观察服务端响应和后续副作用。
5. 用最小必要数据证明影响；不读取、不导出第三方真实数据。
6. 收集 schema、operation name、variables、node/id 解析路径和批量查询能力。
7. 对同一对象分别测试 query、mutation、nested resolver、batching、alias 场景。
8. 关注“列表受限但 node 直取未校验”“mutation 校验弱于 query”的差异。

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

- https://x.com/theXSSrat/status/1936360659949691029

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://x.com/theXSSrat/status/1936360659949691029](https://x.com/theXSSrat/status/1936360659949691029)
one_line_trick: Use introspection plus batching patterns to expose hidden schema paths and weak per-query authorization why_useful: Exposes excessive data or bypasses per-query auth in GraphQL endpoints target_type: GraphQL APIs confidence: high tags: [graphql, introspection, batching, data-leak, auth-bypass]
- **核心思路**
先通过introspection查询获取完整schema（包括隐藏字段/类型），再利用batching（数组查询或aliases）同时发送多个查询，测试/绕过per-query授权限制或批量泄露数据。
- **前置条件**
- 目标暴露GraphQL端点（通常 /graphql）。
- introspection未禁用（__schema查询返回200）。
- 授权Bug Bounty程序或自有GraphQL Lab环境。
- **完整技法细节**
- 发送introspection查询：{__schema{queryType{fields{name}}}}获取所有可用查询/类型/字段。
- 识别隐藏路径或敏感字段。
- 使用batching：POST JSON数组[{"query":"{user(id:1){...}}"}, {"query":"{user(id:2){...}}"}]。
- 或使用aliases批量同一查询不同参数。
- 测试authorization：检查是否每个query独立校验或batch级别绕过弱授权。
- **适用目标画像**
采用GraphQL API的后端服务，特别是未禁用introspection且授权检查粒度过细（per-query而非batch）的应用。
- **为什么有效**
GraphQL introspection默认暴露完整schema，batching/aliases允许一次性获取大量数据或绕过单query rate-limit/授权逻辑，导致数据滥用或泄露。
- **手工验证流程（授权 / Lab only）**
- 在授权BB或Lab GraphQL环境中确认introspection可用。
- 构造batch查询测试敏感字段。
- 验证是否返回额外数据或绕过单query auth。
- 使用测试数据，不涉及真实用户批量查询。
- **可自动化部分**
- GraphQL Voyager / Altair / Burp GraphQL插件自动introspection。
- 脚本生成batch查询测试载荷。
- ffuf或自定义工具fuzz字段+batch。
- **误报/失败条件**
- introspection被禁用（返回null或403）。
- 严格batch-level授权或query depth限制。
- 速率限制/ WAF拦截批量请求。
- **授权边界**
仅在授权范围内测试introspection和batching。禁止大规模真实数据枚举或生产环境滥用，仅演示潜在泄露。
- **报告 impact 角度**
- 暴露隐藏schema导致信息泄露或后续攻击链。
- 绕过授权批量读取敏感数据（PII、业务记录）。
- 违反GraphQL最佳实践，增加数据隐私风险。
- **相关案例链接**
- [https://x.com/theXSSrat/status/1936360659949691029](https://x.com/theXSSrat/status/1936360659949691029)
- GraphQL security checklists (common BB reports)

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/cors_postmessage_websocket.md -->

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->

<!-- backlink: docs/checklists/graphql.md -->

<!-- backlink: docs/checklists/prototype_pollution_xss_chain.md -->
