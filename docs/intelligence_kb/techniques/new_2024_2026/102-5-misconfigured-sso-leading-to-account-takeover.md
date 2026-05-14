<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "Misconfigured SSO Leading to Account Takeover"
vuln_class: "SSO session/token exchange flaw"
source_url: "https://infosecwriteups.com/easy-150-misconfigured-sso-led-to-account-takeover-4e2b83b72395"
source_author: "tinopreter"
source_date: "2025-03-13"
confidence: "high"
risk_level: "medium"
freshness: "2025-03"
target_types:
  - "Web/SSO"
---

# Misconfigured SSO Leading to Account Takeover

## 核心思路
SSO 会话令牌在 OTP 验证前即授予论坛访问权限，导致账户接管。

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
Web/SSO

## 为什么有效
围绕 SSO session/token exchange flaw 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

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
- https://infosecwriteups.com/easy-150-misconfigured-sso-led-to-account-takeover-4e2b83b72395
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核心思路
密码登录初始会话令牌在 SSO 流程中交换为最终令牌时存在缺陷，可拦截或重放。

## 前置条件
应用存在主应用与论坛等子应用 SSO 集成，初始令牌未强制完成 OTP。

## 完整技法细节
1. 主应用密码登录至 OTP 页面。
2. 新标签打开论坛域名，即获完全认证。
3. 在论坛添加次要邮箱，导出含 API token 的 CSV。

## 适用目标画像
Web/SSO 应用，存在多域名会话共享。

## 为什么有效
SSO 会话传播未正确等待最终令牌交换。

## 手工验证流程（授权 / Lab only）
使用测试账户在授权范围内验证会话传播。

## 可自动化部分
检测 SSO 令牌交换端点。

## 误报/失败条件
应用强制所有子应用完成完整 OTP。

## 授权边界
仅限授权程序内测试账户。

## 报告 impact 角度
$150 赏金，SSO vs 密码登录令牌处理缺陷。

## 相关案例链接
- https://infosecwriteups.com/easy-150-misconfigured-sso-led-to-account-takeover-4e2b83b72395

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: 通过 browse_page 直接获取完整文章内容，确认 $150 赏金、核心技巧和利用步骤。
- source_urls:
  - https://infosecwriteups.com/easy-150-misconfigured-sso-led-to-account-takeover-4e2b83b72395
- evidence:
  - claim: 作者 tinopreter，$150 赏金，SSO 会话令牌在 OTP 前授予论坛访问
    source: https://infosecwriteups.com/easy-150-misconfigured-sso-led-to-account-takeover-4e2b83b72395
    verification: browse_page 提取直接确认

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->

<!-- backlink: docs/checklists/subdomain_takeover.md -->
