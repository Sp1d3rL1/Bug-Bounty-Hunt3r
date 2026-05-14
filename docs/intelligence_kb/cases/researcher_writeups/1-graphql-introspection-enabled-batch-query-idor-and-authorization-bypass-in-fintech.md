---
type: case
vuln_class: + Batching + IDOR/Authorization Bypass
source_url: https://infosecwriteups.com/graphql-security-how-i-found-and-exploited-critical-idor-and-authorization-bypass-in-a-42ab78e13642
source_author: Krishna Kumar
source_date: 2026-04-03
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Fintech GraphQL API
---

# GraphQL Introspection Enabled + Batch Query IDOR and Authorization Bypass in Fintech

## 链接

https://infosecwriteups.com/graphql-security-how-i-found-and-exploited-critical-idor-and-authorization-bypass-in-a-42ab78e13642

## 漏洞类型

+ Batching + IDOR/Authorization Bypass

## 目标业务场景

Fintech GraphQL API

## 关键利用链摘要

Introspect full schema then send array of batched queries to exploit IDOR on other users financial transactions

## 可迁移技法

Enables mass data access/modify of other accounts in single HTTP request for high payout in authorized BB

## 为什么值得收藏

- 该案例可作为 `+ Batching + IDOR/Authorization Bypass` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
