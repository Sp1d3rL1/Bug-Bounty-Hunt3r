---
type: case
vuln_class: Condition
source_url: https://infosecwriteups.com/how-i-found-a-10-800-business-impact-bug-race-condition-broken-access-control-de40c9897e91
source_author: Abhishek Gupta
source_date: 2025-12
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - SaaS API
---

# Race Condition + Broken Access Control Leading to Super Admin Creation

## 链接

https://infosecwriteups.com/how-i-found-a-10-800-business-impact-bug-race-condition-broken-access-control-de40c9897e91

## 漏洞类型

Condition

## 目标业务场景

SaaS API

## 关键利用链摘要

Concurrent requests to create/update role in API bypass locking

## 可迁移技法

Old race + auth flaws create business logic impact in SaaS user management

## 为什么值得收藏

- 该案例可作为 `Condition` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->

<!-- backlink: docs/checklists/payment_business_logic.md -->
