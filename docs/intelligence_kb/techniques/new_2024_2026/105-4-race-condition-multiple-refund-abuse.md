<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "Race Condition Multiple Refund Abuse"
vuln_class: "business logic"
source_url: "https://x.com/viehgroup/status/2050840280123785585"
source_author: "VIEH Group"
source_date: "2026-05-03"
confidence: "high"
risk_level: "high"
freshness: "2026-05"
target_types:
  - "API"
---

# Race Condition Multiple Refund Abuse

## 核心思路
Parallel refund requests before status update allow multiple refunds for single order.

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
API

## 为什么有效
围绕 business logic 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

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
- https://x.com/viehgroup/status/2050840280123785585
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核心思路

并发发送退款请求，在服务器更新订单状态前完成多次处理。

## 前置条件

授权测试账户、已下单且可退款的订单、支持并发的 API 客户端（如 Burp Repeater）。

## 完整技法细节

1. 触发一次退款请求。
2. 使用并行工具同时发送多个相同退款请求。
3. 服务器在更新状态前处理全部请求，导致多次退款。

## 适用目标画像

存在退款状态更新竞态条件的 SaaS/API 支付系统。

## 为什么有效

后端缺少适当的锁或原子性检查，允许共享状态在并发操作中被多次修改。

## 手工验证流程（授权 / Lab only）

在授权 Lab 环境中使用测试订单和并发请求工具验证。

## 可自动化部分

Burp Suite Repeater Tab Groups 或自定义脚本并行发送请求。

## 误报/失败条件

服务器已实现分布式锁或幂等性检查时失败。

## 授权边界

仅限授权范围内的测试账户和沙箱/测试卡。

## 报告 impact 角度

财务损失、多次退款滥用。

## 相关案例链接

- https://x.com/viehgroup/status/2050840280123785585

## 来源

- https://x.com/viehgroup/status/2050840280123785585

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: X thread content fully extracted and matches provided metadata and one_line_trick.
- source_urls:
  - https://x.com/viehgroup/status/2050840280123785585
- evidence:
  - claim: Send parallel refund requests before status update to receive multiple refunds
    source: https://x.com/viehgroup/status/2050840280123785585
    verification: Direct POC steps from post: Trigger refund, send multiple parallel requests, server processes all before status update.

<!-- GROK_API_EXPANSION_END -->
