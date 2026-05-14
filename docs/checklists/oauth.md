---
id: clk-oauth
title: OAuth 2.0 / OAuth 2.1 / OIDC Client Flaws
owasp_anchor: [API2:2023, WSTG-ATHN, WSTG-SESS]
cwe: [CWE-287, CWE-345, CWE-601, CWE-294]
severity_typical: P1-P3
playbook: playbooks/oauth.yaml
last_updated: 2026-05-15
sources: []
maturity: stable
---

# OAuth 2.0 / 2.1 / OIDC Checklist

> 双语 / Bilingual: OAuth/OIDC 客户端缺陷专项。
> SAML / SSO 全集见 `sso_oidc_saml.md`。JWT 单独深度见下文 §6。
> Authorization-only：测试自己注册的两个账号。不要触碰真实用户的 OAuth 凭据。

---

## 1. Recon

- [ ] 找 well-known endpoints
  - OIDC discovery: `/.well-known/openid-configuration`
  - JWKS: `jwks_uri`（从 discovery 获取）
- [ ] 列出所有 redirect_uri / callback URL（前端 config / Swagger / mobile manifest）
- [ ] 列出 client_id 与对应的 grant_type
- [ ] response_type 列表：code / id_token / token / code id_token / device_code / hybrid
- [ ] PKCE 是否强制（OAuth 2.1 要求 public client 必须）
- [ ] 区分 confidential client vs public client（mobile / SPA）

## 2. redirect_uri 校验

- [ ] 是否严格 exact-match？尝试：
  - 路径追加：`https://app/callback/../evil`
  - URL 编码：`%2f`、`%2e`、`%5c`、`%252f` 双编码
  - 子域混淆：`app.evil.com`、`app%23.evil.com`、`app@evil.com`
  - 协议降级：`http://` vs `https://`
  - 端口 / fragment / query 注入：`callback?next=//evil`、`callback#@evil.com`
- [ ] open redirect 链：找站内 open redirect → 套到 redirect_uri → 拿到 code
- [ ] 多 redirect_uri 注册支持：能否在注册时加上 attacker.com

## 3. state / nonce / PKCE

- [ ] state 缺失或可预测 → CSRF / 账号绑定攻击（Account A 拿走 Account B 的 SSO）
- [ ] state 跨 session 重用
- [ ] nonce（OIDC）：缺失 → ID Token replay；接受空 nonce
- [ ] PKCE：未强制 → downgrade attack；服务端不校验 code_verifier 与 code_challenge 关联
- [ ] code_challenge_method=plain 被接受（应只允许 S256）

## 4. authorization_code / token 重用

- [ ] code 一次性？复用拿第二个 token
- [ ] code 跨 client_id 可换（rare but exists）
- [ ] code 跨 redirect_uri 可换
- [ ] refresh_token 撤销链：登出 / 改密 / 解绑后 refresh 是否仍有效
- [ ] access_token audience 校验：A 的 token 直击 B 服务

## 5. Implicit / Hybrid / Device flow 弱点

- [ ] Implicit flow 仍启用：access_token 走 fragment，易被 referrer 泄露
- [ ] Hybrid flow `code id_token`：id_token 中的 c_hash 校验缺失
- [ ] Device flow：user_code / device_code 可被远程钓骗
- [ ] CIBA / Backchannel：手机端确认页可被注入

## 6. JWT / ID Token 深度

### 6.1 算法层
- [ ] alg=`none` 接受
- [ ] alg=`HS256` 用 RSA 公钥当 HMAC 密钥（key confusion）
- [ ] alg=`RS256` 切到 `HS256`
- [ ] kid header 注入文件路径 / URL → JWKS spoof / SQL injection
- [ ] jwk header 直接嵌入 attacker 公钥

### 6.2 声明层
- [ ] iss / aud / exp / iat / nbf 任一缺校验
- [ ] 时钟偏移容忍 > 5 分钟
- [ ] sub 声明可被覆盖
- [ ] custom claim 注入：`{"roles":["admin"]}`

### 6.3 签名 / 编码
- [ ] base64url 大小写不敏感被利用
- [ ] header / payload 多余字段绕过签名
- [ ] JWE 加密 token 密钥协商弱（dir / RSA-OAEP / A128KW）

## 7. 账号绑定 / 邮箱信任

- [ ] 不同 IdP 同一邮箱 → 自动合并到既有账号？
- [ ] `email_verified=false` 被信任？
- [ ] 大小写 / Unicode 同形：`Admin@x.com` vs `admin@x.com` vs `аdmin@x.com`
- [ ] SSO 绑定时是否要求重新输入密码 / 二次确认
- [ ] 解绑流程：解绑后是否仍能用 OAuth 登录、是否清空所有 sessions
- [ ] 邮箱所有权时间窗口：第一次注册时未验证邮箱，后续验证用别人 token

## 8. 自动化辅助

```bash
# OIDC discovery
curl -sL https://target/.well-known/openid-configuration | jq .

# JWKS 抓取
curl -sL <jwks_uri> | jq '.keys[]'

# JWT 拆解 (不验证)
python3 -c "import sys,json,base64; t=sys.argv[1]; h,p,_=t.split('.'); print(json.dumps(json.loads(base64.urlsafe_b64decode(p+'==')), indent=2))" <jwt>

# JWT 攻击
jwt_tool <token> -X a       # alg=none
jwt_tool <token> -X k -pk pubkey.pem  # key confusion HS256
jwt_tool <token> -X i -I -ic kid -iv "../../../../etc/passwd"  # kid injection

# Burp / Caido 扩展
# Burp: JWT Editor / JWT Analyzer / Autorize
# Caido: workflow OAuth state strip

# nuclei
nuclei -tags oauth,jwt -u https://target
```

## 9. Reporting Angle

* **Title 模板**：`OAuth <flaw> in <flow/endpoint> allows <attacker role> to <impact>`
  例：`OAuth redirect_uri loose match allows attacker to steal authorization codes via callback/../`
* **Severity 自评**：
  * 完整 ATO（不需要受害者点击或仅需点击一个看似正常的链接） → CVSS ≥ 8.0 / VRT P1
  * 信息泄露（仅 access token 泄露但 audience 受限）→ CVSS ≥ 5.0 / VRT P3
  * Implicit / Hybrid 残留警告 → P4-P5
* **CWE 推荐**：CWE-287（Auth bypass）/ CWE-345（不充分校验）/ CWE-601（open redirect）/ CWE-294（auth replay）
* **PoC 必须**：完整 HTTP 序列、URL 全展开、token 仅前 8 字 + 后 4 字
* **Suggested Fix**：exact-match redirect_uri + 强制 PKCE + 禁用 alg=none + state 必填 + 一次性 code + audience 校验
