---
type: case
vuln_class: request smuggling (CL.TE)
source_url: https://undercodetesting.com/how-i-earned-a-00-bounty-with-clte-request-smuggling-a-step-by-step-guide-to-exploiting-http-desync-attacks-video/
source_author: UNDERCODE TESTING hunter
source_date: 2026-04
collected_at: 2026-05-05
freshness: 2026
confidence: high
target_types:
  - real authorized BB target
---

# CL.TE Request Smuggling Bounty Win via Desync (Step-by-Step)

## 链接

https://undercodetesting.com/how-i-earned-a-00-bounty-with-clte-request-smuggling-a-step-by-step-guide-to-exploiting-http-desync-attacks-video/

## 漏洞类型

request smuggling (CL.TE)

## 目标业务场景

real authorized BB target

## 关键利用链摘要

CL.TE desync in real target leading to full exploitation chain

## 可迁移技法

Earned bounty demonstrating practical desync impact; video + steps for hunters

## 为什么值得收藏

- 该案例可作为 `request smuggling (CL.TE)` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。

<!-- backlink: docs/checklists/http_request_smuggling.md -->
