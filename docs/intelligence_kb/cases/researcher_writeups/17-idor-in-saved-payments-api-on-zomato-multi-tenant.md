---
type: case
vuln_class: IDOR
source_url: https://prateeksrivastavaa.medium.com/zomatoooo-idor-in-saved-payments-f8c014879741
source_author: Prateek Srivastava
source_date: 2024-09
collected_at: 2026-05-05
freshness: 2024
confidence: high
target_types:
  - SaaS payments API
---

# IDOR in Saved Payments API on Zomato (multi-tenant)

## 链接

https://prateeksrivastavaa.medium.com/zomatoooo-idor-in-saved-payments-f8c014879741

## 漏洞类型

IDOR

## 目标业务场景

SaaS payments API

## 关键利用链摘要

ID": - /url: https://prateeksrivastavaa.medium.com/zomatoooo-idor-in-saved-payments-f8c014879741§IDOR§ID - text: swap in payments endpoint exposing other user cards

## 可迁移技法

Classic IDOR in e-commerce SaaS payments still critical in 2024+

## 为什么值得收藏

- 该案例可作为 `IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
