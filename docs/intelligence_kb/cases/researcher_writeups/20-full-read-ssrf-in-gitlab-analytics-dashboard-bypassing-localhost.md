---
type: case
vuln_class: SSRF
source_url: https://gitlab.com/gitlab-org/gitlab/-/issues/491060
source_author: GitLab researcher (disclosed)
source_date: 2026
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - SaaS dev tool
---

# Full-Read SSRF in GitLab Analytics Dashboard Bypassing Localhost

## 链接

https://gitlab.com/gitlab-org/gitlab/-/issues/491060

## 漏洞类型

SSRF

## 目标业务场景

SaaS dev tool

## 关键利用链摘要

Cube": - /url: https://gitlab.com/gitlab-org/gitlab/-/issues/491060§SSRF§Cube - text: API URL with redirect to unix socket for redis scrape

## 可迁移技法

Classic full-read SSRF in modern dev SaaS dashboards for internal data

## 为什么值得收藏

- 该案例可作为 `SSRF` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
