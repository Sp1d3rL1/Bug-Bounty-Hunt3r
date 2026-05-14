---
type: case
vuln_class: Hijacking
source_url: https://joshua.hu/2025-bug-bounty-stories-fail
source_author: Joshua Rogers
source_date: 2025-11
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - NextJS + Auth0 apps
---

# NextJS-Auth0 Insecure Session Cache Key Hijack

## 链接

https://joshua.hu/2025-bug-bounty-stories-fail

## 漏洞类型

Hijacking

## 目标业务场景

NextJS + Auth0 apps

## 关键利用链摘要

Race auth0.getAccessToken calls to steal victim sessions via weak caching key

## 可迁移技法

Full account takeover without knowing user details; $1500 Bugcrowd bounty

## 为什么值得收藏

- 该案例可作为 `Hijacking` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
