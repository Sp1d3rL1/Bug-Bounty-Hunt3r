---
type: case
vuln_class: Escalation
source_url: https://hackerone.com/reports/1457471
source_author: Shopify Hunter
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - SaaS e-commerce platform
---

# Shopify Partner Portal Limited Privilege Referral Creation

## 链接

https://hackerone.com/reports/1457471

## 漏洞类型

Escalation

## 目标业务场景

SaaS e-commerce platform

## 关键利用链摘要

Low-priv user creates POS leads without View referrals perm

## 可迁移技法

Violates role boundary in partner org/workspace context

## 为什么值得收藏

- 该案例可作为 `Escalation` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
