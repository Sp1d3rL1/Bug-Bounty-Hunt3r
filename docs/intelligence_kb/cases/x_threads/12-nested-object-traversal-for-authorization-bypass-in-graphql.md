---
type: case
vuln_class: Bypass via Nested Queries
source_url: https://x.com/0xacb/status/2040000000000000000
source_author: @0xacb follow-up
source_date: 2026-04-10
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Social Media GraphQL API
---

# Nested Object Traversal for Authorization Bypass in GraphQL

## 链接

https://x.com/0xacb/status/2040000000000000000

## 漏洞类型

Bypass via Nested Queries

## 目标业务场景

Social Media GraphQL API

## 关键利用链摘要

Query publicPost { author { sensitiveField } } to traverse and leak data bypassing direct field auth

## 可迁移技法

Exploits missing resolver-level checks on nested relations in authorized hunts

## 为什么值得收藏

- 该案例可作为 `Bypass via Nested Queries` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/graphql.md -->
