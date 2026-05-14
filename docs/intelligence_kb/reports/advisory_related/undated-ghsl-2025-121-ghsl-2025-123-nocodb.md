<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: github_security_lab
canonical_report_url: https://securitylab.github.com/advisories/GHSL-2025-121_GHSL-2025-123_nocodb
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
  - https://securitylab.github.com/advisories/GHSL-2025-121_GHSL-2025-123_nocodb
---
# Ghsl 2025 121_Ghsl 2025 123_Nocodb

## TL;DR

NocoDB 0.265.1 存在多处漏洞 (GHSL-2025-121/122/123)：存储型 XSS、未验证重定向及远程代理能力。

## 来源与关联材料

- 官方报告: https://securitylab.github.com/advisories/GHSL-2025-121_GHSL-2025-123_nocodb
- 相关材料: https://securitylab.github.com/advisories/GHSL-2025-121_GHSL-2025-123_nocodb

## 业务/技术背景

NocoDB 开源数据库工具的附件与 API 处理。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）

认证用户上传恶意 SVG 触发 XSS；未验证 redirect；未认证端点提供远程代理。

## 根因

SVG 上传未 sanitization；login redirect 逻辑缺陷；axiosRequestMake 端点无认证限制。

## Impact 表达方式

账户接管、数据外泄、远程代理滥用。

## 可迁移狩猎思路

检查文件上传 sanitization、重定向验证及未认证代理端点。

## 与现有 technique/case 卡关联

存储型 XSS 与开放代理模式。

## 授权边界与不复现说明

仅限已公开披露的研究，授权测试应在自有 NocoDB 实例进行。

## Evidence / 核查元数据

- 索赔: GitHub Security Lab advisory is publicly listed
  源 URL: https://securitylab.github.com/advisories/GHSL-2025-121_GHSL-2025-123_nocodb/
  验证备注: Discovered from GitHub Security Lab advisories index.
- 主要来源片段验证: https://securitylab.github.com/advisories/GHSL-2025-121_GHSL-2025-123_nocodb (raw_content_hash: ae7c3b826ee5a866)

<!-- REPORT_INTEL_END -->
