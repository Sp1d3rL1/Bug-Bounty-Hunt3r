---
type: technique
category: trick
derived_from_case: false
vuln_class: Access Control
source_url: https://x.com/theXSSrat/status/2049049212076118387
source_author: theXSSrat
source_date: 2026-04-28
collected_at: 2026-05-05
freshness: 2026
confidence: high
risk_level: low
target_types:
  - Web APIs
---

# BAC via HTTP Method Swap Version Rollback Array ID Injection

## 核心思路

Swap GET↔POST, rollback to /v1/ legacy endpoint, or inject ID as array [123]

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Access Control` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Exploits inconsistent auth logic across HTTP methods versions or data structures
- 适用场景：Web APIs
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。
- 测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。
- 重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。

## 适用目标画像

- Web APIs

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Exploits inconsistent auth logic across HTTP methods versions or data structures

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

- https://x.com/theXSSrat/status/2049049212076118387

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://x.com/theXSSrat/status/2049049212076118387](https://x.com/theXSSrat/status/2049049212076118387)
" author: "theXSSrat / 2026-04-28" target_type: "Web APIs" confidence: "high" tags:
- bac
- access-control
- method-swap
- version-rollback
- array-injection date: "2026-04-28"

## 核心思路
针对访问控制不一致问题，通过 HTTP 方法切换（GET↔POST）、版本回滚至遗留端点（/v1/）或将 ID 注入为数组形式（[123]），触发后端不同处理逻辑从而实现 Broken Access Control（BAC）。

## 前置条件
- 目标 API 存在多版本或多方法支持的端点。
- 认证/授权逻辑在不同方法、版本或数据类型间实现不一致。
- 授权 Bug Bounty 程序或 lab 环境。

## 完整技法细节
：将 GET 请求改为 POST/PUT（或反之），观察授权检查是否被跳过。
：将 /v2/ 端点强制改为 /v1/，利用遗留版本未打补丁。
：将 {"id": 123} 改为 {"id": [123, 456]}，后端可能仅处理第一个或全部而跳过权限校验。
结合使用 Burp Repeater 测试响应差异。
，不针对真实用户数据。

## 适用目标画像
采用 RESTful 或 GraphQL API、存在多版本共存或认证逻辑分散在中间件/控制器中的 Web 应用。

## 为什么有效
开发者常假设“相同端点不同方法/版本/数据格式”会统一检查权限，但实际实现中逻辑路径差异导致绕过。

## 手工验证流程（授权 / Lab only）
- 在授权环境中定位受保护的资源端点（如 /user/settings）。
- 分别测试 GET/POST 切换、/v1/ vs /v2/、ID 改为数组形式。
- 使用测试账号 A 尝试访问账号 B 的资源，确认是否成功。
- 记录原始 vs 绕过请求/响应作为 PoC。
- 仅限 lab 验证边界，不执行任何数据修改。

## 可自动化部分
Burp Intruder 使用 payload 列表自动化方法切换、版本枚举和数组变体测试。

## 误报/失败条件
- 所有方法/版本均使用统一授权中间件。
- WAF 拦截方法变更或数组 payload。
- 后端严格类型检查拒绝数组 ID。

## 授权边界
仅在授权 Bug Bounty 程序的自有测试资源或完全控制的 lab 环境中操作。禁止针对生产用户数据的任何访问尝试。

## 报告 impact 角度
- 绕过访问控制可导致水平/垂直权限提升、敏感数据泄露或业务逻辑破坏。
- 常见于遗留代码或快速迭代的 API 场景。

## 相关案例链接
- [https://x.com/theXSSrat/status/2049049212076118387](https://x.com/theXSSrat/status/2049049212076118387)
- BAC 逻辑绕过通用方法论

<!-- GROK_EXPANSION_END -->
