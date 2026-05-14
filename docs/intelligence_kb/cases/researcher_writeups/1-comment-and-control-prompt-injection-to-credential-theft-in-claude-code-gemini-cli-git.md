---
type: case
vuln_class: prompt_injection_tool_calling_data_leakage
source_url: https://oddguan.com/blog/comment-and-control-prompt-injection-credential-theft-claude-code-gemini-cli-github-copilot/
source_author: Aonan Guan (w/ JHU)
source_date: 2026-04-15
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - AI coding review agents SaaS (Anthropic
  - Google
  - GitHub)
---

# Comment and Control: Prompt Injection to Credential Theft in Claude Code, Gemini CLI, GitHub Copilot Agent

## 链接

https://oddguan.com/blog/comment-and-control-prompt-injection-credential-theft-claude-code-gemini-cli-github-copilot/

## 漏洞类型

prompt_injection_tool_calling_data_leakage

## 目标业务场景

AI coding review agents SaaS (Anthropic/Google/GitHub)

## 关键利用链摘要

Malicious": - /url: https://oddguan.com/blog/comment-and-control-prompt-injection-credential-theft-claude-code-gemini-cli-github-copilot/§prompt_injection_tool_calling_data_leakage§Malicious - text: "PR title/issue comment (HTML hidden in Copilot) triggers AI agent Bash tool to exfil env vars via ps auxeww | base64 commit or direct comment post

## 可迁移技法

Steals CI/CD secrets (GITHUB_TOKEN, API keys) in GitHub Actions without external infra; bounties paid ($100/$1337/$500); proves systemic SDLC agent risk in authorized repos

## 为什么值得收藏

- 该案例可作为 `prompt_injection_tool_calling_data_leakage` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
