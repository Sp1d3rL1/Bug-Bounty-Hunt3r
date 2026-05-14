<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: hackerone
canonical_report_url: https://hackerone.com/reports/3320669
program_or_vendor: HackerOne program
reporter_or_author: unknown
disclosed_at: 2026-05-01
severity: High
bounty: 10000
cwe: unknown
cve: 
vuln_class: Double fdrop on a socket through sys_netcontrol
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
  - https://hackerone.com/reports/3320669
---
# Double fdrop on a socket through sys_netcontrol

## TL;DR

通过sys_netcontrol在socket上执行双重fdrop。

## 来源与关联材料

- https://hackerone.com/reports/3320669

## 业务/技术背景

系统网络控制相关socket操作场景。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）

通过HackerOne公开披露报告确认双重fdrop缺陷。

## 根因

socket操作中的fdrop重复调用。

## Impact 表达方式

可能导致资源释放异常或服务不稳定。

## 可迁移狩猎思路

检查系统调用路径中的资源释放逻辑。

## 与现有 technique/case 卡关联

暂无直接关联。

## 授权边界与不复现说明

仅基于公开披露信息进行学习验证，禁止在未授权环境中复现。

## Evidence / 核查元数据

- 主要来源: https://hackerone.com/reports/3320669
- 验证状态: HackerOne API确认已披露报告

<!-- REPORT_INTEL_END -->
