---
type: case
vuln_class: Tenant Isolation / BOLA
source_url: https://mixbanana.medium.com/when-multi-tenant-isolation-completely-falls-apart-2b969110d400
source_author: MixBanana (Sahar Shlichove)
source_date: 2026-02
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - SaaS PRM platform
---

# Multi-Tenant Isolation Failure via Client-Controlled X-PRM-TenantId Header

## 链接

https://mixbanana.medium.com/when-multi-tenant-isolation-completely-falls-apart-2b969110d400

## 漏洞类型

Tenant Isolation / BOLA

## 目标业务场景

SaaS PRM platform

## 关键利用链摘要

Set X-PRM-TenantId header to other tenant ID in API calls

## 可迁移技法

Unauth full data access and schema exposure across PRM tenants in authorized BB

## 为什么值得收藏

- 该案例可作为 `Tenant Isolation / BOLA` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->
