---
type: case
vuln_class: Link Param Tampering
source_url: https://sl4x0.medium.com/magic-links-as-gateways-account-takeovers-e9c911ceb6f9
source_author: sl4x0 (Abdelrhman Allam)
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Apps using magic link auth
---

# Magic Links as Gateways to Account Takeovers

## 链接

https://sl4x0.medium.com/magic-links-as-gateways-account-takeovers-e9c911ceb6f9

## 漏洞类型

Link Param Tampering

## 目标业务场景

Apps using magic link auth

## 关键利用链摘要

Tamper require_ad_spend / account_type params in magic link URL or reuse leaked token

## 可迁移技法

1-click ATO via email link manipulation in auth flows

## 为什么值得收藏

- 该案例可作为 `Link Param Tampering` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
