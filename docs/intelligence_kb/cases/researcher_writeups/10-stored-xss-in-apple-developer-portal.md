---
type: case
vuln_class: XSS
source_url: https://medium.com/@ZombieHack/apple-developer-stored-xss-5-000-bounty-writeup-2025-cc34a030a5bf
source_author: ZombieHack
source_date: 2025-11
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - SaaS portal
---

# Stored XSS in Apple Developer Portal

## 链接

https://medium.com/@ZombieHack/apple-developer-stored-xss-5-000-bounty-writeup-2025-cc34a030a5bf

## 漏洞类型

XSS

## 目标业务场景

SaaS portal

## 关键利用链摘要

Stored": - /url: https://medium.com/@ZombieHack/apple-developer-stored-xss-5-000-bounty-writeup-2025-cc34a030a5bf§XSS§Stored - text: payload in developer field rendered without sanitization

## 可迁移技法

Old stored XSS still pays $5k in modern developer SaaS portals

## 为什么值得收藏

- 该案例可作为 `XSS` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/cors_postmessage_websocket.md -->

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->

<!-- backlink: docs/checklists/prototype_pollution_xss_chain.md -->
