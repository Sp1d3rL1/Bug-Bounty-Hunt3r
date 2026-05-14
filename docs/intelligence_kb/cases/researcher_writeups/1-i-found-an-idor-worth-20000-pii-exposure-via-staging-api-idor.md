---
type: case
vuln_class: BOLA/IDOR
source_url: https://medium.com/@MohaseenK/i-found-an-idor-worth-20-000-heres-what-happened-62d6b8c4f17d
source_author: MohaseenK
source_date: 2025-10-01
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - API endpoint in web app
---

# I Found an IDOR Worth $20000 - PII Exposure via Staging API IDOR

## 链接

https://medium.com/@MohaseenK/i-found-an-idor-worth-20-000-heres-what-happened-62d6b8c4f17d

## 漏洞类型

BOLA/IDOR

## 目标业务场景

API endpoint in web app

## 关键利用链摘要

Modify object ID in /api/user-records endpoint from staging to prod data leak

## 可迁移技法

Mass PII exposure across real users in authorized BB program yields high bounty

## 为什么值得收藏

- 该案例可作为 `BOLA/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->
