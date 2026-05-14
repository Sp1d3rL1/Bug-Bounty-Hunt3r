<!-- GROK_API_SCAFFOLD_START -->
---
type: case
title: "From IDOR to SQL Injection in GraphQL WebSocket Escalated to PII Leak"
vuln_class: "BOLA/IDOR GraphQL"
source_url: "https://medium.com/@DarkyOS/sql-injection-in-graphql-websocket-escalated-to-pii-document-leak-09ba7ad2800a"
source_author: "Ahmed Ghadban"
source_date: "2026-04"
confidence: "low"
risk_level: "high"
freshness: "2026-04"
target_types:
  - "GraphQL WebSocket API"
---

# From IDOR to SQL Injection in GraphQL WebSocket Escalated to PII Leak

## 链接
- https://medium.com/@DarkyOS/sql-injection-in-graphql-websocket-escalated-to-pii-document-leak-09ba7ad2800a

## 漏洞类型
BOLA/IDOR GraphQL

## 目标业务场景
GraphQL WebSocket API

## 关键利用链摘要
Start with IDOR on GraphQL operation ID then escalate via WebSocket error-based Postgres injection. Disclosed $2,000 critical bounty.

## 可迁移技法
仅迁移到授权项目、靶场或自有环境；优先提炼前置条件、权限边界、状态机或集成点，不复现真实第三方目标。

## 为什么值得收藏
用于学习公开案例的根因、impact 表达、报告结构与授权范围内的验证思路。
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核查结果

来源 URL 提取失败（tavily_extract_failed: Failed to fetch url），无法验证具体案例细节、赏金金额或 测试载荷。

## 来源列表
- https://medium.com/@DarkyOS/sql-injection-in-graphql-websocket-escalated-to-pii-document-leak-09ba7ad2800a

## 验证说明
无法获取页面内容，建议人工访问验证或标记为 needs_review。

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `needs_review`
- verification_summary: Source URL could not be fetched/extracted; content unverified.
- source_urls:
  - https://medium.com/@DarkyOS/sql-injection-in-graphql-websocket-escalated-to-pii-document-leak-09ba7ad2800a
- tavily_verification:
  - status: needs_review
  - summary: verified_urls=0 failed_urls=1 skipped_urls=0 search_candidates=5
  - checked_at: 2026-05-09T04:26:57.960982
  - mode: default
  - usage: {'credits': 1}
  - failed_urls:
    - https://medium.com/@DarkyOS/sql-injection-in-graphql-websocket-escalated-to-pii-document-leak-09ba7ad2800a (tavily_extract_failed)

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/api.md -->

<!-- backlink: docs/checklists/cors_postmessage_websocket.md -->

<!-- backlink: docs/checklists/graphql.md -->
