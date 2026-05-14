---
type: technique
category: new_method
vuln_class: + Introspection Bypass
source_url: https://github.com/aw-junaid/bug-bounty/blob/main/resources/cheatsheets/GraphQL.md
source_author: aw-junaid (GitHub methodology)
source_date: 2025-06-15
collected_at: 2026-05-04
freshness: 2025
confidence: high
risk_level: medium
target_types:
  - Parse Server GraphQL
raw_file: data/grok_research/raw/2026-05-04/topic_04_graphql_schema.md
---

# WebSocket Subscription Introspection Bypass in Parse Server

## 核心思路

Connect to GraphQL WS endpoint bypassing Express middleware for unauth introspection and complex queries

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `+ Introspection Bypass` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

Bypasses auth/complexity limits via alternate transport in owned lab environments

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- Parse Server GraphQL

## 为什么有效

Bypasses auth/complexity limits via alternate transport in owned lab environments

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

围绕 `+ Introspection Bypass` 说明可导致的未授权数据访问、权限提升、业务绕过、财务影响或合规风险。

## 相关案例链接

- https://github.com/aw-junaid/bug-bounty/blob/main/resources/cheatsheets/GraphQL.md

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://github.com/aw-junaid/bug-bounty/blob/main/resources/cheatsheets/GraphQL.md](https://github.com/aw-junaid/bug-bounty/blob/main/resources/cheatsheets/GraphQL.md)
" author: "aw-junaid (GitHub methodology) / 2025-06-15" target_type: "Parse Server GraphQL" confidence: "high" tags:
- graphql
- websocket
- parse-server
- introspection-bypass
- auth-bypass date: "2025-06-15"

## 核心思路
Parse Server 的 GraphQL 订阅功能使用独立的 WebSocket 端点，该端点未经过 Express 中间件链处理，从而绕过应用层的认证检查、内省禁用机制以及查询复杂度限制，实现未授权 schema 枚举和复杂查询执行。

## 前置条件
- 目标使用 Parse Server 并启用 GraphQL API，支持订阅功能的 WebSocket 端点（典型路径为 /subscriptions 或 /graphql 的 WS 升级）。
- 实验室环境或授权 Bug Bounty 程序中已配置 GraphQL 订阅。
- HTTP 端点已启用认证、禁用公开内省或设置查询复杂度限制（用于验证绕过效果）。

## 完整技法细节
- 发现 GraphQL HTTP 端点（如 /graphql）。
- 尝试连接对应的 WebSocket 端点（例如 wss://target.com/graphql 或 /subscriptions，使用 graphql-ws 协议）。
- 发送 connection_init 消息初始化连接（可尝试空或伪造的 Authorization header）。
- 通过 WS 发送 introspection 查询（如 __schema { types { name fields { name } } }），即使 HTTP 端点已禁用内省。
- 发送任意复杂查询，绕过服务器配置的复杂度限制。 仅限授权环境或自有 Parse Server lab 实例测试；禁止在生产环境执行敏感订阅或数据操作。

## 适用目标画像
使用 Parse Server 作为后端、暴露 GraphQL API 并依赖 Express middleware 进行认证/限流/内省控制的 Web 应用或移动后端服务。

## 为什么有效
GraphQL WebSocket 订阅端点独立于主 HTTP 路由，未继承 Express middleware 的认证、复杂度检查和内省控制逻辑，形成传输层差异化绕过。

## 手工验证流程（授权 / Lab only）
- 在本地或授权测试环境中部署 Parse Server lab 实例，启用 GraphQL 和 subscriptions。
- 在 HTTP /graphql 端点配置严格认证、禁用 introspection 并设置低查询复杂度阈值。
- 使用 WebSocket 客户端（如 wscat 或浏览器 DevTools）连接 WS 端点。
- 发送 connection_init 和 introspection 查询，确认成功获取 schema。
- 发送复杂查询验证绕过效果，记录响应差异。
- 仅在 lab 内验证，不对生产目标执行。

## 可自动化部分
使用 graphql-ws 库、Burp Suite WebSocket 扩展或自定义 Python 脚本自动化 WS 连接、内省查询和响应解析。

## 误报/失败条件
- WebSocket 端点被反向代理或 WAF 阻挡升级请求。
- Parse Server 版本已修复（CVE-2026-32594 相关补丁可能移除独立订阅路径）。
- 网络层明确禁止 /subscriptions 路径的 WS 连接。

## 授权边界
严格限定在授权 Bug Bounty 程序的自有测试账号环境或完全自控的 lab 实例中。禁止任何未授权目标的 WebSocket 连接、查询发送或数据订阅操作。

## 报告 impact 角度
- 未授权 GraphQL schema 枚举可进一步发现敏感 mutation/subscription，导致信息泄露或逻辑绕过风险。
- 绕过查询复杂度限制可能放大后续攻击面（lab 验证）。
- 认证机制失效，影响整体 API 安全边界。

## 相关案例链接
- [https://github.com/aw-junaid/bug-bounty/blob/main/resources/cheatsheets/GraphQL.md](https://github.com/aw-junaid/bug-bounty/blob/main/resources/cheatsheets/GraphQL.md)
- CVE-2026-32594 Parse Server WebSocket Bypass 相关公告

<!-- GROK_EXPANSION_END -->
