---
type: technique
category: evergreen
derived_from_case: false
vuln_class: Broken Access Control
source_url: X post 100 exploits list (real hunter)
source_author: @theXSSrat (X hunter)
source_date: 2025-04
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: low
target_types:
  - SaaS API
---

# API Versioning Bypass: Legacy /v1/ Endpoints Lack Patches in SaaS

## 核心思路

Test /v0 or /v1/user when /v2 is secured

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Broken Access Control` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Old versioning flaw exposes unpatched classic bugs in modern SaaS APIs
- 适用场景：SaaS API
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。
- 测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。
- 重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。

## 适用目标画像

- SaaS API

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Old versioning flaw exposes unpatched classic bugs in modern SaaS APIs

## 手工验证流程（授权 / Lab only）

1. 确认 scope、禁止项、速率限制与是否允许该功能测试。
2. 准备至少两个自有测试账号；多租户场景准备两个 organization/workspace。
3. 先完整走通正常业务流，记录对象 ID、角色、状态、token、请求路径。
4. 只替换一个变量或一步状态，观察服务端响应和后续副作用。
5. 用最小必要数据证明影响；不读取、不导出第三方真实数据。
6. 建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。
7. 测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。
8. 重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。

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

- X post 100 exploits list (real hunter)

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

### 核心思路
现代SaaS API通常升级到/v2并加强安全，但遗留/v1或/v0端点仍保持旧逻辑且未同步打补丁，通过版本回滚访问未修补的经典漏洞。

### 前置条件
- 目标SaaS应用暴露REST API，且使用版本化路径（如/v2/user/settings）。
- 已认证会话或API密钥（授权Lab环境）。
- 通过Burp或浏览器DevTools观察到/v2端点。

### 完整技法细节
- 识别当前安全端点（如/v2/user/settings返回403或限制数据）。
- 手动修改路径为/v1/user/settings或/v0/user/settings。
- 重放请求，观察是否返回更多数据、绕过访问控制或触发旧逻辑错误。
- 示例（来自@theXSSrat清单）：如果/v2/user/settings安全，则强制/v1/user/settings常暴露未打补丁的BAC或逻辑缺陷。

### 适用目标画像
- 多版本并存的SaaS平台（CRM、协作工具、支付系统）。
- 后端使用微服务或旧代码路径未完全弃用。
- 常见于快速迭代的初创SaaS企业。

### 为什么有效
开发团队专注于新版本安全，但遗留版本代码路径仍活跃且未同步安全更新，导致“版本不一致”成为隐藏的后门。

### 手工验证流程（授权 / Lab only）
- 在授权BB程序或自建SaaS Lab中创建测试用户。
- 使用Burp Repeater修改API路径从/v2切换到/v1。
- 对比响应：/v1是否返回额外敏感数据或绕过检查。
- 记录前后响应差异作为PoC。
- 立即停止测试，避免任何破坏性操作。

### 可自动化部分
- Burp Intruder或自定义脚本fuzz常见版本前缀（/v0、/v1、/api/v1、/legacy）。
- ZAP或自定义Python脚本批量测试已知端点版本。

### 误报/失败条件
- 所有版本均返回相同403或已统一打补丁。
- API严格强制版本头（如X-API-Version）而非路径。
- 端点已完全移除返回404。

### 授权边界
仅限授权Bug Bounty范围内的SaaS API端点。禁止对生产环境进行DoS、凭证填充或任何数据修改操作；仅路径切换验证。

### 报告 impact 角度
- 严重访问控制绕过：暴露旧版未修补漏洞，可能导致数据泄露或权限提升。
- 合规风险：遗留代码违反安全开发生命周期要求。
- 业务影响：未授权第三方可能利用遗留路径绕过现代防护。

### 相关案例链接
@theXSSrat Bug Bounty Checklist（包含API Versioning部分）：
- [https://x.com/theXSSrat/status/2041962050482794678](https://x.com/theXSSrat/status/2041962050482794678)
相关API版本不匹配利用讨论：
- [https://infosecwriteups.com/exploiting-api-version-mismatches-for-hidden-vulnerabilities-7680d854c0fb](https://infosecwriteups.com/exploiting-api-version-mismatches-for-hidden-vulnerabilities-7680d854c0fb)

<!-- GROK_EXPANSION_END -->
