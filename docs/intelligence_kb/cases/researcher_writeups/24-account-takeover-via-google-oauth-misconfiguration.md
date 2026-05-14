---
type: case
vuln_class: OAuth Misconfig
source_url: https://cybersecuritywriteups.com/account-takeover-via-google-auth-misconfiguration-af4a59dd82e7
source_author: Anonymous hunter (Medium)
source_date: 2024-11-02
collected_at: 2026-05-05
freshness: 2024
confidence: high
target_types:
  - Public bug bounty programs
---

# Account Takeover via Google OAuth Misconfiguration

## 链接

https://cybersecuritywriteups.com/account-takeover-via-google-auth-misconfiguration-af4a59dd82e7

## 漏洞类型

OAuth Misconfig

## 目标业务场景

Public bug bounty programs

## 关键利用链摘要

Open redirect_uri or missing validation allows code exchange on attacker domain

## 可迁移技法

Full ATO via Google OAuth in public programs

## 为什么值得收藏

- 该案例可作为 `OAuth Misconfig` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
