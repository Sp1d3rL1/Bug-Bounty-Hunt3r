<!-- GROK_API_SCAFFOLD_START -->
---
type: case
title: "OAuth query parameter injection in Next.js withPageAuthRequired"
vuln_class: "OAuth Parameter Injection / ATO"
source_url: "https://joshua.hu/2025-bug-bounty-stories-fail"
source_author: "Joshua Rogers"
source_date: "2025-12-22"
confidence: "high"
risk_level: "medium"
freshness: "2025-12"
target_types:
  - "Web/API/SaaS OAuth"
---

# OAuth query parameter injection in Next.js withPageAuthRequired

## 链接
- https://joshua.hu/2025-bug-bounty-stories-fail

## 漏洞类型
OAuth Parameter Injection / ATO

## 目标业务场景
Web/API/SaaS OAuth

## 关键利用链摘要
returnTo parameter injection in nextjs-auth0 library allows OAuth scope/audience override; $1,500 bounty.

## 可迁移技法
仅迁移到授权项目、靶场或自有环境；优先提炼前置条件、权限边界、状态机或集成点，不复现真实第三方目标。

## 为什么值得收藏
用于学习公开案例的根因、impact 表达、报告结构与授权范围内的验证思路。
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 案例概述
Next.js App Router 中 withPageAuthRequired 的 returnTo 参数未 URL 编码，导致注入 ?/& 覆盖 Auth0 参数。

## 重现步骤（高层次）
1. 在 returnTo 中添加 ?scope=...&audience=... 注入。
2. 观察 /auth/login 转发至 Auth0 /authorize。

## 影响
可修改 scope/audience，实现 ATO 相关绕过。

## 修复状态
已通过 PR https://github.com/auth0/nextjs-auth0/pull/2413 修复。

## 来源
https://joshua.hu/2025-bug-bounty-stories-fail

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: Snippet and full extraction match provided metadata and details.
- source_urls:
  - https://joshua.hu/2025-bug-bounty-stories-fail
- evidence:
  - claim: $1,500 bounty awarded after re-open
    source: https://joshua.hu/2025-bug-bounty-stories-fail
    verification: Directly stated in extracted content.

<!-- GROK_API_EXPANSION_END -->
