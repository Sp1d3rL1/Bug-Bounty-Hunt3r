---
type: case
vuln_class: Account Linking Bypass
source_url: https://medium.com/@tinopreter/500-oauth-account-fusion-pre-takeover-attack-477484aa3813
source_author: tinopreter
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - HackerOne bug bounty programs
---

# $500 OAuth Account Fusion Pre-Takeover Attack

## 链接

https://medium.com/@tinopreter/500-oauth-account-fusion-pre-takeover-attack-477484aa3813

## 漏洞类型

Account Linking Bypass

## 目标业务场景

HackerOne bug bounty programs

## 关键利用链摘要

Unverified email/password acct + same email OAuth signup fuses and bypasses verification

## 可迁移技法

Pre-ATO grants attacker dashboard access before victim verifies in hybrid email+OAuth flows

## 为什么值得收藏

- 该案例可作为 `Account Linking Bypass` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->

<!-- backlink: docs/checklists/subdomain_takeover.md -->
