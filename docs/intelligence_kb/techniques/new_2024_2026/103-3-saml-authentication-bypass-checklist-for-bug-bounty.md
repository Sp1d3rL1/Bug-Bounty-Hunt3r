<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "SAML Authentication Bypass Checklist for Bug Bounty"
vuln_class: "SAML manipulation"
source_url: "https://x.com/vuln_X/status/2042936028990968055"
source_author: "vuln_X"
source_date: "2026-04-11"
confidence: "high"
risk_level: "high"
freshness: "2026-04"
target_types:
  - "SSO/SAML"
---

# SAML Authentication Bypass Checklist for Bug Bounty

## 核心思路
SAML 绕过实用 checklist：移除 Signature、空签名值、NameID 替换、XML 注释、响应重放、InResponseTo 检查。

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
SSO/SAML

## 为什么有效
围绕 SAML manipulation 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

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
- https://x.com/vuln_X/status/2042936028990968055
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核心思路

SAML 响应操纵 checklist，用于快速发现常见认证绕过。

## 前置条件

- 存在 SAML SSO 集成
- 可拦截/修改 SAMLResponse

## 完整技法细节

- 移除 <Signature> 元素
- 将 Signature 值置空
- 将 NameID 替换为 admin/victim 邮箱
- NameID 中注入 XML 注释
- 重放旧的有效 SAMLResponse
- 检查 InResponseTo 是否被验证

## 适用目标画像

使用 SAML 的企业 SSO 应用。

## 为什么有效

许多 SAML 实现对签名、NameID 或重放缺乏严格验证。

## 手工验证流程（授权 / Lab only）

1. Burp 拦截 SAMLResponse
2. 按 checklist 逐项修改测试
3. 观察是否成功登录目标账户

## 可自动化部分

Burp 或自定义脚本自动化 SAMLResponse 修改。

## 误报/失败条件

严格签名验证或绑定 InResponseTo 的实现。

## 授权边界

仅限授权范围内的 SSO 测试账号。

## 报告 impact 角度

直接导致 ATO，可提权至 admin。

## 相关案例链接

- https://x.com/vuln_X/status/2042936028990968055

## 核查结果

X 帖子内容已通过原生抓取验证，checklist 与摘要一致。

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: X 帖子完整验证通过。
- source_urls:
  - https://x.com/vuln_X/status/2042936028990968055
- evidence:
  - claim: SAML bypass checklist 有效
    source: https://x.com/vuln_X/status/2042936028990968055
    verification: 帖子直接列出 6 项 checklist

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/oauth.md -->

<!-- backlink: docs/checklists/sso_oidc_saml.md -->
