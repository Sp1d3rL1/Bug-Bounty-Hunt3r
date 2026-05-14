<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "JWT.md Cheatsheet with 2025-2026 Real-World CVEs"
vuln_class: "JWT algorithm confusion / none / JWE handling"
source_url: "https://github.com/aw-junaid/bug-bounty/blob/main/resources/cheatsheets/JWT.md"
source_author: "aw-junaid"
source_date: "2026"
confidence: "high"
risk_level: "medium"
freshness: "2026"
target_types:
  - "API/JWT auth"
---

# JWT.md Cheatsheet with 2025-2026 Real-World CVEs

## 核心思路
JWT 备忘录包含 2025-2026 真实 CVE，包括 pac4j-jwt none 算法绕过。

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
API/JWT auth

## 为什么有效
围绕 JWT algorithm confusion / none / JWE handling 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

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
- https://github.com/aw-junaid/bug-bounty/blob/main/resources/cheatsheets/JWT.md
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 资源概述
JWT.md 备忘录列出 2025-2026 真实世界 CVE，重点 alg:none 在 JWE 中的应用和 /jwks 公钥算法混淆。

## 关键 CVE
- CVE-2026-29000 pac4j-jwt 绕过
- CVE-2026-22817 Hono
- CVE-2025-68620 Signal K

## 来源链接
- https://github.com/aw-junaid/bug-bounty/blob/main/resources/cheatsheets/JWT.md

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: TAVILY 提取确认源内容，CVE 列表和 none 算法示例匹配。
- source_urls:
  - https://github.com/aw-junaid/bug-bounty/blob/main/resources/cheatsheets/JWT.md
- evidence:
  - claim: CVE-2026-29000 pac4j-jwt 绕过，使用 JWE 内 alg:none
    source: https://github.com/aw-junaid/bug-bounty/blob/main/resources/cheatsheets/JWT.md
    verification: TAVILY 提取片段直接确认

<!-- GROK_API_EXPANSION_END -->
