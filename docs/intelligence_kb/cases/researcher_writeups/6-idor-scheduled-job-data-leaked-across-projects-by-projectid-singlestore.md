---
type: case
vuln_class: BOLA/IDOR
source_url: https://www.bountieshub.com/case/88
source_author: Bounties Hub hunter (anon)
source_date: 2025-08-12
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - API in SaaS platform
---

# IDOR → Scheduled Job Data Leaked Across Projects by projectID (SingleStore)

## 链接

https://www.bountieshub.com/case/88

## 漏洞类型

BOLA/IDOR

## 目标业务场景

API in SaaS platform

## 关键利用链摘要

Swap projectID param in scheduled job API to access cross-project data

## 可迁移技法

Exposes internal job artifacts in BB-authorized env; practical multi-project bypass

## 为什么值得收藏

- 该案例可作为 `BOLA/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->
