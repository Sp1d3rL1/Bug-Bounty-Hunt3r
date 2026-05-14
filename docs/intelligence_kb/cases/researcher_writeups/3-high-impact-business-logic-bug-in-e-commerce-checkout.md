---
type: case
vuln_class: price manipulation
source_url: https://medium.com/@impyhacker/how-i-found-a-high-impact-business-logic-bug-in-an-e-commerce-checkout-57e0493c9675
source_author: PRASHU
source_date: 2026
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - e-commerce checkout
---

# High-Impact Business Logic Bug in E-commerce Checkout

## 链接

https://medium.com/@impyhacker/how-i-found-a-high-impact-business-logic-bug-in-an-e-commerce-checkout-57e0493c9675

## 漏洞类型

price manipulation

## 目标业务场景

e-commerce checkout

## 关键利用链摘要

intercept checkout request and tamper price field from high value to near-zero before server processing

## 可迁移技法

allows high-value orders at minimal cost causing direct revenue loss in BB program

## 为什么值得收藏

- 该案例可作为 `price manipulation` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/payment_business_logic.md -->
