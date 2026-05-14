---
type: case
vuln_class: CSRF
source_url: https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-161-ai-workflows-csrf-despite-xfo-and-dtmf-exfil
source_author: Critical Thinking Podcast hunter
source_date: 2026-02
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - AI SaaS
---

# CSRF Despite X-Frame-Options in AI Workflow Endpoint

## 链接

https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-161-ai-workflows-csrf-despite-xfo-and-dtmf-exfil

## 漏洞类型

CSRF

## 目标业务场景

AI SaaS

## 关键利用链摘要

Bypass": - /url: https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-161-ai-workflows-csrf-despite-xfo-and-dtmf-exfil§CSRF§Bypass - text: XFO via auxclick or modern UI quirks in AI workflows

## 可迁移技法

Classic CSRF survives modern headers in new AI/SaaS workflow features

## 为什么值得收藏

- 该案例可作为 `CSRF` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/cors_postmessage_websocket.md -->
