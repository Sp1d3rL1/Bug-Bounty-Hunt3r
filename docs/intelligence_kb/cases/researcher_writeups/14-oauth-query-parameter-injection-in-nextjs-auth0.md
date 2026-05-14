---
type: case
vuln_class: Query Param Injection
source_url: https://joshua.hu/2025-bug-bounty-stories-fail
source_author: Joshua Rogers
source_date: 2025-12-22
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Okta
  - Auth0 bug bounty
---

# OAuth Query Parameter Injection in nextjs-auth0

## 链接

https://joshua.hu/2025-bug-bounty-stories-fail

## 漏洞类型

Query Param Injection

## 目标业务场景

Okta/Auth0 bug bounty

## 关键利用链摘要

Inject scope/audience via returnTo param breaking out to top-level /authorize query

## 可迁移技法

Privilege escalation / unauthorized OAuth flows in Auth0-integrated apps

## 为什么值得收藏

- 该案例可作为 `Query Param Injection` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->
