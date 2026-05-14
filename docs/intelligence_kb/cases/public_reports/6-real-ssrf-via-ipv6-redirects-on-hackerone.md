---
type: case
vuln_class: SSRF
source_url: https://medium.com/@red_darkin/a-real-ssrf-story-from-hackerone-featuring-ipv6-redirects-9aa5e2ad8c2e
source_author: red_darkin
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - SaaS
  - API
---

# Real SSRF via IPv6 Redirects on HackerOne

## 链接

https://medium.com/@red_darkin/a-real-ssrf-story-from-hackerone-featuring-ipv6-redirects-9aa5e2ad8c2e

## 漏洞类型

SSRF

## 目标业务场景

SaaS/API

## 关键利用链摘要

IPv6": - /url: https://medium.com/@red_darkin/a-real-ssrf-story-from-hackerone-featuring-ipv6-redirects-9aa5e2ad8c2e§SSRF§IPv6 - text: address + redirect chain bypasses URL filters to internal resources

## 可迁移技法

Classic SSRF bypasses persist in 2025 SaaS with modern cloud filters

## 为什么值得收藏

- 该案例可作为 `SSRF` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/api.md -->

<!-- backlink: docs/checklists/cloud_aws_metadata_iam.md -->

<!-- backlink: docs/checklists/cloud_gcp_azure.md -->
