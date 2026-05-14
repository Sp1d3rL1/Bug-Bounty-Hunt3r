---
type: case
vuln_class: reuse logic flaw
source_url: https://medium.com/@tarekmohamed0106/reusing-a-one-time-coupon-code-multiple-times-business-logic-bug-664766230b53
source_author: Tarekmohamed
source_date: 2026-03
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - e-commerce billing
---

# Reusing a One-Time Coupon Code Multiple Times

## 链接

https://medium.com/@tarekmohamed0106/reusing-a-one-time-coupon-code-multiple-times-business-logic-bug-664766230b53

## 漏洞类型

reuse logic flaw

## 目标业务场景

e-commerce billing

## 关键利用链摘要

complete order with one-time coupon then create new order on same account and re-apply same code with no per-user redemption check

## 可迁移技法

repeated discounts on single-use codes leading to revenue leakage in ecom BB

## 为什么值得收藏

- 该案例可作为 `reuse logic flaw` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/payment_business_logic.md -->
