---
type: technique
category: new_method
vuln_class: Bypass via Field Suggestions
source_url: https://github.com/nikitastupin/clairvoyance
source_author: nikitastupin (via @VivekIntel)
source_date: 2026-04-22
collected_at: 2026-05-04
freshness: 2026
confidence: high
risk_level: medium
target_types:
  - Any GraphQL API
raw_file: data/grok_research/raw/2026-05-04/topic_04_graphql_schema.md
---

# Clairvoyance for Schema Extraction When Introspection Disabled

## 核心思路

Fuzz malformed queries and parse "Did you mean..." errors to blindly reconstruct full schema then import to Voyager

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `Bypass via Field Suggestions` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

Reveals hidden fields/mutations for IDOR/BOLA in hardened GraphQL endpoints during BB hunts

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- Any GraphQL API

## 为什么有效

Reveals hidden fields/mutations for IDOR/BOLA in hardened GraphQL endpoints during BB hunts

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

围绕 `Bypass via Field Suggestions` 说明可导致的未授权数据访问、权限提升、业务绕过、财务影响或合规风险。

## 相关案例链接

- https://github.com/nikitastupin/clairvoyance

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://github.com/nikitastupin/clairvoyance](https://github.com/nikitastupin/clairvoyance)
" vuln_class: "Bypass via Field Suggestions" one_line_trick: "Fuzz malformed queries and parse "Did you mean..." errors to blindly reconstruct full schema then import to Voyager" why_useful: "Reveals hidden fields/mutations for IDOR/BOLA in hardened GraphQL endpoints during BB hunts" target_type: "Any GraphQL API" confidence: "high" tags: ["graphql", "schema-extraction", "introspection-bypass", "bugbounty"]

# Clairvoyance for Schema Extraction When Introspection Disabled

## 核心思路
当 GraphQL 端点禁用 introspection（__schema 查询被屏蔽）时，通过向服务器发送畸形查询，触发 GraphQL 引擎返回的“Did you mean ...?” 错误提示，逐步收集有效类型、字段、参数等信息，最终重建完整 schema JSON 并导入 Voyager 等工具可视化。

## 前置条件
- GraphQL API 暴露但 introspection 已禁用（生产环境常见，如 Apollo Server 在 NODE_ENV=production 时自动关闭）。
- 服务器会返回字段建议错误消息（GraphQL 标准行为）。
- 可访问 GraphQL 端点且未被 WAF 完全阻断畸形查询。

## 完整技法细节
- 使用 Clairvoyance 工具或手动 fuzz 常见字段名（基于英文词表或业务特定词表）。
- 发送包含无效字段的查询，例如 { ussr { id } }，服务器返回 “Cannot query field 'ussr'. Did you mean 'user'?”。
- 解析错误中的建议字段，递归收集所有类型、字段、mutation、subscription 等。
- 输出 JSON schema 文件，可直接导入 GraphQL Voyager、InQL 或 graphql-path-enum。
- 推荐词表：Escape Technologies GraphQL wordlist 或 cewl 从前端提取的业务词汇。

## 适用目标画像
- 任何生产环境 GraphQL API（Apollo、Hasura 等），尤其禁用 introspection 的硬化目标。
- Bug Bounty 程序中隐藏字段/ mutation 导致的 IDOR、BOLA、权限绕过场景。

## 为什么有效
GraphQL 引擎为开发者友好，默认返回字段建议错误，即使 introspection 关闭也会泄露 schema 结构。此工具自动化了该过程，极大降低手动枚举难度。

## 手工验证流程（授权 / Lab only）
- 在授权 Lab 或自有 GraphQL 测试环境中部署带 introspection 禁用的端点。
- 安装 Clairvoyance（pip install clairvoyance）。
- 运行 clairvoyance https://target/graphql -o schema.json -w wordlist.txt。
- 导入 Voyager 可视化 schema，确认是否发现隐藏字段。
- 仅在授权 BB 程序内测试，记录所有请求日志。

## 可自动化部分
- Clairvoyance 工具本身已完全自动化，支持 Docker 运行。
- 结合 cewl 生成目标特定词表，进一步提升覆盖率。
- 可集成到 Burp Suite 或自定义扫描器。

## 误报/失败条件
- 服务器完全抑制“Did you mean”错误或返回泛化消息。
- WAF 阻断高频畸形查询。
- 词表质量差导致覆盖不全（需结合业务词表）。

## 授权边界
仅限授权 Bug Bounty 程序或自有 GraphQL Lab 环境。禁止在未授权生产环境进行高频 fuzz。报告时强调“信息泄露导致的后续攻击面扩大”。

## 报告 impact 角度
- 暴露隐藏字段/ mutation，导致 IDOR、BOLA、敏感数据读取或业务逻辑绕过。
- 业务影响：完整 schema 映射后可发现高危漏洞，潜在数据泄露或权限提升。
- 建议修复：完全禁用字段建议错误，或在生产环境自定义错误消息。

## 相关案例链接
- [Clairvoyance GitHub](https://github.com/nikitastupin/clairvoyance)

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/graphql.md -->

<!-- backlink: docs/checklists/recon_methodology.md -->
