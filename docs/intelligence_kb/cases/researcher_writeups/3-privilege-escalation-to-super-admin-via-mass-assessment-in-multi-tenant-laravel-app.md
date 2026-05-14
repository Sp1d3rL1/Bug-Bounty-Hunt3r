---
type: case
vuln_class: + Missing Role Validation
source_url: https://medium.com/@rahulms_71093/privilege-escalation-to-super-admin-via-mass-assessment-in-a-multi-tenant-laravel-app-526d1309de73
source_author: Rahul M S
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Multi-tenant Laravel SaaS
---

# Privilege Escalation to Super Admin via Mass Assessment in Multi-Tenant Laravel App

## 链接

https://medium.com/@rahulms_71093/privilege-escalation-to-super-admin-via-mass-assessment-in-a-multi-tenant-laravel-app-526d1309de73

## 漏洞类型

+ Missing Role Validation

## 目标业务场景

Multi-tenant Laravel SaaS

## 关键利用链摘要

Fuzz POST /api/users/assign-role with other tenant user_id and SuperAdmin role from low-priv account

## 可迁移技法

Rapid vertical escalation and persistence across tenant boundaries in Laravel SaaS

## 为什么值得收藏

- 该案例可作为 `+ Missing Role Validation` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
