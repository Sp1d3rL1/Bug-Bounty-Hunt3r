---
type: case
vuln_class: price manipulation
source_url: https://spyboy.blog/2026/01/05/this-is-how-i-hacked-a-payment-flow-using-business-logic-abuse/
source_author: Spyboy
source_date: 2026-01-05
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - e-commerce REST API payment
---

# This Is How I Hacked a Payment Flow Using Business Logic Abuse

## 链接

https://spyboy.blog/2026/01/05/this-is-how-i-hacked-a-payment-flow-using-business-logic-abuse/

## 漏洞类型

price manipulation

## 目标业务场景

e-commerce REST API payment

## 关键利用链摘要

tamper cart_total to negative/low value or submit status:success in /payment/verify bypassing gateway

## 可迁移技法

turns system into free/negative payment processor undetectable financial exploit

## 为什么值得收藏

- 该案例可作为 `price manipulation` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
