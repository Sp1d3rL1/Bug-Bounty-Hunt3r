---
id: clk-payment-business-logic
title: 支付 / 业务逻辑 Checklist
owasp_anchor: [API6:2023, WSTG-BUSL]
cwe: [CWE-840, CWE-841, CWE-362, CWE-639]
severity_typical: P1-P3
playbook: playbooks/payment.yaml
last_updated: 2026-05-15
sources:
  - docs/intelligence_kb/cases/public_reports/11-business-logic-bypass-allows-setting-read-access-role-without-pro-plan-subscription.md
  - docs/intelligence_kb/cases/public_reports/2-business-logic-vulnerability-in-dells-payment-api.md
  - docs/intelligence_kb/cases/public_reports/24-graphql-idor-in-shopify-staff-access-cross-shop-billing-data.md
  - docs/intelligence_kb/cases/public_reports/25-business-logic-race-condition-idor-in-fintech-recharge-history-api.md
  - docs/intelligence_kb/cases/researcher_writeups/1-artipacked-github-actions-artifact-token-leak.md
  - docs/intelligence_kb/cases/researcher_writeups/1-subscription-bypass-leading-to-full-access-to-paid-features.md
  - docs/intelligence_kb/cases/researcher_writeups/10-business-logic-error-bypassing-payment-with-test-cards-in-production.md
  - docs/intelligence_kb/cases/researcher_writeups/105-1-business-logic-vulnerability-in-subscription-checkout.md
  - docs/intelligence_kb/cases/researcher_writeups/105-2-business-logic-error-bypassing-payment-with-test-cards.md
  - docs/intelligence_kb/cases/researcher_writeups/105-3-business-logic-bypass-allows-setting-read-access-role-without-pro-plan-subscript.md
  - docs/intelligence_kb/cases/researcher_writeups/12-race-condition-broken-access-control-leading-to-super-admin-creation.md
  - docs/intelligence_kb/cases/researcher_writeups/15-reusing-one-time-coupon-via-order-state-confusion.md
  - docs/intelligence_kb/cases/researcher_writeups/18-price-manipulation-in-public-bug-bounty-program-subscription-plans.md
  - docs/intelligence_kb/cases/researcher_writeups/22-business-logic-flaw-in-subscription-paywall-for-profile-access.md
  - docs/intelligence_kb/cases/researcher_writeups/3-high-impact-business-logic-bug-in-e-commerce-checkout.md
  - docs/intelligence_kb/cases/researcher_writeups/4-how-i-bypassed-premium-subscription-escalated-privileges-using-a-0-vcc.md
  - docs/intelligence_kb/cases/researcher_writeups/5-how-insecure-apis-allow-hackers-to-break-subscription-logic-and-unlock-premium-feature.md
  - docs/intelligence_kb/cases/researcher_writeups/6-reusing-a-one-time-coupon-code-multiple-times.md
  - docs/intelligence_kb/cases/researcher_writeups/7-subscription-paywall-bypass-leading-to-talent-profile-access-and-pii-disclosure.md
  - docs/intelligence_kb/cases/researcher_writeups/8-business-logic-flaw-ability-to-bypass-user-limit-and-add-multiple-members-without-paym.md
  - docs/intelligence_kb/cases/researcher_writeups/9-next-js-cache-poisoning-race-condition-cve-2025-32421.md
  - docs/intelligence_kb/cases/researcher_writeups/9-this-is-how-i-hacked-a-payment-flow-using-business-logic-abuse.md
  - docs/intelligence_kb/review_queue/16-payment-bypass-bug-lab-for-hands-on-techniques.md
  - docs/intelligence_kb/review_queue/24-how-i-discovered-price-manipulation-in-public-bb-program-subscription-focus.md
  - docs/intelligence_kb/review_queue/resource-16-payment-bypass-bug-lab-for-hands-on-techniques.md
  - docs/intelligence_kb/review_queue/resource-24-how-i-discovered-price-manipulation-in-public-bb-program-subscription-focus.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-12-race-condition-broken-access-control-leading-to-super-admin-creation.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-25-business-logic-race-condition-idor-in-fintech-recharge-history-api.md
  - docs/intelligence_kb/techniques/new_2024_2026/101-4-race-conditions-and-business-logic-in-microservices-for-2026-bug-bounties.md
  - docs/intelligence_kb/techniques/new_2024_2026/105-4-race-condition-multiple-refund-abuse.md
  - docs/intelligence_kb/techniques/new_2024_2026/12-webhook-replay-attack-for-multiple-upgrades-without-payment.md
  - docs/intelligence_kb/techniques/new_2024_2026/14-fareid-parameter-tampering-for-unauthorized-subscription-pricing.md
  - docs/intelligence_kb/techniques/new_2024_2026/16-websocket-subscription-introspection-bypass-in-parse-server.md
  - docs/intelligence_kb/techniques/new_2024_2026/17-refund-race-condition-for-multiple-refunds.md
  - docs/intelligence_kb/techniques/new_2024_2026/19-invoice-idor-for-unauthorized-access-refund-manipulation.md
  - docs/intelligence_kb/techniques/new_2024_2026/20-coupon-stacking-via-parallel-api-calls.md
  - docs/intelligence_kb/techniques/new_2024_2026/21-webhook-signature-missing-leading-to-spoofed-payment-success.md
  - docs/intelligence_kb/techniques/new_2024_2026/23-negative-cart-total-for-wallet-credit-exploit.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-1-artipacked-github-actions-artifact-token-leak.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-18-price-manipulation-in-public-bug-bounty-program-subscription-plans.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-2-business-logic-vulnerability-in-dells-payment-api.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-24-graphql-idor-in-shopify-staff-access-cross-shop-billing-data.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-3-high-impact-business-logic-bug-in-e-commerce-checkout.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-6-reusing-a-one-time-coupon-code-multiple-times.md
  - docs/intelligence_kb/techniques/niche_tricks/105-5-refunds-one-of-the-most-underrated-engineering-problems.md
  - docs/intelligence_kb/techniques/niche_tricks/14-fareid-parameter-tampering-for-unauthorized-subscription-pricing.md
  - docs/intelligence_kb/techniques/niche_tricks/16-websocket-subscription-introspection-bypass-in-parse-server.md
  - docs/intelligence_kb/techniques/niche_tricks/20-coupon-stacking-via-parallel-api-calls.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-1-subscription-bypass-leading-to-full-access-to-paid-features.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-10-business-logic-error-bypassing-payment-with-test-cards-in-production.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-11-business-logic-bypass-allows-setting-read-access-role-without-pro-plan-s.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-15-reusing-one-time-coupon-via-order-state-confusion.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-22-business-logic-flaw-in-subscription-paywall-for-profile-access.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-4-how-i-bypassed-premium-subscription-escalated-privileges-using-a-0-vcc.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-5-how-insecure-apis-allow-hackers-to-break-subscription-logic-and-unlock-pr.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-7-subscription-paywall-bypass-leading-to-talent-profile-access-and-pii-disc.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-8-business-logic-flaw-ability-to-bypass-user-limit-and-add-multiple-members.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-9-next-js-cache-poisoning-race-condition-cve-2025-32421.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-9-this-is-how-i-hacked-a-payment-flow-using-business-logic-abuse.md
maturity: stable
---

# 支付 / 业务逻辑 Checklist

> 只在项目明确允许支付测试时使用。优先 sandbox、test card、0 元订单、小额规则。不要制造真实损失。

## Pricing / Coupon

- [ ] 客户端价格是否被服务端信任
- [ ] 负数/小数/精度/币种转换
- [ ] coupon 是否可重复叠加
- [ ] plan downgrade/upgrade prorate 计算
- [ ] tax/shipping/fee 是否可绕过

## Subscription State Machine

- [ ] trial → paid → canceled → resumed
- [ ] failed payment 后权限是否仍保留
- [ ] downgrade 后高级资源是否仍可访问
- [ ] seat count 与成员数量不一致
- [ ] org owner/merchant 权限变化是否影响 billing

## Refund / Cancel / Race

- [ ] cancel 与 refund 并发
- [ ] webhook replay 后重复发货/加余额
- [ ] payment success 与 order create 顺序错乱
- [ ] invoice paid 状态可否被低权限动作触发

## Invoice / Receipt / Merchant Boundary

- [ ] invoice_id / receipt_id IDOR
- [ ] merchant_id / org_id 参数篡改
- [ ] download/export endpoint 权限弱
- [ ] webhook secret / signing key 泄露或复用

## Evidence Rules

- 使用自己的测试账号。
- 不读取第三方真实账单内容。
- 金额、订单、交易 ID 截图打码。
- impact 用“可导致未授权折扣/越权访问账单/重复发放权益”等表达。
