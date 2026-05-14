---
type: technique
category: trick
derived_from_case: false
vuln_class: Functionality
source_url: https://x.com/intigriti/status/2004494400601129247
source_author: intigriti
source_date: 2025-02-24
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: low
target_types:
  - Multi-platform web apps
---

# Mobile vs Desktop User-Agent Crawl for Version Diffs

## 核心思路

Crawl target twice with desktop + mobile UA headers and diff responses

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Functionality` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Apps serve different endpoints/auth/features per platform; reveals extra attack surface
- 适用场景：Multi-platform web apps
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。
- 先找 lab/本地靶场复现，再映射到授权目标。

## 适用目标画像

- Multi-platform web apps

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Apps serve different endpoints/auth/features per platform; reveals extra attack surface

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
one_line_trick: Crawl target twice with desktop + mobile UA headers and diff responses why_useful: Apps serve different endpoints/auth/features per platform; reveals extra attack surface target_type: Multi-platform web apps confidence: high tags: [user-agent, recon, version-diff, mobile-desktop, attack-surface]
- **核心思路**
使用桌面和移动User-Agent分别爬取目标站点，比较响应差异（端点、功能、认证机制、JS资源），发现平台特定版本暴露的额外攻击面。
- **前置条件**
- 目标为多平台Web应用（同时支持桌面和移动端）。
- 可控制爬虫的User-Agent头（如ffuf、Burp、ZAP）。
- 授权Bug Bounty程序或自有测试环境。
- **完整技法细节**
- 准备两个User-Agent：标准桌面（如Mozilla/5.0 ... Windows）和移动（如Mozilla/5.0 ... Mobile Safari）。
- 分别完整爬取站点（相同起始URL、深度）。
- 使用diff工具对比响应体、headers、链接、JS文件。
- 重点检查：新端点、不同认证、隐藏功能、平台专属API。
- 手动验证差异端点是否增加攻击面。
- **适用目标画像**
同时面向Web和移动用户的应用（如银行、电商、SaaS），常为桌面/移动部署不同版本或特性。
- **为什么有效**
许多应用根据UA提供定制版本（性能、功能、A/B测试），导致桌面爬虫遗漏移动专属端点或反之，扩大攻击面。
- **手工验证流程（授权 / Lab only）**
- 在授权程序或本地测试环境中，使用curl或爬虫工具分别以两种UA爬取。
- 保存响应并diff（e.g. diff -r desktop/ mobile/）。
- 手动访问差异URL，确认新功能/端点。
- 测试差异是否引入新漏洞（如不同auth逻辑）。
- **可自动化部分**
- ffuf / katana / Hakrawler with custom UA header。
- 脚本自动diff响应（Python difflib或Burp Comparer）。
- 批量URL列表对比。
- **误报/失败条件**
- 目标不区分UA（单版本应用）。
- 响应仅含随机/时间戳差异。
- WAF/速率限制阻挡爬虫。
- **授权边界**
仅在授权Bug Bounty in-scope资产或自有Lab中爬取。避免高频请求造成服务影响。
- **报告 impact 角度**
- 扩大攻击面，发现隐藏端点/功能/认证差异。
- 可能引入平台特定漏洞（如移动版弱auth）。
- 提升recon质量，增加后续漏洞发现概率。
- **相关案例链接**
- [https://x.com/intigriti/status/2004494400601129247](https://x.com/intigriti/status/2004494400601129247)
- Intigriti recon article (linked in thread)

<!-- GROK_EXPANSION_END -->
