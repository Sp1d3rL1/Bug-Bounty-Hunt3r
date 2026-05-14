<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: hackerone
canonical_report_url: https://hackerone.com/reports/3521434
program_or_vendor: HackerOne program
reporter_or_author: unknown
disclosed_at: 2026-05-08
severity: Low
bounty: unknown
cwe: unknown
cve: 
vuln_class: View-only guests could see deleted Collectives pages in the trashbin
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
  - https://hackerone.com/reports/3521434
---
# View-only guests could see deleted Collectives pages in the trashbin

## TL;DR

仅查看权限的访客可看到回收站中的已删除Collectives页面。

## 来源与关联材料

- https://hackerone.com/reports/3521434

## 业务/技术背景

Collectives页面与回收站访问控制场景。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）

通过HackerOne公开披露报告确认访客权限与删除页面可见性缺陷。

## 根因

回收站访问权限验证不足。

## Impact 表达方式

可能导致已删除内容意外暴露。

## 可迁移狩猎思路

检查回收站与访客权限边界。

## 与现有 technique/case 卡关联

暂无直接关联。

## 授权边界与不复现说明

仅基于公开披露信息进行学习验证，禁止在未授权环境中复现。

## Evidence / 核查元数据

- 主要来源: https://hackerone.com/reports/3521434
- 验证状态: HackerOne API确认已披露报告

<!-- REPORT_INTEL_END -->
