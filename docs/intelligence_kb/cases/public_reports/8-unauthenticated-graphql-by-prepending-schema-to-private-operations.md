---
type: case
vuln_class: Bypass + Authentication Bypass
source_url: https://hackerone.com/reports/3452015
source_author: pwnie
source_date: 2025-12-04
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Enjin Platform GraphQL
---

# Unauthenticated GraphQL by Prepending __schema to Private Operations

## 链接

https://hackerone.com/reports/3452015

## 漏洞类型

Bypass + Authentication Bypass

## 目标业务场景

Enjin Platform GraphQL

## 关键利用链摘要

Prepend __schema query fragment to bypass auth middleware on otherwise private operations

## 可迁移技法

Exposes schema and executes restricted queries in Enjin platform BB program

## 为什么值得收藏

- 该案例可作为 `Bypass + Authentication Bypass` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/graphql.md -->
