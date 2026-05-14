---
type: technique
category: new_method
vuln_class: OAuth State / Redirect Manipulation
source_url: (X posts on state decoding)
source_author: (from multiple hunter X posts e.g. hackrkid)
source_date: 2026
collected_at: 2026-05-04
freshness: 2026
confidence: high
risk_level: high
target_types:
  - OAuth SSO implementations
raw_file: data/grok_research/raw/2026-05-04/topic_03_oauth_sso_jwt_magic_link.md
---

# OAuth Redirect URI Manipulation for Token Leak

## 核心思路

Decode/manipulate state param in OAuth callback to leak tokens or bypass checks

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `OAuth State / Redirect Manipulation` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

Practical token interception in SSO flows

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- OAuth SSO implementations

## 为什么有效

Practical token interception in SSO flows

## 手工验证流程（授权 / Lab only）

1. 确认项目 rules of engagement 明确允许该类别测试。
2. 搭建双账号或 sandbox 测试数据，避免触达真实用户数据。
3. 复现来源中的业务前提，只记录最小必要证据。
4. 证明 server-side impact；不要依赖客户端表现。
5. 截图/保存请求响应时打码 token、cookie、PII、支付信息。

## 可自动化部分

- 资产/endpoint 发现、参数枚举、schema 对比、变更 diff 可自动化。
- 权限、支付、状态机、业务影响必须手工确认。

## 误报/失败条件

- 目标不存在相同业务前提。
- 防护在服务端强校验。
- 只影响自有账号且无跨权限/跨租户/财务/数据影响。

## 授权边界

仅用于授权 Bug Bounty、靶场、自有环境。不得用于越界扫描、爆破、DoS、真实支付损害、非授权读取第三方数据。

## 报告 impact 角度

围绕 `OAuth State / Redirect Manipulation` 说明可导致的未授权数据访问、权限提升、业务绕过、财务影响或合规风险。

## 相关案例链接

- (X posts on state decoding)

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://x.com/hackrkid/status/2037137846629499094](https://x.com/hackrkid/status/2037137846629499094)
(state decoding示例) author_date: hackrkid等猎人X帖 / 2026 tags: ["oauth", "redirect-uri", "state-manipulation", "token-leak"] confidence: high

# OAuth Redirect URI Manipulation for token exposure risk

## 核心思路
解码/篡改OAuth callback中的state参数，或操纵redirect_uri参数，绕过弱验证机制，导致授权码/访问令牌泄露或CSRF式账号链接。

## 前置条件
- 目标实现OAuth SSO或账号链接流程。
- 授权测试账号和合成OAuth client（或目标提供的测试IdP）。
- redirect_uri或state验证不严格。

## 完整技法细节
- 发起OAuth授权请求，捕获state参数并解码其内容。
- 篡改state中的redirect_uri或附加恶意参数。
- 提交修改后的callback URL，观察是否将token/code泄露到测试者控制的URI。
- 或利用弱state验证实现CSRF账号链接（攻击者账号绑定到受害者）。

## 适用目标画像
OAuth SSO实现、社交登录系统、支持第三方IdP账号链接的应用。

## 为什么有效
许多实现仅对redirect_uri进行部分匹配，或state未正确绑定/验证，导致parser/redirect混淆。

## 手工验证流程（授权 / Lab only）
- 在授权lab中使用测试IdP和2个测试账号。
- 构造OAuth授权URL，修改state/redirect_uri。
- 完成登录流程，确认token是否泄露到修改后的URI。
- 仅记录泄露行为，不实际窃取真实token。

## 可自动化部分
- Burp Repeater +自定义state解码脚本。
- OAuth测试工具（如oauth2-proxy测试环境）自动化变异。

## 误报/失败条件
- redirect_uri严格exact match + state强制验证。
- IdP启用PKCE或严格state nonce。
- 应用使用库强制验证（e.g. oauthlib）。

## 授权边界
仅限授权bug bounty程序的测试账号和sandbox OAuth流程。严禁针对真实用户发起未经授权的OAuth请求。

## 报告 impact 角度
“OAuth令牌泄露或账号劫持风险：未授权第三方可能通过state/redirect_uri操纵窃取授权码/访问令牌，或实现CSRF账号链接”。

## 相关案例链接
- [https://x.com/hackrkid/status/2037137846629499094](https://x.com/hackrkid/status/2037137846629499094)
(state decoding)
- [https://x.com/hackrkid/status/2043738122438254600](https://x.com/hackrkid/status/2043738122438254600)
(OAuth misconfig CSRF)
- 其他猎人X帖关于OAuth redirect/state操纵

<!-- GROK_EXPANSION_END -->
