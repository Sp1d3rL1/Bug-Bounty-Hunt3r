<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: github_security_lab
canonical_report_url: https://securitylab.github.com/advisories/GHSL-2025-120_Sentry
program_or_vendor: GitHub Security Lab advisory
reporter_or_author: GitHub Security Lab
disclosed_at: unknown
severity: unknown
bounty: unknown
cwe: unknown
cve: 
vuln_class: Security advisory / report
confidence: high
learning_value: medium
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
  - https://securitylab.github.com/advisories/GHSL-2025-120_Sentry
---
# Ghsl 2025 120_Sentry

## TL;DR

Sentry 25.11.0 中 group reprocessing 流程存在权限提升漏洞 (GHSL-2025-120)。

## 来源与关联材料

- 官方报告: https://securitylab.github.com/advisories/GHSL-2025-120_Sentry
- 相关材料: https://securitylab.github.com/advisories/GHSL-2025-120_Sentry

## 业务/技术背景

Sentry 事件分组与权限模型。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）

持有 event:write 权限的用户可通过 reprocessing endpoint 触发 mass deletion。

## 根因

GroupPermission 模型对 POST 仅要求 event:write，而 DELETE 操作本应要求 event:admin。

## Impact 表达方式

绕过权限导致事件数据完整性受损。

## 可迁移狩猎思路

检查 API 端点权限模型中 scope 与 action 类型的 mismatch。

## 与现有 technique/case 卡关联

权限提升与 scope mismatch 模式。

## 授权边界与不复现说明

仅限已公开披露的研究，授权测试应在自有 Sentry 实例进行。

## Evidence / 核查元数据

- 索赔: GitHub Security Lab advisory is publicly listed
  源 URL: https://securitylab.github.com/advisories/GHSL-2025-120_Sentry/
  验证备注: Discovered from GitHub Security Lab advisories index.
- 主要来源片段验证: https://securitylab.github.com/advisories/GHSL-2025-120_Sentry (raw_content_hash: 0eaf03b791f08596)

<!-- REPORT_INTEL_END -->
