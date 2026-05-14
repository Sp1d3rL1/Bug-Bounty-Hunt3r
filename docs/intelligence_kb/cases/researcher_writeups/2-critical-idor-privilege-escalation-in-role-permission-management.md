---
type: case
vuln_class: + Privilege Escalation
source_url: https://medium.com/@mrro0o0tt/hunting-access-control-bugs-how-i-found-a-critical-idor-privilege-escalation-in-a-fort-knox-like-a4aeb46d8714
source_author: Whoami (mrro0o0tt)
source_date: 2026
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - SaaS enterprise platform
---

# Critical IDOR & Privilege Escalation in Role Permission Management

## 链接

https://medium.com/@mrro0o0tt/hunting-access-control-bugs-how-i-found-a-critical-idor-privilege-escalation-in-a-fort-knox-like-a4aeb46d8714

## 漏洞类型

+ Privilege Escalation

## 目标业务场景

SaaS enterprise platform

## 关键利用链摘要

Replace admin Role-ID in PUT /security/[Role-ID]/businessroles/ with Manager cookie to enable all perms

## 可迁移技法

Bypasses role boundaries allowing low-priv to Global Admin in hardened multi-tenant SaaS

## 为什么值得收藏

- 该案例可作为 `+ Privilege Escalation` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
