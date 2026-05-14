<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: hackerone
canonical_report_url: https://hackerone.com/reports/3580511
program_or_vendor: HackerOne program
reporter_or_author: unknown
disclosed_at: 2026-05-07
severity: Medium
bounty: unknown
cwe: unknown
cve: 
vuln_class: ActiveStorage Disk Service Path Traversal via Custom Blob Key Injection
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
  - https://hackerone.com/reports/3580511
---
# ActiveStorage Disk Service Path Traversal via Custom Blob Key Injection

## TL;DR

ActiveStorage Disk Service通过自定义Blob Key注入实现路径遍历。

## 来源与关联材料

- https://hackerone.com/reports/3580511

## 业务/技术背景

Rails ActiveStorage磁盘服务文件处理场景。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）

通过HackerOne公开披露报告确认Blob Key注入缺陷。

## 根因

自定义Blob Key验证不足导致路径遍历。

## Impact 表达方式

可能访问或操作任意文件路径。

## 可迁移狩猎思路

检查存储服务中的Key生成与路径拼接逻辑。

## 与现有 technique/case 卡关联

暂无直接关联。

## 授权边界与不复现说明

仅基于公开披露信息进行学习验证，禁止在未授权环境中复现。

## Evidence / 核查元数据

- 主要来源: https://hackerone.com/reports/3580511
- 验证状态: HackerOne API确认已披露报告

<!-- REPORT_INTEL_END -->
