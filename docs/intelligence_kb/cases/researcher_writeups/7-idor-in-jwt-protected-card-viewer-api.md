---
type: case
vuln_class: BOLA/IDOR
source_url: https://medium.com/@zaid.zrf/dor-in-a-jwt-protected-card-viewer-api-codereviewlab-writeup-57d437a5d481
source_author: zaid.zrf
source_date: 2026-03-20
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Card viewer API
---

# IDOR in JWT-Protected Card Viewer API

## 链接

https://medium.com/@zaid.zrf/dor-in-a-jwt-protected-card-viewer-api-codereviewlab-writeup-57d437a5d481

## 漏洞类型

BOLA/IDOR

## 目标业务场景

Card viewer API

## 关键利用链摘要

Bypass JWT validation by direct object ID swap in card viewer endpoint

## 可迁移技法

Edge case where JWT present but no server-side ownership check

## 为什么值得收藏

- 该案例可作为 `BOLA/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->
