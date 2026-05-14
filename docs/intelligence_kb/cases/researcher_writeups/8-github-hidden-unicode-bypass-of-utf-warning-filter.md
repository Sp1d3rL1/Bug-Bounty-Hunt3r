---
type: case
vuln_class: Bypass
source_url: https://joshua.hu/2025-bug-bounty-stories-fail
source_author: Joshua Rogers
source_date: 2025-05
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - GitHub code UI
---

# GitHub Hidden Unicode Bypass of UTF Warning Filter

## 链接

https://joshua.hu/2025-bug-bounty-stories-fail

## 漏洞类型

Bypass

## 目标业务场景

GitHub code UI

## 关键利用链摘要

Insert invisible Unicode (U+85A4 etc.) after commands in queries to skip GitHub warning

## 可迁移技法

Evades security filter allowing code injection in Node.js repos; visible only via sed -n l

## 为什么值得收藏

- 该案例可作为 `Bypass` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
