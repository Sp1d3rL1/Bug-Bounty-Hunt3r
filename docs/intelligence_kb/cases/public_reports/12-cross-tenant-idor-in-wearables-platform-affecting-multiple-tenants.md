---
type: case
vuln_class: IDOR
source_url: https://hackerone.com/reports/XXXXXX
source_author: hohky_
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - SaaS wearables
  - IoT platform
---

# Cross-Tenant IDOR in Wearables Platform Affecting Multiple Tenants

## 链接

https://hackerone.com/reports/XXXXXX

## 漏洞类型

IDOR

## 目标业务场景

SaaS wearables/IoT platform

## 关键利用链摘要

Increment object IDs across tenant boundaries without checks

## 可迁移技法

Data access/modification across unrelated user workspaces

## 为什么值得收藏

- 该案例可作为 `IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
