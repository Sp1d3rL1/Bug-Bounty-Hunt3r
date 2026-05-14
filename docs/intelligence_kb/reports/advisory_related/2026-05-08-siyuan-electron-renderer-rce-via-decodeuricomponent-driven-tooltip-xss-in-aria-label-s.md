<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: github_advisory
canonical_report_url: https://github.com/advisories/GHSA-25rp-h46x-2hjm
program_or_vendor: GHSA-25rp-h46x-2hjm
reporter_or_author: GitHub Advisory Database
disclosed_at: 2026-05-08
severity: critical
bounty: unknown
cwe: CWE-79, CWE-116, CWE-1188
cve: CVE-2026-44588
vuln_class: SiYuan: Electron Renderer RCE via decodeURIComponent-driven tooltip XSS in aria-label sink (incomplete fix for CVE-2026-34585)
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
  - https://github.com/advisories/GHSA-25rp-h46x-2hjm
---
# SiYuan: Electron Renderer RCE via decodeURIComponent-driven tooltip XSS in aria-label sink (incomplete fix for CVE-2026-34585)

## TL;DR
SiYuan Electron 渲染进程中，tooltip 组件通过 decodeURIComponent 处理 aria-label 属性导致 XSS，可被构造为 RCE（不完整修复 CVE-2026-34585）。

## 来源与关联材料
- GitHub 安全公告：https://github.com/advisories/GHSA-25rp-h46x-2hjm

## 业务/技术背景
SiYuan 笔记应用使用 Electron，popover.ts 与 tooltip.ts 共同处理文档标题的 aria-label 提示。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）
1. 生产端 escapeAriaLabel 只转义 HTML 特殊字符，不处理 %XX。
2. 消费者端 decodeURIComponent 将 %3C 还原为真实 <，直接 innerHTML 注入。

## 根因
escapeAriaLabel 未对 URL 编码字符进行防御性处理，decodeURIComponent 直接作用于不受信任的属性值。

## Impact 表达方式
Electron 渲染进程 RCE，攻击者可执行任意代码。

## 可迁移狩猎思路
搜索 decodeURIComponent 直接作用于 getAttribute 结果的 innerHTML 赋值点。

## 与现有 technique/case 卡关联
与 CWE-79 XSS 及不安全反序列化模式关联。

## 授权边界与不复现说明
仅限已披露的公开 GHSA 信息，不在生产环境复现。

## Evidence / 核查元数据
- 主要来源：https://github.com/advisories/GHSA-25rp-h46x-2hjm

<!-- REPORT_INTEL_END -->
