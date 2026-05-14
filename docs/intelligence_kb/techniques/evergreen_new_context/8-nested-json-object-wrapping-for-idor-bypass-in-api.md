---
type: technique
category: evergreen
derived_from_case: false
vuln_class: IDOR
source_url: https://x.com/vuln_X/status/2050914267336265901
source_author: @vuln_X (X hunter)
source_date: 2026-05
collected_at: 2026-05-05
freshness: 2026
confidence: high
risk_level: high
target_types:
  - SaaS API
---

# Nested JSON Object Wrapping for IDOR Bypass in API

## 核心思路

Wrap": - /url: https://x.com/vuln_X/status/2050914267336265901§IDOR§Wrap - text: "ID as {\"Account\":{\"Account\":3333}} to evade outer validation but hit inner logic

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `IDOR` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Niche JSON trick evades scanners in complex modern SaaS APIs
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
- 本条技巧的价值点：Niche JSON trick evades scanners in complex modern SaaS APIs

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
tags: [idor, json, parser-mismatch, api, saas] confidence: high

# 核心思路
利用 JSON 对象嵌套包装目标 ID，制造解析器与验证器之间的不匹配。外层键通过认证检查，内层键被业务逻辑实际使用，从而实现 IDOR 绕过。

# 前置条件
- API 请求体为 JSON 格式。
- 存在 ID 相关参数，验证逻辑与业务执行逻辑对嵌套结构的处理不同。
- 已授权测试环境。

# 完整技法细节
- 标量替换通常被拦截：{"Account": 3333}
- 嵌套包装绕过：{"Account": {"Account": 3333}} 或更深层 {"Account": {"Account": {"Account": 3333}}}
- 部分框架（如某些 ORM 或自定义 binder）会优先取最内层同名键值。
- 可结合数组或多键测试进一步绕过。

# 适用目标画像
复杂 SaaS API，尤其是微服务架构下前端/后端解析不一致的现代 Web 应用。扫描器难以覆盖的边缘场景。

# 为什么有效
现代 API 常采用多层 JSON 处理管道，认证层浅层校验 + 业务层深度解析导致不一致。扫描器默认 测试载荷 缺乏此类嵌套变体。

# 手工验证流程（授权 / Lab only）
- 在授权 Lab 创建多用户测试数据。
- 登录用户 A，发送正常标量请求。
- 切换为嵌套 测试载荷，目标指向用户 B。
- 验证是否成功操作 B 的资源（仅记录日志，不执行破坏性动作）。
- 使用 Repeater 逐步增加嵌套层级测试。

# 可自动化部分
- Burp Suite Extensions 或自定义 Python 脚本生成嵌套 测试载荷 字典。
- 针对已知键名（如 userId、accountId）自动化包装。

# 误报/失败条件
- 严格的 JSON Schema / DTO 验证拒绝非标量类型。
- 后端统一使用展平后的 Map 或强类型绑定。
- 框架在反序列化时抛出重复键异常。

# 授权边界
仅在授权 Bug Bounty scope 或 Lab 环境中测试。所有操作必须在合法测试账号内完成。

# 报告 impact 角度
- 隐蔽 IDOR 绕过自动化检测。
- 潜在用户数据隔离破坏。
- 强调“扫描器盲区”提升报告专业性。

# 相关案例链接
- [https://x.com/vuln_X/status/2050914267336265901](https://x.com/vuln_X/status/2050914267336265901)
（@vuln_X 原帖）

<!-- GROK_EXPANSION_END -->
