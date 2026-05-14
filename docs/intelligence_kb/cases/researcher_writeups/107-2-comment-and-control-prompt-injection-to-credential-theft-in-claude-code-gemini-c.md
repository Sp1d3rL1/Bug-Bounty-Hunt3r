<!-- GROK_API_SCAFFOLD_START -->
---
type: case
title: "Comment and Control: Prompt Injection to Credential Theft in Claude Code, Gemini CLI, and GitHub Copilot Agent"
vuln_class: "Prompt Injection in AI/LLM GitHub Actions Agents"
source_url: "https://oddguan.com/blog/comment-and-control-prompt-injection-credential-theft-claude-code-gemini-cli-github-copilot/"
source_author: "Aonan Guan (with Johns Hopkins University’s Zhengyu Liu and Gavin Zhong)"
source_date: "2026-05-04"
confidence: "high"
risk_level: "high"
freshness: "2026-05"
target_types:
  - "Authorized GitHub Actions + AI/LLM SaaS integrations (Claude Code, Gemini CLI, Copilot Agent)"
---

# Comment and Control: Prompt Injection to Credential Theft in Claude Code, Gemini CLI, and GitHub Copilot Agent

## 链接
- https://oddguan.com/blog/comment-and-control-prompt-injection-credential-theft-claude-code-gemini-cli-github-copilot/

## 漏洞类型
Prompt Injection in AI/LLM GitHub Actions Agents

## 目标业务场景
Authorized GitHub Actions + AI/LLM SaaS integrations (Claude Code, Gemini CLI, Copilot Agent)

## 关键利用链摘要
Demonstrates concrete impact (API key/token exfil) from untrusted GitHub content processed by AI agents in CI/CD workflows; valid for authorized SaaS/AI integration testing.

## 可迁移技法
仅迁移到授权项目、靶场或自有环境；优先提炼前置条件、权限边界、状态机或集成点，不复现真实第三方目标。

## 为什么值得收藏
用于学习公开案例的根因、impact 表达、报告结构与授权范围内的验证思路。
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

高水平复现概述（仅限授权范围 / Lab）：

- 通过 PR 标题、Issue 正文或评论注入恶意指令。
- AI Agent 在 GitHub Actions 中执行并在响应中泄露仓库 secrets。

链接：https://oddguan.com/blog/comment-and-control-prompt-injection-credential-theft-claude-code-gemini-cli-github-copilot/

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: Tavily extracted and verified the source content; no conflicts with provided metadata.
- source_urls:
  - https://oddguan.com/blog/comment-and-control-prompt-injection-credential-theft-claude-code-gemini-cli-github-copilot/
- evidence:
  - claim: Prompt injection via GitHub comments hijacks AI agents (Claude Code, Gemini CLI, Copilot) leading to API key/token theft
    source: https://oddguan.com/blog/comment-and-control-prompt-injection-credential-theft-claude-code-gemini-cli-github-copilot/
    verification: Snippet confirms TL;DR and impact on ANTHROPIC_API_KEY and other secrets

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/ai_llm_prompt_injection.md -->

<!-- backlink: docs/checklists/cicd_github_actions.md -->

<!-- backlink: docs/checklists/recon_methodology.md -->
