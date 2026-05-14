---
type: case
vuln_class: Account Linking
source_url: https://rikeshbaniya.medium.com/account-takeover-using-sso-logins-fa35f28a358b
source_author: Rikesh Baniya
source_date: 2024-12-12
collected_at: 2026-05-05
freshness: 2024
confidence: high
target_types:
  - HackerOne
  - Bugcrowd programs with SSO
---

# Account Takeover using SSO Login

## 链接

https://rikeshbaniya.medium.com/account-takeover-using-sso-logins-fa35f28a358b

## 漏洞类型

Account Linking

## 目标业务场景

HackerOne / Bugcrowd programs with SSO

## 关键利用链摘要

Bypass SSO identity provider checks during account linking to hijack existing users

## 可迁移技法

Critical ATO via misconfigured enterprise SSO flows

## 为什么值得收藏

- 该案例可作为 `Account Linking` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->

<!-- backlink: docs/checklists/subdomain_takeover.md -->
