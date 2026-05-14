---
type: case
vuln_class: Link Token Exposure
source_url: https://chocapikk.com/posts/2026/xboard-v2board-account-takeover/
source_author: chocapikk
source_date: 2026-04-08
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Open source panels
  - self-hosted auth
---

# Xboard/V2Board Magic Link Token Leak - Unauthenticated ATO

## 链接

https://chocapikk.com/posts/2026/xboard-v2board-account-takeover/

## 漏洞类型

Link Token Exposure

## 目标业务场景

Open source panels / self-hosted auth

## 关键利用链摘要

Call loginWithMailLink endpoint unauth to receive full magic link/token in HTTP response body

## 可迁移技法

Direct ATO without email access on VPN/proxy panels (12k+ stars)

## 为什么值得收藏

- 该案例可作为 `Link Token Exposure` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->

<!-- backlink: docs/checklists/subdomain_takeover.md -->
