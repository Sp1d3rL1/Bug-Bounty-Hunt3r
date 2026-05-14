---
type: case
vuln_class: prompt_injection_data_leakage
source_url: https://www.promptarmor.com/resources/data-exfiltration-from-slack-ai-via-indirect-prompt-injection
source_author: PromptArmor
source_date: 2025-08
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Slack AI SaaS
---

# Slack AI Indirect Prompt Injection Data Exfil from Private Channels

## 链接

https://www.promptarmor.com/resources/data-exfiltration-from-slack-ai-via-indirect-prompt-injection

## 漏洞类型

prompt_injection_data_leakage

## 目标业务场景

Slack AI SaaS

## 关键利用链摘要

Malicious": - /url: https://www.promptarmor.com/resources/data-exfiltration-from-slack-ai-via-indirect-prompt-injection§prompt_injection_data_leakage§Malicious - text: prompt in public channel ingested into context; victim query triggers markdown link exfil of private data

## 可迁移技法

Shows cross-channel RAG poisoning in enterprise SaaS chat AI; authorized disclosure

## 为什么值得收藏

- 该案例可作为 `prompt_injection_data_leakage` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
