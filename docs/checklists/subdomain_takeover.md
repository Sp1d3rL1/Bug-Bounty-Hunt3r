---
id: clk-subdomain-takeover
title: Subdomain & DNS Takeover
owasp_anchor: [WSTG-CONF]
cwe: [CWE-99, CWE-353]
severity_typical: P2-P3
playbook: playbooks/subdomain_takeover.yaml
last_updated: 2026-05-14
sources:
  - docs/intelligence_kb/cases/public_reports/1-improper-access-control-on-enterprise-invitation-endpoint-leading-to-account-takeover.md
  - docs/intelligence_kb/cases/researcher_writeups/1-500-oauth-account-fusion-pre-takeover-attack.md
  - docs/intelligence_kb/cases/researcher_writeups/1-client-side-path-traversal-cspt-to-account-takeover-xss-via-profile-url-traversal.md
  - docs/intelligence_kb/cases/researcher_writeups/10-postmessage-listener-with-target-com-wildcard-cors-misconfig-to-home-automation-takeo.md
  - docs/intelligence_kb/cases/researcher_writeups/11-hidden-role-escalation-via-invite-api-in-organization.md
  - docs/intelligence_kb/cases/researcher_writeups/11-how-i-found-5-oauth-misconfigurations-leading-to-pre-account-takeover.md
  - docs/intelligence_kb/cases/researcher_writeups/13-magic-links-as-gateways-to-account-takeovers.md
  - docs/intelligence_kb/cases/researcher_writeups/16-pre-account-takeover-via-oauth-email-modification.md
  - docs/intelligence_kb/cases/researcher_writeups/2-graphql-introspection-to-admin-takeover-via-unauthenticated-mutations.md
  - docs/intelligence_kb/cases/researcher_writeups/23-cve-2025-22146-sentry-saml-sso-auth-bypass.md
  - docs/intelligence_kb/cases/researcher_writeups/24-account-takeover-via-google-oauth-misconfiguration.md
  - docs/intelligence_kb/cases/researcher_writeups/4-chatgpt-account-takeover-wildcard-web-cache-deception.md
  - docs/intelligence_kb/cases/researcher_writeups/5-oauth-misbinding-vulnerability-silent-account-takeover.md
  - docs/intelligence_kb/cases/researcher_writeups/6-full-workspace-account-takeover-via-jwt-alg-none.md
  - docs/intelligence_kb/cases/researcher_writeups/7-xboard-v2board-magic-link-token-leak-unauthenticated-ato.md
  - docs/intelligence_kb/cases/researcher_writeups/8-account-takeover-using-sso-login.md
  - docs/intelligence_kb/cases/researcher_writeups/9-nextjs-auth0-insecure-session-cache-key-hijack.md
  - docs/intelligence_kb/techniques/new_2024_2026/102-2-oauth-account-fusion-pre-takeover-via-email-matching-bypass.md
  - docs/intelligence_kb/techniques/new_2024_2026/102-5-misconfigured-sso-leading-to-account-takeover.md
  - docs/intelligence_kb/techniques/new_2024_2026/15-jwt-signature-bypass-leading-to-admin-password-change.md
  - docs/intelligence_kb/techniques/new_2024_2026/16-subdomain-takeover-check-with-subzy.md
  - docs/intelligence_kb/techniques/new_2024_2026/2-aws-account-takeover-via-github-actions-oidc-wildcard-trust.md
  - docs/intelligence_kb/techniques/new_2024_2026/5-s3-bucket-takeover-via-nosuchbucket-error.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-1-client-side-path-traversal-cspt-to-account-takeover-xss-via-profile-url-t.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-1-improper-access-control-on-enterprise-invitation-endpoint-leading-to-acco.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-10-postmessage-listener-with-target-com-wildcard-cors-misconfig-to-home-aut.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-11-hidden-role-escalation-via-invite-api-in-organization.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-11-how-i-found-5-oauth-misconfigurations-leading-to-pre-account-takeover.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-13-magic-links-as-gateways-to-account-takeovers.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-2-graphql-introspection-to-admin-takeover-via-unauthenticated-mutations.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-24-account-takeover-via-google-oauth-misconfiguration.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-4-chatgpt-account-takeover-wildcard-web-cache-deception.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-5-oauth-misbinding-vulnerability-silent-account-takeover.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-7-xboard-v2board-magic-link-token-leak-unauthenticated-ato.md
  - docs/intelligence_kb/techniques/niche_tricks/15-jwt-signature-bypass-leading-to-admin-password-change.md
  - docs/intelligence_kb/techniques/niche_tricks/201-3-oauth-2-0-bug-bounty-2026-csrf-in-oauth-token-leakage-account-takeover-chains.md
  - docs/intelligence_kb/techniques/niche_tricks/21-otp-bypass-via-response-manipulation.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-1-500-oauth-account-fusion-pre-takeover-attack.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-16-pre-account-takeover-via-oauth-email-modification.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-23-cve-2025-22146-sentry-saml-sso-auth-bypass.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-6-full-workspace-account-takeover-via-jwt-alg-none.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-8-account-takeover-using-sso-login.md
maturity: stable
---

# Subdomain & DNS Takeover Checklist

> 双语 / Bilingual: 子域接管 + dangling DNS + 服务端 fingerprint 接管攻击面合一。
> 用法：先做"Recon & DNS 资产收敛"列出所有 record + 当前 service，然后按 record 类型与服务清单逐项核对。
> Authorization-only：只有当目标 SRT 明确允许接管 PoC 时才注册资源；接管后立刻挂"Hold by researcher"页并通报，不挂任何执行性 payload。

---

## 1. Recon & DNS 资产收敛

- [ ] 子域收集：被动（crt.sh / chaos / Censys / SecurityTrails / DNSDumpster）+ 主动（amass / subfinder / puredns / shuffledns）
- [ ] 解析全记录：`dnsx -resp -a -aaaa -cname -ns -mx -txt`
- [ ] 区分 wildcard 解析与真实记录（`dnsx -wd target.com`）
- [ ] 收集历史记录：SecurityTrails / Wayback / passive DNS
- [ ] 找内部域名（`*.corp.` / `*.internal.` / `*.staging.`）
- [ ] GitHub 公开 repo grep `cname:`、`s3.amazonaws.com`、`herokuapp.com`、`azurewebsites.net`
- [ ] 列出云资产 ID 与生命周期（活跃 / 已下线 / 测试残留）

## 2. CNAME-based Takeover（最常见）

按服务清单核对（fingerprint 见 can-i-take-over-xyz）：

- [ ] AWS：S3 `<bucket>.s3.amazonaws.com` (`NoSuchBucket`)、S3 website、CloudFront `*.cloudfront.net`、Elastic Beanstalk、API Gateway/AppSync、ACM 验证 CNAME、Global Accelerator
- [ ] Heroku：`*.herokuapp.com`、custom domain `<app>.herokudns.com`、SSL endpoints
- [ ] Pages 类：GitHub Pages `*.github.io`、GitLab `*.gitlab.io`、Bitbucket `*.bitbucket.io`、Codespaces `*.app.github.dev`
- [ ] Blog/Storefront：Tumblr、Shopify `*.myshopify.com`、Tilda、Webflow、Strikingly、Wix、Squarespace、Ghost.io
- [ ] CDN/Edge：Fastly `*.fastly.net`、Akamai EdgeKey/EdgeSuite、KeyCDN、BunnyCDN、StackPath
- [ ] PaaS：Surge.sh、Netlify、Vercel/Now、Cloudflare Pages/Workers、Pantheon、WP Engine、Kinsta、Pressable
- [ ] Azure：Web App `*.azurewebsites.net`、CDN/Front Door、Traffic Manager、Storage Static Site
- [ ] GCP：App Engine/Cloud Run、Cloud Storage、Firebase `*.web.app`/`*.firebaseapp.com`、Google Sites
- [ ] Helpdesk：Zendesk (`Help Center Closed`)、Freshdesk、Helpscout、Intercom、Statuspage
- [ ] Marketing：LaunchDarkly、Optimizely、Segment、Mixpanel、Hubspot
- [ ] 邮件代发 CNAME：Mailgun / SendGrid / Postmark / Mandrill `mta*.target.com`
- [ ] 文档/社区：Readme.io、Gitbook、Algolia DocSearch、Discourse、Discord vanity、Slack
- [ ] 现代 PaaS：DigitalOcean App、Render、Fly.io、Railway

> 完整 fingerprint 表见 `can-i-take-over-xyz`；未列服务用通用流程：响应体 + 状态码 + cookie 共同判别。

## 3. 其他 Record 类型 Takeover

- [ ] A / AAAA dangling：弹性 IP 回收 → 抢注同 IP（[example: AWS Elastic IP reuse 类]）
- [ ] NS dangling：`NS sub.target.com -> ns.deleted-zone.com` → 注册外部域 / 在 NS 提供商创建对应 zone（破坏力最大）
- [ ] MX dangling：`MX -> mail.deleted-saas.com` → 接管邮件 → 拿密码重置 → ATO
- [ ] SRV dangling：服务发现 SRV 指向回收资源
- [ ] TXT 信任引用：SPF `include:` / `_dmarc rua=mailto:` / `_acme-challenge` CNAME 指向第三方域 → 注册同名签发证书或接收 DMARC 报告
- [ ] DKIM `_domainkey` CNAME 到 SaaS 选择器 → 注册同名签发任意 DKIM
- [ ] Verification record dangling：Google / Microsoft / Atlassian 域校验 TXT 残留 → 接管 workspace 域

## 4. Wildcard / 内部域 / 中间件 Takeover

- [ ] `*.target.com` 通配符指向 SaaS → 任意子域可被预订（若 SaaS 仅信任 host header 仍生效）
- [ ] 内部 DNS（split-horizon）：外部解析失败但内部可达，VPN 接入后 takeover 可能（仅在授权下）
- [ ] 反代 / Ingress 残留 host 规则：`Host: deleted.target.com` 仍被 proxy 转发到回收 origin
- [ ] CDN origin pull：原 origin S3 桶被删 → 抢注桶 → 接管 CDN 缓存

## 5. 二阶利用 / 业务影响

- [ ] cookie scope `Domain=.target.com` → session 窃取
- [ ] CSP `script-src` / CORS `Allow-Origin` / OAuth redirect_uri / SSO ACS URL 白名单含 dangling 子域
- [ ] 邮件域接管 → 密码重置 ATO（结合 email 流程）
- [ ] 接管子域 → Let's Encrypt HTTP-01 / DNS-01 拿合法证书 → MITM
- [ ] 内部 dangling 子域用于 CI 工件 / package registry → 供应链
- [ ] 钓鱼可信度：直接展示真实子域

## 6. 自动化辅助

```bash
# 资产收敛
subfinder -d target.com -all -silent | tee subs.txt
amass enum -passive -d target.com -o amass.txt
chaos -d target.com -silent >> subs.txt && sort -u subs.txt -o subs.txt

# 全记录解析
dnsx -l subs.txt -a -aaaa -cname -ns -mx -txt -resp -o dns.txt

# 主接管检测器
subzy run --targets subs.txt --concurrency 50 --hide_fails --verify_ssl
nuclei -l subs.txt -tags takeover -severity high,critical -o takeovers.txt
tko-subs -domains=subs.txt -data=providers-data.csv -output=takeovers.csv
python3 dnsReaper.py file --filename subs.txt

# dangling NS / MX
for s in $(cat subs.txt); do
  for n in $(dig +short NS $s); do dig +short $n A | grep -q . || echo "DANGLING NS $s -> $n"; done
  for m in $(dig +short MX $s | awk '{print $2}'); do
    whois ${m%.} | grep -qiE 'no match|not found' && echo "DANGLING MX $s -> $m"
  done
done

# Caido workflow: takeover-fingerprint.yml — 匹配 'NoSuchBucket' / GitHub Pages / Azure 等
# Burp Bambda：响应体含已知 fingerprint 的请求高亮
# 参考 https://github.com/EdOverflow/can-i-take-over-xyz
```

## 7. PoC 与接管后纪律

- [ ] 注册资源 → 仅上传说明文字静态页（`Held by security researcher, contact security@target.com`）
- [ ] 不放 cookie 收集 / fetch / 重定向；不对真实用户做会话操作
- [ ] 报告中说明资产 ID（S3 bucket / Heroku app name），便于厂商回收
- [ ] 接管证据：注册时间戳、whois / 控制台截图、HTTP 响应对比
- [ ] 修复后 24h 内删除占位资源，不留侧通道

## 8. Reporting Angle

* **Title 模板**：`<sub.target.com> dangling <record type> on <provider> allows takeover, leading to <impact>`
  例：`assets.target.com CNAME points to deprovisioned S3 bucket, enabling content takeover and cookie theft`
* **Severity 自评**：
  * NS 接管 → 全 zone 控制 → CVSS 3.1 9.0-9.8 / VRT P1
  * 主域 cookie scope（`Domain=.target.com`）+ 接管 → CVSS 8.0-9.0 / VRT P1
  * MX 接管能拿密码重置邮件 → CVSS 8.0-9.0 / VRT P1-P2
  * 接管子域 + CSP / CORS / OAuth 白名单含该子域 → CVSS 7.0-8.0 / VRT P2
  * 仅静态内容接管（无 cookie / 无 SSO 信任）→ CVSS 5.0-6.0 / VRT P3
  * 仅 dangling 但服务方阻止抢注 → informational P5
* **CWE 推荐**：CWE-99 / CWE-353；接管引发 ATO 追加 CWE-287
* **PoC 必须**：dig 输出 + 控制台截图 + 静态占位页 URL；不展示真实用户被劫持过程
* **Suggested Fix**（至少 2 条）：
  * 资源下线流程必须先删 DNS 再删服务，加自动化巡检（dnsReaper / subzy）
  * 收紧 cookie scope；CSP / CORS / OAuth 白名单只保留生产域
  * 第三方托管 inventory + 季度审计；废弃即清理 CNAME / TXT
  * 启用 DNSSEC；Route 53 Resolver query logging 监控异常 NXDOMAIN

## 9. 已迁移技法（来自 KB）

- [[techniques/s3_bucket_takeover|S3 dangling CNAME 接管]]
- [[techniques/azure_webapp_takeover|Azure Web App 子域接管]]
- [[techniques/dangling_ns_external|NS 指向外部已注销域]]
- [[techniques/mx_takeover_password_reset|MX 接管 → 密码重置 ATO]]
- [[techniques/cname_acme_challenge|_acme-challenge CNAME 接管 → 任意签发证书]]
