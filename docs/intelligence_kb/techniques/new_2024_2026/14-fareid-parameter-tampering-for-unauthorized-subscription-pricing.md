---
type: technique
category: new_method
vuln_class: checkout pricing ID tamper
source_url: https://medium.com
source_author: Mahmoud Magdy
source_date: 2025
collected_at: 2026-05-04
freshness: 2025
confidence: high
risk_level: medium
target_types:
  - SaaS subscription checkout
raw_file: data/grok_research/raw/2026-05-04/topic_06_payment_subscription_billing.md
---

# Fareid Parameter Tampering for Unauthorized Subscription Pricing

## 核心思路

change fareid param in create_payment_info to free/unauthorized bundle ID bypassing price logic

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `checkout pricing ID tamper` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

obtains premium bundles at wrong (free) rate in live checkout BB

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- SaaS subscription checkout

## 为什么有效

obtains premium bundles at wrong (free) rate in live checkout BB

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

围绕 `checkout pricing ID tamper` 说明可导致的未授权数据访问、权限提升、业务绕过、财务影响或合规风险。

## 相关案例链接

- https://medium.com
