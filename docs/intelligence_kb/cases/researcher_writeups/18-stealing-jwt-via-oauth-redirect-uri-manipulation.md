---
type: case
vuln_class: OAuth Redirect URI Manipulation
source_url: (from X hunter writeups referenced in searches)
source_author: Shah kaif
source_date: 2025-10-03
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - OAuth providers in BB programs
---

# Stealing JWT via OAuth redirect_uri Manipulation

## 链接

(from X hunter writeups referenced in searches)

## 漏洞类型

OAuth Redirect URI Manipulation

## 目标业务场景

OAuth providers in BB programs

## 关键利用链摘要

Manipulate redirect_uri to attacker-controlled domain to leak id_token/JWT in URL

## 可迁移技法

Token theft leading to session hijack in OAuth flows

## 为什么值得收藏

- 该案例可作为 `OAuth Redirect URI Manipulation` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
