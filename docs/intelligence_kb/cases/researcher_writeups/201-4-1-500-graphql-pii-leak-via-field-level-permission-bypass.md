<!-- GROK_API_SCAFFOLD_START -->
---
type: case
title: "$1,500 GraphQL PII Leak via field-level permission bypass"
vuln_class: "GraphQL field-level permission bypass"
source_url: "https://medium.com/@tinopreter/1-500-pii-leak-via-graphql-field-level-permission-bypass-1e7ea2d1a019"
source_author: "tinopreter"
source_date: "2026-04-13"
confidence: "high"
risk_level: "medium"
freshness: "2026"
target_types:
  - "API/GraphQL"
---

# $1,500 GraphQL PII Leak via field-level permission bypass

## 链接
- https://medium.com/@tinopreter/1-500-pii-leak-via-graphql-field-level-permission-bypass-1e7ea2d1a019

## 漏洞类型
GraphQL field-level permission bypass

## 目标业务场景
API/GraphQL

## 关键利用链摘要
Real 2026 disclosed writeup showing PII leak in GraphQL for authorized API bug bounty work.

## 可迁移技法
仅迁移到授权项目、靶场或自有环境；优先提炼前置条件、权限边界、状态机或集成点，不复现真实第三方目标。

## 为什么值得收藏
用于学习公开案例的根因、impact 表达、报告结构与授权范围内的验证思路。
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## Summary
Disclosed case of $1,500 bounty for bypassing field-level permissions in GraphQL to leak PII (emails, IDs, roles) via nested Organization queries and GetOrgWebhooks. High-level reproduction: query restricted fields through org-level objects after basic auth; discovered via frontend JS inspection. Reported as High severity.

Source: direct article verification confirms bounty amount, PII impact, and GraphQL permission bypass details.

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: Article title, author, vulnerability details, and $1,500 bounty fully match; content verified via direct page fetch despite date not explicitly restated in body.
- source_urls:
  - https://medium.com/@tinopreter/1-500-pii-leak-via-graphql-field-level-permission-bypass-1e7ea2d1a019
- evidence:
  - claim: Title, author, $1,500 bounty, field-level permission bypass leading to PII leak via GetOrgWebhooks and nested fields
    source: https://medium.com/@tinopreter/1-500-pii-leak-via-graphql-field-level-permission-bypass-1e7ea2d1a019
    verification: Direct browse confirmed exact match to provided title, author, and technical details

<!-- GROK_API_EXPANSION_END -->
