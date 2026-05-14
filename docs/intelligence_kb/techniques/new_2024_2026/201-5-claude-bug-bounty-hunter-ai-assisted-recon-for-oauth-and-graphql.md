<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "Claude Bug Bounty Hunter - AI-assisted recon for OAuth and GraphQL"
vuln_class: "OAuth token issues, GraphQL abuse, IDOR, SSRF"
source_url: "https://github.com/shuvonsec/claude-bug-bounty"
source_author: "shuvonsec"
source_date: "2026-03-04"
confidence: "high"
risk_level: "low"
freshness: "2026"
target_types:
  - "API/OAuth/GraphQL"
---

# Claude Bug Bounty Hunter - AI-assisted recon for OAuth and GraphQL

## 核心思路
2026 open-source tool for efficient discovery of API/OAuth/GraphQL flaws in bug bounty labs.

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
API/OAuth/GraphQL

## 为什么有效
围绕 OAuth token issues, GraphQL abuse, IDOR, SSRF 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

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
- https://github.com/shuvonsec/claude-bug-bounty
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核心思路
Use Claude Code with custom prompts for automated recon, vulnerability detection across 20 classes including OAuth and GraphQL.

## 前置条件
Claude Code environment, authorized bug bounty scope, test accounts only.

## 完整技法细节
Prompts target OAuth token flows, GraphQL auth bypass/data leaks, IDOR, SSRF; tool generates reports.

## 适用目标画像
API, OAuth, GraphQL endpoints in SaaS and web apps (lab validation only).

## 为什么有效
Covers 20 vuln classes with payouts $500-$30K; GraphQL specifically $1K-$10K for auth bypass.

## 手工验证流程（授权 / Lab only）
Run prompts in terminal, validate findings in isolated lab environment with synthetic data.

## 可自动化部分
Full recon, scanning, and report generation via Claude.

## 误报/失败条件
Non-authorized targets, prompt misconfiguration.

## 授权边界
Strictly within program scope; no real user data.

## 报告 impact 角度
Link to typical payouts: GraphQL $1K-10K, OAuth $500-5K.

## 相关案例链接
https://github.com/shuvonsec/claude-bug-bounty

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: Repo title, author, description, GraphQL/OAuth classes, and payouts fully match provided details; latest commit May 2026.
- source_urls:
  - https://github.com/shuvonsec/claude-bug-bounty
- evidence:
  - claim: Repo supports OAuth and GraphQL as vuln classes with specific payouts
    source: https://github.com/shuvonsec/claude-bug-bounty
    verification: Direct browse confirmed repo content, listed classes #19 OAuth ($500-$5K), #20 GraphQL ($1K-$10K)

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/api.md -->

<!-- backlink: docs/checklists/cloud_aws_metadata_iam.md -->

<!-- backlink: docs/checklists/cloud_gcp_azure.md -->

<!-- backlink: docs/checklists/graphql.md -->

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/recon_methodology.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->
