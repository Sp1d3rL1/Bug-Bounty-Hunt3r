---
type: case
vuln_class: BOLA/IDOR
source_url: https://hackerone.com/reports/3382343
source_author: cyberjoker
source_date: 2026-04-14
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Nextcloud API
---

# Nextcloud BOLA in /outOfOffice/{userId} API - Cross-User OOO Data Leak

## 链接

https://hackerone.com/reports/3382343

## 漏洞类型

BOLA/IDOR

## 目标业务场景

Nextcloud API

## 关键利用链摘要

Swap {userId} path param in app-password auth requests to read any user's out-of-office status

## 可迁移技法

Bypasses tenant isolation in multi-user collab app; real H1 disclosure by hunter

## 为什么值得收藏

- 该案例可作为 `BOLA/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
