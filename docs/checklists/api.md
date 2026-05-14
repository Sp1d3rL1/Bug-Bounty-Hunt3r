---
id: clk-api
title: API Security (OWASP API Top 10 2023 完整覆盖)
owasp_anchor: [API1:2023, API2:2023, API3:2023, API4:2023, API5:2023, API6:2023, API7:2023, API8:2023, API9:2023, API10:2023]
cwe: [CWE-639, CWE-285, CWE-269, CWE-770, CWE-918, CWE-1230, CWE-829]
severity_typical: P1-P3
playbook: playbooks/api.yaml
last_updated: 2026-05-15
sources:
  - docs/intelligence_kb/cases/public_reports/1-improper-access-control-on-enterprise-invitation-endpoint-leading-to-account-takeover.md
  - docs/intelligence_kb/cases/public_reports/10-graphql-introspection-enabled-on-shopify-storefront-api.md
  - docs/intelligence_kb/cases/public_reports/11-unauth-idor-on-nasa-gitlab-users-api-pii-hostnames-exposed.md
  - docs/intelligence_kb/cases/public_reports/12-cross-tenant-idor-in-wearables-platform-affecting-multiple-tenants.md
  - docs/intelligence_kb/cases/public_reports/14-builder-role-secrets-overwrite-violating-permission-boundaries-in-workspace.md
  - docs/intelligence_kb/cases/public_reports/17-slack-integration-allowing-unauthorized-workspace-self-join-bypassing-settings.md
  - docs/intelligence_kb/cases/public_reports/20-h1-2487889-idor-on-bugs-json-exposing-private-report-details.md
  - docs/intelligence_kb/cases/public_reports/21-mass-assignment-idor-in-rest-api-for-privilege-escalation.md
  - docs/intelligence_kb/cases/public_reports/24-graphql-idor-in-shopify-staff-access-cross-shop-billing-data.md
  - docs/intelligence_kb/cases/public_reports/25-business-logic-race-condition-idor-in-fintech-recharge-history-api.md
  - docs/intelligence_kb/cases/public_reports/3-nextcloud-bola-in-outofoffice-userid-api-cross-user-ooo-data-leak.md
  - docs/intelligence_kb/cases/public_reports/6-real-ssrf-via-ipv6-redirects-on-hackerone.md
  - docs/intelligence_kb/cases/public_reports/6-unauthorized-cross-tenant-data-access-in-stripo-ai-hub-via-deleted-project.md
  - docs/intelligence_kb/cases/public_reports/8-cross-tenant-improper-access-control-in-import-flow.md
  - docs/intelligence_kb/cases/public_reports/9-unauthenticated-ssrf-via-public-reference-api-sharing-token-bypass.md
  - docs/intelligence_kb/cases/researcher_writeups/1-artipacked-github-actions-artifact-token-leak.md
  - docs/intelligence_kb/cases/researcher_writeups/1-finding-an-idor-in-user-profile-api-a-15-000-journey-to-critical.md
  - docs/intelligence_kb/cases/researcher_writeups/1-graphql-introspection-enabled-batch-query-idor-and-authorization-bypass-in-fintech.md
  - docs/intelligence_kb/cases/researcher_writeups/1-i-found-an-idor-worth-20000-pii-exposure-via-staging-api-idor.md
  - docs/intelligence_kb/cases/researcher_writeups/10-idor-hunting-with-burp-suite-1000-order-api-exposure.md
  - docs/intelligence_kb/cases/researcher_writeups/103-5-graphql-security-how-i-found-and-exploited-critical-idor-and-authorization-bypas.md
  - docs/intelligence_kb/cases/researcher_writeups/104-2-from-idor-to-sql-injection-in-graphql-websocket-escalated-to-pii-leak.md
  - docs/intelligence_kb/cases/researcher_writeups/11-idor-fetching-5-million-images-via-broken-access-control.md
  - docs/intelligence_kb/cases/researcher_writeups/12-autogpt-ssrf-protection-bypass-to-internal-services.md
  - docs/intelligence_kb/cases/researcher_writeups/12-race-condition-broken-access-control-leading-to-super-admin-creation.md
  - docs/intelligence_kb/cases/researcher_writeups/13-bola-in-lovable-vibe-coding-api-cross-project-source-db-leak.md
  - docs/intelligence_kb/cases/researcher_writeups/15-oauth-dynamic-client-registration-open-redirect-to-full-read-ssrf.md
  - docs/intelligence_kb/cases/researcher_writeups/17-idor-in-saved-payments-api-on-zomato-multi-tenant.md
  - docs/intelligence_kb/cases/researcher_writeups/18-idor-in-graphql-invitation-flow-leading-to-ato.md
  - docs/intelligence_kb/cases/researcher_writeups/19-500-uuid-swap-idor-in-device-management-api.md
  - docs/intelligence_kb/cases/researcher_writeups/2-critical-idor-privilege-escalation-in-role-permission-management.md
  - docs/intelligence_kb/cases/researcher_writeups/2-idor-in-user-profile-api-15k-critical-via-parameter-swap.md
  - docs/intelligence_kb/cases/researcher_writeups/2-ssrf-protection-bypass-in-autogpt-ai-agent-tool.md
  - docs/intelligence_kb/cases/researcher_writeups/20-full-read-ssrf-in-gitlab-analytics-dashboard-bypassing-localhost.md
  - docs/intelligence_kb/cases/researcher_writeups/20-microsoft-teams-guest-access-cross-tenant-policy-bypass.md
  - docs/intelligence_kb/cases/researcher_writeups/22-supportcandy-ticket-attachment-idor-cve-2026-1251-cross-ticket-file-access.md
  - docs/intelligence_kb/cases/researcher_writeups/3-rce-via-group-access-validation-flaw-in-ssh-key-authority-open-source-tool.md
  - docs/intelligence_kb/cases/researcher_writeups/4-massive-cross-tenant-access-control-bug-in-crm-via-host-header-swap.md
  - docs/intelligence_kb/cases/researcher_writeups/5-multi-tenant-isolation-failure-via-client-controlled-x-prm-tenantid-header.md
  - docs/intelligence_kb/cases/researcher_writeups/5-ssrf-indirect-prompt-injection-chain-in-ai-assistant-feature.md
  - docs/intelligence_kb/cases/researcher_writeups/5-uuid-idor-chained-with-id-leak-endpoint-critical-cross-tenant.md
  - docs/intelligence_kb/cases/researcher_writeups/6-idor-scheduled-job-data-leaked-across-projects-by-projectid-singlestore.md
  - docs/intelligence_kb/cases/researcher_writeups/7-idor-in-jwt-protected-card-viewer-api.md
  - docs/intelligence_kb/cases/researcher_writeups/7-idor-in-multi-tenant-api-via-uuid-swap-in-device-info-endpoint.md
  - docs/intelligence_kb/cases/researcher_writeups/7-subscription-paywall-bypass-leading-to-talent-profile-access-and-pii-disclosure.md
  - docs/intelligence_kb/cases/researcher_writeups/7-tenant-admin-idor-allowing-cross-tenant-file-deletion.md
  - docs/intelligence_kb/cases/researcher_writeups/9-from-idor-to-bypass-fixed-bug-still-exposed-6-4m-users-data-part-2.md
  - docs/intelligence_kb/cases/researcher_writeups/9-low-privilege-access-to-workspace-members-data-via-direct-api.md
  - docs/intelligence_kb/cases/researcher_writeups/9-next-js-cache-poisoning-race-condition-cve-2025-32421.md
  - docs/intelligence_kb/cases/x_threads/14-post-api-rooms-room-templates-idor-cross-org-template-creation.md
  - docs/intelligence_kb/cases/x_threads/16-otp-qr-link-base64-idor-admin-session-hijack-via-employer-portal.md
  - docs/intelligence_kb/cases/x_threads/18-1500-idor-fetching-5m-images-via-object-id-swap.md
  - docs/intelligence_kb/cases/x_threads/4-unauthenticated-bola-on-managed-bbp-500-critical.md
  - docs/intelligence_kb/review_queue/13-graphql-voyager-introspection-for-schema-mapping-in-bb.md
  - docs/intelligence_kb/review_queue/15-finding-broken-access-control-in-multi-tenant-systems-practical-techniques.md
  - docs/intelligence_kb/review_queue/17-api-bug-bounty-mastery-2026-hidden-endpoints-bola-chains.md
  - docs/intelligence_kb/review_queue/22-intigriti-bug-bytes-235-real-ssrf-ipv6-and-idor-methodology.md
  - docs/intelligence_kb/review_queue/23-bugquest-2026-day-23-spot-basic-idor-advanced-variants-in-api.md
  - docs/intelligence_kb/review_queue/resource-13-graphql-voyager-introspection-for-schema-mapping-in-bb.md
  - docs/intelligence_kb/review_queue/resource-15-finding-broken-access-control-in-multi-tenant-systems-practical-techniques.md
  - docs/intelligence_kb/review_queue/resource-17-api-bug-bounty-mastery-2026-hidden-endpoints-bola-chains.md
  - docs/intelligence_kb/review_queue/resource-22-intigriti-bug-bytes-235-real-ssrf-ipv6-and-idor-methodology.md
  - docs/intelligence_kb/review_queue/resource-23-bugquest-2026-day-23-spot-basic-idor-advanced-variants-in-api.md
  - docs/intelligence_kb/techniques/evergreen_new_context/14-blind-ssrf-via-dns-in-pdf-generator-of-saas-export-feature.md
  - docs/intelligence_kb/techniques/evergreen_new_context/19-second-order-idor-via-profile-update-affecting-high-privilege-module.md
  - docs/intelligence_kb/techniques/evergreen_new_context/24-api-versioning-bypass-legacy-v1-endpoints-lack-patches-in-saas.md
  - docs/intelligence_kb/techniques/evergreen_new_context/8-nested-json-object-wrapping-for-idor-bypass-in-api.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-1-finding-an-idor-in-user-profile-api-a-15-000-journey-to-critical.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-11-idor-fetching-5-million-images-via-broken-access-control.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-12-race-condition-broken-access-control-leading-to-super-admin-creation.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-15-oauth-dynamic-client-registration-open-redirect-to-full-read-ssrf.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-17-idor-in-saved-payments-api-on-zomato-multi-tenant.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-2-ssrf-protection-bypass-in-autogpt-ai-agent-tool.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-20-full-read-ssrf-in-gitlab-analytics-dashboard-bypassing-localhost.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-21-mass-assignment-idor-in-rest-api-for-privilege-escalation.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-25-business-logic-race-condition-idor-in-fintech-recharge-history-api.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-5-ssrf-indirect-prompt-injection-chain-in-ai-assistant-feature.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-6-real-ssrf-via-ipv6-redirects-on-hackerone.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-7-idor-in-multi-tenant-api-via-uuid-swap-in-device-info-endpoint.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-9-unauthenticated-ssrf-via-public-reference-api-sharing-token-bypass.md
  - docs/intelligence_kb/techniques/new_2024_2026/101-1-graphql-introspection-enabled-leading-to-idor-and-authorization-bypass.md
  - docs/intelligence_kb/techniques/new_2024_2026/101-4-race-conditions-and-business-logic-in-microservices-for-2026-bug-bounties.md
  - docs/intelligence_kb/techniques/new_2024_2026/104-3-idor-hunting-tips.md
  - docs/intelligence_kb/techniques/new_2024_2026/105-4-race-condition-multiple-refund-abuse.md
  - docs/intelligence_kb/techniques/new_2024_2026/12-path-param-app-password-bola-in-nextcloud-style-apps.md
  - docs/intelligence_kb/techniques/new_2024_2026/13-testing-static-keywords-like-my-vs-tenant-id-for-cross-tenant-access.md
  - docs/intelligence_kb/techniques/new_2024_2026/15-method-switching-for-idor-impact-getpost-put-delete.md
  - docs/intelligence_kb/techniques/new_2024_2026/17-refund-race-condition-for-multiple-refunds.md
  - docs/intelligence_kb/techniques/new_2024_2026/19-invoice-idor-for-unauthorized-access-refund-manipulation.md
  - docs/intelligence_kb/techniques/new_2024_2026/201-5-claude-bug-bounty-hunter-ai-assisted-recon-for-oauth-and-graphql.md
  - docs/intelligence_kb/techniques/new_2024_2026/21-capitalization-nested-object-tricks-for-bola-bypass-in-mass-assignment.md
  - docs/intelligence_kb/techniques/new_2024_2026/21-tenant-id-manipulation-in-graphql-field-selection-for-workspace-data.md
  - docs/intelligence_kb/techniques/new_2024_2026/24-array-idor-in-graphql-by-wrapping-ids-in-nested-objects.md
  - docs/intelligence_kb/techniques/new_2024_2026/25-mass-fuzzing-company-user-role-ids-in-multi-tenant-rbac-apis.md
  - docs/intelligence_kb/techniques/new_2024_2026/25-second-order-idor-via-scheduled-jobs-async-processing.md
  - docs/intelligence_kb/techniques/new_2024_2026/8-json-nested-id-wrapping-bypass-for-outer-auth-validation.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-1-artipacked-github-actions-artifact-token-leak.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-1-i-found-an-idor-worth-20000-pii-exposure-via-staging-api-idor.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-1-improper-access-control-on-enterprise-invitation-endpoint-leading-to-acco.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-10-idor-hunting-with-burp-suite-1000-order-api-exposure.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-11-unauth-idor-on-nasa-gitlab-users-api-pii-hostnames-exposed.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-12-cross-tenant-idor-in-wearables-platform-affecting-multiple-tenants.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-13-bola-in-lovable-vibe-coding-api-cross-project-source-db-leak.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-14-builder-role-secrets-overwrite-violating-permission-boundaries-in-worksp.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-14-post-api-rooms-room-templates-idor-cross-org-template-creation.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-16-otp-qr-link-base64-idor-admin-session-hijack-via-employer-portal.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-18-1500-idor-fetching-5m-images-via-object-id-swap.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-18-idor-in-graphql-invitation-flow-leading-to-ato.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-19-500-uuid-swap-idor-in-device-management-api.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-2-critical-idor-privilege-escalation-in-role-permission-management.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-2-idor-in-user-profile-api-15k-critical-via-parameter-swap.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-20-h1-2487889-idor-on-bugs-json-exposing-private-report-details.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-22-supportcandy-ticket-attachment-idor-cve-2026-1251-cross-ticket-file-acce.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-24-graphql-idor-in-shopify-staff-access-cross-shop-billing-data.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-3-nextcloud-bola-in-outofoffice-userid-api-cross-user-ooo-data-leak.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-4-massive-cross-tenant-access-control-bug-in-crm-via-host-header-swap.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-4-unauthenticated-bola-on-managed-bbp-500-critical.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-5-multi-tenant-isolation-failure-via-client-controlled-x-prm-tenantid-heade.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-5-uuid-idor-chained-with-id-leak-endpoint-critical-cross-tenant.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-6-idor-scheduled-job-data-leaked-across-projects-by-projectid-singlestore.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-6-unauthorized-cross-tenant-data-access-in-stripo-ai-hub-via-deleted-projec.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-7-tenant-admin-idor-allowing-cross-tenant-file-deletion.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-8-cross-tenant-improper-access-control-in-import-flow.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-9-low-privilege-access-to-workspace-members-data-via-direct-api.md
  - docs/intelligence_kb/techniques/niche_tricks/1-nested-json-idor-bypass.md
  - docs/intelligence_kb/techniques/niche_tricks/104-1-the-depths-of-bola-and-idor.md
  - docs/intelligence_kb/techniques/niche_tricks/104-4-graphql-pentesting-for-bug-bounty-hunters.md
  - docs/intelligence_kb/techniques/niche_tricks/104-5-state-of-api-security-2026-report.md
  - docs/intelligence_kb/techniques/niche_tricks/15-wayback-for-private-post-file-access-post-removal.md
  - docs/intelligence_kb/techniques/niche_tricks/16-subgroupid-manipulation-for-unauthorized-post-creation.md
  - docs/intelligence_kb/techniques/niche_tricks/201-1-what-bugs-you-should-look-for-in-a-graphql-api-bug-bounty-case-study.md
  - docs/intelligence_kb/techniques/niche_tricks/21-capitalization-nested-object-tricks-for-bola-bypass-in-mass-assignment.md
  - docs/intelligence_kb/techniques/niche_tricks/22-parameter-discovery-for-sqli-xss-ssrf-via-6-methods.md
  - docs/intelligence_kb/techniques/niche_tricks/24-array-idor-in-graphql-by-wrapping-ids-in-nested-objects.md
  - docs/intelligence_kb/techniques/niche_tricks/3-bac-via-http-method-swap-version-rollback-array-id-injection.md
  - docs/intelligence_kb/techniques/niche_tricks/8-json-nested-id-wrapping-bypass-for-outer-auth-validation.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-1-graphql-introspection-enabled-batch-query-idor-and-authorization-bypass-i.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-12-autogpt-ssrf-protection-bypass-to-internal-services.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-17-slack-integration-allowing-unauthorized-workspace-self-join-bypassing-se.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-20-microsoft-teams-guest-access-cross-tenant-policy-bypass.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-7-idor-in-jwt-protected-card-viewer-api.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-7-subscription-paywall-bypass-leading-to-talent-profile-access-and-pii-disc.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-9-from-idor-to-bypass-fixed-bug-still-exposed-6-4m-users-data-part-2.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-9-next-js-cache-poisoning-race-condition-cve-2025-32421.md
maturity: stable
---

# API Security Checklist

> 双语 / Bilingual: 全面覆盖 REST / RPC / Webhook / Server-Sent Events / Internal API。
> GraphQL 单列在 `graphql.md`。OAuth/SSO 单列在 `oauth.md`、`sso_oidc_saml.md`。
> Authorization-only：必须使用项目允许的测试账号，不动真实用户数据。

---

## 1. Recon

### 1.1 端点发现
- [ ] OpenAPI / Swagger / Postman collection（站点 robots.txt / sitemap.xml / GitHub / NPM）
- [ ] 从 JS bundle 抓 `endpoint`、`baseURL`、`API_HOST`：`grep -RE "/api/v[0-9]" *.js`
- [ ] Mobile API ≠ Web API：抓 APK / IPA → strings + jadx → 找内部 endpoint
- [ ] 版本化端点：`/v1`、`/v2`、`/v3`、`/internal`、`/mobile`、`/admin`、`/legacy`
- [ ] 隐藏方法：每个端点尝试 GET/POST/PUT/PATCH/DELETE/OPTIONS/HEAD/CONNECT/PROPFIND
- [ ] Verb tampering：被路由 `GET /admin` 拒绝时，试 `POST /admin?_method=GET`、`X-HTTP-Method-Override: GET`

### 1.2 API 网关 / WAF 指纹
- [ ] 发送畸形请求看 503/403 落到谁（Kong/AWS API Gateway/Apigee/Tyk/Cloudflare/Akamai）
- [ ] 内部 IP 反向解析：`curl -H "Host: internal.example.com" https://api.example.com`
- [ ] CORS 探测：每个端点 `OPTIONS` 看 `Access-Control-Allow-Origin`/`-Credentials` 头

## 2. API1:2023 — Broken Object Level Authorization (BOLA / IDOR)

- [ ] 直接对象 ID：`/api/users/{id}`、`/api/invoices/{uuid}`，用 Account A 的 token 拿 Account B 的资源
- [ ] 间接 ID：filename / hash / slug / signed URL —— 把别人的猜出来或拿到一次后复用
- [ ] 嵌套 ID：`/api/orgs/{org}/projects/{proj}` — 枚举跨 org
- [ ] List 端点过滤：`/api/orders?owner=*` 或省略 owner 参数
- [ ] export / download / receipt / report：权限通常比 read 弱
- [ ] 后台 job / webhook callback：暴露 object ID
- [ ] 二次校验缺失：先调 `/me/cart/add` 再 `/cart/{id}/checkout` 不验所有权

## 3. API2:2023 — Broken Authentication

- [ ] 详见 `oauth.md`、`sso_oidc_saml.md`
- [ ] API Key 写进 URL：日志/Referer/CDN cache 泄露
- [ ] Bearer token 在所有 subdomain 共享
- [ ] long-lived JWT 无 jti 撤销机制
- [ ] /reset-password 接受任意 user_id（bypass current password）
- [ ] login rate-limit 仅按 IP（用户名级 brute-force 仍可）

## 4. API3:2023 — Broken Object Property Level Authorization (BOPLA / Mass Assignment)

- [ ] PUT / PATCH 接受隐藏字段：`role`、`is_admin`、`tenant_id`、`owner_id`、`plan`、`verified`、`balance`、`internal_note`
- [ ] Create vs Update 字段差异：注册时传不进去的字段，update 时能传
- [ ] PATCH 接受从 GET 响应里拷贝的所有字段
- [ ] 移动 API 接受比 Web API 多的字段
- [ ] Excessive data exposure：GET 返回了客户端不需要的字段（PII、internal_id、stripe_customer）

## 5. API4:2023 — Unrestricted Resource Consumption

- [ ] 大量 ID 批量查询：`POST /api/items/bulk?ids=1,2,3,...,10000`
- [ ] 文件上传无大小限制 / 无并发限制
- [ ] PDF / 图片处理：上传 zip bomb / billion laughs / pixel flood
- [ ] 邮件 / SMS 触发：`POST /forgot-password` 不限频
- [ ] WebSocket 长连接：未关闭旧连接堆积资源

## 6. API5:2023 — Broken Function Level Authorization (BFLA)

- [ ] 普通用户调管理函数：`/admin/users/delete`、`/admin/audit/export`
- [ ] 路径里加 admin：`GET /api/admin/users` vs `GET /api/users` 是否仅靠路径校验
- [ ] HTTP 方法差异：`PUT /api/users/{id}` 限制了，但 `POST /api/users/{id}/_update` 没限制
- [ ] header-based role：`X-Role: admin` 是否被信任

## 7. API6:2023 — Unrestricted Access to Sensitive Business Flows

- [ ] 抢购 / 限购：同一账号发 1000 个并发请求
- [ ] 邀请码：枚举 / 重放 / 跨账号重用
- [ ] 退款：发起后立即取消是否仍发钱
- [ ] 订阅：升级 → 立即降级 → 是否被多扣或多得权益

## 8. API7:2023 — Server-Side Request Forgery

- [ ] URL 参数：`?image_url=`、`?webhook=`、`?callback=`、`?import_url=`
- [ ] DNS rebinding（target server 解析两次）
- [ ] Cloud metadata：`http://169.254.169.254/latest/meta-data/`
- [ ] Internal services：`http://localhost:6379`（Redis）、`http://localhost:9200`（ES）
- [ ] PDF generator / Headless browser：`<iframe src="file:///etc/passwd">`、`<img src="http://internal">`
- [ ] gopher:// / dict:// / ftp:// 协议
- [ ] 详见 cloud_aws_metadata_iam.md / cloud_gcp_azure.md

## 9. API8:2023 — Security Misconfiguration

- [ ] 详细 error stack trace 泄露
- [ ] 默认 admin 账号 / 默认 API key
- [ ] HTTP TRACE 启用
- [ ] HSTS / X-Frame-Options / CSP 缺失
- [ ] 详见 cache_deception_poisoning.md / http_request_smuggling.md

## 10. API9:2023 — Improper Inventory Management

- [ ] 旧版本 API 仍可用：`/api/v1/...`
- [ ] 隐藏的 staging / dev API：`api-dev.target.com`
- [ ] 第三方 API 凭据保留在前端 JS（旧供应商）
- [ ] 文档里的端点不在生产上，但生产上有未文档化端点

## 11. API10:2023 — Unsafe Consumption of APIs

- [ ] 调上游 API 时未验证响应：上游被攻击后污染下游
- [ ] 上游返回 HTML 当 JSON 解析
- [ ] 上游 redirect 跟随到内部
- [ ] 第三方 webhook 入站无签名校验（HMAC / mTLS）
- [ ] 第三方供应商 token 滥用：测试 token 流入生产

## 12. 自动化辅助

```bash
# 端点发现
katana -u https://target -d 3 -o endpoints.txt
hakrawler -u https://target -depth 3
gau target.com | tee endpoints.txt
linkfinder -i bundle.js  # 从 JS 抓 endpoint

# OpenAPI fuzz
ffuf -w endpoints.txt -u https://api.target/FUZZ -mc 200,401,403
nuclei -tags exposure,misconfig,api -u https://api.target

# IDOR 自动化（替换两个 token 跑同一组请求）
autorize  # Burp ext

# Mass assignment
arjun -u https://target/api/users -m POST  # 找隐藏字段

# Caido / Burp 配置：自动给所有 PUT/PATCH 加 role/is_admin/tenant_id 字段
```

## 13. Reporting Angle

* **Title 模板**：`<API category> <flaw> allows <attacker role> to <impact> via <endpoint>`
  例：`BOLA in /api/v2/invoices/{id} allows org member to download cross-tenant invoices`
* **Severity 自评**：
  * 跨 tenant 数据读取 → CVSS ≥ 6.5 / VRT P2
  * 跨 tenant 数据写入 / 资金动作 → CVSS ≥ 8.5 / VRT P1
  * 单账号信息泄露 → CVSS ≥ 4.0 / VRT P3-P4
* **CWE 推荐**：CWE-639（IDOR） / CWE-285（不当授权） / CWE-770（资源消耗）
* **PoC 必须**：两个测试账号 A/B，完整 HTTP 请求/响应，token 全脱敏
* **Suggested Fix**：服务端按 user/tenant 重新查找资源；不要信任客户端传的 id；引入 ABAC/RBAC 中央策略
