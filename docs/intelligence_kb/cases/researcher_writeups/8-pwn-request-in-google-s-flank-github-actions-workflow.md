---
type: case
vuln_class: Actions Script Injection
source_url: https://adnanthekhan.com/2024/04/15/an-obscure-actions-workflow-vulnerability-in-googles-flank/
source_author: Adnan Khan
source_date: 2024-04-15
collected_at: 2026-05-05
freshness: 2024
confidence: high
target_types:
  - GitHub Actions
---

# Pwn Request in Google's Flank GitHub Actions Workflow

## 链接

https://adnanthekhan.com/2024/04/15/an-obscure-actions-workflow-vulnerability-in-googles-flank/

## 漏洞类型

Actions Script Injection

## 目标业务场景

GitHub Actions

## 关键利用链摘要

Craft branch/PR title with malicious payload on pull_request_target trigger

## 可迁移技法

Credential theft and RCE in big-tech CI/CD via authorized bounty ($7.5k)

## 为什么值得收藏

- 该案例可作为 `Actions Script Injection` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
