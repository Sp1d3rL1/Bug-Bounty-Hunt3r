---
type: case
vuln_class: disclosure
source_url: https://infosecwriteups.com/how-i-found-a-5-500-bug-using-just-reconnaissance-2768fdba5ff2
source_author: Codi (infosecwriteups)
source_date: 2025-12-25
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - web apps internal
---

# $5500 recon-only bug via passive enum to internal config

## 链接

https://infosecwriteups.com/how-i-found-a-5-500-bug-using-just-reconnaissance-2768fdba5ff2

## 漏洞类型

disclosure

## 目标业务场景

web apps internal

## 关键利用链摘要

Amass Subfinder CRT.sh waybackurls → internal-dashboard → /admin-config.json

## 可迁移技法

Passive recon alone uncovered creds/AWS keys in forgotten internal subdomain on BB program

## 为什么值得收藏

- 该案例可作为 `disclosure` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
