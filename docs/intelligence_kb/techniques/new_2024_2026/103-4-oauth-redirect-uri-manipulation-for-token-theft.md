<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "OAuth Redirect URI Manipulation for Token Theft"
vuln_class: "OAuth redirect misconfig"
source_url: "https://x.com/theXSSrat/status/2036713274218012822"
source_author: "The XSS Rat"
source_date: "2026-03-25"
confidence: "high"
risk_level: "high"
freshness: "2026-03"
target_types:
  - "OAuth/API"
---

# OAuth Redirect URI Manipulation for Token Theft

## 核心思路
2026 方法论中 OAuth redirect_uri 操纵以窃取 token 的技术之一。

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
OAuth/API

## 为什么有效
围绕 OAuth redirect misconfig 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

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
- https://x.com/theXSSrat/status/2036713274218012822
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核心思路

操纵 OAuth redirect_uri 参数指向攻击者域名，捕获授权码/令牌。

## 前置条件

- OAuth 流程中 redirect_uri 可控

## 完整技法细节

- 在授权请求中替换 redirect_uri 为 attacker.com
- 捕获 code/token

## 适用目标画像

OAuth 2.0 实现的 Web/API 应用。

## 为什么有效

部分应用未严格白名单 redirect_uri。

## 手工验证流程（授权 / Lab only）

1. 分析授权 URL
2. 修改 redirect_uri 测试

## 可自动化部分

Burp Intruder 批量测试 redirect_uri。

## 误报/失败条件

严格 redirect_uri 白名单。

## 授权边界

仅授权测试账户。

## 报告 impact 角度

直接导致 token 窃取与 ATO。

## 相关案例链接

- https://x.com/theXSSrat/status/2036713274218012822

## 核查结果

X 帖子已验证，包含该技术作为 2026 方法论的一部分。

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: X 帖子验证通过。
- source_urls:
  - https://x.com/theXSSrat/status/2036713274218012822
- evidence:
  - claim: OAuth Redirect URI Manipulation 是有效技术
    source: https://x.com/theXSSrat/status/2036713274218012822
    verification: 帖子明确列出该技术

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/cors_postmessage_websocket.md -->

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/prototype_pollution_xss_chain.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->
