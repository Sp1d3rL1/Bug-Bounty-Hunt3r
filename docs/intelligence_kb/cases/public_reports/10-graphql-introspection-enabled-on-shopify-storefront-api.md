---
type: case
vuln_class: + Schema Exposure
source_url: https://hackerone.com/reports/2886723
source_author: Shopify Hunter (H1)
source_date: 2025-10-15
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Shopify GraphQL API
---

# GraphQL Introspection Enabled on Shopify Storefront API

## 链接

https://hackerone.com/reports/2886723

## 漏洞类型

+ Schema Exposure

## 目标业务场景

Shopify GraphQL API

## 关键利用链摘要

Enabled introspection query reveals full schema including sensitive merchant fields

## 可迁移技法

Provides blueprint for further BOLA/IDOR attacks in Shopify BB program

## 为什么值得收藏

- 该案例可作为 `+ Schema Exposure` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
