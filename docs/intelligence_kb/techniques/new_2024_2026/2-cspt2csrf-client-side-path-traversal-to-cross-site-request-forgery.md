---
type: technique
category: new_method
derived_from_case: false
vuln_class: CSPT
source_url: https://blog.doyensec.com/2024/07/02/cspt2csrf.html
source_author: Maxence Schmitt (Doyensec)
source_date: 2024-07
collected_at: 2026-05-05
freshness: 2024
confidence: high
risk_level: low
target_types:
  - web app (SPA with fetch
  - XHR)
---

# CSPT2CSRF: Client-Side Path Traversal to Cross-Site Request Forgery

## 核心思路

Manipulate": - /url: https://blog.doyensec.com/2024/07/02/cspt2csrf.html§CSPT§Manipulate - text: client-side fetch paths with ../ to force same-origin requests to unintended endpoints

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `CSPT` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Bypasses CSRF protections in SPA frameworks by controlling request path without server changes; high-impact in authorized BB programs
- 适用场景：web app (SPA with fetch/XHR)
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 枚举 message listeners、URL fragment/query sink、client-side routing、sanitizer 配置和 trusted origins。
- 优先在本地或授权测试页面复现，真实项目只证明可控 sink 与安全影响。
- 关注 OAuth callback、embed/widget、support chat、docs preview 等富客户端功能。

## 适用目标画像

- web app (SPA with fetch
- XHR)

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Bypasses CSRF protections in SPA frameworks by controlling request path without server changes; high-impact in authorized BB programs

## 手工验证流程（授权 / Lab only）

1. 确认 scope、禁止项、速率限制与是否允许该功能测试。
2. 准备至少两个自有测试账号；多租户场景准备两个 organization/workspace。
3. 先完整走通正常业务流，记录对象 ID、角色、状态、token、请求路径。
4. 只替换一个变量或一步状态，观察服务端响应和后续副作用。
5. 用最小必要数据证明影响；不读取、不导出第三方真实数据。
6. 枚举 message listeners、URL fragment/query sink、client-side routing、sanitizer 配置和 trusted origins。
7. 优先在本地或授权测试页面复现，真实项目只证明可控 sink 与安全影响。
8. 关注 OAuth callback、embed/widget、support chat、docs preview 等富客户端功能。

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

- https://blog.doyensec.com/2024/07/02/cspt2csrf.html

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://blog.doyensec.com/2024/07/02/cspt2csrf.html](https://blog.doyensec.com/2024/07/02/cspt2csrf.html)
" vuln_class: "CSPT" one_line_trick: "Manipulate client-side fetch paths with ../ to force same-origin requests to unintended endpoints" why_useful: "Bypasses CSRF protections in SPA frameworks by controlling request path without server changes; high-impact in authorized BB programs" target_type: "web app (SPA with fetch/XHR)" confidence: "high" tags: ["bug-bounty", "csp t", "csrf", "spa", "client-side"]
- **核心思路**
在单页应用（SPA）中，前端JavaScript 常使用模板字符串或字符串拼接构造 API 请求路径（如 fetch(\\/api/${userControlledPath}`)）。攻击者通过在用户可控输入中注入 ../` 实现
- **客户端路径遍历**
（Client-Side Path Traversal），迫使浏览器向同一源的非预期端点发起请求。由于请求仍是 same-origin，会自动携带认证 Cookie、Authorization Header 等，绕过传统的 CSRF 防护（如 SameSite、CSRF Token 检查），实现状态修改操作。
- **前置条件**
- SPA 框架（React、Vue、Angular 等）中存在客户端动态路径拼接的 fetch/XHR 或动态 import；
- 用户可控输入（URL 参数、查询字符串、POST body 等）直接或间接影响请求路径；
- 目标端点存在但未对路径进行严格服务端校验（仅依赖 CSRF 防护）；
- 授权 Bug Bounty 程序或自建 Lab 环境。
- **完整技法细节**
- 发现客户端路径拼接点（Burp 或浏览器 DevTools 搜索 fetch、XMLHttpRequest、axios 等调用）。
- 构造 payload 如 ../../admin/delete-user 或 ..%2F..%2Fapi%2Fchange-email，让浏览器实际请求 /api/change-email。
- 利用 same-origin 特性，请求自动附带认证凭证，实现 CSRF 等效攻击。
- 可结合 CORS 错误或响应差异确认端点存在（Lab 验证时仅观察网络请求）。 （所有操作仅限授权环境或本地 Lab 搭建的 SPA 模拟环境）
- **适用目标画像**
- 使用现代 SPA 框架且 API 路径由前端动态拼接的 Web 应用；
- 存在敏感状态修改端点（如修改邮箱、密码重置、权限变更）；
- 依赖 SameSite Lax/Strict 或自定义 CSRF Token 但未对路径做服务端白名单的程序。
- **为什么有效**
传统 CSRF 防护假设请求路径由服务端完全控制，而客户端路径遍历让攻击者“伪造”了路径，请求仍保持 same-origin 特性，认证信息自动携带，绕过所有基于 Origin/Referer/SameSite 的防护。
- **手工验证流程（授权 / Lab only）**
- 在授权目标或自建 Lab SPA 中，找到路径拼接点。
- 使用浏览器 DevTools 或 Burp Repeater 构造带 ../ 的请求。
- 观察网络面板确认请求实际命中了非预期端点，并携带了认证 Cookie。
- 仅在 Lab 中触发状态变更（例如修改测试账号的邮箱），验证成功后立即回滚。
- 记录请求/响应截图作为报告证据。
- **可自动化部分**
- 使用 Burp CSPT Burp Extension 自动扫描客户端路径拼接点；
- 自写脚本遍历常见路径模式（如 ../../admin/*）并发送测试请求（仅 Lab）。
- **误报/失败条件**
- 服务端对路径进行规范化（normalize）或白名单校验；
- 请求路径受 CSP 或 fetch 模式限制（no-cors）；
- 端点本身要求额外参数或 CSRF Token 且路径校验严格。
- **授权边界**
仅在明确授权的 Bug Bounty 程序或完全自有 Lab 环境中测试。严禁对生产环境未授权端点进行任何状态修改操作。测试后立即通知程序方并提供 PoC 回滚方式。
- **报告 impact 角度**
- 高危：无需用户交互即可执行敏感操作（如账户接管、数据修改）；
- 可与 XSS 或开放重定向结合形成完整攻击链；
- 影响范围广，适用于大量现代 Web 应用。
- **相关案例链接**
- [https://blog.doyensec.com/2024/07/02/cspt2csrf.html](https://blog.doyensec.com/2024/07/02/cspt2csrf.html)
- Doyensec CSPT2CSRF Whitepaper（授权环境验证参考）

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/cors_postmessage_websocket.md -->

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->
