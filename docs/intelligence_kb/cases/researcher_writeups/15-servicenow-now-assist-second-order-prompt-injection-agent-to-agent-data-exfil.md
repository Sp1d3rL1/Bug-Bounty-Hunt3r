---
type: case
vuln_class: prompt_injection_data_leakage_tool_calling
source_url: https://www.appomni.com/
source_author: AppOmni researchers
source_date: 2025-11
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - ServiceNow Now Assist SaaS
---

# ServiceNow Now Assist Second-Order Prompt Injection Agent-to-Agent Data Exfil

## 链接

https://www.appomni.com/

## 漏洞类型

prompt_injection_data_leakage_tool_calling

## 目标业务场景

ServiceNow Now Assist SaaS

## 关键利用链摘要

PI in one agent propagates to second agent causing cross-tenant exfil

## 可迁移技法

Niche multi-agent escalation in enterprise SaaS workflow tools; authorized disclosure

## 为什么值得收藏

- 该案例可作为 `prompt_injection_data_leakage_tool_calling` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/ai_llm_prompt_injection.md -->
