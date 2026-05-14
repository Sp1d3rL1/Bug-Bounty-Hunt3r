---
type: case
vuln_class: API BOLA/IDOR
source_url: https://medium.com
source_author: tinopreter
source_date: 2026-01-01
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Device API
---

# $500 UUID Swap IDOR in Device Management API

## 链接

https://medium.com

## 漏洞类型

API BOLA/IDOR

## 目标业务场景

Device API

## 关键利用链摘要

Replace UUID in device endpoint despite sequential guessing resistance

## 可迁移技法

Shows UUIDs still vulnerable without proper authz; practical for IoT-like APIs

## 为什么值得收藏

- 该案例可作为 `API BOLA/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
