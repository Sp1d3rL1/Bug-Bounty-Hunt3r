---
type: technique
category: trick
derived_from_case: false
vuln_class: IDOR
source_url: https://x.com/vuln_X/status/2050914267336265901
source_author: vuln_X
source_date: 2026-05-03
collected_at: 2026-05-05
freshness: 2026
confidence: high
risk_level: high
target_types:
  - Web APIs
---

# Nested JSON IDOR Bypass

## 核心思路

Wrap": - /url: https://x.com/vuln_X/status/2050914267336265901§IDOR§Wrap - text: "target ID as {\"Account\":{\"Account\":3333}} instead of plain swap

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `IDOR` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Bypasses outer auth validation while inner key executes business logic; scanners miss nested structs
- 适用场景：Web APIs
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。
- 测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。
- 重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。

## 适用目标画像

- Web APIs

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Bypasses outer auth validation while inner key executes business logic; scanners miss nested structs

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

- https://x.com/vuln_X/status/2050914267336265901

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://x.com/vuln_X/status/2050914267336265901](https://x.com/vuln_X/status/2050914267336265901)
tags: [idor, json-parser, api-bypass, saas] confidence: high

# 核心思路
将目标 ID 包裹成嵌套 JSON 对象（如 {"Account":{"Account":3333}}），利用外层认证校验与内层业务逻辑解析器不一致，实现 IDOR 绕过。扫描器通常仅处理标量值，忽略嵌套结构。

# 前置条件
- 目标 API 接受 JSON 请求体。
- 存在 ID 字段（如 Account ID），外层校验使用该键但业务逻辑深入解析内层同名键。
- 已授权 Lab 或 scope 内测试。

# 完整技法细节
- 正常请求示例：{"Account": 1111}
- 绕过请求：{"Account": {"Account": 3333}}
- 认证中间件仅校验外层 Account 键（匹配当前用户），而后端业务逻辑（如 ORM 查询或服务调用）使用内层 Account 值执行操作。
- 适用于 POST/PUT 等修改或查询接口。

# 适用目标画像
现代 SaaS Web API，尤其是 Node.js / Java / Go 等使用 JSON 反序列化的复杂后端系统。常见于账户、订单、配置等模块。

# 为什么有效
JSON 解析器与验证器在嵌套深度处理上的不一致：外层校验通过，内层键被业务代码直接提取使用。自动化扫描器默认不生成深层嵌套 测试载荷。

# 手工验证流程（授权 / Lab only）
- Lab 中创建两个测试账户 A 和 B。
- 用账户 A 登录，构造正常请求修改自身数据。
- 修改 测试载荷 为嵌套结构，目标 ID 指向账户 B。
- 观察是否成功影响 B 的数据（仅读/记录响应）。
- 使用 Burp 或 Postman 手动构造多层嵌套测试。

# 可自动化部分
- 自定义 Burp Intruder 或 ffuf 测试载荷 生成嵌套 JSON 变体。
- 脚本遍历常见键名进行嵌套包装。

# 误报/失败条件
- 后端使用严格 Schema 验证（如 JSON Schema）拒绝嵌套。
- 所有层级均使用相同上下文对象解析。
- 反序列化时展平或忽略重复键。

# 授权边界
仅限授权 Lab 或 Bug Bounty 明确 scope。禁止对真实用户数据进行任何修改操作。

# 报告 impact 角度
- 跨用户/租户数据修改或泄露。
- 绕过自动化防护，属于高隐蔽性 IDOR。
- 业务影响视模块而定（如账户接管、支付绕过）。

# 相关案例链接
- [https://x.com/vuln_X/status/2050914267336265901](https://x.com/vuln_X/status/2050914267336265901)
（vuln_X 原帖）

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/api.md -->
