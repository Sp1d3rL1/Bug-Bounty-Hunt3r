---
type: case
vuln_class: Pre-ATO Misconfigs
source_url: https://medium.com/@KhaledAhmed107/how-i-found-5-oauth-misconfigurations-leading-to-pre-account-takeover-in-public-bug-bounty-programs-021d4c8c6954
source_author: KhaledAhmed107
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Bugcrowd public programs
---

# How I Found 5 OAuth Misconfigurations Leading to Pre-Account Takeover

## 链接

https://medium.com/@KhaledAhmed107/how-i-found-5-oauth-misconfigurations-leading-to-pre-account-takeover-in-public-bug-bounty-programs-021d4c8c6954

## 漏洞类型

Pre-ATO Misconfigs

## 目标业务场景

Bugcrowd public programs

## 关键利用链摘要

Multiple redirect_uri / state / PKCE / response_type flaws allowing code/token interception

## 可迁移技法

P2 dupes but high-signal patterns for public programs on Bugcrowd

## 为什么值得收藏

- 该案例可作为 `Pre-ATO Misconfigs` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
