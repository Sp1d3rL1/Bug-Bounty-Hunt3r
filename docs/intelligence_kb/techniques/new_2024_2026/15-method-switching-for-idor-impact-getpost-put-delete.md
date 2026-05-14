---
type: technique
category: new_method
derived_from_case: false
vuln_class: BOLA/IDOR
source_url: https://infosecwriteups.com/bug-bounty-bootcamp-34-idor-beyond-get-modifying-deleting-and-method-switching-for-maximum-159554377462
source_author: Aman Sharma
source_date: 2026-04-15
collected_at: 2026-05-05
freshness: 2026
confidence: high
risk_level: high
target_types:
  - REST API
---

# Method Switching for IDOR Impact (GET→POST/PUT/DELETE)

## 核心思路

Test ID swap not just in GET but POST/PUT/DELETE bodies for modify/delete

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `BOLA/IDOR` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Escalates info disclosure to destructive impact; common missed vector in BB
- 适用场景：REST API
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。
- 测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。
- 重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。

## 适用目标画像

- REST API

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Escalates info disclosure to destructive impact; common missed vector in BB

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

- https://infosecwriteups.com/bug-bounty-bootcamp-34-idor-beyond-get-modifying-deleting-and-method-switching-for-maximum-159554377462

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

id: 15 title: Method Switching for IDOR Impact (GET→POST/PUT/DELETE) type: technique vuln_class: BOLA/IDOR author_date: Aman Sharma / 2026-04-15 source_url:
- [https://infosecwriteups.com/bug-bounty-bootcamp-34-idor-beyond-get-modifying-deleting-and-method-switching-for-maximum-159554377462](https://infosecwriteups.com/bug-bounty-bootcamp-34-idor-beyond-get-modifying-deleting-and-method-switching-for-maximum-159554377462)
one_line_trick: Test ID swap not just in GET but POST/PUT/DELETE bodies for modify/delete target_type: REST API confidence: high tags: [idor-escalation, method-switching, impact-max]

## 核心思路
多数 API 仅在 GET 请求中对 ID 进行对象级授权校验，而忽略 POST/PUT/DELETE 方法中 body/query 中的 ID 参数。通过切换 HTTP 方法并在 body 中携带 victimID，可将信息泄露升级为修改/删除操作，实现更高 impact。

## 前置条件
- 目标 REST API 支持多种 HTTP 方法对同一资源路径操作。
- ID 参数同时出现在 query（GET）和 body（POST/PUT/DELETE）中。
- 授权环境/Lab 中存在至少两个用户账号。
- API 未对所有方法统一实施相同 auth 校验。

## 完整技法细节
- 确认 GET /resource/{id} 存在 IDOR（可读取 victim 数据）。
- 构造 POST/PUT/DELETE 请求至同一路径，在 body 中放入 {"id": "victim123", "newValue": "malicious"}。
- 切换方法后重放，观察是否成功修改/删除 victim 资源。
：仅在自建 API Lab 中测试，使用只读账号验证；禁止真实删除操作，仅确认响应 200 并返回修改确认（不实际持久化）。

## 适用目标画像
- 现代 REST API（尤其是 Node/Express、Spring、Laravel 等框架）。
- 资源管理型业务（如文档、配置、用户设置）。
- Bug Bounty 程序中常见“仅 GET 防护”的遗留端点。

## 为什么有效
开发者常假设 IDOR 只存在于读取场景（GET），忘记 CRUD 操作需统一 auth；框架路由器默认允许方法切换，而 auth middleware 未覆盖所有 verb。

## 手工验证流程（授权 / Lab only）
- Lab 环境中创建 attacker/victim 账号。
- 用 Burp 记录 GET IDOR 请求。
- 复制为 POST/PUT/DELETE，修改 body ID。
- 发送并确认更高 impact（仅 lab 读取修改结果）。
：严格限制为 Lab 测试；任何写操作必须在授权程序明确允许的测试账号内完成。

## 可自动化部分
- Burp Repeater + Macro 自动切换方法并替换 ID。
- ffuf / custom Python 脚本枚举方法 + payload。
- 可集成 ZAP 主动扫描规则检测 method-based IDOR。

## 误报/失败条件
- API 对所有 HTTP 方法统一强制相同 auth 中间件。
- 使用 GraphQL/REST 混合但 body schema 严格校验 ID 所有权。
- 服务器返回 405 Method Not Allowed。

## 授权边界
仅限授权 Bug Bounty 程序或完全自控 Lab。禁止任何真实修改/删除生产数据。边界：测试账号间操作，立即回滚 Lab 状态。

## 报告 impact 角度
：可未授权修改 victim 资源（High）。
：潜在删除导致服务中断（Critical）。
：Critical（当可删除/修改敏感数据时），强调“IDOR 从读取升级为破坏性操作”。

## 相关案例链接
- [https://infosecwriteups.com/bug-bounty-bootcamp-34-idor-beyond-get-modifying-deleting-and-method-switching-for-maximum-159554377462](https://infosecwriteups.com/bug-bounty-bootcamp-34-idor-beyond-get-modifying-deleting-and-method-switching-for-maximum-159554377462)

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/api.md -->
