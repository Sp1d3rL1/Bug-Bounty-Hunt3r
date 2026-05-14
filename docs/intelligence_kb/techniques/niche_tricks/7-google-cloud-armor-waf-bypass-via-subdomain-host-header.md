---
type: technique
category: trick
derived_from_case: false
vuln_class: Bypass
source_url: https://joshua.hu/2025-bug-bounty-stories-fail
source_author: Joshua Rogers
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: medium
target_types:
  - Google Cloud WAF
---

# Google Cloud Armor WAF Bypass via Subdomain Host Header

## 核心思路

Set Host to test.example.com.attacker.com to evade 'contains' rules on host header

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Bypass` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Bypasses entire WAF rule set exposing backend; fixed in Google docs to use endsWith
- 适用场景：Google Cloud WAF
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。
- 先找 lab/本地靶场复现，再映射到授权目标。

## 适用目标画像

- Google Cloud WAF

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Bypasses entire WAF rule set exposing backend; fixed in Google docs to use endsWith

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

- https://joshua.hu/2025-bug-bounty-stories-fail

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://joshua.hu/2025-bug-bounty-stories-fail](https://joshua.hu/2025-bug-bounty-stories-fail)
" vuln_class: "Bypass" one_line_trick: "Set Host to test.example.com.attacker.com to evade 'contains' rules on host header" why_useful: "Bypasses entire WAF rule set exposing backend; fixed in Google docs to use endsWith" target_type: "Google Cloud WAF" confidence: "high" tags: ["waf-bypass", "host-header", "google-cloud-armor", "bugbounty"]

# Google Cloud Armor WAF Bypass via Subdomain Host Header

## 核心思路
通过在 Host 请求头中构造包含目标域名的子字符串（如 test.example.com.attacker.com），绕过 WAF 使用 .contains() 或类似子串匹配规则的 Host 检查逻辑，使请求被误判为允许流量，从而绕过整个 WAF 规则集直接到达后端服务。

## 前置条件
- 目标使用 Google Cloud Armor 或类似支持自定义表达式的 WAF。
- WAF 规则中 Host 头检查采用 .lower().contains('example.com') 等子串包含判断，而非精确匹配或后缀匹配（.endsWith()）。
- 未授权第三方可能控制请求的 Host 头（常见于反向代理、CDN 或自定义客户端场景）。

## 完整技法细节
- 构造恶意 Host 头：将目标域名作为子串嵌入攻击者控制的域名中，例如将 Host 设置为 test.example.com.attacker.com。
- 发送请求时，WAF 规则如 if (request.headers['host'].lower().contains('test.example.com')) { allow all; } 会因子串匹配而直接放行。
- 绕过所有后续 WAF 防护规则，后端直接处理请求。
- Google 官方文档已修复示例，推荐使用 .endsWith('.example.com') 进行后缀匹配。

## 适用目标画像
- 使用 Google Cloud Armor 配置不当的云服务或企业应用。
- 任何依赖 Host 头子串匹配进行允许/拒绝判断的 WAF（非仅限于 Google Cloud）。
- 生产环境中未严格验证 Host 头的反向代理或 API 网关。

## 为什么有效
WAF 规则编写者常依赖文档中的简单 contains 示例，认为足以限制域名，但子域名拼接可轻松制造包含关系，导致短路放行。浏览器和标准客户端均支持自定义 Host 头，此类规则在真实部署中极易被绕过。

## 手工验证流程（授权 / Lab only）
- 在授权实验室环境中搭建 Google Cloud Armor WAF 并配置 contains 规则。
- 使用 curl 或 Burp Repeater 发送请求，修改 Host 头为 target.example.com.attacker.com。
- 观察是否绕过 WAF 规则并到达后端。
- 切换为 .endsWith() 规则后重新测试，验证修复效果。
- 仅在自有测试环境或授权 BB 程序内执行，记录前后对比日志。

## 可自动化部分
- Burp Suite Intruder 或自定义 Python 脚本批量测试不同 subdomain 拼接模式。
- Nuclei 模板可检测常见 contains Host 规则（授权目标限定）。

## 误报/失败条件
- WAF 使用 .endsWith()、exact match 或正则后缀匹配时失效。
- 后端额外验证 Host 头或启用严格 SNI 检查。
- Cloud Armor 已更新为推荐安全配置的最新版本。

## 授权边界
仅限授权 Bug Bounty 程序或自有 Google Cloud 测试环境。严禁在未授权生产环境测试 Host 头操纵。报告时强调“文档误导导致的配置风险”。

## 报告 impact 角度
- 绕过整个 WAF 防护层，导致后端业务逻辑暴露、敏感 API 访问、潜在 IDOR/BOLA 等高危漏洞。
- 业务影响：绕过速率限制、IP 封禁、SQLi/XSS 等防护，可能导致数据泄露或服务滥用。
- 建议修复：强制使用 .endsWith() 或精确域名匹配，并审计所有 WAF 规则。

## 相关案例链接
- [My 2025 Bug Bounty Stories](https://joshua.hu/2025-bug-bounty-stories-fail)

<!-- GROK_EXPANSION_END -->
