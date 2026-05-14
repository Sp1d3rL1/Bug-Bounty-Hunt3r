---
id: clk-sso-oidc-saml
title: SSO / OIDC / SAML
owasp_anchor: [API2:2023, WSTG-IDNT, WSTG-ATHN, WSTG-SESS]
cwe: [CWE-287, CWE-345, CWE-384, CWE-294, CWE-601]
severity_typical: P1-P2
playbook: playbooks/sso_oidc.yaml
last_updated: 2026-05-15
sources:
  - docs/intelligence_kb/techniques/oauth_misbinding.md
  - docs/intelligence_kb/techniques/saml_signup_bypass.md
  - docs/intelligence_kb/techniques/jwt_alg_none.md
maturity: stable
---

# SSO / OIDC / SAML Checklist

> 双语 / Bilingual: 单点登录、OpenID Connect、SAML 攻击面合一。
> 用法：先做"Recon & 协议指纹"判断 IdP / SP 类型，再按 OAuth/OIDC 或 SAML 分支走。
> Authorization-only：必须在项目允许测试 SSO 的 scope 内进行，且只用自己的两个测试账号。

---

## 1. Recon & 协议指纹

- [ ] 抓登录入口的 `WWW-Authenticate` / 重定向链 / `client_id` / `response_type`
- [ ] 区分协议：OAuth 2.0 / OAuth 2.1 / OIDC / SAML 2.0 / WS-Federation / Magic Link
- [ ] 找 well-known endpoints
  - OIDC discovery: `/.well-known/openid-configuration`
  - JWKS: `/.well-known/jwks.json` 或从 discovery 获取 `jwks_uri`
  - SAML metadata: `/saml/metadata`、`/SAML2/IdpMetadata`、`/Shibboleth.sso/Metadata`
- [ ] 列出 IdP（Auth0 / Okta / Azure AD / Google / Apple / GitHub / Keycloak / 自研）
- [ ] 列出 SP 入口和回调（authorization_endpoint、token_endpoint、redirect_uri、ACS URL）
- [ ] 是否支持多 tenant？多 tenant 边界在哪里（路径 / subdomain / claim）

## 2. OAuth / OIDC 客户端缺陷

### 2.1 redirect_uri 校验
- [ ] 是否严格 exact-match？尝试：
  - 追加路径：`https://app/callback/../evil`
  - URL 编码：`%2f`、`%2e`、`%5c`
  - 子域名混淆：`https://app.evil.com`、`https://app%23.evil.com`
  - 协议降级：`http://` vs `https://`
  - 端口/查询串注入：`callback?next=//evil`
- [ ] open redirect 链组合：找站内 open redirect → 套到 redirect_uri 走完授权 → 拿到 code

### 2.2 state / nonce / PKCE
- [ ] state 缺失或可预测 → CSRF / 账号绑定攻击
- [ ] nonce（OIDC）缺失 → ID Token replay
- [ ] PKCE：是否强制？code_verifier 是否真的与签发时一致？（公共客户端必须 PKCE）
- [ ] 同一 state 是否能复用多次

### 2.3 code / token 重用与替换
- [ ] authorization code 是否一次性？复用 → 拿到第二个 token
- [ ] code 跨客户端 / 跨 redirect_uri 是否仍可换 token
- [ ] refresh_token 撤销链：登出后 refresh 是否还能用
- [ ] access_token 是否能直接命中其他 client_id 的资源（audience 校验）

### 2.4 ID Token 校验
- [ ] alg 接受 `none`、`HS256`（用 RSA 公钥当 HMAC 密钥）
- [ ] kid header 注入文件路径或 URL → JWKS-spoof
- [ ] iss / aud / exp / iat / nbf 任一缺校验
- [ ] 接受未签名 token？接受过期 token？时钟偏移容忍 > 5 分钟？

### 2.5 账号绑定 / 邮箱信任
- [ ] 不同 IdP 同一邮箱 → 自动合并到既有账号？
- [ ] `email_verified=false` 是否被信任？
- [ ] 大小写 / Unicode 同形异码：`Admin@x.com` vs `admin@x.com` vs `аdmin@x.com`
- [ ] SSO 绑定时是否要求重新输入密码 / 二次确认
- [ ] 解绑流程：解绑 SSO 后是否仍能用密码登录、是否清空 sessions

### 2.6 Magic Link / Passwordless
- [ ] token 长度、熵、过期窗
- [ ] 是否绑定原始 IP / UA / 浏览器指纹
- [ ] 同 token 多次使用、跨设备使用
- [ ] 邮件 forwarding / quoted-printable 编码绕过

## 3. SAML 客户端缺陷

- [ ] XML Signature Wrapping（XSW）：在 Response 外包裹 / 内嵌一个被签名的 Assertion，原始内容被忽略
- [ ] XXE / XSLT 注入（在 Assertion 中嵌入实体或样式表）
- [ ] SAML Raider 12 攻击向量逐个过：alg 替换 / 签名位置错位 / KeyInfo 替换
- [ ] NameID 格式被 SP 信任（emailAddress / unspecified / persistent）
- [ ] InResponseTo 缺失 / 不校验 → CSRF 绑定
- [ ] AssertionConsumerService URL 可被参数覆盖 → ACS smuggling
- [ ] AudienceRestriction 不校验 → 跨 SP 重放
- [ ] 没有 NotBefore/NotOnOrAfter 校验 → token 永生
- [ ] 重复登录时 NameID 信任：同 NameID 不同 IdP

## 4. 跨账号 / 跨租户攻击

- [ ] 用 Account A 走 SSO → 拿到 code → 用 Account B 完成回调 → 哪个账号被登录
- [ ] 多 tenant：tenant_id claim 可篡改？Authorization Code 跨 tenant 可换 token？
- [ ] org-level SSO 强制：SCIM 删除用户后 token 是否立即失效
- [ ] just-in-time provisioning：JIT 创建账号时角色 / org 是否可控

## 5. 注销与会话

- [ ] /logout 不撤销 refresh token / cookie
- [ ] Single Logout (SLO) 失败时主会话仍存活
- [ ] back-channel logout（OIDC）端点缺失 → 多 tab 同时活跃
- [ ] 浏览器指纹绑定（重要）：换 UA / 换 IP 后 session 仍有效

## 6. 自动化辅助

```bash
# OIDC discovery
curl -sL https://target/.well-known/openid-configuration | jq .

# JWKS
curl -sL <jwks_uri> | jq .

# Decode JWT (no verify)
python3 -c "import sys,json,base64; t=sys.argv[1]; h,p,_=t.split('.'); print(json.dumps(json.loads(base64.urlsafe_b64decode(p+'==')), indent=2))" <jwt>

# SAML Raider (Burp ext) for XSW probing
# https://github.com/CompassSecurity/SAMLRaider

# Nuclei templates relevant to OAuth/OIDC misconfig
nuclei -tags oauth,oidc,saml -u https://target
```

## 7. Reporting Angle

* **Title 模板**：`<协议> <具体 flaw> allows <attacker role> to <impact> via <feature>`
  例：`OAuth redirect_uri loose match allows attacker to steal authorization codes via app/callback/../evil`
* **Severity 自评**：
  * 完整 ATO 跨账号 → CVSS 3.1 ≥ 8.0 / VRT P1
  * 仅本账号信息泄露 → CVSS ≥ 5.0 / VRT P3
* **CWE 推荐**：CWE-287 / CWE-345 / CWE-294 / CWE-601 三选其一最贴切的
* **PoC 必须**：两个测试账号、完整 HTTP 请求/响应、token 全部脱敏（仅保留前 8 字 + 后 4 字）
* **Reproducer Account**：报告中说明是用自己注册的 a@example.com / b@example.com 复现
* **Suggested Fix**：列出至少 2 条防御措施（exact-match redirect_uri / 强制 PKCE / 禁用 alg=none / 校验 InResponseTo）

## 8. 已迁移技法（来自 KB）

- [[techniques/oauth_misbinding|OAuth 账号绑定混淆]]
- [[techniques/saml_signup_bypass|SAML 注册流绕过]]
- [[techniques/jwt_alg_none|JWT alg=none 接受]]
- [[techniques/saml_xsw_smuggling|SAML Signature Wrapping 12 vector]]
