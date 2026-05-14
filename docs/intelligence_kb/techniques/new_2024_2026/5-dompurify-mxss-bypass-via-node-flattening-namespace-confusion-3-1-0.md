---
type: technique
category: new_method
vuln_class: DOMPurify
source_url: https://mizu.re/post/exploring-the-dompurify-library-bypasses-and-fixes
source_author: Kevin Mizu (@kevin_mizu)
source_date: 2024-11
collected_at: 2026-05-04
freshness: 2024
confidence: high
risk_level: medium
target_types:
  - client-side HTML sanitizers
raw_file: data/grok_research/raw/2026-05-04/topic_07_client_side_dom_cspt.md
---

# DOMPurify mXSS Bypass via Node Flattening + Namespace Confusion (3.1.0)

## 核心思路

Nested": - /url: https://mizu.re/post/exploring-the-dompurify-library-bypasses-and-fixes§DOMPurify§Nested - text: SVG/HTML nodes + integration points ( - text: "," - text: ) to trigger browser re-parsing mutation

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `DOMPurify` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

Exploits depth limits and stack popping for mXSS; reported to maintainer leading to fixes; lab-tested

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- client-side HTML sanitizers

## 为什么有效

Exploits depth limits and stack popping for mXSS; reported to maintainer leading to fixes; lab-tested

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

围绕 `DOMPurify` 说明可导致的未授权数据访问、权限提升、业务绕过、财务影响或合规风险。

## 相关案例链接

- https://mizu.re/post/exploring-the-dompurify-library-bypasses-and-fixes

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://mizu.re/post/exploring-the-dompurify-library-bypasses-and-fixes](https://mizu.re/post/exploring-the-dompurify-library-bypasses-and-fixes)
" vuln_class: "DOMPurify" one_line_trick: "Use nested SVG/HTML nodes plus integration points to trigger browser re-parsing mutation" why_useful: "Exploits depth limits and stack popping for mXSS; reported to maintainer leading to fixes; lab-tested" target_type: "client-side HTML sanitizers" confidence: "high" tags: ["bug-bounty", "mxss", "dompurify", "namespace-confusion"]
- **核心思路**
利用浏览器 HTML 解析器的嵌套深度限制（512 层）和命名空间切换（SVG ↔ HTML），通过深度嵌套 + integration point（如 <foreignObject>、<caption>）触发节点扁平化（flattening）和栈弹出（stack popping）。DOMPurify 清理后的 HTML 在 innerHTML 二次解析时发生结构突变，产生可执行的 mXSS。
- **前置条件**
- 目标使用 DOMPurify ≤ 3.1.0（或未修复对应深度/命名空间逻辑的版本）；
- 输入可控的 HTML 会经过 sanitize 后插入 DOM。
- **完整技法细节**
- **适用目标画像**
- 任何客户端 HTML 净化器（DOMPurify、HTML Sanitizer 等）；
- 富文本编辑器、评论系统、Markdown 渲染器。
- **为什么有效**
DOMPurify 未充分处理浏览器解析器的二次解析行为和跨命名空间扁平化，导致清理后的 DOM 在插入页面时发生突变。
- **手工验证流程（授权 / Lab only）**
- 在本地 Lab 部署受影响版本的 DOMPurify。
- 注入构造好的嵌套 payload。
- 观察清理后 DOM 是否出现可执行属性或脚本。
- 仅使用测试账号验证，立即清理 Lab 环境。
- **可自动化部分**
- 使用 fuzzing 工具生成深度嵌套变体；
- 集成 DOMPurify 版本扫描。
- **误报/失败条件**
- DOMPurify 版本 ≥ 3.1.1（已加入深度检查）；
- 浏览器版本过新或解析规则已变更。
- **授权边界**
仅限授权程序或完全自有 Lab。严禁在生产环境注入真实用户可见的测试 payload。
- **报告 impact 角度**
- 绕过客户端 XSS 防护，导致存储型/反射型 XSS；
- 可升级为账户接管或数据泄露；
- 已促成 DOMPurify 官方修复，具有极高技术价值。
- **相关案例链接**
- [https://mizu.re/post/exploring-the-dompurify-library-bypasses-and-fixes](https://mizu.re/post/exploring-the-dompurify-library-bypasses-and-fixes)

<!-- GROK_EXPANSION_END -->
