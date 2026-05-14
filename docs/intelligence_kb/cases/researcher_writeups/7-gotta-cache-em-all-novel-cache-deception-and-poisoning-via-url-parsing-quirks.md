---
type: case
vuln_class: cache deception/poisoning
source_url: https://portswigger.net/research/gotta-cache-em-all
source_author: Martin Doyhenard (PortSwigger)
source_date: 2024-08
collected_at: 2026-05-05
freshness: 2024
confidence: high
target_types:
  - CDNs (Cloudflare
  - Akamai) and frameworks
---

# Gotta Cache 'Em All: Novel Cache Deception and Poisoning via URL Parsing Quirks

## 链接

https://portswigger.net/research/gotta-cache-em-all

## 漏洞类型

cache deception/poisoning

## 目标业务场景

CDNs (Cloudflare, Akamai) and frameworks

## 关键利用链摘要

Delimiter (; # %00) and ../ normalization diffs between CDN/origin poison arbitrary paths

## 可迁移技法

Bypasses cache key logic on Cloudflare/Akamai for deception or poisoning; practical BB testing tricks

## 为什么值得收藏

- 该案例可作为 `cache deception/poisoning` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
