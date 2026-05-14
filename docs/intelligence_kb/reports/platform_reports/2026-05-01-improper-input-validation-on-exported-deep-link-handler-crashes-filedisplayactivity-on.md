<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: hackerone
canonical_report_url: https://hackerone.com/reports/3399016
program_or_vendor: HackerOne program
reporter_or_author: unknown
disclosed_at: 2026-05-01
severity: None
bounty: unknown
cwe: unknown
cve: 
vuln_class: Improper input validation On Exported deep-link handler crashes `FileDisplayActivity` on crafted external URL — Denial-of-Service
confidence: high
learning_value: high
source_tier: 
source_id: 
access_level: 
license_policy: 
collection_policy: 
risk_flag: 
human_review_required: 
source_reliability: 
legal_risk: 
blocked_for_content_collection: 
related_urls:
  - https://hackerone.com/reports/3399016
---
# Improper input validation On Exported deep-link handler crashes `FileDisplayActivity` on crafted external URL — Denial-of-Service

## TL;DR
Improper input validation On Exported deep-link handler crashes `FileDisplayActivity` on crafted external URL — Denial-of-Service

## 来源与关联材料
- HackerOne report: https://hackerone.com/reports/3399016

## 业务/技术背景
Exported deep-link handler in FileDisplayActivity (limited public details available from disclosure).

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）
Crafted external URL triggers crash via improper input validation (publicly disclosed on HackerOne).

## 根因
Improper input validation on exported deep-link handler.

## Impact 表达方式
Denial-of-Service via application crash.

## 可迁移狩猎思路
Test deep-link handlers and exported activities for input validation issues in authorized mobile/app environments.

## 与现有 technique/case 卡关联
No prior associations noted in source.

## 授权边界与不复现说明
Public disclosure only; reproduction limited to authorized lab environments on owned or permitted systems.

## Evidence / 核查元数据
- Claim: HackerOne API returned a disclosed Hacktivity/report item
- Source: https://hackerone.com/reports/3399016
- Verification: HackerOne API row id: 3399016

<!-- REPORT_INTEL_END -->
