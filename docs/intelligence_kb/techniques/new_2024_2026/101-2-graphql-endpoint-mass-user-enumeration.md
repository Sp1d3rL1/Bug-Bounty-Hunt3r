<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "GraphQL Endpoint Mass User Enumeration"
vuln_class: "GraphQL Information Disclosure"
source_url: "https://prateekpulastya.medium.com/how-i-found-a-graphql-endpoint-leaking-millions-5cbfd55d994e"
source_author: "Prateekpulastya"
source_date: "2026-04"
confidence: "high"
risk_level: "high"
freshness: "2026-04"
target_types:
  - "Web/API/SaaS GraphQL"
---

# GraphQL Endpoint Mass User Enumeration

## 核心思路
Unauthenticated GraphQL queries on e-commerce marketplace API leak millions of user records via pagination.

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
Web/API/SaaS GraphQL

## 为什么有效
围绕 GraphQL Information Disclosure 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

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
- https://prateekpulastya.medium.com/how-i-found-a-graphql-endpoint-leaking-millions-5cbfd55d994e
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核心思路
通过错误消息推断字段，使用 Relay 分页无认证查询用户数据。

## 前置条件
公开 /graphql 端点、无需认证、无速率限制。

## 完整技法细节
1. 发送不存在字段查询触发错误，暴露 users/user 字段。
2. 查询 { users(first: 1) { totalCount } } 获取用户总数（5700+ 万）。
3. 使用分页查询提取 id、username 等字段。

## 适用目标画像
SaaS/电商 GraphQL API（生产环境）。

## 为什么有效
GraphQL 默认允许公共查询且错误信息泄露 schema。

## 手工验证流程（授权 / Lab only）
在授权测试账户或合成数据 Lab 中重现上述查询。

## 可自动化部分
使用 graphql-client 脚本批量分页提取。

## 误报/失败条件
端点已禁用 introspection 或添加认证/限速。

## 授权边界
仅在授权范围内的测试端点执行。

## 报告 impact 角度
大量 PII 泄露，高严重性。

## 相关案例链接
https://prateekpulastya.medium.com/how-i-found-a-graphql-endpoint-leaking-millions-5cbfd55d994e

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: Content fully verified from source; matches provided metadata.
- source_urls:
  - https://prateekpulastya.medium.com/how-i-found-a-graphql-endpoint-leaking-millions-5cbfd55d994e
- evidence:
  - claim: Unauthenticated users query returns 57M+ records
    source: https://prateekpulastya.medium.com/how-i-found-a-graphql-endpoint-leaking-millions-5cbfd55d994e
    verification: Directly extracted from article with query examples and responses.

<!-- GROK_API_EXPANSION_END -->
