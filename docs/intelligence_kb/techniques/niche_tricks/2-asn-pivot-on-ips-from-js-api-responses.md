---
type: technique
category: trick
derived_from_case: false
vuln_class: Recon
source_url: https://x.com/obscaries/status/2050569465163874655
source_author: obscaries
source_date: 2026-05-02
collected_at: 2026-05-05
freshness: 2026
confidence: high
risk_level: low
target_types:
  - JS-heavy web apps
---

# ASN Pivot on IPs from JS/API Responses

## 核心思路

Extract": - /url: https://x.com/obscaries/status/2050569465163874655§Recon§Extract - text: IPs embedded in JS or responses then perform ASN lookup to map target infra

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Recon` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Expands attack surface to related/owned networks missed in initial subdomain recon
- 适用场景：JS-heavy web apps
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。
- 先找 lab/本地靶场复现，再映射到授权目标。

## 适用目标画像

- JS-heavy web apps

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Expands attack surface to related/owned networks missed in initial subdomain recon

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

- https://x.com/obscaries/status/2050569465163874655

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://x.com/obscaries/status/2050569465163874655](https://x.com/obscaries/status/2050569465163874655)
vuln_class: Recon target_type: JS-heavy web apps confidence: high type: technique tags: [recon, asn-lookup, infrastructure-mapping, osint]

# ASN Pivot on IPs from JS/API Responses
- **核心思路**
从 JS 文件或 API 响应中提取嵌入的 IP 地址，再通过 ASN 查询工具映射关联基础设施，扩大目标所有权范围，找出初始子域枚举遗漏的资产。
- **前置条件**
- 已爬取目标 JS 文件、API 响应或前端资源。
- 发现硬编码或动态返回的 IP 地址。
- 授权 Bug Bounty 程序或自有 Lab 环境。
- **完整技法细节**
- 使用 grep / nuclei / JS 解析工具从响应中提取 IPv4/IPv6。
- 将 IP 输入 ASN 查询工具（例如 devina.io/asn-lookup）。
- 分析返回的 ASN 信息，识别同一组织/云提供商的其他网段/域名。
- 将新发现的 IP/域名加入 recon 清单继续枚举。
- **适用目标画像**
前端 JS 重度应用、微服务架构或使用 CDN/云函数的 Web 项目，常在 JS 中嵌入后端 IP 或 API 地址。
- **为什么有效**
许多组织在 JS/API 中意外暴露内部/边缘 IP，通过 ASN 可快速发现同一 ASN 下其他未被子域枚举覆盖的基础设施，显著扩展攻击面。
- **手工验证流程（授权 / Lab only）**
- 在授权 Lab 中提取 IP 后，使用公开 ASN 查询工具验证所有权。
- 交叉比对 WHOIS / BGP 数据确认属于目标组织。
- 将新资产加入 scope 内继续测试（仅授权范围）。
- **可自动化部分**
自定义 Burp 扩展或 Python 脚本自动解析响应 → ASN 查询 → 新域名/IP 发现；集成到 Amass / Subfinder 流水线。
- **误报/失败条件**
- IP 为公共 CDN / 第三方服务（非目标所有）。
- ASN 查询返回无关联域名。
- 目标使用严格的 IP 混淆或代理。
- **授权边界**
仅对授权 Bug Bounty 程序明确 scope 内的资产及关联基础设施进行 pivot。禁止任何超出授权范围的进一步扫描。
- **报告 impact 角度**
- 攻击面显著扩大（新增子域/IP 资产）
- 发现隐藏基础设施导致的新漏洞机会
- 提升整体 recon 深度与覆盖率
- **相关案例链接**
- [https://x.com/obscaries/status/2050569465163874655](https://x.com/obscaries/status/2050569465163874655)

<!-- GROK_EXPANSION_END -->
