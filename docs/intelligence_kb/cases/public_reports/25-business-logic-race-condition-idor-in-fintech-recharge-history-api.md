---
type: case
vuln_class: Condition/IDOR
source_url: https://hackerone.com/reports/2746709
source_author: MTN Group Hunter (HackerOne)
source_date: 2025-01
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - SaaS fintech API
---

# Business Logic Race Condition + IDOR in Fintech Recharge History API

## 链接

https://hackerone.com/reports/2746709

## 漏洞类型

Condition/IDOR

## 目标业务场景

SaaS fintech API

## 关键利用链摘要

Concurrent access to /v2/rechargeTransactionHistory without auth

## 可迁移技法

Classic race + IDOR leaks sensitive transaction data in fintech SaaS APIs

## 为什么值得收藏

- 该案例可作为 `Condition/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->

<!-- backlink: docs/checklists/payment_business_logic.md -->
