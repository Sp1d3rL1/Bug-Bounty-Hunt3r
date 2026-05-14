---
type: case
vuln_class: CSPT
source_url: https://matanber.com/blog/cspt-levels
source_author: Matan Berson (via Doyensec list)
source_date: 2024
collected_at: 2026-05-05
freshness: 2024
confidence: high
target_types:
  - web apps
---

# CSPT Levels & Practical Attacks (hunter X post reference)

## 链接

https://matanber.com/blog/cspt-levels

## 漏洞类型

CSPT

## 目标业务场景

web apps

## 关键利用链摘要

Graded path traversal levels with fetch diversion

## 可迁移技法

Niche technique shared by hunter; used in real BB chains

## 为什么值得收藏

- 该案例可作为 `CSPT` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->
