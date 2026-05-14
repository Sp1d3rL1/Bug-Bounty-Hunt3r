---
type: case
vuln_class: Duplication + Batching
source_url: https://kizerh.medium.com/exploiting-graphql-a-full-spectrum-security-assessment-covering-introspection-injection-and-560f49a44f36
source_author: Kizerh Medium writeup
source_date: 2026-03-15
collected_at: 2026-05-05
freshness: 2026
confidence: medium
target_types:
  - General GraphQL APIs
---

# GraphQL Field Duplication for Resource Exhaustion

## 链接

https://kizerh.medium.com/exploiting-graphql-a-full-spectrum-security-assessment-covering-introspection-injection-and-560f49a44f36

## 漏洞类型

Duplication + Batching

## 目标业务场景

General GraphQL APIs

## 关键利用链摘要

Duplicate fields (content content content) in batched queries to force repeated resolver execution

## 可迁移技法

Amplifies DoS impact when combined with batching in authorized pentests

## 为什么值得收藏

- 该案例可作为 `Duplication + Batching` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/graphql.md -->
