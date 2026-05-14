<!-- GROK_API_SCAFFOLD_START -->
---
type: case
title: "Business Logic Bypass Allows Setting Read Access Role Without Pro Plan Subscription"
vuln_class: "business logic"
source_url: "https://hackerone.com/reports/3591764"
source_author: "Lovable VDP"
source_date: "2026-03-08"
confidence: "low"
risk_level: "medium"
freshness: "2026-03"
target_types:
  - "SaaS/API"
---

# Business Logic Bypass Allows Setting Read Access Role Without Pro Plan Subscription

## 链接
- https://hackerone.com/reports/3591764

## 漏洞类型
business logic

## 目标业务场景
SaaS/API

## 关键利用链摘要
Manipulate access_level parameter in invitation link creation to bypass subscription requirement.

## 可迁移技法
仅迁移到授权项目、靶场或自有环境；优先提炼前置条件、权限边界、状态机或集成点，不复现真实第三方目标。

## 为什么值得收藏
用于学习公开案例的根因、impact 表达、报告结构与授权范围内的验证思路。
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核查结果

Source URL browse returned insufficient content (HackerOne report likely requires authentication/login). Tavily extract failed. Cannot verify POC, parameters, or remediation details beyond item metadata.

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `needs_review`
- verification_summary: Exactly what could not be verified: report body, reproduction steps, access_level manipulation evidence, and bounty/impact details.
- source_urls:
  - https://hackerone.com/reports/3591764
- tavily_verification:
  - status: needs_review
  - summary: verified_urls=0 failed_urls=1 skipped_urls=0 search_candidates=0
  - checked_at: 2026-05-09T04:27:18.626643
  - mode: default
  - usage: {'credits': 1}
  - failed_urls:
    - https://hackerone.com/reports/3591764 (tavily_extract_failed)

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/payment_business_logic.md -->
