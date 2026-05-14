---
type: case
vuln_class: + Undocumented Mutation
source_url: https://x.com/rashed_hasan00/status/2045000000000000000
source_author: @rashed_hasan00 (X hunter tip)
source_date: 2026-04-05
collected_at: 2026-05-05
freshness: 2026
confidence: medium
target_types:
  - Admin GraphQL APIs
---

# Undocumented Admin Mutation Discovery via Introspection

## 链接

https://x.com/rashed_hasan00/status/2045000000000000000

## 漏洞类型

+ Undocumented Mutation

## 目标业务场景

Admin GraphQL APIs

## 关键利用链摘要

Introspect schema to find hidden admin-only mutations not referenced in frontend

## 可迁移技法

Enables privilege escalation via schema mapping in production BB targets

## 为什么值得收藏

- 该案例可作为 `+ Undocumented Mutation` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
