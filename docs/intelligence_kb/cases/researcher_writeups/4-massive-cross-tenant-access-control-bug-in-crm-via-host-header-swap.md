---
type: case
vuln_class: Broken Access Control
source_url: https://medium.com/@mrro0o0tt/i-found-a-massive-cross-tenant-access-control-bug-by-testing-multiple-roles-heres-what-i-learned-ed9c7b7f8b92
source_author: Whoami (mrro0o0tt)
source_date: 2026
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - SaaS CRM multi-tenant
---

# Massive Cross-Tenant Access Control Bug in CRM via Host Header Swap

## 链接

https://medium.com/@mrro0o0tt/i-found-a-massive-cross-tenant-access-control-bug-by-testing-multiple-roles-heres-what-i-learned-ed9c7b7f8b92

## 漏洞类型

Broken Access Control

## 目标业务场景

SaaS CRM multi-tenant

## 关键利用链摘要

Swap Host header to victim tenant while replaying low-priv role API requests

## 可迁移技法

Reveals inconsistent tenant isolation per role allowing full cross-org data access/edit

## 为什么值得收藏

- 该案例可作为 `Broken Access Control` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->
