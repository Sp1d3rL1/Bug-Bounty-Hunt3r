<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "CSPT Resources"
vuln_class: "CSPT"
source_url: "https://blog.doyensec.com/2025/03/27/cspt-resources.html"
source_author: "Maxence Schmitt (Doyensec)"
source_date: "2025-03-27"
confidence: "high"
risk_level: "low"
freshness: "2026-05"
target_types:
  - "Web/API/SaaS client-side"
---

# CSPT Resources

## 核心思路
Curated list of CSPT blogs, reports, tools, and challenges for bug hunters.

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
Web/API/SaaS client-side

## 为什么有效
围绕 CSPT 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

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
- https://blog.doyensec.com/2025/03/27/cspt-resources.html
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## CSPT Resources

Curated list of CSPT blogs, reports, tools, and challenges (2025 update).

Key links from source:
- Maxence Schmitt: Exploiting Client-Side Path Traversal to Perform Cross-Site Request Forgery - Introducing CSPT2CSRF
- Maxence Schmitt: CSPT & File Upload Bypasses
- Dafydd Stuttard: PortSwigger - On-Site Request Forgery
- Renwa: Client-Side Path Traversal (CSPT) Bug Bounty Reports and Techniques
- Kapytein: From an Innocent Client-Side Path Traversal to Account Takeover
- Mr. Medi: Practical Client-Side Path Traversal Attacks
- Alvaro Balada: The Power of Client-Side Path Traversal: How I Found and Escalated 2 Bugs
- Michelin CERT: Grafana CVE-2023-5123 Write-Up
- Netragard: Saving CSRF: Client-Side Path Traversal to the Rescue
- Sam Curry: CSPT2CSRF and CSPT->Open Redirect

All links point to real 2024-2025 bug bounty CSPT reports and automation for authorized client-side hunting in Web/GraphQL apps.

Source: https://blog.doyensec.com/2025/03/27/cspt-resources.html

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: Snippet extracted and verified against source URL on 2026-05-09. Matches supplied metadata exactly; no conflicts.
- source_urls:
  - https://blog.doyensec.com/2025/03/27/cspt-resources.html
- evidence:
  - claim: Curated CSPT resources list including specific reports and authors from 2024-2025
    source: https://blog.doyensec.com/2025/03/27/cspt-resources.html
    verification: Direct snippet match: 'Maxence Schmitt: Exploiting Client-Side Path Traversal...' etc.

<!-- GROK_API_EXPANSION_END -->
