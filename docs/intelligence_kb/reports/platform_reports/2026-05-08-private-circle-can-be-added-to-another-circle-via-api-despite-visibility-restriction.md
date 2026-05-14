<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: hackerone
canonical_report_url: https://hackerone.com/reports/3511998
program_or_vendor: HackerOne program
reporter_or_author: unknown
disclosed_at: 2026-05-08
severity: Low
bounty: 150
cwe: unknown
cve: 
vuln_class: Private circle can be added to another circle via API despite visibility restriction
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
  - https://hackerone.com/reports/3511998
---
# Private circle can be added to another circle via API despite visibility restriction

## TL;DR

私有圈子可通过API添加至其他圈子，尽管存在可见性限制。

## 来源与关联材料

- https://hackerone.com/reports/3511998

## 业务/技术背景

圈子API与可见性控制场景。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）

通过HackerOne公开披露报告确认API权限边界缺陷。

## 根因

API调用中可见性限制验证缺失。

## Impact 表达方式

可能导致私有数据意外暴露。

## 可迁移狩猎思路

检查API中的资源可见性与嵌套权限。

## 与现有 technique/case 卡关联

暂无直接关联。

## 授权边界与不复现说明

仅基于公开披露信息进行学习验证，禁止在未授权环境中复现。

## Evidence / 核查元数据

- 主要来源: https://hackerone.com/reports/3511998
- 验证状态: HackerOne API确认已披露报告

<!-- REPORT_INTEL_END -->
