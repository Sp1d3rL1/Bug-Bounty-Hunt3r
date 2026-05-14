---
type: case
vuln_class: Server-Side Authz
source_url: https://medium.com/@dedrknex/export-button-team-id-bypass-multi-tenant
source_author: Dedrknex
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - SaaS team collaboration tool
---

# Export Button Bypassing Team Permission via Client-Supplied Team ID

## 链接

https://medium.com/@dedrknex/export-button-team-id-bypass-multi-tenant

## 漏洞类型

Server-Side Authz

## 目标业务场景

SaaS team collaboration tool

## 关键利用链摘要

Supply victim team_id in export endpoint request

## 可迁移技法

Cross-team/workspace data leakage in multi-tenant environments

## 为什么值得收藏

- 该案例可作为 `Server-Side Authz` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
