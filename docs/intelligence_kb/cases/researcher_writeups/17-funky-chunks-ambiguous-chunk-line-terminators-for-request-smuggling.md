---
type: case
vuln_class: request smuggling
source_url: https://w4ke.info/2025/06/18/funky-chunks.html
source_author: w4ke.info researcher
source_date: 2025-06-18
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - proxies with chunked parsing quirks
---

# Funky Chunks: Ambiguous Chunk Line Terminators for Request Smuggling

## 链接

https://w4ke.info/2025/06/18/funky-chunks.html

## 漏洞类型

request smuggling

## 目标业务场景

proxies with chunked parsing quirks

## 关键利用链摘要

Abuse chunked-body terminator ambiguity in extensions/oversized chunks for new desync variants

## 可迁移技法

Bypasses CL/TE confusion reliance; practical for 2025+ smuggling in BB

## 为什么值得收藏

- 该案例可作为 `request smuggling` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/http_request_smuggling.md -->
