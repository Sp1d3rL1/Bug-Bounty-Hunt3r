---
type: case
vuln_class: Debug Artifact Leak
source_url: https://github.com/aw-junaid/bug-bounty/blob/main/methodologies/web%20technologies/CI-CD%20Security.md
source_author: Praetorian Researchers
source_date: 2024 (Q4)
collected_at: 2026-05-05
freshness: 2024
confidence: high
target_types:
  - GitHub Actions
---

# CodeQLEAKED Debug Artifacts Exposing GitHub Tokens

## 链接

https://github.com/aw-junaid/bug-bounty/blob/main/methodologies/web%20technologies/CI-CD%20Security.md

## 漏洞类型

Debug Artifact Leak

## 目标业务场景

GitHub Actions

## 关键利用链摘要

Inspect CodeQL workflow debug artifacts for exposed GITHUB_TOKEN

## 可迁移技法

Token abuse for repo control in authorized open-source BB programs

## 为什么值得收藏

- 该案例可作为 `Debug Artifact Leak` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
