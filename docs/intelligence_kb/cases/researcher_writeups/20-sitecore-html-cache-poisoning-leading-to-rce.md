---
type: case
vuln_class: web cache poisoning
source_url: https://medium.com
source_author: BB hunter (2025 disclosure)
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Sitecore CMS with HTML caching
---

# Sitecore HTML Cache Poisoning Leading to RCE

## 链接

https://medium.com

## 漏洞类型

web cache poisoning

## 目标业务场景

Sitecore CMS with HTML caching

## 关键利用链摘要

Poison HTML cache with malicious payload via cache key manipulation

## 可迁移技法

Escalates to RCE in Sitecore environments; high BB value

## 为什么值得收藏

- 该案例可作为 `web cache poisoning` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/cache_deception_poisoning.md -->
