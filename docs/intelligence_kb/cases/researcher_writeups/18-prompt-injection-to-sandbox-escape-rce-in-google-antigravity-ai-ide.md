---
type: case
vuln_class: Injection (classic injection)
source_url: https://www.pointguardai.com/ai-security-incidents/a-crafted-search-pattern-unlocked-rce-inside-googles-antigravity-ide
source_author: Pillar Security
source_date: 2026-04
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - AI IDE SaaS
---

# Prompt Injection to Sandbox Escape RCE in Google Antigravity AI IDE

## 链接

https://www.pointguardai.com/ai-security-incidents/a-crafted-search-pattern-unlocked-rce-inside-googles-antigravity-ide

## 漏洞类型

Injection (classic injection)

## 目标业务场景

AI IDE SaaS

## 关键利用链摘要

find_by_name tool injection bypasses Secure Mode to RCE

## 可迁移技法

Old injection class enables RCE in new AI agent IDE SaaS tools

## 为什么值得收藏

- 该案例可作为 `Injection (classic injection)` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
