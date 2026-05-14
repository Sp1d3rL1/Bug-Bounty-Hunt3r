---
type: case
vuln_class: API BOLA/IDOR
source_url: https://x.com
source_author: shivangmauryaa
source_date: 2026-03-01
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Media API
---

# $1500 IDOR Fetching 5M Images via Object ID Swap

## 链接

https://x.com

## 漏洞类型

API BOLA/IDOR

## 目标业务场景

Media API

## 关键利用链摘要

Swap image/object ID in media API to access millions of private images

## 可迁移技法

Scale demonstrates mass data exfil potential in image-heavy platforms

## 为什么值得收藏

- 该案例可作为 `API BOLA/IDOR` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->
