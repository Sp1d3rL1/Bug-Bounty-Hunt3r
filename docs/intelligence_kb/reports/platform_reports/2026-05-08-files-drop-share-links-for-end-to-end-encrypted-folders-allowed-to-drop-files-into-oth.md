<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: hackerone
canonical_report_url: https://hackerone.com/reports/3304830
program_or_vendor: HackerOne program
reporter_or_author: unknown
disclosed_at: 2026-05-08
severity: Low
bounty: unknown
cwe: unknown
cve: 
vuln_class: Files drop share links for end-to-end encrypted folders allowed to drop files into other folders of the share owner 
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
  - https://hackerone.com/reports/3304830
---
# Files drop share links for end-to-end encrypted folders allowed to drop files into other folders of the share owner

## TL;DR
端到端加密文件夹的Files drop share links允许将文件放入共享所有者的其他文件夹。

## 来源与关联材料
- 原始报告: https://hackerone.com/reports/3304830
- HackerOne API验证: https://hackerone.com/reports/3304830

## 业务/技术背景
Nextcloud端到端加密文件夹的共享drop链接功能存在权限边界问题。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）
已披露的HackerOne报告，涉及Files drop share links的跨文件夹文件放置。

## 根因
Files drop share links for end-to-end encrypted folders允许将文件放入其他文件夹。

## Impact 表达方式
低严重性，影响共享所有者文件夹的隔离。

## 可迁移狩猎思路
检查端到端加密共享链接的权限验证逻辑。

## 与现有 technique/case 卡关联
暂无关联。

## 授权边界与不复现说明
仅限已披露公开报告，不进行任何复现或测试。

## Evidence / 核查元数据
- 声明: HackerOne API returned a disclosed Hacktivity/report item
- 来源URL: https://hackerone.com/reports/3304830
- 验证备注: HackerOne API row id: 3304830

<!-- REPORT_INTEL_END -->
