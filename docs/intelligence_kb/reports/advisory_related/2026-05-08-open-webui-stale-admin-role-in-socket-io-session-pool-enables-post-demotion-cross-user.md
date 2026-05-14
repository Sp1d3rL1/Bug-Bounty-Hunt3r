<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: github_advisory
canonical_report_url: https://github.com/advisories/GHSA-45m8-cpm2-3v65
program_or_vendor: GHSA-45m8-cpm2-3v65
reporter_or_author: GitHub Advisory Database
disclosed_at: 2026-05-08
severity: high
bounty: unknown
cwe: CWE-384, CWE-863
cve: CVE-2026-44553
vuln_class: Open WebUI: Stale Admin Role in Socket.IO Session Pool Enables Post-Demotion Cross-User Note Access
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
  - https://github.com/advisories/GHSA-45m8-cpm2-3v65
---
# Open WebUI: Stale Admin Role in Socket.IO Session Pool Enables Post-Demotion Cross-User Note Access

## TL;DR
Open WebUI Socket.IO 会话池中角色快照未失效，导致降权后仍可跨用户访问笔记。

## 来源与关联材料
- GitHub 安全公告：https://github.com/advisories/GHSA-45m8-cpm2-3v65

## 业务/技术背景
Open WebUI 使用 Socket.IO 处理协作文档，SESSION_POOL 缓存角色。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）
connect 时快照角色，角色变更不清理 SESSION_POOL，heartbeat 不刷新。

## 根因
会话角色未与数据库实时同步。

## Impact 表达方式
已降权用户保留管理权限。

## 可迁移狩猎思路
检查会话缓存是否在权限变更时失效。

## 与现有 technique/case 卡关联
与 CWE-384 会话固定及 CWE-863 授权绕过关联。

## 授权边界与不复现说明
仅限已披露的公开 GHSA 信息，不在生产环境复现。

## Evidence / 核查元数据
- 主要来源：https://github.com/advisories/GHSA-45m8-cpm2-3v65

<!-- REPORT_INTEL_END -->
