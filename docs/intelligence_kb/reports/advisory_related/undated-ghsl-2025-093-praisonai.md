<!-- REPORT_INTEL_START -->
---
type: report_cluster
source_platform: github_security_lab
canonical_report_url: https://securitylab.github.com/advisories/GHSL-2025-093_PraisonAI
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
  - https://securitylab.github.com/advisories/GHSL-2025-093_PraisonAI
---
# Ghsl 2025 093_Praisonai

## TL;DR

PraisonAI 仓库的 claude-code-action GitHub Actions 可复用工作流存在代码注入漏洞 (GHSL-2025-093)。

## 来源与关联材料

- 官方报告: https://securitylab.github.com/advisories/GHSL-2025-093_PraisonAI
- 相关材料: https://securitylab.github.com/advisories/GHSL-2025-093_PraisonAI

## 业务/技术背景

PraisonAI 项目在 GitHub Actions 中使用可复用 action 处理 issue 事件。

## 漏洞链路摘要（授权 / 已披露 / 高层复盘）

攻击者通过创建或编辑 issue，注入恶意内容到 workflow 执行上下文。

## 根因

action.yml 第 145 行直接使用 `ISSUE_BODY="${{ github.event.issue.body }}"`，第 146 行类似处理 title，未进行 sanitization。

## Impact 表达方式

代码注入可能导致任意命令执行。

## 可迁移狩猎思路

检查 GitHub Actions workflow 中对 github.event.issue.* 的直接插值，尤其在 reusable actions。

## 与现有 technique/case 卡关联

GitHub Actions 上下文注入模式。

## 授权边界与不复现说明

仅限已公开披露的研究，授权测试应在自有仓库进行。

## Evidence / 核查元数据

- 索赔: GitHub Security Lab advisory is publicly listed
  源 URL: https://securitylab.github.com/advisories/GHSL-2025-093_PraisonAI/
  验证备注: Discovered from GitHub Security Lab advisories index.
- 主要来源片段验证: https://securitylab.github.com/advisories/GHSL-2025-093_PraisonAI (raw_content_hash: 44786103deda669f)

<!-- REPORT_INTEL_END -->
