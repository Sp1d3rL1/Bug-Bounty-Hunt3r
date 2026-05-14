---
type: case
vuln_class: Client Credentials Misuse
source_url: https://medium.com/@bugbounty0901/oauth-authentication-bypass-leading-to-pii-disclosure-5d243b62d532
source_author: janlele91
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Bugcrowd private programs
---

# OAuth Authentication Bypass leading to PII disclosure

## 链接

https://medium.com/@bugbounty0901/oauth-authentication-bypass-leading-to-pii-disclosure-5d243b62d532

## 漏洞类型

Client Credentials Misuse

## 目标业务场景

Bugcrowd private programs

## 关键利用链摘要

Send grant_type=client_credentials to /api/token endpoint without client_id/secret to obtain valid access token

## 可迁移技法

Extracts 12MB+ customer PII via search endpoints in commercial platforms

## 为什么值得收藏

- 该案例可作为 `Client Credentials Misuse` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
