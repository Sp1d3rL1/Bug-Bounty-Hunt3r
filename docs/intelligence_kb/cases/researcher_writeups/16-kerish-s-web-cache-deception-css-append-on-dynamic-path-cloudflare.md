---
type: case
vuln_class: web cache deception
source_url: https://medium.com
source_author: Kerish (BB hunter Medium)
source_date: 2026
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Cloudflare-protected web apps
---

# Kerish's Web Cache Deception: .css Append on Dynamic Path (Cloudflare)

## 链接

https://medium.com

## 漏洞类型

web cache deception

## 目标业务场景

Cloudflare-protected web apps

## 关键利用链摘要

Append .css to /account dynamic path on Cloudflare site to cache authenticated emails

## 可迁移技法

Leads to PII leak via cached CSS-like response; niche practical for Cloudflare-protected apps

## 为什么值得收藏

- 该案例可作为 `web cache deception` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/cache_deception_poisoning.md -->
