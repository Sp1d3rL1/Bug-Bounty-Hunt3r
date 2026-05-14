---
id: clk-waf-bypass
title: WAF / CDN Rule Bypass
owasp_anchor: [WSTG-INPV, A05:2021]
cwe: [CWE-693, CWE-444]
severity_typical: P2-P4
playbook: playbooks/waf_bypass.yaml
last_updated: 2026-05-15
sources:
  - docs/intelligence_kb/techniques/niche_tricks/17-react2shell-scanner-for-next-js-cve-bypass-waf.md
  - docs/intelligence_kb/techniques/niche_tricks/7-google-cloud-armor-waf-bypass-via-subdomain-host-header.md
maturity: extending
---

# WAF / CDN Rule Bypass Checklist

> 双语 / Bilingual: 把已知漏洞绕过 WAF/CDN 规则，让 payload 真正触达后端。
> 这本身不是漏洞，但是 *让其他漏洞可被利用* 的关键。
> Authorization-only：所有绕过尝试只在授权目标上做；**不**用于规避真实流量限制。

---

## 1. WAF / CDN 指纹识别

- [ ] 发送典型恶意 payload (e.g. `<script>alert(1)</script>` / `' OR 1=1--`) 看 403/406/429 响应特征
- [ ] header 特征：CF-RAY (Cloudflare) / X-Akamai-* / X-Sucuri-* / X-Iinfo (Incapsula) / X-CDN
- [ ] favicon hash 对照已知 WAF
- [ ] tools: wafw00f / whatwaf / nuclei -tags waf / chrome devtools network panel

## 2. Method / Verb tampering

- [ ] `GET /admin` 阻断 → 试 `POST /admin?_method=GET`
- [ ] `X-HTTP-Method-Override: GET` / `X-Original-URL: /admin` 头
- [ ] verb 大小写：`gEt /admin`
- [ ] `OPTIONS /admin` 看是否泄露 Allow 头里的方法
- [ ] HTTP/0.9 raw request（部分 CDN 不解析）

## 3. URL 编码 / Unicode tricks

- [ ] 双重 URL 编码：`%2527` (= `%27` after one decode)
- [ ] 大小写混合：`%2E` vs `%2e`
- [ ] Unicode overlong UTF-8：`%C0%AF` (= `/`)
- [ ] Unicode 同形：`／` (U+FF0F) vs `/`
- [ ] base64 / hex / 数字实体编码 (HTML entity / decimal / hex)
- [ ] URL fragment：`?q=<script>#fragment` (WAF 不看 fragment)

## 4. Path / Case games

- [ ] 路径混淆：`/admin/./` `/admin//` `/admin;jsessionid=x` `/admin..;/`
- [ ] 大小写：`/Admin` `/ADMIN` (case-sensitive routing)
- [ ] 反斜杠：`/admin\..` `/admin\\`
- [ ] 后缀加 `.json` `.php` `.bak`
- [ ] WAF 路由规则 vs origin 路由规则差异

## 5. Header / Body smuggling

- [ ] `Content-Type: application/xml` 走不同解析路径
- [ ] `Content-Encoding: gzip` + 解压后藏 payload
- [ ] `Transfer-Encoding: chunked` + 多 chunk 拆分
- [ ] charset confusion: `Content-Type: text/html; charset=ibm500`
- [ ] HTTP/2 pseudo-header 注入 (`:path` 替代 `Host`)

## 6. Origin direct access

- [ ] 找到 origin IP（censys / shodan / favicon hash / DNS history）
- [ ] 直接访问 origin：`curl -H "Host: target.com" https://<origin-ip>`
- [ ] 如果 origin 不验 Host 头 → WAF 完全绕过
- [ ] subdomain takeover 的 dangling DNS 也常通向 origin

## 7. Rate limit / Captcha bypass

- [ ] 旋转 IP（X-Forwarded-For / X-Real-IP / X-Cluster-Client-IP / Forwarded）
- [ ] 旋转 User-Agent
- [ ] sleep + jitter
- [ ] 利用 cdn cache：相同请求只算一次

## 8. CDN-specific tricks

### Cloudflare
- [ ] CF-Connecting-IP 头注入 (origin 信任 → IP spoof)
- [ ] CF cache poisoning via X-Forwarded-Host
- [ ] WAF rule downgrade via plan 检测 (free vs enterprise)

### AWS WAF / CloudFront
- [ ] AWS managed rules 大小限制：body > 8KB 部分不被检测
- [ ] CloudFront 的 forwarded headers 配置差异

### Akamai
- [ ] EdgeWorker race condition
- [ ] Akamai Pragma debug headers

### Imperva / Incapsula
- [ ] visid_incap_* cookie 重用
- [ ] _Incapsula_Resource pwned auth flow

## 9. 自动化辅助

```bash
# WAF 指纹
wafw00f https://target.com
nuclei -tags waf -u https://target.com

# 编码 fuzz
ffuf -u https://target.com/admin -w encodings.txt:FUZZ -X POST -mc all

# Origin 探测
favfreak -t target.com   # favicon hash → shodan
shodan search "favicon.hash:<hash>"

# Burp / Caido extensions
# - Burp Bambdas: WAF Bypass collection
# - Caido HTTPQL: filter for blocked vs allowed
```

## 10. Reporting Angle

* **Severity**: WAF bypass 本身通常 P4-P5；与具体漏洞链一起报才有高赏金（"WAF bypass + IDOR" → P2/P3）
* **Title 模板**：`<original vuln> via WAF bypass using <technique>`
  例：`SQLi in /api/search via Unicode overlong UTF-8 bypass of Cloudflare WAF`
* **CWE**：CWE-693（保护机制失效）/ CWE-444（HTTP 请求走私）
* **PoC 必须**：(1) 不绕过时 payload 被拦截截图 (2) 加上绕过技巧后 payload 触达后端的证据 (3) 后端因此暴露的实际影响
* **Suggested Fix**：在 origin 也部署同等过滤；不要把所有过滤逻辑只放在 WAF 层；origin 验证 Host 头
* **重要**：单独的 WAF bypass 没有具体漏洞触达原本不可达端点，平台普遍不收

## 11. 已迁移技法（来自 KB — 由 checklist_extend.py 自动填充）

<!-- BACKLINKS START -->
<!-- 由 scripts/checklist_extend.py --apply --commit 自动写入 -->
<!-- BACKLINKS END -->
