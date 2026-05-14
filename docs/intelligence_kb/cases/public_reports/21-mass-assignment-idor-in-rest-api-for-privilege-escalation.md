---
type: case
vuln_class: Assignment
source_url: https://medium.com/@HackerMD/real-bug-reports-hackerone-disclosures-se-seekho-top-hunters-ki-writing-style-copy-karo-275be9c7a7f8
source_author: Hacker MD real report pattern
source_date: 2026-04
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - SaaS API
---

# Mass Assignment + IDOR in REST API for Privilege Escalation

## 链接

https://medium.com/@HackerMD/real-bug-reports-hackerone-disclosures-se-seekho-top-hunters-ki-writing-style-copy-karo-275be9c7a7f8

## 漏洞类型

Assignment

## 目标业务场景

SaaS API

## 关键利用链摘要

Add is_admin:true in PUT request to user object

## 可迁移技法

Classic mass assignment in JSON APIs still escalates in 2026 SaaS

## 为什么值得收藏

- 该案例可作为 `Assignment` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
