<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: github_security_lab
canonical_report_url: https://securitylab.github.com/advisories/GHSL-2025-129_woocommerce
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
  - https://securitylab.github.com/advisories/GHSL-2025-129_woocommerce
---
# Ghsl 2025 129_Woocommerce

## TL;DR

WooCommerce 10.4.2 中登录客户可通过 REST API 查看任意 guest 订单详情 (GHSL-2025-129)。

## 来源与关联材料

- 官方报告: https://securitylab.github.com/advisories/GHSL-2025-129_woocommerce
- 相关材料: https://securitylab.github.com/advisories/GHSL-2025-129_woocommerce

## 业务/技术背景

WooCommerce Store API 与订单权限模型。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）

登录用户可传递 is_authorized() 检查绕过 guest 订单限制。

## 根因

current_user_can(pay_for_order, $order_id) 对无关联用户的订单返回 true。

## Impact 表达方式

guest 订单敏感信息泄露。

## 可迁移狩猎思路

检查 REST API 权限检查中 guest vs logged-in 订单的 capability 逻辑。

## 与现有 technique/case 卡关联

权限绕过与信息泄露模式。

## 授权边界与不复现说明

仅限已公开披露的研究，授权测试应在自有 WooCommerce 站点进行。

## Evidence / 核查元数据

- 索赔: GitHub Security Lab advisory is publicly listed
  源 URL: https://securitylab.github.com/advisories/GHSL-2025-129_woocommerce/
  验证备注: Discovered from GitHub Security Lab advisories index.
- 主要来源片段验证: https://securitylab.github.com/advisories/GHSL-2025-129_woocommerce (raw_content_hash: 20db969c32e70866)

<!-- REPORT_INTEL_END -->
