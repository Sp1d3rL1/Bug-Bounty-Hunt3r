---
type: case
vuln_class: BOLA/IDOR
source_url: https://thenextweb.com/news/lovable-vibe-coding-security-crisis-exposed
source_author: Security researcher (H1)
source_date: 2026-03-03
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - SaaS
  - API platform
---

# BOLA in Lovable Vibe-Coding API - Cross-Project Source/DB Leak

## 链接

https://thenextweb.com/news/lovable-vibe-coding-security-crisis-exposed

## 漏洞类型

BOLA/IDOR

## 目标业务场景

SaaS/API platform

## 关键利用链摘要

5 API calls with free account token to fetch any user's projects/source/credentials

## 可迁移技法

Exposes AI-generated apps in BB program; highlights 2026 vibe-coding risks

## 为什么值得收藏

- 该案例可作为 `BOLA/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
