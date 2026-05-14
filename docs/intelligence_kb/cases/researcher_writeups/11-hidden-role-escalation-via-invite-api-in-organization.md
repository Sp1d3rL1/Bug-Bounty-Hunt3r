---
type: case
vuln_class: Escalation
source_url: https://medium.com/@0xm394tr0n/hidden-role-via-invite-api-org-owner-takeover
source_author: 0xm394tr0n
source_date: 2026
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Multi-tenant SaaS
---

# Hidden Role Escalation via Invite API in Organization

## 链接

https://medium.com/@0xm394tr0n/hidden-role-via-invite-api-org-owner-takeover

## 漏洞类型

Escalation

## 目标业务场景

Multi-tenant SaaS

## 关键利用链摘要

Inject hidden role param in invite POST to escalate to org owner

## 可迁移技法

Bypasses role/permission boundary checks in multi-tenant org management

## 为什么值得收藏

- 该案例可作为 `Escalation` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/subdomain_takeover.md -->
