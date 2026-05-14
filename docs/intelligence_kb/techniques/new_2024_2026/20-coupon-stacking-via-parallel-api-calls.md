---
type: technique
category: new_method
vuln_class: discount endpoint race
source_url: https://hackerone.com/reports/1849626
source_author: Stripe unlimited discount example (H1 #1849626 style)
source_date: 2024-2025
collected_at: 2026-05-04
freshness: 2025
confidence: high
risk_level: high
target_types:
  - e-commerce discount system
raw_file: data/grok_research/raw/2026-05-04/topic_06_payment_subscription_billing.md
---

# Coupon Stacking via Parallel API Calls

## 核心思路

parallel POSTs to /apply-coupon bypassing single-use check

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `discount endpoint race` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

stacks discounts to near-zero order total in BB reports

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- e-commerce discount system

## 为什么有效

stacks discounts to near-zero order total in BB reports

## 手工验证流程（授权 / Lab only）

1. 确认项目 rules of engagement 明确允许该类别测试。
2. 搭建双账号或 sandbox 测试数据，避免触达真实用户数据。
3. 复现来源中的业务前提，只记录最小必要证据。
4. 证明 server-side impact；不要依赖客户端表现。
5. 截图/保存请求响应时打码 token、cookie、PII、支付信息。

## 可自动化部分

- 资产/endpoint 发现、参数枚举、schema 对比、变更 diff 可自动化。
- 权限、支付、状态机、业务影响必须手工确认。

## 误报/失败条件

- 目标不存在相同业务前提。
- 防护在服务端强校验。
- 只影响自有账号且无跨权限/跨租户/财务/数据影响。

## 授权边界

仅用于授权 Bug Bounty、靶场、自有环境。不得用于越界扫描、爆破、DoS、真实支付损害、非授权读取第三方数据。

## 报告 impact 角度

围绕 `discount endpoint race` 说明可导致的未授权数据访问、权限提升、业务绕过、财务影响或合规风险。

## 相关案例链接

- https://hackerone.com/reports/1849626
