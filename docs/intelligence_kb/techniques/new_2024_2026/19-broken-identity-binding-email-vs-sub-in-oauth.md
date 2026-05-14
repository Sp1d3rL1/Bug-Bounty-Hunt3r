---
type: technique
category: new_method
derived_from_case: false
vuln_class: OAuth Identity Binding Flaw
source_url: (disclosed BB reports referenced)
source_author: Digvijay Gholase
source_date: 2025-05
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: high
target_types:
  - OAuth account linking systems
---

# Broken Identity Binding (email vs sub) in OAuth

## 核心思路

Link provider using email claim mismatch to sub without verification check

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `OAuth Identity Binding Flaw` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Login as other user via provider account linking
- 适用场景：OAuth account linking systems
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 绘制登录、注册、账号绑定、邀请、SSO 回调、magic link 的完整状态机。
- 重点确认 redirect/state/nonce/audience/issuer/email claim/account linking 的服务端校验。
- 使用自有账号验证跨账号绑定或会话混淆，避免触达第三方账户。

## 适用目标画像

- OAuth account linking systems

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Login as other user via provider account linking

## 手工验证流程（授权 / Lab only）

1. 确认 scope、禁止项、速率限制与是否允许该功能测试。
2. 准备至少两个自有测试账号；多租户场景准备两个 organization/workspace。
3. 先完整走通正常业务流，记录对象 ID、角色、状态、token、请求路径。
4. 只替换一个变量或一步状态，观察服务端响应和后续副作用。
5. 用最小必要数据证明影响；不读取、不导出第三方真实数据。
6. 绘制登录、注册、账号绑定、邀请、SSO 回调、magic link 的完整状态机。
7. 重点确认 redirect/state/nonce/audience/issuer/email claim/account linking 的服务端校验。
8. 使用自有账号验证跨账号绑定或会话混淆，避免触达第三方账户。

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

- (disclosed BB reports referenced)

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://systemweakness.com/how-i-logged-in-as-another-user-via-broken-oauth-identity-binding-9a5265d84046](https://systemweakness.com/how-i-logged-in-as-another-user-via-broken-oauth-identity-binding-9a5265d84046)
author_date: Digvijay Gholase / 2025-05 tags: ["oauth", "identity-binding", "account-linking", "ato"] confidence: high

# Broken Identity Binding (email vs sub) in OAuth

## 核心思路
OAuth账号链接时使用可变的email claim而非稳定的sub claim，导致email变更后出现身份混淆，可将攻击者账号绑定到受害者身份。

## 前置条件
- 目标支持OAuth账号链接（Google/其他IdP）。
- 授权测试账号（至少2个，用于email变更模拟）。
- 目标允许email变更且不强制重新验证链接。

## 完整技法细节
- 使用OAuth provider（Google）创建一个账号A。
- 在目标应用使用账号A的email链接OAuth身份。
- 将账号A的email更改为目标受害者账号B的email。
- 使用新email重新发起OAuth链接流程，观察是否错误绑定sub导致身份混淆。

## 适用目标画像
支持社交登录/OAuth账号链接的Web应用，尤其是使用email而非sub进行身份绑定的系统。

## 为什么有效
sub是IdP提供的稳定唯一ID，而email可被用户/攻击者更改，导致绑定逻辑失效。

## 手工验证流程（授权 / Lab only）
- 在授权lab中使用测试IdP和2个测试账号模拟流程。
- 完成链接后变更email并重新链接。
- 验证是否成功以受害者身份登录/访问数据。
- 仅使用合成测试账号和授权测试IdP。

## 可自动化部分
- Burp Repeater重复OAuth callback请求。
- 自定义Python脚本模拟email变更+链接流程。

## 误报/失败条件
- 应用严格使用sub claim绑定。
- 链接时强制验证email所有权或sub一致性。
- IdP禁止email快速变更。

## 授权边界
仅限授权bug bounty程序提供的测试账号和sandbox IdP。严禁使用真实用户账号。

## 报告 impact 角度
“账号接管（Account Takeover）风险：未授权第三方可能通过email变更将自身OAuth身份绑定到受害者账号，实现登录其他用户”。

## 相关案例链接
- [https://systemweakness.com/how-i-logged-in-as-another-user-via-broken-oauth-identity-binding-9a5265d84046](https://systemweakness.com/how-i-logged-in-as-another-user-via-broken-oauth-identity-binding-9a5265d84046)
(Digvijay Gholase报告)
- 其他已披露OAuth identity binding BB报告

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->
