---
type: case
vuln_class: Actions Build Artifact Exposure
source_url: https://unit42.paloaltonetworks.com/github-repo-artifacts-leak-tokens/
source_author: Yaron Avital (Unit42)
source_date: 2024-08-13
collected_at: 2026-05-05
freshness: 2024
confidence: high
target_types:
  - GitHub Actions build artifacts
---

# ArtiPACKED GitHub Actions Artifact Token Leak

## 链接

https://unit42.paloaltonetworks.com/github-repo-artifacts-leak-tokens/

## 漏洞类型

Actions Build Artifact Exposure

## 目标业务场景

GitHub Actions build artifacts

## 关键利用链摘要

Race condition: DL artifact mid-run to extract GITHUB_TOKEN from .git/config/logs

## 可迁移技法

High-impact supply-chain compromise on large OSS repos (Firebase/MS projects) via authorized BB

## 为什么值得收藏

- 该案例可作为 `Actions Build Artifact Exposure` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
