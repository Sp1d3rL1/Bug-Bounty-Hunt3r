<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "HackerOne GraphQL and OAuth Top Reports (2025-2026)"
vuln_class: "GraphQL / OAuth"
source_url: "https://github.com/reddelexc/hackerone-reports"
source_author: "reddelexc"
source_date: "2026-04-25"
confidence: "high"
risk_level: "low"
freshness: "2026-04"
target_types:
  - "Web/API/SaaS OAuth GraphQL"
---

# HackerOne GraphQL and OAuth Top Reports (2025-2026)

## 核心思路
Curated GitHub repo with TOPGRAPHQL.md and TOPOAUTH.md for disclosed high-signal cases.

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
Web/API/SaaS OAuth GraphQL

## 为什么有效
围绕 GraphQL / OAuth 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

## 手工验证流程
在授权范围内以只读或最小影响方式验证：确认前置条件、构造合成数据/测试账号、观察授权边界或状态差异、记录证据并停止在安全影响证明处。

## 可自动化部分
可自动化收集公开入口、参数、JS/API schema、配置差异和变更信号；实际漏洞确认保留人工复核。

## 误报/失败条件
目标无对应功能、权限模型不同、补丁已生效、测试账号权限不足、来源无法复核或影响无法用最小证明表达。

## 授权边界
不访问非授权目标；不导出真实敏感数据；不进行破坏性、DoS、爆破、认证批量尝试或真实支付损害测试。

## 报告 impact 角度
说明可影响的资产、权限边界、业务状态、数据类别、可复现前置条件和最小影响证据。

## 相关案例链接
- https://github.com/reddelexc/hackerone-reports
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 资源概述
GitHub 仓库 reddelexc/hackerone-reports 提供 TOPGRAPHQL.md 与 TOPOAUTH.md 文件，列出 HackerOne 已公开的高价值报告。

## 使用方式
浏览 tops_by_bug_type 目录下的对应 Markdown 文件获取最新案例。

## 来源
https://github.com/reddelexc/hackerone-reports

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: Repo structure and file references verified from source.
- source_urls:
  - https://github.com/reddelexc/hackerone-reports
- evidence:
  - claim: TOPGRAPHQL.md and TOPOAUTH.md contain top disclosed reports
    source: https://github.com/reddelexc/hackerone-reports
    verification: Confirmed via repository structure extraction.

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/graphql.md -->

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/recon_methodology.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->
