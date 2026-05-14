---
type: case
vuln_class: BOLA/IDOR
source_url: https://x.com/shreerajaput/status/2048751213915906312
source_author: cyber_shree
source_date: 2026-04-27
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Web
  - API platform
---

# Unauthenticated BOLA on Managed BBP - $500 Critical

## 链接

https://x.com/shreerajaput/status/2048751213915906312

## 漏洞类型

BOLA/IDOR

## 目标业务场景

Web/API platform

## 关键利用链摘要

Direct access to sensitive objects without auth token via missing object-level checks

## 可迁移技法

Shows unauth escalation still possible in 2026 BBPs; quick high-signal win

## 为什么值得收藏

- 该案例可作为 `BOLA/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
