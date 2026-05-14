---
type: case
vuln_class: Parser Differential
source_url: https://github.blog/security/sign-in-as-anyone-bypassing-saml-sso-authentication-with-parser-differentials/
source_author: p- (GitHub Security Lab) / ahacker1
source_date: 2025-03-12
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - GitHub private bug bounty lab environments
---

# Sign in as anyone: Bypassing SAML SSO with parser differentials

## 链接

https://github.blog/security/sign-in-as-anyone-bypassing-saml-sso-authentication-with-parser-differentials/

## 漏洞类型

Parser Differential

## 目标业务场景

GitHub private bug bounty lab environments

## 关键利用链摘要

Craft SAML assertion with REXML/Nokogiri diffs (DOCTYPE/namespace/attribute pollution) while keeping one valid signature

## 可迁移技法

Full ATO by impersonating any user with single valid sig in ruby-saml SPs like GitLab/GitHub test envs

## 为什么值得收藏

- 该案例可作为 `Parser Differential` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
