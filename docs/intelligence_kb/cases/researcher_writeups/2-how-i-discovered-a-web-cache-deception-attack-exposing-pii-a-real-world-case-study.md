---
type: case
vuln_class: cache deception
source_url: https://infosecwriteups.com/how-i-discovered-a-web-cache-deception-attack-exposing-pii-a-real-world-case-study-49aabe4258a3
source_author: Pratik Dabhi
source_date: 2025-05-31
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - web app
  - CDN with misconfigured cache
---

# How I Discovered a Web Cache Deception Attack Exposing PII — A Real-World Case Study

## 链接

https://infosecwriteups.com/how-i-discovered-a-web-cache-deception-attack-exposing-pii-a-real-world-case-study-49aabe4258a3

## 漏洞类型

cache deception

## 目标业务场景

web app/CDN with misconfigured cache

## 关键利用链摘要

URL/file extension (.html) + Cache-Control misconfig caches dynamic authenticated content as static

## 可迁移技法

Unintended PII exposure to unauth users via CDN; high-impact real BB report on multinational app

## 为什么值得收藏

- 该案例可作为 `cache deception` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/cache_deception_poisoning.md -->
