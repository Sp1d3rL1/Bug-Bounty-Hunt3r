---
type: case
vuln_class: cache poisoning
source_url: https://blog.cloudflare.com/pingora-oss-smuggling-vulnerabilities/
source_author: xclow3n (Rajat Raghav)
source_date: 2026-01
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Cloudflare Pingora
  - CDN
---

# Cloudflare Pingora Default Cache Key Poisoning (Host Ignored)

## 链接

https://blog.cloudflare.com/pingora-oss-smuggling-vulnerabilities/

## 漏洞类型

cache poisoning

## 目标业务场景

Cloudflare Pingora/CDN

## 关键利用链摘要

CacheKey construction ignores Host header enabling host collision poisoning

## 可迁移技法

Poisons cache across tenants in default config; part of multiple BB reports to Cloudflare

## 为什么值得收藏

- 该案例可作为 `cache poisoning` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/cache_deception_poisoning.md -->

<!-- backlink: docs/checklists/http_request_smuggling.md -->
