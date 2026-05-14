---
type: case
vuln_class: Access Control/IDOR
source_url: https://medium.com/@montaser_mohsen/breaking-access-control-how-a-low-privilege-user-accessed-workspace-members-data-af2e72d64bb9
source_author: Montaser Mohsen
source_date: 2026-04
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - SaaS workspace platform
---

# Low-Privilege Access to Workspace Members Data via Direct API

## 链接

https://medium.com/@montaser_mohsen/breaking-access-control-how-a-low-privilege-user-accessed-workspace-members-data-af2e72d64bb9

## 漏洞类型

Access Control/IDOR

## 目标业务场景

SaaS workspace platform

## 关键利用链摘要

Direct GET /rest/workspaces/{id}/users as low-priv member

## 可迁移技法

Exposes PII/emails/roles for org reconnaissance bypassing role checks

## 为什么值得收藏

- 该案例可作为 `Access Control/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
