---
type: case
vuln_class: prototype pollution
source_url: https://bugbounty.info/Attack-Surface/Web/Client-Side/Prototype-Pollution
source_author: Multiple hunters (HackerOne refs)
source_date: 2024-2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - web apps using lodash
---

# Prototype Pollution to XSS via lodash merge gadget on Shopify (updated 2024 chain)

## 链接

https://bugbounty.info/Attack-Surface/Web/Client-Side/Prototype-Pollution

## 漏洞类型

prototype pollution

## 目标业务场景

web apps using lodash

## 关键利用链摘要

Pollute via JSON source → lodash merge → DOM sink

## 可迁移技法

Classic gadget still yielding BB in 2024+; client-side focus per authorized reports

## 为什么值得收藏

- 该案例可作为 `prototype pollution` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
