<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: github_advisory
canonical_report_url: https://github.com/advisories/GHSA-2r4p-jpmg-48f4
program_or_vendor: GHSA-2r4p-jpmg-48f4
reporter_or_author: GitHub Advisory Database
disclosed_at: 2026-05-08
severity: critical
bounty: unknown
cwe: CWE-287
cve: CVE-2026-44551
vuln_class: Open WebUI has an LDAP Empty Password Authentication Bypass
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
  - https://github.com/advisories/GHSA-2r4p-jpmg-48f4
---
# Open WebUI has an LDAP Empty Password Authentication Bypass

## TL;DR
Open WebUI LDAP 认证未检查空密码，导致未认证简单绑定绕过。

## 来源与关联材料
- GitHub 安全公告：https://github.com/advisories/GHSA-2r4p-jpmg-48f4

## 业务/技术背景
Open WebUI 支持 LDAP 登录，auths.py 处理用户绑定。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）
LdapForm 接受空 password，Connection.bind() 在支持 RFC 4513 的 LDAP 服务器上返回成功。

## 根因
未对 password 字段进行非空验证。

## Impact 表达方式
任意用户可冒充已知 DN 登录。

## 可迁移狩猎思路
检查所有认证端点对空凭证的处理。

## 与现有 technique/case 卡关联
与 CWE-287 认证绕过模式关联。

## 授权边界与不复现说明
仅限已披露的公开 GHSA 信息，不在生产环境复现。

## Evidence / 核查元数据
- 主要来源：https://github.com/advisories/GHSA-2r4p-jpmg-48f4

<!-- REPORT_INTEL_END -->
