<!-- GROK_API_SCAFFOLD_START -->
---
type: case
title: "DOS via Mutation Aliasing in GraphQL Account Recovery API"
vuln_class: "GraphQL DoS"
source_url: "https://www.redpacketsecurity.com/hackerone-bugbounty-disclosure-dos-via-mutation-aliasing-in-graphql-account-recovery-phone-number-verification-api-hellokbit/"
source_author: "hellokbit"
source_date: "2026-04"
confidence: "high"
risk_level: "high"
freshness: "2026-04"
target_types:
  - "Web/API/SaaS GraphQL"
---

# DOS via Mutation Aliasing in GraphQL Account Recovery API

## 链接
- https://www.redpacketsecurity.com/hackerone-bugbounty-disclosure-dos-via-mutation-aliasing-in-graphql-account-recovery-phone-number-verification-api-hellokbit/

## 漏洞类型
GraphQL DoS

## 目标业务场景
Web/API/SaaS GraphQL

## 关键利用链摘要
HackerOne report on DoS via aliasing in GraphQL phone verification mutation for account recovery.

## 可迁移技法
仅迁移到授权项目、靶场或自有环境；优先提炼前置条件、权限边界、状态机或集成点，不复现真实第三方目标。

## 为什么值得收藏
用于学习公开案例的根因、impact 表达、报告结构与授权范围内的验证思路。
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 案例概述
HackerOne 报告披露了 GraphQL Account Recovery Phone Number Verification API 中的突变别名导致 可用性影响风险（仅 Lab/限速验证）。

## 核心发现
通过在 phone verification mutation 上使用别名触发账户恢复 可用性影响风险（仅 Lab/限速验证）。

## 影响
授权测试中针对支付/SaaS 认证流的特定 GraphQL 业务逻辑 可用性影响风险（仅 Lab/限速验证）。

## 来源链接
- https://www.redpacketsecurity.com/hackerone-bugbounty-disclosure-可用性影响风险（仅 Lab/限速验证）-via-mutation-aliasing-in-graphql-account-recovery-phone-number-verification-api-hellokbit/

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: TAVILY 提取确认源内容，披露日期 2026-04，作者 hellokbit，完整细节匹配。
- source_urls:
  - https://www.redpacketsecurity.com/hackerone-bugbounty-disclosure-dos-via-mutation-aliasing-in-graphql-account-recovery-phone-number-verification-api-hellokbit/
- evidence:
  - claim: HackerOne 报告标题 DOS via Mutation Aliasing in GraphQL Account Recovery Phone Number Verification API，提交日期 2026-04-16
    source: https://www.redpacketsecurity.com/hackerone-bugbounty-disclosure-dos-via-mutation-aliasing-in-graphql-account-recovery-phone-number-verification-api-hellokbit/
    verification: TAVILY 提取片段直接确认

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/graphql.md -->
