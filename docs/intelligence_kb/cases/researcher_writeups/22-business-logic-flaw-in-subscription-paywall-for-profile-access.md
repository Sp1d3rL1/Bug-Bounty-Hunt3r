---
type: case
vuln_class: direct access
source_url: https://medium.com/@ashiq.r.emon/subscription-paywall-bypass-leading-to-talent-profile-access-and-pii-disclosure-including-deleted-a3eb7cb09ca0
source_author: Ashiqur Emon (PII extension)
source_date: 2026-03
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - talent subscription platform
---

# Business Logic Flaw in Subscription Paywall for Profile Access

## 链接

https://medium.com/@ashiq.r.emon/subscription-paywall-bypass-leading-to-talent-profile-access-and-pii-disclosure-including-deleted-a3eb7cb09ca0

## 漏洞类型

direct access

## 目标业务场景

talent subscription platform

## 关键利用链摘要

direct URL navigation to paid profile bypassing subscription gate

## 可迁移技法

exposes PII from active/deleted accounts in BB program

## 为什么值得收藏

- 该案例可作为 `direct access` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/payment_business_logic.md -->
