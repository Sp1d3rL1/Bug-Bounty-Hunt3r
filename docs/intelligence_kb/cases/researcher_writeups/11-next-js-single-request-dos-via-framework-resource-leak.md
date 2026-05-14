---
type: case
vuln_class: DoS
source_url: https://joshua.hu/2025-bug-bounty-stories-fail
source_author: Joshua Rogers
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Next.js
  - Vercel apps
---

# Next.js Single-Request DoS via Framework Resource Leak

## 链接

https://joshua.hu/2025-bug-bounty-stories-fail

## 漏洞类型

DoS

## 目标业务场景

Next.js / Vercel apps

## 关键利用链摘要

Craft": - /url: https://joshua.hu/2025-bug-bounty-stories-fail§DoS§Craft - text: one small request exploiting Next.js resource leakage bugs

## 可迁移技法

Crashes any Next.js server worldwide; out-of-scope initially but manually reviewed

## 为什么值得收藏

- 该案例可作为 `DoS` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
