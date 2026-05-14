---
type: case
vuln_class: CI/CD Leak
source_url: https://infosecwriteups.com/bug-bounty-recon-tokens-pii-and-ci-cd-metadata-leaked-via-javascript-76e3c2594957
source_author: Medusa
source_date: 2025-07-19
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - Web apps with CI
  - CD pipelines
---

# CI/CD Metadata & Tokens Leaked via JS Files

## 链接

https://infosecwriteups.com/bug-bounty-recon-tokens-pii-and-ci-cd-metadata-leaked-via-javascript-76e3c2594957

## 漏洞类型

CI/CD Leak

## 目标业务场景

Web apps with CI/CD pipelines

## 关键利用链摘要

Scan packed JS for embedded pipeline metadata/artifact links (Docker/NPM/Maven)

## 可迁移技法

Reveals internal build processes for targeted supply-chain attacks in public BB programs

## 为什么值得收藏

- 该案例可作为 `CI/CD Leak` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/cicd_github_actions.md -->

<!-- backlink: docs/checklists/recon_methodology.md -->
