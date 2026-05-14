# 全球项目筛选标准

## 优先选

- SaaS 多租户
- Fintech / billing / subscription
- API-first 产品
- Developer platform
- AI SaaS with integrations
- E-commerce / travel / logistics

## 打分表

| 维度 | 0 分 | 1 分 | 2 分 |
|---|---|---|---|
| Triage 活跃 | 30 天无响应 | 偶尔响应 | 30 天内持续响应 |
| Scope 质量 | 很窄 | 一般 | wildcard/API/mobile/sandbox |
| 奖励 | 低 | 中 | 高危奖金值得投入 |
| 业务复杂度 | 静态站 | 普通 CRUD | 多租户/支付/集成 |
| 自动化规则 | 禁止 | 模糊 | 明确允许合理自动化 |
| 历史报告 | 不公开 | 少量 | 接受业务逻辑/高危报告 |

总分 8+ 才进入 1 周深测。

## 避免

- 低奖金大流量项目。
- 禁止自动化但资产巨大。
- 只收 P1/P2 且规则模糊。
- 明确不收业务逻辑或支付测试。
- Scope 中大量第三方 SaaS，容易误伤。
