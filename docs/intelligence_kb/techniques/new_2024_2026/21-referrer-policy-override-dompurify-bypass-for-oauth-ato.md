---
type: technique
category: new_method
vuln_class: DOMPurify
source_url: https://x.com/AmirMSafari/status/1923065022508318798
source_author: AmirMohammad Safari (@AmirMSafari)
source_date: 2025-05
collected_at: 2026-05-04
freshness: 2025
confidence: high
risk_level: high
target_types:
  - OAuth flows
raw_file: data/grok_research/raw/2026-05-04/topic_07_client_side_dom_cspt.md
---

# Referrer Policy Override + DOMPurify Bypass for OAuth ATO

## 核心思路

Google": - /url: https://x.com/AmirMSafari/status/1923065022508318798§DOMPurify§Google - text: fix window + PP trick on public H1 program for $4k

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `DOMPurify` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

Timing-based chain on authorized H1 program; practical 2025 technique

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- OAuth flows

## 为什么有效

Timing-based chain on authorized H1 program; practical 2025 technique

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

围绕 `DOMPurify` 说明可导致的未授权数据访问、权限提升、业务绕过、财务影响或合规风险。

## 相关案例链接

- https://x.com/AmirMSafari/status/1923065022508318798

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://x.com/AmirMSafari/status/1923065022508318798](https://x.com/AmirMSafari/status/1923065022508318798)
" vuln_class: "DOMPurify" one_line_trick: "Combine referrer-policy override timing with a DOMPurify-side bypass in an OAuth flow" why_useful: "Timing-based chain on authorized H1 program; practical 2025 technique" target_type: "OAuth flows" confidence: "high" tags: ["bug-bounty", "oauth", "dompurify", "referrer-policy", "ato"]
- **核心思路**
通过 DOMPurify Bypass 注入 <meta name="referrer" content="unsafe-url"> 或 preload link 覆盖 Referrer Policy，在 OAuth 授权重定向流程中让 Referrer 包含敏感 token，从而实现账户接管（ATO）。
- **前置条件**
- 目标 OAuth 流程中 Referrer 会被后端用于 token 验证或状态传递；
- 存在可控输入经过 DOMPurify 净化的位置；
- 授权 HackerOne 程序环境。
- **完整技法细节**
- 使用 DOMPurify Bypass（结合上述 Hook 或 mXSS 技法）注入 referrer-policy override。
- 在 OAuth 登录/授权流程中触发重定向。
- Referrer 携带完整 URL 参数（含 token），被攻击者捕获实现 ATO。 （全部操作仅在授权程序的测试账号完成）
- **适用目标画像**
- 使用 OAuth 2.0 / OpenID Connect 的 Web 应用；
- 同时存在客户端 HTML 净化器；
- Referrer Policy 默认 restrictive 但可被客户端覆盖。
- **为什么有效**
OAuth 流程常依赖 Referrer 传递状态，而现代浏览器默认严格 Referrer Policy 可被客户端 meta/link 覆盖，配合 DOMPurify Bypass 即可注入。
- **手工验证流程（授权 / Lab only）**
- 在授权 H1 程序的测试环境中定位 OAuth 流程。
- 注入构造的 DOMPurify Bypass payload。
- 完成一次 OAuth 登录，观察 Referrer 是否泄露 token。
- 仅使用测试账号，验证后立即撤销所有授权。
- **可自动化部分**
- 自动化扫描常见 OAuth 端点 + DOMPurify 版本。
- **误报/失败条件**
- Referrer Policy 被服务端强制；
- OAuth 流程不依赖 Referrer；
- 最新浏览器/框架已修复 override。
- **授权边界**
严格限定在授权 HackerOne 程序。任何 token 泄露测试必须使用程序提供的测试账号，且立即通知 triager。
- **报告 impact 角度**
- 完整账户接管（ATO）；
- 影响 OAuth 登录安全，潜在大规模用户影响；
- 实际 Bounty 约 $4K，证明了高商业价值。
- **相关案例链接**
- [https://x.com/AmirMSafari/status/1923065022508318798](https://x.com/AmirMSafari/status/1923065022508318798)

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/prototype_pollution_xss_chain.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->
