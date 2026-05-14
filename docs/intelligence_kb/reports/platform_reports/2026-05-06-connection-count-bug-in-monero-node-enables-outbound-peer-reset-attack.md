<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: hackerone
canonical_report_url: https://hackerone.com/reports/3185083
program_or_vendor: HackerOne program
reporter_or_author: unknown
disclosed_at: 2026-05-06
severity: unknown
bounty: unknown
cwe: unknown
cve: 
vuln_class: Connection Count Bug in Monero Node Enables Outbound Peer Reset Attack
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
  - https://hackerone.com/reports/3185083
---
# Connection Count Bug in Monero Node Enables Outbound Peer Reset Attack

## TL;DR
Connection Count Bug in Monero Node Enables Outbound Peer Reset Attack

## 来源与关联材料
- HackerOne report: https://hackerone.com/reports/3185083

## 业务/技术背景
Monero node connection handling (limited public details available from disclosure).

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）
Connection count bug enabling outbound peer reset attack (publicly disclosed on HackerOne).

## 根因
Connection Count Bug (per report title).

## Impact 表达方式
Enables outbound peer reset attack.

## 可迁移狩猎思路
Review node connection limits and peer management in similar P2P protocols under authorized testing.

## 与现有 technique/case 卡关联
No prior associations noted in source.

## 授权边界与不复现说明
Public disclosure only; reproduction limited to authorized lab environments on owned or permitted systems.

## Evidence / 核查元数据
- Claim: HackerOne API returned a disclosed Hacktivity/report item
- Source: https://hackerone.com/reports/3185083
- Verification: HackerOne API row id: 3185083

<!-- REPORT_INTEL_END -->
