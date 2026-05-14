---
type: technique
category: trick
derived_from_case: false
vuln_class: Disclosure
source_url: https://x.com/intigriti/status/2004494400601129247
source_author: intigriti
source_date: 2025-08-29
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: low
target_types:
  - Firebase backends
---

# Firebase Rule Enumeration & Data Leak via Misconfig

## 核心思路

Enumerate Firebase DB rules and query unauth paths for exposed data

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Disclosure` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Common misconfig leaks user data; full thread details practical enumeration
- 适用场景：Firebase backends
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。
- 先找 lab/本地靶场复现，再映射到授权目标。

## 适用目标画像

- Firebase backends

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Common misconfig leaks user data; full thread details practical enumeration

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
one_line_trick: Enumerate Firebase DB rules and query unauth paths for exposed data why_useful: Common misconfig leaks user data; full thread details practical enumeration target_type: Firebase backends confidence: high tags: [firebase, security-rules, data-leak, misconfiguration, enumeration]
- **核心思路**
通过在JS文件、HTTP请求或Google dork中定位Firebase项目ID和配置，枚举数据库路径并直接查询REST API（如*.firebaseio.com/<path>.json），验证安全规则（Security Rules）是否误配（如.read: true允许匿名读取），从而发现未经授权的数据泄露。
- **前置条件**
- 目标应用使用Firebase Realtime Database、Firestore或Storage
- JS文件中暴露firebaseConfig（projectId、databaseURL等）或可通过网络请求/ dork发现
- 授权Bug Bounty程序或自有Lab环境（禁止生产环境真实数据操作）
- **完整技法细节**
- 识别目标：搜索JS中的firebaseConfig或使用Google dork site:.firebaseio.com "target"。
- 构造REST API：尝试https://<project-id>.firebaseio.com/<collection>/.json或Firestore API路径。
- 枚举常见路径：users、contacts、messages、orders等，测试GET请求（无auth token）。
- 验证规则：不同路径/操作（read/write/delete）分别测试，观察是否返回200+数据。
- 扩展：拦截App流量获取结构，或测试Storage对象访问。仅读取公开数据，不修改/删除。
- **适用目标画像**
使用Google Firebase作为后端数据库或存储的Web/Mobile应用，特别是初创公司、快速迭代项目或移动App后端，未严格审计安全规则。
- **为什么有效**
Firebase默认deny-by-default，但开发者常为简化开发设置宽松规则（如test mode遗留或粒度规则写错），导致真实世界大量数据泄露案例。
- **手工验证流程（授权 / Lab only）**
- 在授权BB程序或本地Firebase Emulator Lab中创建测试项目，故意设置宽松规则（e.g. allow read: if true）。
- 部署简单测试App暴露config。
- 使用curl/Postman无认证查询路径，确认数据可读（使用测试/脱敏数据）。
- 修复规则后重新验证访问被拒。
- 记录响应但不实际dump生产用户数据。
- **可自动化部分**
- JS扫描提取projectId（自定义脚本/Burp）。
- ffuf fuzz常见路径集合（如users/, orders/）。
- 自动化API查询工具检查返回状态和数据量。
- **误报/失败条件**
- 规则要求request.auth != null或App Check启用。
- 路径不存在/返回403/404。
- Firebase额外保护（如VPC SC）或正确配置。
- **授权边界**
仅限授权Bug Bounty in-scope Firebase资产或自有Lab。禁止写入、删除、大规模真实数据拉取或生产环境操作。始终强调“潜在”而非实际验证暴露风险（不导出真实敏感数据）。
- **报告 impact 角度**
- 未授权访问用户PII、联系方式、业务数据等敏感信息。
- 可能引发大规模数据泄露、GDPR/隐私合规风险、业务声誉损害。
- 高危：未授权第三方可能轻松枚举并窃取全部公开集合数据。
- **相关案例链接**
- [https://x.com/intigriti/status/1961373389295149271](https://x.com/intigriti/status/1961373389295149271)
- [https://www.intigriti.com/researchers/blog/hacking-tools/hacking-google-firebase-targets](https://www.intigriti.com/researchers/blog/hacking-tools/hacking-google-firebase-targets)

<!-- GROK_EXPANSION_END -->
