---
type: technique
category: new_method
vuln_class: BOLA/IDOR
source_url: https://x.com/vuln_X/status/2048709380166889642
source_author: vuln_X
source_date: 2026-04-27
collected_at: 2026-05-04
freshness: 2026
confidence: high
risk_level: high
target_types:
  - REST
  - JSON API
raw_file: data/grok_research/raw/2026-05-04/topic_02_api_bola_idor.md
---

# JSON Nested ID Wrapping Bypass for Outer Auth Validation

## 核心思路

Wrap ID as {\"Account\":{\"Account\":victimID}} in JSON body to evade top-level checks

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `BOLA/IDOR` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

Bypasses flawed validation layers common in modern APIs; niche JSON parsing trick

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- REST/JSON API

## 为什么有效

Bypasses flawed validation layers common in modern APIs; niche JSON parsing trick

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

围绕 `BOLA/IDOR` 说明可导致的未授权数据访问、权限提升、业务绕过、财务影响或合规风险。

## 相关案例链接

- https://x.com/vuln_X/status/2048709380166889642

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

id: 8 title: JSON Nested ID Wrapping Bypass for Outer Auth Validation type: technique vuln_class: BOLA/IDOR author_date: vuln_X / 2026-04-27 source_url:
- [https://x.com/vuln_X/status/2048709380166889642](https://x.com/vuln_X/status/2048709380166889642)
one_line_trick: Wrap ID as {"Account":{"Account":victimID}} in JSON body to evade top-level checks target_type: REST/JSON API confidence: high tags: [json-parsing, idor-bypass, auth-validation]

## 核心思路
在 REST/JSON API 中，许多应用仅对顶层 JSON 字段（如 "id"）进行授权校验，而忽略嵌套对象结构。当开发者使用深度解析（如 lodash.get 或自定义 getter）提取 ID 时，通过将 victimID 包装为嵌套对象（如 {"Account":{"Account":victimID}}）可绕过外层 auth 校验，直接引用目标对象。

## 前置条件
- 目标 API 使用 JSON 请求体，且 ID 参数位于可嵌套位置（如 Account、User 等对象字段）。
- 外层 auth 校验仅检查顶层字段或浅层结构，未进行递归/深度验证。
- 授权环境或自建 Lab（Next.js、Spring Boot、Node.js 等常见 JSON 处理框架）。
- 已知 victimID（通过枚举或公开信息获取）。

## 完整技法细节
- 正常请求示例：{"id": "victim123"}（被外层校验拦截）。
- 构造嵌套 payload：{"Account":{"Account":"victim123"}} 或 {"data":{"Account":{"Account":"victim123"}}}。
- 将嵌套 JSON 放入 POST/PUT 请求体中，保持 Content-Type: application/json。
- API 解析器自动提取最内层 ID 值，绕过仅校验顶层 "Account" 字段的逻辑。
：仅在自建环境中测试，确认返回 victim 资源数据但不进行任何修改/删除操作。

## 适用目标画像
- 现代微服务/REST API（尤其是使用 ORM 如 Prisma、Sequelize 或自定义 JSON 解析器的后端）。
- 企业级 SaaS、协作工具、金融 API 等采用分层 auth 的系统。
- 常见于 2024-2026 年新架构中，未对 JSON 深度解析做完整 auth 覆盖的目标。

## 为什么有效
外层 auth middleware 通常只扫描 request.body.id 或 request.body.accountId 等顶层键，未处理嵌套对象；后端业务层则直接使用深度提取的值，导致校验与实际使用脱节。这是 JSON 灵活解析带来的经典解析差异问题。

## 手工验证流程（授权 / Lab only）
- 在授权 Bug Bounty 程序或自建 Nextcloud/自建 API Lab 中准备两个账号（attacker + victim）。
- 使用 Burp/Requester 构造正常请求，确认 auth 拦截。
- 切换为嵌套 JSON payload，重放请求。
- 观察响应：若返回 victim 数据（仅读取），则确认 bypass。
：仅验证读取行为，绝不在生产环境执行任何写操作；立即停止测试并报告。

## 可自动化部分
- Burp Intruder / ffuf 使用 payload 列表生成嵌套变体（如 {"Account":{"Account":"^ID^"}}）。
- Python requests 脚本批量测试已知 ID 列表。
- 可与 nuclei 自定义模板结合检测常见嵌套模式。

## 误报/失败条件
- API 使用严格 schema 校验（如 Zod、Joi）强制顶层扁平结构。
- 后端同样进行深度 auth 校验或使用 JSONPath 严格匹配。
- 框架启用全局 JSON 深度 sanitization（如 express-validator）。

## 授权边界
仅限授权 Bug Bounty 程序或完全自控 Lab 环境。禁止在未授权目标上测试任何嵌套 payload。边界：仅读取公开/授权范围内数据，绝不触碰写操作或第三方数据。

## 报告 impact 角度
：绕过 auth 导致敏感对象数据泄露（用户资料、财务记录等）。
：破坏对象级隔离，可能导致水平权限提升。
：High（视数据敏感度），强调“绕过多层 auth 校验的 JSON 解析差异”。

## 相关案例链接
- [https://x.com/vuln_X/status/2048709380166889642](https://x.com/vuln_X/status/2048709380166889642)

<!-- GROK_EXPANSION_END -->
