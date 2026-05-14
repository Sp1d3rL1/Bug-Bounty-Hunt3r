---
id: clk-cspt-client-path-traversal
title: Client-Side Path Traversal (CSPT)
owasp_anchor: [WSTG-CLNT]
cwe: [CWE-22, CWE-352]
severity_typical: P2-P3
playbook: playbooks/cspt.yaml
last_updated: 2026-05-14
sources:
  - docs/intelligence_kb/cases/public_reports/4-reflected-xss-in-cloudflare-ai-playground-oauth-handler-cve-2026-1721.md
  - docs/intelligence_kb/cases/researcher_writeups/1-client-side-path-traversal-cspt-to-account-takeover-xss-via-profile-url-traversal.md
  - docs/intelligence_kb/cases/researcher_writeups/10-postmessage-listener-with-target-com-wildcard-cors-misconfig-to-home-automation-takeo.md
  - docs/intelligence_kb/cases/researcher_writeups/10-stored-xss-in-apple-developer-portal.md
  - docs/intelligence_kb/cases/researcher_writeups/106-4-december-ctf-challenge-chaining-xs-leaks-and-postmessage-xss.md
  - docs/intelligence_kb/cases/researcher_writeups/14-prototype-pollution-to-xss-via-lodash-merge-gadget-on-shopify-updated-2024-chain.md
  - docs/intelligence_kb/cases/researcher_writeups/18-cspt-levels-practical-attacks-hunter-x-post-reference.md
  - docs/intelligence_kb/cases/researcher_writeups/23-xss-via-shodan-in-globalprotect-affects-bug-bounty-programs.md
  - docs/intelligence_kb/cases/researcher_writeups/4-dompurify-prototype-pollution-to-xss-bypass-cve-2026-41238-via-custom-element-handling.md
  - docs/intelligence_kb/cases/researcher_writeups/7-client-side-postmessage-origin-validation-bypass-to-dom-xss.md
  - docs/intelligence_kb/cases/x_threads/20-s3-xss-via-bucket-misconfig-bucketlist-tool.md
  - docs/intelligence_kb/cases/x_threads/22-cspt-to-jsonp-xss-hunter-x-report.md
  - docs/intelligence_kb/cases/x_threads/23-1-click-cspt-to-stored-id-rogue-sentry-put-csrf.md
  - docs/intelligence_kb/review_queue/24-client-side-bugs-roadmap-xss-postmessage-pp-csp-bypass.md
  - docs/intelligence_kb/review_queue/3-cspt-resources-compilation-hunter-blogs-reports-tools.md
  - docs/intelligence_kb/review_queue/resource-24-client-side-bugs-roadmap-xss-postmessage-pp-csp-bypass.md
  - docs/intelligence_kb/review_queue/resource-3-cspt-resources-compilation-hunter-blogs-reports-tools.md
  - docs/intelligence_kb/techniques/evergreen_new_context/14-blind-ssrf-via-dns-in-pdf-generator-of-saas-export-feature.md
  - docs/intelligence_kb/techniques/evergreen_new_context/19-second-order-idor-via-profile-update-affecting-high-privilege-module.md
  - docs/intelligence_kb/techniques/evergreen_new_context/24-api-versioning-bypass-legacy-v1-endpoints-lack-patches-in-saas.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-10-stored-xss-in-apple-developer-portal.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-23-xss-via-shodan-in-globalprotect-affects-bug-bounty-programs.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-4-reflected-xss-in-cloudflare-ai-playground-oauth-handler-cve-2026-1721.md
  - docs/intelligence_kb/techniques/new_2024_2026/103-4-oauth-redirect-uri-manipulation-for-token-theft.md
  - docs/intelligence_kb/techniques/new_2024_2026/106-1-client-side-path-traversal-exploiting-csrf-in-header-based-auth-scenarios.md
  - docs/intelligence_kb/techniques/new_2024_2026/106-3-cspt-client-side-path-traversal.md
  - docs/intelligence_kb/techniques/new_2024_2026/106-5-dom-xss-using-web-messages-and-javascript-url.md
  - docs/intelligence_kb/techniques/new_2024_2026/13-cspt-file-upload-bypass-to-arbitrary-file-read.md
  - docs/intelligence_kb/techniques/new_2024_2026/13-paramspider-arjun-for-hidden-params.md
  - docs/intelligence_kb/techniques/new_2024_2026/19-prototype-pollution-via-deepmerge-in-antfu-utils-huntr-bb.md
  - docs/intelligence_kb/techniques/new_2024_2026/2-cspt2csrf-client-side-path-traversal-to-cross-site-request-forgery.md
  - docs/intelligence_kb/techniques/new_2024_2026/21-referrer-policy-override-dompurify-bypass-for-oauth-ato.md
  - docs/intelligence_kb/techniques/new_2024_2026/25-postmessage-wildcard-origin-samesite-lax-to-pii-leak.md
  - docs/intelligence_kb/techniques/new_2024_2026/5-dompurify-mxss-bypass-via-node-flattening-namespace-confusion-3-1-0.md
  - docs/intelligence_kb/techniques/new_2024_2026/6-dompurify-bypass-via-forcekeepattr-hook-uponsanitizeattribute-setattribute.md
  - docs/intelligence_kb/techniques/new_2024_2026/9-cspt-in-desktop-apps-via-websocket-user-controlled-path.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-1-client-side-path-traversal-cspt-to-account-takeover-xss-via-profile-url-t.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-10-postmessage-listener-with-target-com-wildcard-cors-misconfig-to-home-aut.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-14-prototype-pollution-to-xss-via-lodash-merge-gadget-on-shopify-updated-20.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-18-cspt-levels-practical-attacks-hunter-x-post-reference.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-20-s3-xss-via-bucket-misconfig-bucketlist-tool.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-22-cspt-to-jsonp-xss-hunter-x-report.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-23-1-click-cspt-to-stored-id-rogue-sentry-put-csrf.md
  - docs/intelligence_kb/techniques/niche_tricks/106-2-cspt-resources.md
  - docs/intelligence_kb/techniques/niche_tricks/107-1-client-side-path-traversal-cspt-bug-bounty-reports-and-techniques.md
  - docs/intelligence_kb/techniques/niche_tricks/13-blind-xss-with-js-import-long-term-callback.md
  - docs/intelligence_kb/techniques/niche_tricks/13-cspt-file-upload-bypass-to-arbitrary-file-read.md
  - docs/intelligence_kb/techniques/niche_tricks/22-parameter-discovery-for-sqli-xss-ssrf-via-6-methods.md
  - docs/intelligence_kb/techniques/niche_tricks/24-graphql-introspection-batching-for-data-leak-abuse.md
  - docs/intelligence_kb/techniques/niche_tricks/3-bac-via-http-method-swap-version-rollback-array-id-injection.md
  - docs/intelligence_kb/techniques/niche_tricks/5-dompurify-mxss-bypass-via-node-flattening-namespace-confusion-3-1-0.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-4-dompurify-prototype-pollution-to-xss-bypass-cve-2026-41238-via-custom-ele.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-7-client-side-postmessage-origin-validation-bypass-to-dom-xss.md
maturity: stable
---

# Client-Side Path Traversal (CSPT) Checklist

> 双语 / Bilingual：用户控制的 path 段被前端塞进 `fetch` / `XHR` URL 的非 query 位置 → 服务端按攻击者意愿命中其他 endpoint。
> 用法：先做"前端 fetch URL 拼接审计"，再分别走 CSPT2CSRF（让 victim 调用敏感 API）、CSPT-to-XSS（污染 JSON 响应进 sink）、CSPT-to-ATO（劫持 reset-token / OAuth state）。
> Authorization-only：所有 PoC 在自己注册的 A/B 账号之间复现；不构造能命中他人数据的 URL。

---

## 1. Recon & 前端 fetch 审计

- [ ] 抓 SPA bundle，搜 `fetch(` / `axios.` / `XMLHttpRequest` / `$.ajax` / `useSWR` / `useQuery` 调用点
- [ ] 标记每个调用的 URL 模板：哪些段来自 router param、hash、query、postMessage、localStorage、cookie
- [ ] 找模板拼接：`` `/api/users/${userId}/profile` `` / `` `/v1/${type}/${id}` `` / `'/api/' + section + '/data'`
- [ ] 检查框架自动 URL encoding：原生 `fetch` 不会自动 encode path 段；`axios` 默认也不 encode；`URL` 构造器对 path 不 encode
- [ ] 找 path 段来源：`useParams()` / `route.params` / `location.hash.split('/')` / `window.location.pathname.split('/')`
- [ ] 标记是否存在前端"鉴权降级"：fetch 拿到的 JSON 直接渲染，没二次校验返回字段所属用户

## 2. CSPT 触发原语 (sources)

- [ ] router param 直接进 path：`/app/orders/<orderId>` 中 `orderId` 输入 `123/../../admin/users` 后 fetch `/api/orders/123/../../admin/users`
- [ ] hash 段进 path：`#/profile/<name>` → `fetch('/api/profile/' + name)`
- [ ] query 进 path（少见但有）：`?file=foo` → `` fetch(`/static/${file}`) ``
- [ ] postMessage data 进 path：嵌入页接收消息后 `fetch('/api/' + msg.endpoint)`
- [ ] localStorage / sessionStorage 中污染的 ID
- [ ] 测分隔符家族：`..%2f`、`..%252f`、`..\\`、`..%5c`、`%2e%2e/`、双解码 `%252e%252e%252f`
- [ ] URL.canParse / new URL 的 base 解析差异：`new URL('//evil.com/path', baseUrl)` 会跳到 evil.com

## 3. CSPT2CSRF 链

- [ ] 找到 CSPT 后，目标是让受害者浏览器从其登录态发出"危险方法"请求（POST/PUT/DELETE）
- [ ] 找前端用 `fetch(url, {method: 'POST', body: ...})` 的位置，且 method / body 来自模板而非用户路径
- [ ] 用 CSPT 改 path，但保留 method=POST + 受害者 cookie + 自带 CSRF token（同源所以 token 自动带）
- [ ] 例：把 "POST /api/orders/<id>/cancel" 改成 "POST /api/admin/users/me/role" 类
- [ ] 检查 SameSite cookie 是否阻断（Lax 不阻断同站 fetch）
- [ ] 检查 CSRF token 来源：是否绑定到具体路径；多数 token 只绑 session 不绑 path → 可被 CSPT 重用

## 4. CSPT-to-XSS 链

- [ ] 找前端把 fetch 响应直接喂 sink 的位置：`element.innerHTML = res.html`、`eval(res.code)`、`new Function(res.fn)`
- [ ] 用 CSPT 把 fetch 指向"返回攻击者可控 JSON"的端点：用户上传的 markdown / 评论 / blob storage 的可控对象
- [ ] 关键：找一个允许任意用户上传 JSON / 文本的 endpoint（例如 `/api/notes/<id>` / 公共评论 / 头像 SVG）
- [ ] 把 path 改成 `/api/notes/<attacker-note-id>`，让前端把 attacker 的 JSON 渲染到 victim DOM
- [ ] 测 content-type 嗅探：响应是否被前端按 JSON 解析（即便服务端返回 text/plain，axios 会尝试 JSON.parse）

## 5. CSPT-to-ATO 链

- [ ] reset-password / email-verification token 的领取流程是否走 fetch path：`fetch('/api/reset/' + tokenIdFromHash)`
- [ ] OAuth state / PKCE verifier 是否从 path 段读取
- [ ] 用 CSPT 把 fetch 指到攻击者可控端点 → 把 victim 的 token 发给 attacker
- [ ] 反向：把 attacker token 喂给 victim 的客户端 → 让 victim 帮 attacker 完成绑定 / 登录（cross-account chain）
- [ ] 检查 SSO 回调中的 path 解析

## 6. 鉴权降级 / 跨 origin 链

- [ ] 找前端调内部 admin endpoint 时是否依赖 path 区分（如 `/api/admin/*` vs `/api/user/*`），后端依据 path 做权限分支
- [ ] CSPT 改 path 让 normal user fetch 到 `/api/admin/*`，看后端是否仍按 cookie 鉴权放行
- [ ] cors+CSPT 链：fetch 到一个允许 `Access-Control-Allow-Origin: *` 但本应只在 internal 调用的 endpoint，受害者 cookie 顺带发出
- [ ] CDN+CSPT：CSPT 让响应被 CDN 缓住，构成 stored CSPT
- [ ] iframe + CSPT：嵌入第三方页用 CSPT 把 fetch 指到主站敏感 API

## 7. 边界与防御指纹

- [ ] 看前端是否对 path 段调 `encodeURIComponent`；多数 routing lib（react-router / vue-router）默认 decode 但不 encode 回去
- [ ] 看是否有 `URL` 构造时的相对解析：`new URL(userPath, 'https://api/')` + userPath 以 `//` 开头 → 跨主机
- [ ] 看 fetch 是否走绝对 URL：绝对 URL 不可被 path traversal 改主机，但可被 query/hash 移位
- [ ] 看后端是否对 path normalization（统一处理 `..`）

## 8. 自动化辅助

```bash
# Doyensec CSPTBurpExtension：被动扫前端 fetch 拼接
# https://github.com/doyensec/CSPTBurpExtension

# 静态扫 SPA bundle：找模板拼接的 fetch
node -e '
const fs=require("fs"),src=fs.readFileSync(process.argv[1],"utf8");
const re=/(fetch|axios\.\w+|\$\.ajax)\s*\(\s*[`"\x27]([^`"\x27]*\$\{[^}]+\}[^`"\x27]*)/g;
let m; while((m=re.exec(src))) console.log(m[2]);
' bundle.js

# 动态：在 DevTools 里 hook fetch 看实际 URL
# > const _f = fetch; window.fetch = (u,o)=>{console.log("FETCH",u);return _f(u,o)}

# Burp Bambda：标记 path 中含 ../ 的 URL
# request.path().contains("..") || request.path().contains("%2e%2e")

# Caido workflow：HTTPQL 找候选
# req.path.cont("/api/") AND req.method.eq("GET") AND resp.header.value.cont("application/json")

# 手测 path traversal payload 集
for p in '..%2f' '..%252f' '..%5c' '%2e%2e%2f' '..%c0%af' '..%2f..%2f'; do
  curl -s -o /dev/null -w "%{http_code} $p\n" "https://target/api/orders/${p}admin/users"
done

# Nuclei
nuclei -tags cspt,client-side -u https://target
```

## 9. Reporting Angle

* **Title 模板**：`Client-Side Path Traversal in <component> chained to <CSRF|XSS|ATO> via <fetch site>`
* **CVSS 3.1 区间**：
  * CSPT-to-CSRF（受害者权限提升 / 关键操作）：6.5 – 8.1（AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N）
  * CSPT-to-XSS：6.1 – 8.1（含 S:C 时上界更高）
  * CSPT-to-ATO：8.0 – 9.0
  * 仅 CSPT 原语未链：4.0 – 5.4
* **VRT P-level**：链 ATO → P2 上界；CSRF 关键操作 → P3；仅原语 → P4
* **CWE 推荐**：CWE-22（Path Traversal）+ CWE-352（CSRF, 链时） + CWE-79（XSS, 链时）
* **PoC 必须**：
  - 两个测试账号 A/B；attacker 把 B 引到带 path payload 的 SPA URL，复现 fetch 命中 attacker 端点
  - 完整 DevTools network 截图（被改后的 path）
  - 标明前端框架版本与 routing lib 版本
* **Suggested Fix**（≥2）：
  1. 所有进入 fetch path 段的用户输入强制 `encodeURIComponent`
  2. 拒绝 path 段中含 `..` / `%2e%2e` / 反斜杠的 router param（前端 router 层 schema 校验）
  3. 后端按身份做权限判定，不依赖 path 前缀分支
  4. CSRF token 绑定到具体方法+路径而非仅会话

## 10. 已迁移技法（来自 KB）

- [[techniques/cspt_router_param|Router Param 进 fetch path]]
- [[techniques/cspt2csrf_chain|CSPT2CSRF 链]]
- [[techniques/cspt_to_xss|CSPT-to-XSS via 可控 JSON]]
- [[techniques/cspt_oauth_state|CSPT 劫持 OAuth state/code]]
