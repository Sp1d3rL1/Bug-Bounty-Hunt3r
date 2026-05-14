---
type: case
vuln_class: Bucket XSS
source_url: https://x.com/0x0smilex/status/1979227178966581468
source_author: 0x0smilex
source_date: 2025-10-17
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - AWS S3
---

# S3 XSS via Bucket Misconfig (BucketList Tool)

## 链接

https://x.com/0x0smilex/status/1979227178966581468

## 漏洞类型

Bucket XSS

## 目标业务场景

AWS S3

## 关键利用链摘要

Upload HTML/JS to misconfigured public S3 bucket

## 可迁移技法

Reflected XSS escalation in authorized BB via cloud storage

## 为什么值得收藏

- 该案例可作为 `Bucket XSS` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
