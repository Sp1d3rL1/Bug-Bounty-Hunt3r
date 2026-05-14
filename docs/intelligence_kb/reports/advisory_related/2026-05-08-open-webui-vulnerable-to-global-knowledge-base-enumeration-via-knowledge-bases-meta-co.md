<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: github_advisory
canonical_report_url: https://github.com/advisories/GHSA-6c2x-gcp3-gp73
program_or_vendor: GHSA-6c2x-gcp3-gp73
reporter_or_author: GitHub Advisory Database
disclosed_at: 2026-05-08
severity: medium
bounty: unknown
cwe: CWE-200, CWE-862
cve: CVE-2026-44553
vuln_class: Open WebUI vulnerable to Global Knowledge Base Enumeration via knowledge-bases Meta-Collection
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
  - https://github.com/advisories/GHSA-6c2x-gcp3-gp73
---
# Open WebUI vulnerable to Global Knowledge Base Enumeration via knowledge-bases Meta-Collection

## TL;DR
Open WebUI 知识库元集合 knowledge-bases 可被任意认证用户枚举。

## 来源与关联材料
- GitHub 安全公告：https://github.com/advisories/GHSA-6c2x-gcp3-gp73

## 业务/技术背景
Open WebUI 检索路由使用 _validate_collection_access 控制访问。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）
仅检查 user-memory-* 和 file-* 模式，其余集合直接放行。

## 根因
allowlist 不完整。

## Impact 表达方式
全局知识库 ID、名称、描述泄露。

## 可迁移狩猎思路
审计所有集合访问控制的 allowlist 完整性。

## 与现有 technique/case 卡关联
与 CWE-200 信息泄露及 CWE-862 授权缺失关联。

## 授权边界与不复现说明
仅限已披露的公开 GHSA 信息，不在生产环境复现。

## Evidence / 核查元数据
- 主要来源：https://github.com/advisories/GHSA-6c2x-gcp3-gp73

<!-- REPORT_INTEL_END -->
