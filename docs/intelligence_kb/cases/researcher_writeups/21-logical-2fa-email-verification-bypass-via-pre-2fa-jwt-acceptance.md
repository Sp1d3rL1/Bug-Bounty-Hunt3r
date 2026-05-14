---
type: case
vuln_class: Pre-2FA JWT Acceptance
source_url: (X writeup referenced)
source_author: mhmodgm54
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - MFA + JWT apps
---

# Logical 2FA/Email Verification Bypass via Pre-2FA JWT Acceptance

## 链接

(X writeup referenced)

## 漏洞类型

Pre-2FA JWT Acceptance

## 目标业务场景

MFA + JWT apps

## 关键利用链摘要

JWT issued before OTP/magic link verification accepted on protected endpoints

## 可迁移技法

Bypass 2FA entirely by dropping verification request

## 为什么值得收藏

- 该案例可作为 `Pre-2FA JWT Acceptance` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->
