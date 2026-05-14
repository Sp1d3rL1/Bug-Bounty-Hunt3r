---
type: case
vuln_class: request smuggling
source_url: https://hackerone.com/reports/3665363
source_author: BB hunter (H1 report)
source_date: 2026-04
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - HTTP
  - 2 servers with trailer parsing
---

# Integer Overflow in HTTP/2 Trailer Headers for Smuggling

## 链接

https://hackerone.com/reports/3665363

## 漏洞类型

request smuggling

## 目标业务场景

HTTP/2 servers with trailer parsing

## 关键利用链摘要

Signedness mismatch in printf precision for HTTP/2 trailers enables smuggling

## 可迁移技法

Niche H2-specific primitive for desync in modern protocols

## 为什么值得收藏

- 该案例可作为 `request smuggling` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
