---
type: case
vuln_class: cache deception
source_url: https://systemweakness.com/web-cache-deception-when-a-404-still-leaks-sensitive-data-61338e04b10f
source_author: ValidByAccident
source_date: 2025-06-26
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - real bug bounty target with profile paths
---

# Web Cache Deception: When a 404 Still Leaks Sensitive Data

## 链接

https://systemweakness.com/web-cache-deception-when-a-404-still-leaks-sensitive-data-61338e04b10f

## 漏洞类型

cache deception

## 目标业务场景

real bug bounty target with profile paths

## 关键利用链摘要

Append fake .css extension to dynamic profile path (/settings/profile/anything.css) to cache 404 with embedded user data

## 可迁移技法

Leaks emails/names/auth details cross-user via cached 404; first real BB report (dup but high signal)

## 为什么值得收藏

- 该案例可作为 `cache deception` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/cache_deception_poisoning.md -->
