---
type: case
vuln_class: plan user limit bypass
source_url: https://medium.com/@hgr00x/business-logic-flaw-ability-to-bypass-user-limit-and-add-multiple-members-without-payment-45ccc3d32a89
source_author: hgr00x
source_date: 2026
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - SaaS team billing
---

# Business Logic Flaw — Ability to Bypass User Limit and Add Multiple Members Without Payment

## 链接

https://medium.com/@hgr00x/business-logic-flaw-ability-to-bypass-user-limit-and-add-multiple-members-without-payment-45ccc3d32a89

## 漏洞类型

plan user limit bypass

## 目标业务场景

SaaS team billing

## 关键利用链摘要

deactivate user to free slot add new then parallel reactivate requests via Burp to exceed limit

## 可迁移技法

adds extra members without payment exploiting session and limit enforcement in SaaS

## 为什么值得收藏

- 该案例可作为 `plan user limit bypass` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
