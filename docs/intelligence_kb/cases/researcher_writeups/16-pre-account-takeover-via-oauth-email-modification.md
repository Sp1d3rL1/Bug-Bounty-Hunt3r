---
type: case
vuln_class: Account Linking + Email Modification
source_url: https://www.reddit.com/r/bugbounty/comments/1jy0x4q/preaccount_takeover_via_oauth_email_modification/
source_author: Anonymous hunter (Reddit)
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - OAuth + profile edit flows
---

# Pre-Account Takeover via OAuth + Email Modification

## 链接

https://www.reddit.com/r/bugbounty/comments/1jy0x4q/preaccount_takeover_via_oauth_email_modification/

## 漏洞类型

Account Linking + Email Modification

## 目标业务场景

OAuth + profile edit flows

## 关键利用链摘要

Login via Google OAuth then bypass frontend disabled attr to change profile email to victim

## 可迁移技法

Links attacker OAuth to victim email for takeover

## 为什么值得收藏

- 该案例可作为 `Account Linking + Email Modification` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->

<!-- backlink: docs/checklists/subdomain_takeover.md -->
