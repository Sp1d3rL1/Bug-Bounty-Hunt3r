---
type: case
vuln_class: + Mass Data Exposure
source_url: https://medium.com/@prateekpulastya/graphql-endpoint-leaking-millions-users-without-auth
source_author: Prateekpulastya
source_date: 2026-04-01
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Social
  - Community GraphQL API
---

# GraphQL Endpoint Leaking Millions of Users Without Auth

## 链接

https://medium.com/@prateekpulastya/graphql-endpoint-leaking-millions-users-without-auth

## 漏洞类型

+ Mass Data Exposure

## 目标业务场景

Social/Community GraphQL API

## 关键利用链摘要

Send invalid fields to trigger suggestion errors revealing users/user fields then query unauth /graphql endpoint

## 可迁移技法

Mass user enumeration via schema hints in authorized BB hunt

## 为什么值得收藏

- 该案例可作为 `+ Mass Data Exposure` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
