<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "IDOR Hunting Tips"
vuln_class: "BOLA/IDOR"
source_url: "https://x.com/lex_is1/status/2007083265497379153"
source_author: "Omar Abdelsalam (@lex_is1)"
source_date: "2026-01-02"
confidence: "low"
risk_level: "high"
freshness: "2026-01"
target_types:
  - "REST/GraphQL APIs"
---

# IDOR Hunting Tips

## 核心思路
Swap IDs across roles/tenants; replay with different tokens; test GraphQL variables and batch endpoints.

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
REST/GraphQL APIs

## 为什么有效
围绕 BOLA/IDOR 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

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
- https://x.com/lex_is1/status/2007083265497379153
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核查结果

X 帖子内容未通过 Tavily 提取（x_native_grok_x_search_preferred），无法验证具体提示细节。

## 来源列表
- https://x.com/lex_is1/status/2007083265497379153

## 验证说明
来源为 X 状态，需额外工具或人工确认内容；当前无法提供完整技法细节。

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `needs_review`
- verification_summary: X post source skipped by Tavily; content unverified.
- source_urls:
  - https://x.com/lex_is1/status/2007083265497379153
- tavily_verification:
  - status: skipped_x_native_preferred
  - summary: verified_urls=0 failed_urls=0 skipped_urls=1 search_candidates=5
  - checked_at: 2026-05-09T04:27:00.057206
  - mode: default
  - usage: {'credits': 0}
  - skipped_urls:
    - https://x.com/lex_is1/status/2007083265497379153 (x_native_grok_x_search_preferred)

<!-- GROK_API_EXPANSION_END -->
