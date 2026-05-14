<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "The Depths of BOLA and IDOR"
vuln_class: "BOLA/IDOR GraphQL"
source_url: "https://www.eresussec.com/en/blog/api-bola-idor-expert-guide"
source_author: "Eresus Security"
source_date: "2026-04-06"
confidence: "high"
risk_level: "high"
freshness: "2026-04"
target_types:
  - "REST + GraphQL APIs / microservices"
---

# The Depths of BOLA and IDOR

## 核心思路
In GraphQL, bypass resolver auth by querying nested nodes without per-object ownership checks. 2026 expert guide with concrete GraphQL query examples for BOLA in REST/GraphQL APIs; lab-first validation focus.

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
REST + GraphQL APIs / microservices

## 为什么有效
围绕 BOLA/IDOR GraphQL 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

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
- https://www.eresussec.com/en/blog/api-bola-idor-expert-guide
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核心内容

BOLA (Broken Object Level Authorization) 是现代微服务架构中最常见的致命漏洞，长期位居 OWASP API Top 10 首位。开发者通常仅验证系统级认证（Authentication），但未在对象级别执行授权检查（Authorization）。

示例不安全实现（REST）：
```js
app.get('/api/v2/accounts/:id', async (req, res) => {
  // 仅检查系统认证，无对象授权
  const account = await Database.getAccountById(req.params.id);
  return res.json(account);
});
```

此漏洞同样适用于 GraphQL resolver 层。来源：https://www.eresussec.com/en/blog/api-bola-idor-expert-guide

## 授权边界

- 仅限授权范围内的 API 测试
- 使用测试账号与合成数据
- Lab-first 验证

## 报告 impact 角度

- 高危 PII/数据泄露
- 符合 OWASP API Top 10 BOLA 风险

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: Tavily 成功提取页面片段，内容与 source_url 一致，可用于完整资源卡片。
- source_urls:
  - https://www.eresussec.com/en/blog/api-bola-idor-expert-guide
- evidence:
  - claim: BOLA 是 OWASP API Top 10 长期首位漏洞，因缺少对象级授权检查导致
    source: https://www.eresussec.com/en/blog/api-bola-idor-expert-guide
    verification: Tavily 片段直接引用原文
  - claim: 不安全 REST 示例代码展示仅验证 authentication 未验证 object ownership
    source: https://www.eresussec.com/en/blog/api-bola-idor-expert-guide
    verification: Tavily 提取的代码片段与描述匹配

<!-- GROK_API_EXPANSION_END -->
