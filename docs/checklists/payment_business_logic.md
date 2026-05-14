---
id: clk-payment-business-logic
title: 支付 / 业务逻辑 Checklist
owasp_anchor: [API6:2023, WSTG-BUSL]
cwe: [CWE-840, CWE-841, CWE-362, CWE-639]
severity_typical: P1-P3
playbook: playbooks/payment.yaml
last_updated: 2026-05-15
sources: []
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
