---
type: case
vuln_class: JWT + Auth Bypass
source_url: https://totalshiftleft.ai/blog/jwt-authentication-testing-guide
source_author: Bug Bounty Researcher
source_date: 2026-02
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Multi-tenant SaaS microservices
---

# JWT Claim Forging for Arbitrary Tenant/Role in Multi-Service SaaS

## 链接

https://totalshiftleft.ai/blog/jwt-authentication-testing-guide

## 漏洞类型

JWT + Auth Bypass

## 目标业务场景

Multi-tenant SaaS microservices

## 关键利用链摘要

Change alg to HS256 and forge tenant_id/role claims

## 可迁移技法

Full cross-tenant admin access via broken permission validation

## 为什么值得收藏

- 该案例可作为 `JWT + Auth Bypass` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
