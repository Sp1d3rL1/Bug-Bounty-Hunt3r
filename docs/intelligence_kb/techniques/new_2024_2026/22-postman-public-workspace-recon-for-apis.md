---
type: technique
category: new_method
derived_from_case: false
vuln_class: APIs
source_url: https://x.com/xhackio/status/
source_author: xhackio
source_date: 2026-04
collected_at: 2026-05-05
freshness: 2026
confidence: high
risk_level: low
target_types:
  - APIs
---

# Postman public workspace recon for APIs

## 核心思路

Search Postman for target company workspaces → test endpoints

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `APIs` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Discovers undocumented APIs leading to IDOR/SSRF in BB programs
- 适用场景：APIs
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。
- 先找 lab/本地靶场复现，再映射到授权目标。

## 适用目标画像

- APIs

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Discovers undocumented APIs leading to IDOR/SSRF in BB programs

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

- https://x.com/xhackio/status/

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://x.com/xhackio/status/](https://x.com/xhackio/status/)
" author: "xhackio / 2026-04" target_type: "APIs" confidence: "high" tags:
- postman
- api-recon
- undocumented-endpoints
- bugbounty-recon date: "2026-04"

## 核心思路
通过 Postman 公共工作区搜索功能，查找目标公司或员工创建的公开 workspace，提取其中保存的 API 集合、环境变量和测试请求，从而发现未文档化的内部/测试端点。

## 前置条件
- 目标公司名称、品牌词或员工邮箱可用于 Postman 搜索。
- Postman 平台存在公开 workspace（默认公开或误设权限）。
- 授权 Bug Bounty 程序允许被动 recon。

## 完整技法细节
- 在 Postman 官网搜索目标公司名、产品名或域名。
- 打开匹配的公共 workspace，浏览 Collections、Environments 和 Requests。
- 提取 API 端点、Header、Auth token 示例和参数。
在授权 lab 或 BB 范围内使用提取的端点进行测试，寻找 IDOR/SSRF 等问题。
，禁止任何凭证重用或未授权访问。

## 适用目标画像
拥有大量 API 开发团队、使用 Postman 协作且 workspace 可能误设公开权限的现代 Web/移动应用公司。

## 为什么有效
开发者常将测试 workspace 设为公开，泄露内部 API 设计、隐藏端点和配置细节，成为被动 recon 的金矿。

## 手工验证流程（授权 / Lab only）
- 在授权 BB 程序中搜索目标相关 Postman workspace。
- 记录发现的未文档化端点。
- 在自有测试账号或 lab 环境中重现并测试端点功能。
- 确认是否导致业务逻辑漏洞（如 IDOR）。
- 仅被动观察，不执行破坏性操作。

## 可自动化部分
使用 Postman API 或自定义爬虫脚本批量搜索并导出 workspace 元数据。

## 误报/失败条件
- 所有 workspace 已设为私有。
- 搜索结果无相关公司信息。
- 提取端点已在生产环境中移除或受严格访问控制。

## 授权边界
仅限公开 Postman 搜索和授权 BB 程序的测试环境。禁止访问任何需要凭证的 workspace 或对未授权目标执行 API 调用。

## 报告 impact 角度
- 发现未文档化 API 端点，可链式触发 IDOR、SSRF、权限绕过等高危漏洞。
- 暴露内部配置提升整体攻击面。

## 相关案例链接
- [https://x.com/xhackio/status/](https://x.com/xhackio/status/)
- Postman 公开 workspace 泄露相关安全报告

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/recon_methodology.md -->
