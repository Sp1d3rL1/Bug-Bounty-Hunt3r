<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "What bugs you should look for in a GraphQL API? Bug Bounty Case Study"
vuln_class: "GraphQL access control, DoS, SQLi, CSRF"
source_url: "https://www.youtube.com/watch?v=9tNUPpB1gto"
source_author: "Bug Bounty Reports Explained"
source_date: "2025-06-24"
confidence: "high"
risk_level: "medium"
freshness: "2025"
target_types:
  - "Web/API/GraphQL"
---

# What bugs you should look for in a GraphQL API? Bug Bounty Case Study

## 核心思路
Summarizes real 2025+ GraphQL bugs from HackerOne reports including access control failures and schema disclosure for authorized API testing.

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
Web/API/GraphQL

## 为什么有效
围绕 GraphQL access control, DoS, SQLi, CSRF 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

## 手工验证流程
在授权范围内以只读或最小影响方式验证：确认前置条件、构造合成数据/测试账号、观察授权边界或状态差异、记录证据并停止在安全影响证明处。

## 可自动化部分
可自动化收集公开入口、参数、JS/API schema、配置差异和变更信号；实际漏洞确认保留人工复核。

## 误报/失败条件
目标无对应功能、权限模型不同、补丁已生效、测试账号权限不足、来源无法复核或影响无法用最小证明表达。

## 授权边界
不访问非授权目标；不导出真实敏感数据；不进行破坏性、DoS、爆破、认证批量尝试或真实支付损害测试。

## 报告 impact 角度
说明可影响的资产、权限边界、业务状态、数据类别、可复现前置条件和最小影响证据。

## 相关案例链接
- https://www.youtube.com/watch?v=9tNUPpB1gto
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## Summary
Analyzes disclosed GraphQL bug bounty reports focusing on authorization bypass for read/create/update/delete operations, 可用性影响风险（仅 Lab/限速验证） via complex queries/batching, SQL injection via parameters, and CSRF via method bypasses. Includes specific HackerOne report links and examples like Instagram email leaks and GitLab deletion bypass.

Key links from source:
- https://hackerone.com/reports/343464
- https://hackerone.com/reports/2233480
- https://www.landh.tech/blog/20240304-google-hack-50000/

High-level for authorized testing in bug bounty programs and labs only.

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: Video title, channel, date, description, and transcript points fully match provided details and tavily query; content verified via direct page fetch.
- source_urls:
  - https://www.youtube.com/watch?v=9tNUPpB1gto
- evidence:
  - claim: Video title, author, date, and GraphQL bug categories (access control, DoS, SQLi, CSRF) match exactly
    source: https://www.youtube.com/watch?v=9tNUPpB1gto
    verification: Direct browse confirmed upload date 2025-06-24, channel Bug Bounty Reports Explained, and detailed transcript on authorization, DoS, SQLi, schema disclosure, CSRF

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/api.md -->

<!-- backlink: docs/checklists/cors_postmessage_websocket.md -->

<!-- backlink: docs/checklists/graphql.md -->
