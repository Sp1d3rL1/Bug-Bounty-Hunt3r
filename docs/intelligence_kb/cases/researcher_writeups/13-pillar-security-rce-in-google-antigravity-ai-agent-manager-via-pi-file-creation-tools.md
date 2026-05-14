---
type: case
vuln_class: prompt_injection_tool_calling
source_url: https://oddguan.com/blog/
source_author: Pillar Security researchers
source_date: 2026-04
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - Google Antigravity AI agent SaaS
---

# Pillar Security RCE in Google Antigravity AI Agent Manager via PI + File Creation Tools

## 链接

https://oddguan.com/blog/

## 漏洞类型

prompt_injection_tool_calling

## 目标业务场景

Google Antigravity AI agent SaaS

## 关键利用链摘要

PI bypasses sandbox; file-creation tools execute arbitrary commands

## 可迁移技法

Bypassed highest security settings in authorized Google VRP; tool chaining abuse

## 为什么值得收藏

- 该案例可作为 `prompt_injection_tool_calling` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
