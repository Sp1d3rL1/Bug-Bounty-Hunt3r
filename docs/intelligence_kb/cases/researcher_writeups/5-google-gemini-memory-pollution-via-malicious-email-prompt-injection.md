---
type: case
vuln_class: prompt_injection_data_leakage
source_url: https://dev.to/behi_sec/google-paid-me-15000-for-this-prompt-injection-bug-5fn6
source_author: behi_sec
source_date: 2026-03
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Google Gemini SaaS
---

# Google Gemini Memory Pollution via Malicious Email Prompt Injection

## 链接

https://dev.to/behi_sec/google-paid-me-15000-for-this-prompt-injection-bug-5fn6

## 漏洞类型

prompt_injection_data_leakage

## 目标业务场景

Google Gemini SaaS

## 关键利用链摘要

Email-embedded": - /url: https://dev.to/behi_sec/google-paid-me-15000-for-this-prompt-injection-bug-5fn6§prompt_injection_data_leakage§Email-embedded - text: "PI pollutes Gemini long-term memory causing persistent bias/misinfo on future queries

## 可迁移技法

$15k Google VRP bounty; demonstrates persistent state manipulation in SaaS LLM agents; authorized VRP environment

## 为什么值得收藏

- 该案例可作为 `prompt_injection_data_leakage` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/ai_llm_prompt_injection.md -->
