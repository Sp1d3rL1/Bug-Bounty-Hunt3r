---
type: case
vuln_class: + Subdomain Exposure
source_url: https://medium.com/@ch3tan/graphql-introspection-on-wiki-subdomain
source_author: CH3TAN
source_date: 2025-07-20
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Internal Wiki GraphQL API
---

# GraphQL Introspection on Wiki Subdomain Leading to Schema + Sensitive Data

## 链接

https://medium.com/@ch3tan/graphql-introspection-on-wiki-subdomain

## 漏洞类型

+ Subdomain Exposure

## 目标业务场景

Internal Wiki GraphQL API

## 关键利用链摘要

Introspect /graphql on wiki subdomain exposing internal schema and user data

## 可迁移技法

Chain subdomain discovery with introspection for lateral movement in BB

## 为什么值得收藏

- 该案例可作为 `+ Subdomain Exposure` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
