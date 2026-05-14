---
type: case
vuln_class: BOLA/IDOR
source_url: https://urli.info/1oYlx
source_author: 0d_Asbawy
source_date: 2026-05-01
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Multi-tenant API
---

# UUID IDOR Chained with ID Leak Endpoint - Critical Cross-Tenant

## 链接

https://urli.info/1oYlx

## 漏洞类型

BOLA/IDOR

## 目标业务场景

Multi-tenant API

## 关键利用链摘要

Enumerate UUID via leak endpoint then swap in protected API call for victim data

## 可迁移技法

Combines enumeration + object ref bypass; turns low to critical in authorized hunt

## 为什么值得收藏

- 该案例可作为 `BOLA/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->
