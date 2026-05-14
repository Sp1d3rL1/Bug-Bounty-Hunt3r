---
type: case
vuln_class: CSPT
source_url: https://medium.com/@renwa/client-side-path-traversal-cspt-bug-bounty-reports-and-techniques-8ee6cd2e7ca1
source_author: Renwa
source_date: 2024-03
collected_at: 2026-05-05
freshness: 2024
confidence: high
target_types:
  - web app (REST API frontend)
---

# Client-Side Path Traversal (CSPT) to Account Takeover + XSS via profile URL traversal

## 链接

https://medium.com/@renwa/client-side-path-traversal-cspt-bug-bounty-reports-and-techniques-8ee6cd2e7ca1

## 漏洞类型

CSPT

## 目标业务场景

web app (REST API frontend)

## 关键利用链摘要

%5C..%2F": - /url: https://medium.com/@renwa/client-side-path-traversal-cspt-bug-bounty-reports-and-techniques-8ee6cd2e7ca1§CSPT§%5C..%2F - text: "traversal + %23 hash truncate in fetch URL to spoof JSON response from attacker-controlled file

## 可迁移技法

Chains file upload + unsanitized externalUrl to DOM XSS on Ctrl+Click; real BB $2k payout on authorized program

## 为什么值得收藏

- 该案例可作为 `CSPT` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/cors_postmessage_websocket.md -->

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->

<!-- backlink: docs/checklists/prototype_pollution_xss_chain.md -->

<!-- backlink: docs/checklists/subdomain_takeover.md -->
