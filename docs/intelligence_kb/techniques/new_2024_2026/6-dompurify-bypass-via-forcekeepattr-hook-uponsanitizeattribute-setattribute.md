---
type: technique
category: new_method
vuln_class: DOMPurify
source_url: https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-111-how-to-bypass-dompurify-with-k-vin-mizu
source_author: Kevin Mizu (Critical Thinking Podcast Ep.111)
source_date: 2025-02
collected_at: 2026-05-04
freshness: 2025
confidence: high
risk_level: medium
target_types:
  - web apps using DOMPurify
raw_file: data/grok_research/raw/2026-05-04/topic_07_client_side_dom_cspt.md
---

# DOMPurify Bypass via forceKeepAttr Hook + uponSanitizeAttribute setAttribute

## 核心思路

Hook": - /url: https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-111-how-to-bypass-dompurify-with-k-vin-mizu§DOMPurify§Hook - text: marks attr safe (skips regex) while setAttribute injects during loop

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `DOMPurify` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

Chains with session fixation for ATO in subdomain XSS; real BB chain on authorized program

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- web apps using DOMPurify

## 为什么有效

Chains with session fixation for ATO in subdomain XSS; real BB chain on authorized program

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

- https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-111-how-to-bypass-dompurify-with-k-vin-mizu

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-111-how-to-bypass-dompurify-with-k-vin-mizu](https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-111-how-to-bypass-dompurify-with-k-vin-mizu)
" vuln_class: "DOMPurify" one_line_trick: "Hook marks an attribute safe while setAttribute mutates DOM state during the sanitize loop" why_useful: "Chains with session fixation for ATO in subdomain XSS; real BB chain on authorized program" target_type: "web apps using DOMPurify" confidence: "high" tags: ["bug-bounty", "xss", "dompurify", "mXSS", "client-side"]
- **核心思路**
利用 DOMPurify 的 forceKeepAttr Hook 在属性检查前标记属性为安全，或在 uponSanitizeAttribute Hook 中通过 setAttribute 动态添加新属性。由于属性列表在遍历前已快照，新添加的危险属性（如 onerror、javascript:）会绕过后续正则和清理逻辑，实现 mXSS。
- **前置条件**
- 应用使用 DOMPurify 并配置了 forceKeepAttr 或 uponSanitizeAttribute Hook；
- 未授权第三方可能控的 HTML 输入会经过 DOMPurify.sanitize；
- 存在子域名 XSS 或可注入富文本的点（授权环境）。
- **完整技法细节**
- forceKeepAttr（3.1.3~3.1.5）：Hook 在正则检查前执行，若标记 href 等为安全，则跳过危险内容正则。
- 结合子域名 XSS + Session Fixation 实现完整 ATO（仅授权程序测试）。
- **适用目标画像**
- 使用 DOMPurify 处理用户富文本、评论、Markdown 的 Web 应用；
- 存在子域名或跨域 XSS 入口；
- OAuth / Session 逻辑可被客户端操纵的程序。
- **为什么有效**
DOMPurify 假设属性集在遍历期间静态不变，而 Hook 机制允许在遍历中动态修改 DOM，导致清理逻辑漏掉危险属性。
- **手工验证流程（授权 / Lab only）**
- 在 Lab 环境中部署带 Hook 的 DOMPurify 页面。
- 构造包含危险属性的 payload，触发 sanitize。
- 使用 DevTools 检查清理后 DOM 是否仍存在可执行属性。
- 仅在授权目标的测试账号上验证链式影响，立即回滚所有变更。
- **可自动化部分**
- 自定义 Burp/FFUF payload 列表测试常见 Hook 配置；
- 使用 DOMPurify 版本扫描器辅助发现老版本。
- **误报/失败条件**
- 未启用对应 Hook；
- DOMPurify 版本已打对应补丁且 Hook 使用正确；
- 输入经过额外服务端过滤。
- **授权边界**
严格限制在授权 Bug Bounty 程序或本地 Lab 环境。任何涉及真实用户数据的测试必须获得书面许可，且测试后立即清理测试数据。
- **报告 impact 角度**
- 结合子域名 XSS 可实现账户接管（ATO）；
- 高危客户端 XSS 绕过，影响所有依赖 DOMPurify 的富文本功能；
- 实际 Bounty 案例中已成功用于 OAuth 场景。
- **相关案例链接**
- [https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-111-how-to-bypass-dompurify-with-k-vin-mizu](https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-111-how-to-bypass-dompurify-with-k-vin-mizu)
- [https://mizu.re/post/exploring-the-dompurify-library-bypasses-and-fixes](https://mizu.re/post/exploring-the-dompurify-library-bypasses-and-fixes)

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->
