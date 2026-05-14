---
type: case
vuln_class: Signup Domain Enforcement
source_url: https://hackerone.com/reports/2101076
source_author: 0xacb
source_date: 2024-02-04
collected_at: 2026-05-05
freshness: 2024
confidence: high
target_types:
  - HackerOne internal org
---

# HackerOne SAML signup domain enforcement bypass

## 链接

https://hackerone.com/reports/2101076

## 漏洞类型

Signup Domain Enforcement

## 目标业务场景

HackerOne internal org

## 关键利用链摘要

Append %0d%0a control chars to email param in POST /users to split and bypass domain check

## 可迁移技法

Creates accounts in restricted SAML orgs (e.g. @hackerone.com) for source code access

## 为什么值得收藏

- 该案例可作为 `Signup Domain Enforcement` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
