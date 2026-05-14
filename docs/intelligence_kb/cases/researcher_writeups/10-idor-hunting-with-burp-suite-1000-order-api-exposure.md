---
type: case
vuln_class: BOLA/IDOR
source_url: https://herish.me/blog/idor-bug-bounty-burp-suite/
source_author: herish (hunter)
source_date: 2025-10-24
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - E-commerce API
---

# IDOR Hunting with Burp Suite - $1000 Order API Exposure

## 链接

https://herish.me/blog/idor-bug-bounty-burp-suite/

## 漏洞类型

BOLA/IDOR

## 目标业务场景

E-commerce API

## 关键利用链摘要

Burp Repeater + Intruder fuzz object IDs in e-commerce /api/orders/{id}

## 可迁移技法

Practical workflow for confirming IDOR in authorized BB; turns recon to payout

## 为什么值得收藏

- 该案例可作为 `BOLA/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->

<!-- backlink: docs/checklists/recon_methodology.md -->
