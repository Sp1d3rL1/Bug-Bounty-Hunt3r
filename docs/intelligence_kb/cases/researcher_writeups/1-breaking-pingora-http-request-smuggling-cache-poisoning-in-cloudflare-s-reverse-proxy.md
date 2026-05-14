---
type: case
vuln_class: request smuggling/cache poisoning
source_url: https://xclow3n.github.io/post/6/
source_author: xclow3n (Rajat Raghav)
source_date: 2026-03-03
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Cloudflare Pingora reverse proxy
---

# Breaking Pingora: HTTP Request Smuggling & Cache Poisoning in Cloudflare's Reverse Proxy

## 链接

https://xclow3n.github.io/post/6/

## 漏洞类型

request smuggling/cache poisoning

## 目标业务场景

Cloudflare Pingora reverse proxy

## 关键利用链摘要

Upgrade header triggers premature passthrough smuggling pipelined requests past controls

## 可迁移技法

Cross-user ACL bypass, session hijack, cache poisoning in default proxy config; $5k BB bounty awarded

## 为什么值得收藏

- 该案例可作为 `request smuggling/cache poisoning` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/cache_deception_poisoning.md -->

<!-- backlink: docs/checklists/cicd_github_actions.md -->

<!-- backlink: docs/checklists/http_request_smuggling.md -->
