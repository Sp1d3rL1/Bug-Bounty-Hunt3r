---
type: case
vuln_class: BOLA/IDOR
source_url: https://medium.com/@Dedrknex/from-idor-to-bypass-how-a-fixed-bug-still-exposed-6-4-million-users-data-part-2-21f9dde7cc79
source_author: Dedrknex
source_date: 2026-04-15
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - User data API
---

# From IDOR to Bypass: Fixed Bug Still Exposed 6.4M Users Data (Part 2)

## 链接

https://medium.com/@Dedrknex/from-idor-to-bypass-how-a-fixed-bug-still-exposed-6-4-million-users-data-part-2-21f9dde7cc79

## 漏洞类型

BOLA/IDOR

## 目标业务场景

User data API

## 关键利用链摘要

Post-fix residual IDOR via alternate param/path allowing continued cross-user access

## 可迁移技法

Demonstrates incomplete fixes leave edge vectors; real large-scale impact

## 为什么值得收藏

- 该案例可作为 `BOLA/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->
