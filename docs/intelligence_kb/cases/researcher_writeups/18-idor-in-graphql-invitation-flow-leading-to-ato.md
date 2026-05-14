---
type: case
vuln_class: via GraphQL Mutation
source_url: https://medium.com/@parthnarula/idor-in-graphql-invitation-flow-leading-to-ato
source_author: Parth Narula
source_date: 2025-09-10
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Collaboration Platform GraphQL
---

# IDOR in GraphQL Invitation Flow Leading to ATO

## 链接

https://medium.com/@parthnarula/idor-in-graphql-invitation-flow-leading-to-ato

## 漏洞类型

via GraphQL Mutation

## 目标业务场景

Collaboration Platform GraphQL

## 关键利用链摘要

Swap invitation ID in updateUser mutation discovered via schema introspection

## 可迁移技法

Account takeover via leaked invitation tokens in BB program

## 为什么值得收藏

- 该案例可作为 `via GraphQL Mutation` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
