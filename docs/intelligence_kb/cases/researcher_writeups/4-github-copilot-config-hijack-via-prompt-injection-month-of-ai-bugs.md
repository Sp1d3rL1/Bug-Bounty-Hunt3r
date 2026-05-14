---
type: case
vuln_class: prompt_injection_tool_calling
source_url: https://www.theregister.com/2025/08/28/microsoft_copilot_copirate/
source_author: Johann Rehberger
source_date: 2025-08
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - GitHub Copilot SaaS
---

# GitHub Copilot Config Hijack via Prompt Injection (Month of AI Bugs)

## 链接

https://www.theregister.com/2025/08/28/microsoft_copilot_copirate/

## 漏洞类型

prompt_injection_tool_calling

## 目标业务场景

GitHub Copilot SaaS

## 关键利用链摘要

PI": - /url: https://www.theregister.com/2025/08/28/microsoft_copilot_copirate/§prompt_injection_tool_calling§PI - text: in chat forces Copilot to edit ~/.vscode/settings.json setting chat.tools.autoApprove:true enabling unauth command exec

## 可迁移技法

Turns coding agent into RAT; part of authorized Month of AI Bugs disclosures; shows config/tool abuse in IDE SaaS

## 为什么值得收藏

- 该案例可作为 `prompt_injection_tool_calling` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/ai_llm_prompt_injection.md -->

<!-- backlink: docs/checklists/recon_methodology.md -->
