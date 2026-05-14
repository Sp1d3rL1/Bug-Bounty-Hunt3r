---
type: technique
category: new_method
vuln_class: Bypass via Suggestions
source_url: https://medium.com/@mpjani294/graphql-pentesting-for-bug-bounty-hunters-from-endpoint-discovery-to-high-impact-exploits-821f64a953b5
source_author: MPGODMATCH
source_date: 2025-11-15
collected_at: 2026-05-04
freshness: 2025
confidence: high
risk_level: medium
target_types:
  - Hardened GraphQL APIs
raw_file: data/grok_research/raw/2026-05-04/topic_04_graphql_schema.md
---

# Field Suggestion Abuse to Rebuild Schema Blindly

## 核心思路

Fuzz fields with cewl-generated business wordlist and parse "Did you mean" responses to map schema

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `Bypass via Suggestions` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

Bypasses disabled introspection for full attack surface mapping in production BB targets

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- Hardened GraphQL APIs

## 为什么有效

Bypasses disabled introspection for full attack surface mapping in production BB targets

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

围绕 `Bypass via Suggestions` 说明可导致的未授权数据访问、权限提升、业务绕过、财务影响或合规风险。

## 相关案例链接

- https://medium.com/@mpjani294/graphql-pentesting-for-bug-bounty-hunters-from-endpoint-discovery-to-high-impact-exploits-821f64a953b5

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://medium.com/@mpjani294/graphql-pentesting-for-bug-bounty-hunters-from-endpoint-discovery-to-high-impact-exploits-821f64a953b5](https://medium.com/@mpjani294/graphql-pentesting-for-bug-bounty-hunters-from-endpoint-discovery-to-high-impact-exploits-821f64a953b5)
" vuln_class: "Bypass via Suggestions" one_line_trick: "Fuzz fields with cewl-generated business wordlist and parse "Did you mean" responses to map schema" why_useful: "Bypasses disabled introspection for full attack surface mapping in production BB targets" target_type: "Hardened GraphQL APIs" confidence: "high" tags: ["graphql", "schema-reconstruction", "field-suggestion", "bugbounty"]

# Field Suggestion Abuse to Rebuild Schema Blindly

## 核心思路
利用 GraphQL 服务器在字段拼写错误时返回“Did you mean ...?” 建议的特性，通过业务词表 fuzz 无效字段，解析错误响应逐步重建完整 schema，实现禁用 introspection 下的盲枚举。

## 前置条件
- GraphQL 端点 introspection 已禁用（返回 400 或 “Introspection is Disabled”）。
- 服务器仍返回字段建议错误消息。
- 可从前端或业务文档生成高质量词表。

## 完整技法细节
- 使用 cewl 从目标前端生成业务词表：cewl http://target/ > words.txt。
- 合并通用词表（如 30k English words）。
- 使用 Clairvoyance 或手动发送畸形查询，解析 “Did you mean” 提示。
- 递归收集所有 Query、Mutation、类型、字段及参数。
- 输出 JSON 后导入 GraphQL Voyager 进行可视化映射。

## 适用目标画像
- 生产环境硬化后的 GraphQL API（introspection 关闭）。
- Bug Bounty 目标中隐藏敏感 mutation 或字段的端点。

## 为什么有效
GraphQL 引擎默认提供开发者友好提示，即使禁用 introspection 也会泄露 schema 信息。此方法将“友好错误”转化为攻击面映射工具。

## 手工验证流程（授权 / Lab only）
- 在授权 Lab 环境中部署禁用 introspection 的 GraphQL 服务。
- 生成词表并运行 Clairvoyance 或手动 fuzz。
- 对比重建的 schema 与实际 schema，验证覆盖率。
- 仅在授权 BB 程序内操作，限制请求频率。

## 可自动化部分
- Clairvoyance 工具全自动 fuzz + 解析。
- Burp Intruder + 自定义提取器实现半自动化。
- cewl + 词表合并脚本自动化准备阶段。

## 误报/失败条件
- 服务器禁用所有字段建议或返回自定义泛化错误。
- 词表覆盖不足（业务特定字段缺失）。
- WAF 阻断 fuzz 流量。

## 授权边界
严格限定于授权 Bug Bounty 程序或自有测试环境。禁止无授权高频 fuzz。报告时注明“schema 信息泄露导致的攻击面扩大”。

## 报告 impact 角度
- 完整 schema 映射后发现隐藏字段，导致 IDOR、BOLA、未授权 mutation 执行等高危漏洞。
- 业务影响：数据泄露、权限绕过或业务逻辑操纵。
- 建议修复：在生产环境完全移除字段建议，或使用自定义错误处理。

## 相关案例链接
- [GraphQL Pentesting for Bug Bounty Hunters](https://medium.com/@mpjani294/graphql-pentesting-for-bug-bounty-hunters-from-endpoint-discovery-to-high-impact-exploits-821f64a953b5)

<!-- GROK_EXPANSION_END -->
