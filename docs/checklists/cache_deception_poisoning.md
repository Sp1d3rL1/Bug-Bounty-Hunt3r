---
id: clk-cache-deception-poisoning
title: Web Cache Deception & Poisoning
owasp_anchor: [WSTG-CONF, API8:2023]
cwe: [CWE-525, CWE-444]
severity_typical: P1-P2
playbook: playbooks/cache_attacks.yaml
last_updated: 2026-05-14
sources:
  - docs/intelligence_kb/cases/researcher_writeups/1-breaking-pingora-http-request-smuggling-cache-poisoning-in-cloudflare-s-reverse-proxy.md
  - docs/intelligence_kb/cases/researcher_writeups/11-sveltespill-cache-deception-in-sveltekit-vercel.md
  - docs/intelligence_kb/cases/researcher_writeups/14-cloudflare-pingora-default-cache-key-poisoning-host-ignored.md
  - docs/intelligence_kb/cases/researcher_writeups/16-kerish-s-web-cache-deception-css-append-on-dynamic-path-cloudflare.md
  - docs/intelligence_kb/cases/researcher_writeups/2-how-i-discovered-a-web-cache-deception-attack-exposing-pii-a-real-world-case-study.md
  - docs/intelligence_kb/cases/researcher_writeups/20-sitecore-html-cache-poisoning-leading-to-rce.md
  - docs/intelligence_kb/cases/researcher_writeups/23-web-cache-deception-via-path-mapping-exploitation-portswigger-lab-real-world-variant.md
  - docs/intelligence_kb/cases/researcher_writeups/3-web-cache-deception-when-a-404-still-leaks-sensitive-data.md
  - docs/intelligence_kb/cases/researcher_writeups/4-chatgpt-account-takeover-wildcard-web-cache-deception.md
  - docs/intelligence_kb/cases/researcher_writeups/6-cache-poisoning-reloaded-deep-dive-into-cve-2025-4366-and-pingora-s-request-smuggling.md
  - docs/intelligence_kb/cases/researcher_writeups/7-gotta-cache-em-all-novel-cache-deception-and-poisoning-via-url-parsing-quirks.md
  - docs/intelligence_kb/cases/researcher_writeups/8-next-js-cache-poisoning-via-204-responses-cve-2025-49826.md
  - docs/intelligence_kb/cases/researcher_writeups/9-next-js-cache-poisoning-race-condition-cve-2025-32421.md
  - docs/intelligence_kb/cases/researcher_writeups/9-nextjs-auth0-insecure-session-cache-key-hijack.md
  - docs/intelligence_kb/review_queue/18-the-ultimate-bug-bounty-guide-to-http-request-smuggling-with-cpdos-examples.md
  - docs/intelligence_kb/review_queue/resource-18-the-ultimate-bug-bounty-guide-to-http-request-smuggling-with-cpdos-examples.md
  - docs/intelligence_kb/review_queue/resource-25-top-10-web-hacking-techniques-of-2025-nominations-desync-endgame-chunk-trick.md
  - docs/intelligence_kb/techniques/new_2024_2026/12-http-2-request-tunnelling-for-web-cache-poisoning-portswigger-lab-technique.md
  - docs/intelligence_kb/techniques/new_2024_2026/15-h2-cl-desync-via-early-response-gadgets-for-response-queue-poisoning.md
  - docs/intelligence_kb/techniques/new_2024_2026/9-github-actions-cache-poisoning-for-supply-chain.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-1-breaking-pingora-http-request-smuggling-cache-poisoning-in-cloudflare-s-r.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-11-sveltespill-cache-deception-in-sveltekit-vercel.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-14-cloudflare-pingora-default-cache-key-poisoning-host-ignored.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-16-kerish-s-web-cache-deception-css-append-on-dynamic-path-cloudflare.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-2-how-i-discovered-a-web-cache-deception-attack-exposing-pii-a-real-world-c.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-20-sitecore-html-cache-poisoning-leading-to-rce.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-23-web-cache-deception-via-path-mapping-exploitation-portswigger-lab-real-w.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-4-chatgpt-account-takeover-wildcard-web-cache-deception.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-6-cache-poisoning-reloaded-deep-dive-into-cve-2025-4366-and-pingora-s-reque.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-7-gotta-cache-em-all-novel-cache-deception-and-poisoning-via-url-parsing-qu.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-8-next-js-cache-poisoning-via-204-responses-cve-2025-49826.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-3-web-cache-deception-when-a-404-still-leaks-sensitive-data.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-9-next-js-cache-poisoning-race-condition-cve-2025-32421.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-9-nextjs-auth0-insecure-session-cache-key-hijack.md
maturity: stable
---

# Web Cache Deception & Cache Poisoning Checklist

> 双语 / Bilingual：把 CDN / 反代 / 应用层缓存当成独立的可寻址组件去打。
> 用法：先做"缓存指纹与 cache key 还原"，再分别走 Deception（让缓存把私有响应缓住）和 Poisoning（让缓存把恶意响应缓住）。
> Authorization-only：只在自己注册的两个测试账号上发起 deception；poisoning 测试请使用 `Cache-Buster` 参数避免污染他人。

---

## 1. Recon & 缓存指纹

- [ ] 抓 `Age` / `X-Cache` / `X-Cache-Hits` / `CF-Cache-Status` / `X-Served-By` / `X-Vercel-Cache` / `X-Akamai-*` / `Via` 头，识别 CDN 与回源链路
- [ ] 通过 `Server` / TLS JA3 / `cf-ray` 区分 Cloudflare / Akamai / Fastly / Varnish / CloudFront / Vercel / Pingora / Nginx / Next.js ISR / SvelteKit edge
- [ ] 标记静态扩展白名单：`.css .js .png .gif .ico .svg .woff .woff2 .map .json .txt`（多数 CDN 默认按扩展名缓存）
- [ ] 找 cache key 组成：URL path / query 是否归一化、是否纳入 cookie、是否纳入 `Vary` 头
- [ ] 找未键入头（unkeyed headers）：`X-Forwarded-Host`、`X-Forwarded-Scheme`、`X-Original-URL`、`X-Rewrite-URL`、`Forwarded`、`X-Host`
- [ ] 找未键入 query：参数名大小写差异、`?` vs `;` 分隔、`?utm_*`、`?fbclid` 是否被剥离
- [ ] 标记 SSR 框架的缓存层：Next.js ISR `/_next/data/<buildId>/*.json`、SvelteKit `__data.json`、Nuxt payload

## 2. Web Cache Deception（Omer Gil 类）

- [ ] 在私有页 URL 末尾追加伪静态后缀：`/account/profile/x.css`、`/api/me/y.png`、`/dashboard;.js`
- [ ] 应用是否走"路径前缀路由"导致 `/account/profile/x.css` 仍命中 `/account/profile`
- [ ] 测分隔符：`;`（matrix param）、`%2f`、`%5c`、`%00`、`%3b`、`%23`、`/.`、`/./`
- [ ] 测大小写绕过：`/Account/Profile/x.CSS`，CDN 与应用对大小写归一化不一致时常出 deception
- [ ] 多斜杠归一化差异：`//account//profile//x.css`、`/account/./profile/x.css`、`/account/../account/profile/x.css`
- [ ] 用受害者已登录会话发出请求 → 让 CDN 缓住带个人数据的响应 → 攻击者匿名重放 URL 提取
- [ ] 检查响应是否含 `Cache-Control: private`，CDN 是否真的尊重；很多 CDN 默认按扩展名优先于 Cache-Control
- [ ] 测 Path Confusion + delimiter family：`#`、`?`、`;` 让源站与缓存对路径切分不一致
- [ ] 检查 OAuth 回调 / reset-password / invite token URL 是否能被诱发缓住

## 3. Web Cache Poisoning（unkeyed input）

- [ ] `X-Forwarded-Host: evil.com` → 看响应中是否反射到绝对 URL / `<link rel=canonical>` / `<base>`
- [ ] `X-Forwarded-Scheme: http` → 触发 301 到 http，把 redirect 缓住 → SSL strip
- [ ] `X-Original-URL: /admin`、`X-Rewrite-URL: /admin` → 回源覆盖路径，源站返回 admin 页被缓住
- [ ] `X-Forwarded-Prefix`、`X-Forwarded-For`、`Forwarded`（RFC7239）注入到错误页 / 日志页
- [ ] Fat GET：把 GET 改成带 body / 带 `Content-Length` 的请求，看缓存层是否仍按纯 path 计算 key
- [ ] Parameter cloaking：`?utm_source=x&__proto__[x]=y`、`?lang=en&lang=<payload>`，源站取最后一个值，缓存按第一个键入
- [ ] HTTP method override：`X-HTTP-Method-Override: POST` 让源站返回 POST 内容，被作为 GET 缓住
- [ ] `Vary` 头被滥用：源站不返回 `Vary: Origin/Cookie` 时，跨身份缓存命中
- [ ] 测 cache key normalization 差异：`%2520` vs `%20`、`%41` vs `A`、trailing slash
- [ ] 测错误页缓存：`/?<payload>` 触发 5xx，但 CDN 仍缓住自定义错误页中的 reflected payload

## 4. 框架与 CDN 专项

- [ ] Next.js ISR：`/_next/data/<buildId>/<page>.json` 是否能用未授权 query 触发缓住敏感 props
- [ ] SvelteKit `__data.json`：与 HTML 路由共享 cache key 时的 deception
- [ ] Cloudflare：Cache Rules / Page Rules 中的 "Cache Everything" 与 `Bypass Cache on Cookie` 被设错
- [ ] Cloudflare Pingora 边缘：HTTP/2 trailer 与原响应分裂时的 cache key 漂移 [example: 历史 Pingora 类]
- [ ] Akamai：`Edge-Control` / `Akamai-X-Cache-On` 头被前端注入
- [ ] Varnish：`hash_data()` 自定义 vcl 是否漏掉 cookie 或 Authorization
- [ ] CloudFront behaviors：忘记把 `Authorization` 加进 cache policy origin request
- [ ] Vercel：`s-maxage` 与 `stale-while-revalidate` 在 edge function 与 ISR 同时存在导致双层缓存
- [ ] Service worker 层缓存：`fetch` handler 把私有响应写入 `caches.open()` 给跨用户共享

## 5. 自动化辅助

```bash
# Param Miner 风格：探测未键入头
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:HEADER \
     -u https://target/ -H "HEADER: bugbountyprobe.example" \
     -mr "bugbountyprobe.example" -mc all

# Cache deception 扩展名暴力
for ext in css js png gif ico svg woff woff2 map json txt; do
  curl -sk -b "session=$COOKIE" -o /dev/null -w "%{http_code} %{url_effective} CC:%header{cache-control} XCache:%header{x-cache}\n" \
    "https://target/account/profile/cachebuster.$ext"
done

# 用 cache-buster + Param Miner 自动化（Burp Bambda 过滤）
# response.hasHeader("X-Cache") and response.headerValue("X-Cache").contains("HIT")

# Caido workflow：在 Match&Replace 里给每个请求注入随机 cb 参数，再用 HTTPQL
# req.method.eq("GET") AND resp.header.name.eq("X-Cache") AND resp.header.value.cont("HIT")

# Nuclei 模板
nuclei -tags cache,cache-poisoning,cache-deception -u https://target

# 手测 unkeyed header 反射
curl -sk -H "X-Forwarded-Host: cb$RANDOM.evil.example" "https://target/?cb=$RANDOM" -i | head
```

## 6. Reporting Angle

* **Title 模板**：`Web Cache <Deception|Poisoning> via <vector> on <endpoint> exposes <PII|XSS|redirect>`
* **CVSS 3.1 区间**：
  * Deception 泄露 PII / token：6.5 – 8.6（AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N）
  * Poisoning 注入存储型 XSS：8.0 – 9.6（S:C/C:H/I:H/A:L）
  * 仅缓住静态错误页：3.7 – 5.3
* **VRT P-level**：Deception 全用户范围 → P2；Poisoning 全 edge → P1
* **CWE 推荐**：CWE-525（Web Browser Cache Containing Sensitive Info）/ CWE-444（HTTP 解析不一致）
* **PoC 必须**：
  - 两个测试账号 A/B：A 触发缓住，B（或匿名）匿名命中
  - 完整 `Age` / `X-Cache` 头截图证明 HIT
  - 使用 cache-buster 参数避免影响真实用户
* **Suggested Fix**（≥2）：
  1. CDN 层强制 `Cache-Control: private` / `no-store` 优先于扩展名规则
  2. 把所有可信"伪静态后缀"路径列白名单，其余拒绝缓存
  3. 把 `Cookie` / `Authorization` / `Origin` 加入 cache key 或 Vary
  4. unkeyed header 一律剥离或加入 cache key

## 7. 已迁移技法（来自 KB）

- [[techniques/cache_deception_omer_gil|经典 Path Confusion Deception]]
- [[techniques/cache_poisoning_unkeyed_header|Unkeyed Header Poisoning]]
- [[techniques/nextjs_isr_cache|Next.js ISR Data Route 缓存]]
- [[techniques/parameter_cloaking|Parameter Cloaking 双解析]]
