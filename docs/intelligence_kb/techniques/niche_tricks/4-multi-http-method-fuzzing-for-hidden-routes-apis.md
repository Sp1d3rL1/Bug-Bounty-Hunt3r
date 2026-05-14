---
type: technique
category: trick
derived_from_case: false
vuln_class: Functionality
source_url: https://x.com/intigriti/status/2004494400601129247
source_author: intigriti
source_date: 2025-02-20
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: low
target_types:
  - Web apps & APIs
---

# Multi-HTTP Method Fuzzing for Hidden Routes/APIs

## 核心思路

Fuzz endpoints with GET POST PUT etc. (ffuf -X GET,POST,PUT) instead of single method

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Functionality` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Many routes only accept one method; single-method fuzzers miss them entirely
- 适用场景：Web apps & APIs
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。
- 先找 lab/本地靶场复现，再映射到授权目标。

## 适用目标画像

- Web apps & APIs

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Many routes only accept one method; single-method fuzzers miss them entirely

## 手工验证流程（授权 / Lab only）

1. 确认 scope、禁止项、速率限制与是否允许该功能测试。
2. 准备至少两个自有测试账号；多租户场景准备两个 organization/workspace。
3. 先完整走通正常业务流，记录对象 ID、角色、状态、token、请求路径。
4. 只替换一个变量或一步状态，观察服务端响应和后续副作用。
5. 用最小必要数据证明影响；不读取、不导出第三方真实数据。
6. 把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。
7. 先找 lab/本地靶场复现，再映射到授权目标。

## 可自动化部分

- 可自动化收集 endpoint、参数、对象 ID 形态、历史 URL、JS 中的隐藏 API。
- 可自动化做“候选点标记”和“差异对比”，但越权、支付、账号状态影响必须手工确认。

## 误报/失败条件

- 只有客户端表现异常，没有服务端影响。
- 只能影响当前自有账号，无法证明跨权限、跨租户、财务、数据或流程影响。
- 目标业务前提不存在，或服务端已做完整对象归属/状态校验。
- 来源帖子/案例缺少可验证链接时，需降级为 review_queue 并二次确认。

## 授权边界

仅用于授权项目、靶场或自有环境。禁止无授权扫描、凭证滥用、爆破、DoS、真实支付损害、读取第三方真实隐私数据或绕过平台规则。

## 报告 impact 角度

- 说明攻击者前提、受影响对象、服务端缺失的校验，以及可造成的数据访问、权限提升、财务损失、业务流程绕过或租户隔离破坏。
- 证据只保留最小必要截图/请求响应，并打码 token、cookie、PII、支付信息。

## 相关案例链接

- https://x.com/intigriti/status/2004494400601129247

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://x.com/intigriti/status/2004494400601129247](https://x.com/intigriti/status/2004494400601129247)
one_line_trick: Fuzz endpoints with GET POST PUT etc. (ffuf -X GET,POST,PUT) instead of single method why_useful: Many routes only accept one method; single-method fuzzers miss them entirely target_type: Web apps & APIs confidence: high tags: [fuzzing, http-methods, hidden-routes, api-discovery]
- **核心思路**
使用多HTTP方法（如GET,POST,PUT,DELETE,OPTIONS）对目录/端点进行fuzz，而非单一GET，揭示仅支持特定方法的隐藏路由或API。
- **前置条件**
- 目标Web应用或API存在目录/路径。
- 授权Bug Bounty程序或自有Lab环境。
- ffuf或其他支持多-method的fuzz工具。
- **完整技法细节**
- 准备wordlist（目录、API路径）。
- ffuf命令：ffuf -u https://target/FUZZ -w wordlist.txt -X GET,POST,PUT,DELETE,OPTIONS -mc 200,204,301,302。
- 分别记录每种method的响应。
- 对比单method fuzz结果，找出method-specific路由。
- 手动测试发现的隐藏端点功能。
- **适用目标画像**
任何Web应用或REST/GraphQL API，尤其是框架默认仅允许特定method的路由（如POST-only API）。
- **为什么有效**
许多路由/控制器仅对单一HTTP方法响应，单method fuzz（如仅GET）会完全遗漏，错过大量攻击面。
- **手工验证流程（授权 / Lab only）**
- 在授权BB或Lab环境中运行多method fuzz。
- 访问发现的method-specific URL，确认响应差异（e.g. POST返回功能页面）。
- 测试该路由是否引入新功能或漏洞。
- 记录但不进行破坏性测试。
- **可自动化部分**
- ffuf -X 多method支持。
- 脚本循环不同method自动fuzz并diff响应。
- Burp Intruder或自定义工具批量测试。
- **误报/失败条件**
- 所有method返回相同响应（无method限制）。
- WAF阻挡非GET请求。
- 路由不存在或返回405 Method Not Allowed。
- **授权边界**
仅在授权范围内fuzz，控制请求频率避免DoS。禁止任何破坏性测试载荷，仅发现路由。
- **报告 impact 角度**
- 发现隐藏API/路由，扩大攻击面。
- 可能暴露未文档化功能或逻辑漏洞。
- 提升整体recon效率，发现单method fuzz遗漏的高价值端点。
- **相关案例链接**
- [https://x.com/intigriti/status/2004494400601129247](https://x.com/intigriti/status/2004494400601129247)
- Intigriti multi-method fuzz example in thread

<!-- GROK_EXPANSION_END -->
