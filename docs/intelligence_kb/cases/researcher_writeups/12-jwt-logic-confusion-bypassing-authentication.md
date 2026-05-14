---
type: case
vuln_class: Algorithm Confusion
source_url: https://cybersecuritywriteups.com/5-jwt-logic-confusion-bypassing-authentication-b247f7910f70
source_author: Abhijeet kumawat
source_date: 2026-02-10
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - JWT auth web apps
---

# JWT Logic Confusion Bypassing Authentication

## 链接

https://cybersecuritywriteups.com/5-jwt-logic-confusion-bypassing-authentication-b247f7910f70

## 漏洞类型

Algorithm Confusion

## 目标业务场景

JWT auth web apps

## 关键利用链摘要

Force server to verify HS256 with public key extracted from RS256 or flip alg handling

## 可迁移技法

ATO by forging tokens in apps trusting wrong verification path

## 为什么值得收藏

- 该案例可作为 `Algorithm Confusion` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->
