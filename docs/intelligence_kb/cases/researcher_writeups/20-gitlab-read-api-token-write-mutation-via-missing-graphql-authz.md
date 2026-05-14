---
type: case
vuln_class: Authorization Bypass
source_url: https://gitlab.com/gitlab-org/gitlab/-/issues/462012
source_author: GitLab CVE-2025-11340 (H1 linked)
source_date: 2025-03-20
collected_at: 2026-05-05
freshness: 2025
confidence: high
target_types:
  - GitLab GraphQL API
---

# GitLab read_api Token Write Mutation via Missing GraphQL Authz

## 链接

https://gitlab.com/gitlab-org/gitlab/-/issues/462012

## 漏洞类型

Authorization Bypass

## 目标业务场景

GitLab GraphQL API

## 关键利用链摘要

read_api scoped token executes write mutations because no resolver-level scope enforcement

## 可迁移技法

Exploits missing GraphQL layer checks despite REST auth in BB/hunts

## 为什么值得收藏

- 该案例可作为 `Authorization Bypass` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/cicd_github_actions.md -->

<!-- backlink: docs/checklists/graphql.md -->
