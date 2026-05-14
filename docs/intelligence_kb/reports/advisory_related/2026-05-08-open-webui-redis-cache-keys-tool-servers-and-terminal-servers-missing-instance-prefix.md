<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: github_advisory
canonical_report_url: https://github.com/advisories/GHSA-3x8w-4f7p-xxc2
program_or_vendor: GHSA-3x8w-4f7p-xxc2
reporter_or_author: GitHub Advisory Database
disclosed_at: 2026-05-08
severity: high
bounty: unknown
cwe: CWE-668
cve: CVE-2026-44552
vuln_class: Open WebUI: Redis Cache Keys tool_servers and terminal_servers Missing Instance Prefix Enable Cross-Instance Cache Poisoning
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
  - https://github.com/advisories/GHSA-3x8w-4f7p-xxc2
---
# Open WebUI: Redis Cache Keys tool_servers and terminal_servers Missing Instance Prefix Enable Cross-Instance Cache Poisoning

## TL;DR
Open WebUI Redis 缓存键 tool_servers 和 terminal_servers 缺少实例前缀，导致跨实例缓存投毒。

## 来源与关联材料
- GitHub 安全公告：https://github.com/advisories/GHSA-3x8w-4f7p-xxc2

## 业务/技术背景
Open WebUI 支持多实例共享 Redis，使用 REDIS_KEY_PREFIX 命名空间。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）
utils/tools.py 中仅 tool_servers 和 terminal_servers 未加前缀。

## 根因
缺少 REDIS_KEY_PREFIX 应用。

## Impact 表达方式
跨实例配置覆盖与投毒。

## 可迁移狩猎思路
审计所有 Redis 键是否一致使用命名空间前缀。

## 与现有 technique/case 卡关联
与 CWE-668 信息暴露模式关联。

## 授权边界与不复现说明
仅限已披露的公开 GHSA 信息，不在生产环境复现。

## Evidence / 核查元数据
- 主要来源：https://github.com/advisories/GHSA-3x8w-4f7p-xxc2

<!-- REPORT_INTEL_END -->
