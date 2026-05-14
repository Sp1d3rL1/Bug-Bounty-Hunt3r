---
type: case
vuln_class: IDOR
source_url: https://medium.com/@sid_x95/tenant-admin-idor-cross-tenant-file-deletion-3k-bounty
source_author: Sid_x95
source_date: 2026-01
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Multi-tenant SaaS file platform
---

# Tenant Admin IDOR Allowing Cross-Tenant File Deletion

## 链接

https://medium.com/@sid_x95/tenant-admin-idor-cross-tenant-file-deletion-3k-bounty

## 漏洞类型

IDOR

## 目标业务场景

Multi-tenant SaaS file platform

## 关键利用链摘要

Supply": - /url: https://medium.com/@sid_x95/tenant-admin-idor-cross-tenant-file-deletion-3k-bounty§IDOR§Supply - text: other tenant's file UUID as Tenant Admin to delete

## 可迁移技法

Bypasses workspace/org permission boundaries for destructive cross-tenant actions

## 为什么值得收藏

- 该案例可作为 `IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->
