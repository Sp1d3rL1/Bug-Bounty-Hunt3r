---
type: case
vuln_class: feature bypass
source_url: https://hackerone.com/reports/3591764
source_author: Lovable hunter (report author)
source_date: 2026-03-08
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - SaaS collaboration tool
---

# Business Logic Bypass Allows Setting Read Access Role Without Pro Plan Subscription

## 链接

https://hackerone.com/reports/3591764

## 漏洞类型

feature bypass

## 目标业务场景

SaaS collaboration tool

## 关键利用链摘要

manipulate free-tier requests to assign Pro-only roles/permissions via API logic gap

## 可迁移技法

grants paid features to free users breaking monetization in VDP/BB

## 为什么值得收藏

- 该案例可作为 `feature bypass` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/payment_business_logic.md -->
