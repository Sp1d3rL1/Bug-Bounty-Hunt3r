<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: github_security_lab
canonical_report_url: https://securitylab.github.com/advisories/GHSL-2025-114_Chromium
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
  - https://securitylab.github.com/advisories/GHSL-2025-114_Chromium
---
# Ghsl 2025 114_Chromium

## TL;DR

Chromium V8 引擎存在类型混淆漏洞 (GHSL-2025-114)，涉及 inline cache 原型加载与 WebAssembly 对象原型。

## 来源与关联材料

- 官方报告: https://securitylab.github.com/advisories/GHSL-2025-114_Chromium
- 相关材料: https://securitylab.github.com/advisories/GHSL-2025-114_Chromium

## 业务/技术背景

Chromium V8 JavaScript 引擎的优化机制。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）

原型属性加载时的 inline cache 缓存原型持有者，通过优化处理器访问属性。

## 根因

inline cache prototype loading 错误处理 WebAssembly 对象原型。

## Impact 表达方式

可能结合 V8 heap sandbox escape 导致 Chrome renderer 远程代码执行。

## 可迁移狩猎思路

在 JS 引擎原型缓存与 WebAssembly 交互中寻找类型混淆。

## 与现有 technique/case 卡关联

V8 类型混淆与原型污染模式。

## 授权边界与不复现说明

仅限已公开披露的研究，授权测试应在自有 Chromium 构建中进行。

## Evidence / 核查元数据

- 索赔: GitHub Security Lab advisory is publicly listed
  源 URL: https://securitylab.github.com/advisories/GHSL-2025-114_Chromium/
  验证备注: Discovered from GitHub Security Lab advisories index.
- 主要来源片段验证: https://securitylab.github.com/advisories/GHSL-2025-114_Chromium (raw_content_hash: 1e37c0afb077ad4b)

<!-- REPORT_INTEL_END -->
