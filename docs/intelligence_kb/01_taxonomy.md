# Taxonomy

## 顶层类型

- `technique`：可迁移技法、方法论、检测点、流程。
- `case`：公开案例、disclosed report、X thread、研究文章。
- `resource`：账号、社区、课程、工具、newsletter。

## 技法分类

- `new_method`：2024-2026 出现或明显流行的新方法。
- `evergreen`：旧漏洞/经典洞点在新业务场景下依然有效或有新挖法。
- `trick`：小众技巧、边角场景、hunter 分享的奇技淫巧。

## Vuln Class 标签

- Recon / Asset Discovery
- API / BOLA / IDOR
- OAuth / SSO / SAML / JWT / Magic Link
- GraphQL / API Schema
- SaaS Multi-Tenant / Access Control
- Payment / Billing / Subscription / Coupon / Refund
- Client-side / postMessage / DOM / CSPT
- Cache / Request Smuggling / HTTP2
- Cloud / CI-CD / GitHub Actions / Build Artifacts
- AI / LLM SaaS / Prompt Injection / Tool Calling
- Business Logic / Race / Workflow Abuse

## 置信度

- `high`：有明确 X/报告/博客链接，并能被二次确认。
- `medium`：来源明确但只有单一帖子或信息较简略。
- `low`：Grok 汇总或来源不完整，需要人工复核。

## 风险等级

- `low`：主要是信息收集、读配置、授权内低风险验证。
- `medium`：涉及认证、授权、业务状态变化，需要双账号/沙箱。
- `high`：涉及支付、真实用户数据、并发、破坏性边界；只允许 lab/沙箱/明确授权。
