<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "OAuth Account Fusion Pre-Takeover via Email Matching Bypass"
vuln_class: "OAuth account linking flaw"
source_url: "https://medium.com/@tinopreter/500-oauth-account-fusion-pre-takeover-attack-477484aa3813"
source_author: "tinopreter"
source_date: "2026"
confidence: "high"
risk_level: "medium"
freshness: "2026"
target_types:
  - "Web/API/SaaS OAuth"
---

# OAuth Account Fusion Pre-Takeover via Email Matching Bypass

## 核心思路
通过创建未验证密码账户并用相同邮箱 OAuth 注册实现预 ATO，绕过邮箱验证。

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
Web/API/SaaS OAuth

## 为什么有效
围绕 OAuth account linking flaw 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

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
- https://medium.com/@tinopreter/500-oauth-account-fusion-pre-takeover-attack-477484aa3813
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核心思路
创建目标邮箱的未验证密码账户，随后用相同邮箱进行 OAuth 注册，触发账户自动融合并绕过验证。

## 前置条件
应用支持邮箱/密码 + OAuth 双注册方式，且存在邮箱匹配自动融合逻辑。

## 完整技法细节
1. 用目标邮箱创建密码账户（待验证状态）。
2. 另开会话用相同邮箱 OAuth 注册。
3. OAuth 成功后刷新原待验证会话，账户自动升级为已验证。

## 适用目标画像
SaaS 应用 OAuth 登录流程，支持邮箱匹配融合。

## 为什么有效
应用信任 OAuth 提供的邮箱所有权，错误地将验证状态传播到未验证账户。

## 手工验证流程（授权 / Lab only）
使用测试账户在授权范围内测试融合逻辑。

## 可自动化部分
检测邮箱匹配融合端点。

## 误报/失败条件
应用未实现自动融合或强制邮箱验证。

## 授权边界
仅限授权程序内测试账户和 OAuth 提供商。

## 报告 impact 角度
预账户接管风险，$500 赏金。

## 相关案例链接
- https://medium.com/@tinopreter/500-oauth-account-fusion-pre-takeover-attack-477484aa3813

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: 通过 browse_page 直接获取完整文章内容，确认 $500 赏金、核心融合技巧和利用步骤。
- source_urls:
  - https://medium.com/@tinopreter/500-oauth-account-fusion-pre-takeover-attack-477484aa3813
- evidence:
  - claim: 作者 Clement Osei-Somuah (tinopreter)，$500 赏金，核心技巧：邮箱匹配自动融合绕过验证
    source: https://medium.com/@tinopreter/500-oauth-account-fusion-pre-takeover-attack-477484aa3813
    verification: browse_page 提取直接确认

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->

<!-- backlink: docs/checklists/subdomain_takeover.md -->
