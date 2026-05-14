---
type: case
vuln_class: BOLA/IDOR
source_url: https://hackerone.com/reports/2487889
source_author: H1 hunter (anon)
source_date: 2026-01-01
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Bug tracking API
---

# H1 #2487889 - IDOR on /bugs.json Exposing Private Report Details

## 链接

https://hackerone.com/reports/2487889

## 漏洞类型

BOLA/IDOR

## 目标业务场景

Bug tracking API

## 关键利用链摘要

POST to /bugs.json with org_id + text_query digit to pull cross-org private reports

## 可迁移技法

JSON endpoint IDOR in bug tracker; cross-org leakage in authorized program

## 为什么值得收藏

- 该案例可作为 `BOLA/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->
