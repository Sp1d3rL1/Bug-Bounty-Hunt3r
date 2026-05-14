---
type: technique
category: trick
derived_from_case: false
vuln_class: Disclosure
source_url: https://x.com/intigriti/status/2004494400601129247
source_author: intigriti
source_date: 2025-02-26
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: medium
target_types:
  - JS-heavy sites
---

# Archived JS Files for Legacy Secrets Endpoints Params

## 核心思路

Search Wayback Machine archives of discovered JS files for old endpoints secrets hardcoded params

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Disclosure` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Legacy code often still live processes old params or leaks creds missed in current version
- 适用场景：JS-heavy sites
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。
- 先找 lab/本地靶场复现，再映射到授权目标。

## 适用目标画像

- JS-heavy sites

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Legacy code often still live processes old params or leaks creds missed in current version

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
" vuln_class: "Disclosure" one_line_trick: "Search Wayback Machine archives of discovered JS files for old endpoints secrets hardcoded params" why_useful: "Legacy code often still live processes old params or leaks creds missed in current version" target_type: "JS-heavy sites" confidence: "high" tags: ["bug-bounty", "recon", "js", "wayback", "legacy"]
- **核心思路**
当发现目标的 JavaScript 文件后，使用 Wayback Machine 搜索其历史归档版本，从旧版 JS 中挖掘已删除的 API 端点、硬编码密钥、遗留参数。这些遗留逻辑可能仍被当前后端处理，从而发现隐藏功能或敏感信息泄露。
- **前置条件**
- 已通过爬虫或目录扫描发现当前 JS 文件；
- 目标站点 JS 资源有历史版本（常见于大型 JS-heavy 站点）。
- **完整技法细节**
- 使用 waybackurls 或手动 Wayback Machine 查询 JS 文件历史。
- 下载旧版 JS，grep 搜索 api/, key=, secret=, token= 等关键词。
- 测试发现的旧端点或参数是否仍被当前版本接受（仅授权环境）。
- **适用目标画像**
- 前端重度依赖 JS、频繁迭代但后端兼容性强的站点；
- 使用 CDN 或未清理历史资源的 Web 应用。
- **为什么有效**
开发者常在重构时删除前端逻辑，但后端仍保留对旧参数/端点的处理，导致信息泄露或未授权访问。
- **手工验证流程（授权 / Lab only）**
- 在授权程序中找到当前 JS 文件。
- 查询 Wayback Machine 历史版本并下载。
- 对比新旧版本，提取遗留端点/参数。
- 使用测试账号在授权环境下请求验证，观察是否返回敏感信息或执行旧逻辑。
- 测试后立即向程序报告并建议清理历史资源。
- **可自动化部分**
- 脚本结合 waybackurls + grep 批量处理 JS 文件列表；
- 集成到 recon pipeline 中自动标记可疑旧端点。
- **误报/失败条件**
- 旧端点已被服务端彻底移除；
- JS 已压缩/混淆且未保留历史字符串；
- CDN 未开启历史归档。
- **授权边界**
仅在授权 Bug Bounty 程序中对归档内容进行测试。严禁对第三方归档服务或未授权站点进行大规模爬取。
- **报告 impact 角度**
- 信息泄露（硬编码密钥、内部端点）；
- 潜在未授权访问或业务逻辑绕过；
- 帮助程序清理历史遗留风险，提升整体安全。
- **相关案例链接**
- [https://x.com/intigriti/status/2004494400601129247](https://x.com/intigriti/status/2004494400601129247)

<!-- GROK_EXPANSION_END -->
