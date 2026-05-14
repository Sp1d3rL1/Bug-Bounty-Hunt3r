<!-- GROK_API_SCAFFOLD_START -->
---
type: case
title: "JWT alg=none Authentication Bypass for Full Workspace ATO"
vuln_class: "JWT signature bypass"
source_url: "https://medium.com/@belalshohaip222/my-first-bug-bounty-how-i-hijacked-an-entire-workspace-using-a-jwt-alg-none-attack-fef78ad00df8"
source_author: "BelScarabX"
source_date: "2026-04"
confidence: "high"
risk_level: "high"
freshness: "2026-04"
target_types:
  - "API/GraphQL/JWT"
---

# JWT alg=none Authentication Bypass for Full Workspace ATO

## 链接
- https://medium.com/@belalshohaip222/my-first-bug-bounty-how-i-hijacked-an-entire-workspace-using-a-jwt-alg-none-attack-fef78ad00df8

## 漏洞类型
JWT signature bypass

## 目标业务场景
API/GraphQL/JWT

## 关键利用链摘要
High/Critical ATO via JWT alg=none combined with GraphQL ID leak and unauthorized email update mutation on collaborative workspace platform.

## 可迁移技法
仅迁移到授权项目、靶场或自有环境；优先提炼前置条件、权限边界、状态机或集成点，不复现真实第三方目标。

## 为什么值得收藏
用于学习公开案例的根因、impact 表达、报告结构与授权范围内的验证思路。
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 案例概述

BelScarabX 通过 JWT `alg=none` 绕过认证，结合 GraphQL 信息泄露实现完整工作区接管。

- 目标：app.target.com 协作平台
- 影响：完全接管 Owner 账户及工作区所有数据
- 赏金：首次有效 Bug Bounty

## 漏洞链

1. JWT 算法混淆（alg=none）
2. GraphQL `PageSideBarMeQuery` 泄露用户内部 ID
3. `ProfileFormUpdateUser` 未授权修改任意用户邮箱
4. 密码重置流程接管

## 来源链接
- https://medium.com/@belalshohaip222/my-first-bug-bounty-how-i-hijacked-an-entire-workspace-using-a-jwt-alg-none-attack-fef78ad00df8

## 核查结果

来源已通过直接页面抓取完整验证，内容与提供摘要一致，无冲突。

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: Medium 文章完整抓取验证通过，技术细节、payload、影响均匹配。
- source_urls:
  - https://medium.com/@belalshohaip222/my-first-bug-bounty-how-i-hijacked-an-entire-workspace-using-a-jwt-alg-none-attack-fef78ad00df8
- evidence:
  - claim: JWT alg=none 接受导致认证绕过
    source: https://medium.com/@belalshohaip222/my-first-bug-bounty-how-i-hijacked-an-entire-workspace-using-a-jwt-alg-none-attack-fef78ad00df8
    verification: 文章明确描述修改 header 为 alg:none 后 200 OK
  - claim: GraphQL ID 泄露 + 未授权邮箱修改链式 ATO
    source: https://medium.com/@belalshohaip222/my-first-bug-bounty-how-i-hijacked-an-entire-workspace-using-a-jwt-alg-none-attack-fef78ad00df8
    verification: 完整 exploit 链及 payload 已提取

<!-- GROK_API_EXPANSION_END -->
