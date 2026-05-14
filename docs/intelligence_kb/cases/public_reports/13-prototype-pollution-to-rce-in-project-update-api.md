---
type: case
vuln_class: Pollution
source_url: https://www.intigriti.com/researchers/blog/bug-bytes/intigriti-bug-bytes-235-april-2026
source_author: Hunter from Intigriti Bug Bytes
source_date: 2026-04
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - SaaS
  - API
---

# Prototype Pollution to RCE in Project Update API

## 链接

https://www.intigriti.com/researchers/blog/bug-bytes/intigriti-bug-bytes-235-april-2026

## 漏洞类型

Pollution

## 目标业务场景

SaaS/API

## 关键利用链摘要

- strong: proto - text: manipulation in JSON update endpoint

## 可迁移技法

Classic client-side pollution leads to RCE in modern JS-heavy SaaS apps

## 为什么值得收藏

- 该案例可作为 `Pollution` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
