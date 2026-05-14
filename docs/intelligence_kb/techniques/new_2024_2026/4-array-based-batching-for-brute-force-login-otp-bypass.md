---
type: technique
category: new_method
vuln_class: + Rate Limit Bypass
source_url: https://x.com/0xacb/status/2036003602875990153
source_author: André Baptista (@0xacb)
source_date: 2026-03-23
collected_at: 2026-05-04
freshness: 2026
confidence: high
risk_level: medium
target_types:
  - GraphQL Auth Endpoints
raw_file: data/grok_research/raw/2026-05-04/topic_04_graphql_schema.md
---

# Array-Based Batching for Brute Force Login/OTP Bypass

## 核心思路

Send array of 1000 login/OTP mutations in one HTTP request to brute passwords in single operation

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `+ Rate Limit Bypass` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

Bypasses per-HTTP rate limits allowing mass brute in authorized programs where single req limit is loose

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- GraphQL Auth Endpoints

## 为什么有效

Bypasses per-HTTP rate limits allowing mass brute in authorized programs where single req limit is loose

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

围绕 `+ Rate Limit Bypass` 说明可导致的未授权数据访问、权限提升、业务绕过、财务影响或合规风险。

## 相关案例链接

- https://x.com/0xacb/status/2036003602875990153

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://x.com/0xacb/status/2036003602875990153](https://x.com/0xacb/status/2036003602875990153)
" author: "André Baptista (@0xacb) / 2026-03-23" target_type: "GraphQL Auth Endpoints" confidence: "high" tags:
- graphql
- batching
- rate-limit-bypass
- auth date: "2026-03-23"

## 核心思路
GraphQL 端点支持在单个 HTTP 请求中发送操作数组（array of operations），服务器按操作逐个处理但速率限制通常仅基于 HTTP 请求计数，从而实现单请求内批量登录/OTP 尝试，绕过 per-request 速率限制。

## 前置条件
- 目标 GraphQL 认证端点接受数组形式的批量 mutation（常见于 Apollo/Hasura 等实现）。
- 速率限制仅针对 HTTP 请求数，而非单个操作数。
- 授权 Bug Bounty 程序或自有 GraphQL lab 环境，允许安全测试。

## 完整技法细节
构造包含多个 mutation 的 JSON 数组 payload，例如：
- 使用单个 POST 请求发送至 GraphQL 端点。
- 观察响应数组，提取每个操作的结果。
相同技巧适用于 OTP 验证或用户枚举 mutation。
，禁止任何凭证填充或生产暴力破解；推荐使用测试账号验证。

## 适用目标画像
采用 GraphQL 构建登录、OTP 或用户管理功能的 Web/移动应用，且速率限制未在操作级别实现。

## 为什么有效
多数 GraphQL 服务器将数组视为单个 HTTP 请求处理，而速率限制逻辑通常未深入检查操作数量，形成计数差异。

## 手工验证流程（授权 / Lab only）
- 在授权 BB 程序或本地 GraphQL lab 中识别登录/OTP mutation。
- 使用 Burp Repeater 或 Postman 发送单 mutation 测试速率限制阈值。
- 切换为数组 payload（100+ 操作），确认单请求内全部执行且未触发限流。
- 使用测试凭证逐步验证，不涉及真实用户数据。
- 记录请求/响应差异作为证据。

## 可自动化部分
使用 Burp Intruder、自定义 Python requests 脚本或 GraphQL 客户端批量生成操作数组并发送。

## 误报/失败条件
- 服务器明确禁止批量操作（返回错误或仅处理第一个）。
- 速率限制在 GraphQL 操作级别实现（alias 或 operationName 计数）。
- WAF/中间件拦截数组 payload。

## 授权边界
仅在授权 Bug Bounty 程序的测试账号或完全自控 lab 环境中使用。严禁生产环境任何形式的暴力尝试或凭证填充。

## 报告 impact 角度
- 绕过速率限制可放大认证暴力攻击面，影响账户安全。
- 在授权场景下可能导致 OTP/密码猜测成功，建议修复为操作级限流。

## 相关案例链接
- [https://x.com/0xacb/status/2036003602875990153](https://x.com/0xacb/status/2036003602875990153)
- GraphQL 批量处理相关安全讨论

<!-- GROK_EXPANSION_END -->
