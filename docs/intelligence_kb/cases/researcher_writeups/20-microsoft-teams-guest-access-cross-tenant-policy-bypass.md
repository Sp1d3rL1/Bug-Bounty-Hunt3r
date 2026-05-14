---
type: case
vuln_class: Access Control
source_url: https://www.linkedin.com/pulse/microsoft-teams-guest-access-exposes-cross-tenant-ly48e
source_author: Ontinue Researchers
source_date: 2026
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - SaaS collaboration (Teams)
---

# Microsoft Teams Guest Access Cross-Tenant Policy Bypass

## 链接

https://www.linkedin.com/pulse/microsoft-teams-guest-access-exposes-cross-tenant-ly48e

## 漏洞类型

Access Control

## 目标业务场景

SaaS collaboration (Teams)

## 关键利用链摘要

Guest user inherits host tenant policies bypassing own org controls

## 可迁移技法

Exposes permission boundary gaps in workspace collaboration

## 为什么值得收藏

- 该案例可作为 `Access Control` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
