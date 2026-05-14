---
type: case
vuln_class: prompt_injection
source_url: https://hackerone.com/reports/2372363
source_author: hazemel/hacktus (rez0)
source_date: 2024-02-13 (disclosed 2024-05-13)
collected_at: 2026-05-05
freshness: 2024
confidence: high
target_types:
  - HackerOne Hai AI SaaS triage tool
---

# Invisible Prompt Injection via Unicode Tag Characters in HackerOne Hai AI Assistant

## 链接

https://hackerone.com/reports/2372363

## 漏洞类型

prompt_injection

## 目标业务场景

HackerOne Hai AI SaaS triage tool

## 关键利用链摘要

Unicode": - /url: https://hackerone.com/reports/2372363§prompt_injection§Unicode - text: tags (U+E0000-E007F range) hide instructions in triage prompts suggesting high severity/bounty amounts

## 可迁移技法

Stealth context poisoning in bug bounty AI triage tools; LLM decodes hidden text humans miss; valid medium severity in authorized HackerOne beta

## 为什么值得收藏

- 该案例可作为 `prompt_injection` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/ai_llm_prompt_injection.md -->
