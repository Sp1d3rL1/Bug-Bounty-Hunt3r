<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "🚀 CSPT (Client-Side Path Traversal)"
vuln_class: "CSPT"
source_url: "https://medium.com/@shadyfarouk1986/cspt-client-side-path-traversal-d7d446a88da1"
source_author: "Shady Farouk"
source_date: "2026-04"
confidence: "low"
risk_level: "low"
freshness: "2026-05"
target_types:
  - "Web apps with client-side routing"
---

# 🚀 CSPT (Client-Side Path Traversal)

## 核心思路
Unsanitized JS URL construction from user input allows browser-side path traversal to unintended endpoints.

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
Web apps with client-side routing

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
- https://medium.com/@shadyfarouk1986/cspt-client-side-path-traversal-d7d446a88da1
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核查结果

Tavily fetch failed for source URL (tavily_extract_failed: Failed to fetch url). Content limited to supplied metadata only; no page content available for verification. Cannot expand to full technique details per evidence policy.

- Source URL: https://medium.com/@shadyfarouk1986/cspt-client-side-path-traversal-d7d446a88da1
- Author/Date: Shady Farouk / 2026-04

## 核心思路
(Insufficient verified content)

## 前置条件
(Insufficient verified content)

## 完整技法细节
(Insufficient verified content)

## 适用目标画像
Web apps with client-side routing

## 为什么有效
(Insufficient verified content)

## 手工验证流程（授权 / Lab only）
(Insufficient verified content)

## 可自动化部分
(Insufficient verified content)

## 误报/失败条件
(Insufficient verified content)

## 授权边界
Authorized scope, Lab only, synthetic data, test accounts

## 报告 impact 角度
2026 Medium post with practical bug bounty examples for safe lab validation of CSPT in client-side code.

## 相关案例链接
(Insufficient verified content)

## Evidence / 核查元数据
- verification_status: `needs_review`
- verification_summary: Source page fetch failed; metadata only (one_line_trick and why_useful) used. Exact claim: 'tavily_extract_failed: Failed to fetch url' from tavily_context.
- source_urls:
  - https://medium.com/@shadyfarouk1986/cspt-client-side-path-traversal-d7d446a88da1
- evidence:
  - claim: Source fetch failed via Tavily on 2026-05-09
    source: https://medium.com/@shadyfarouk1986/cspt-client-side-path-traversal-d7d446a88da1
    verification: tavily_context.skipped_urls[0].reason = 'tavily_extract_failed'
- tavily_verification:
  - status: needs_review
  - summary: verified_urls=0 failed_urls=1 skipped_urls=0 search_candidates=0
  - checked_at: 2026-05-09T04:27:25.976046
  - mode: default
  - usage: {'credits': 1}
  - failed_urls:
    - https://medium.com/@shadyfarouk1986/cspt-client-side-path-traversal-d7d446a88da1 (tavily_extract_failed)

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->
