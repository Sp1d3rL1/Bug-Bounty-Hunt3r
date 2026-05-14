---
type: case
vuln_class: Access Control
source_url: https://infosecwriteups.com/breaking-and-reporting-bugs-the-story-behind-my-comet-and-black-hole-wins-on-yeswehack-15d5f0d39d50
source_author: Jeewan Bhatta
source_date: 2026-03-14
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - SaaS enterprise platform (YesWeHack BB)
---

# Improper Access Control on Enterprise Invitation Endpoint Leading to Account Takeover

## 链接

https://infosecwriteups.com/breaking-and-reporting-bugs-the-story-behind-my-comet-and-black-hole-wins-on-yeswehack-15d5f0d39d50

## 漏洞类型

Access Control

## 目标业务场景

SaaS enterprise platform (YesWeHack BB)

## 关键利用链摘要

Swap enterprise_id in POST invitation request to add self as Owner to any enterprise without rights check

## 可迁移技法

Full admin takeover of unrelated organizations with PII exposure and owner removal in multi-tenant SaaS

## 为什么值得收藏

- 该案例可作为 `Access Control` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->

<!-- backlink: docs/checklists/subdomain_takeover.md -->
