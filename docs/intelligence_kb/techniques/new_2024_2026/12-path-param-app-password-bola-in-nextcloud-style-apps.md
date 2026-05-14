---
type: technique
category: new_method
derived_from_case: false
vuln_class: BOLA/IDOR
source_url: https://hackerone.com/reports/3382343
source_author: cyberjoker (via H1)
source_date: 2025-10-01
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: high
target_types:
  - Collab API
---

# Path Param + App Password BOLA in Nextcloud-style Apps

## 核心思路

Use app-specific passwords with swapped {userId} in /outOfOffice path

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `BOLA/IDOR` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Bypasses standard auth in API-heavy collab tools; niche for self-hosted targets
- 适用场景：Collab API
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。
- 测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。
- 重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。

## 适用目标画像

- Collab API

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Bypasses standard auth in API-heavy collab tools; niche for self-hosted targets

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

- https://hackerone.com/reports/3382343

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

id: 12 title: Path Param + App Password BOLA in Nextcloud-style Apps type: technique vuln_class: BOLA/IDOR author_date: cyberjoker (via H1) / 2025-10-01 source_url:
- [https://hackerone.com/reports/3382343](https://hackerone.com/reports/3382343)
one_line_trick: Use app-specific passwords with swapped {userId} in /outOfOffice path target_type: Collab API confidence: high tags: [bola, path-param, app-password, nextcloud]

## 核心思路
Nextcloud 类协作应用中，/ocs/v2.php/apps/dav/api/v1/outOfOffice/{userId} 等端点使用路径参数 {userId}，结合 app-specific password 认证时，未校验 userId 是否属于当前认证用户，导致任意用户可读取他人 Out-of-Office 数据。

## 前置条件
- Nextcloud（或类似 DAV/协作 API）v32+ 版本，启用 Out-of-Office 功能。
- 拥有 app password（通过 occ user:add-app-password 生成）。
- Lab 或授权程序中至少两个用户账号，且 victim 已配置 OOO 数据。

## 完整技法细节
- 为 attacker 和 victim 分别生成 app password。
- victim 配置 OOO 数据（POST /outOfOffice/victim）。
- attacker 使用自身 app password 发送 GET /outOfOffice/victim（路径参数替换）。
- 返回 200 并包含 victim 完整 OOO 信息（日期、消息、联系方式）。
：仅在自建 Nextcloud Lab 中执行读取操作，绝不修改或删除。

## 适用目标画像
- Nextcloud、ownCloud 及其他自托管协作工具。
- 使用 app password 认证的 API-heavy 企业应用。
- 任何路径参数暴露用户特定数据的协作平台。

## 为什么有效
端点标记 #[NoAdminRequired]，控制器直接使用路径 {userId} 查询数据，未与认证用户进行所有权比对；app password 绕过浏览器 session 限制，进一步放大攻击面。

## 手工验证流程（授权 / Lab only）
- 自建 Nextcloud Lab，创建 alice（victim）与 bob（attacker）。
- 用 occ 生成 app password。
- alice 配置 OOO，bob 用 app password GET /outOfOffice/alice。
- 确认返回 alice 数据（预期应 403）。
：仅 lab 读取测试；报告后立即验证修复（添加所有权检查）。

## 可自动化部分
- Python requests 脚本遍历用户名列表，批量查询 OOO 端点并导出 JSON。
- 支持 app password 头认证自动化。

## 误报/失败条件
- 端点已要求 admin 权限或明确文档化共享。
- 返回 404（无数据）而非敏感内容。
- 已实施 userId 与认证用户比对。

## 授权边界
仅限授权 Bug Bounty 程序或自控 Lab。禁止任何真实用户数据访问。边界：测试账号间读取，严格遵守程序 scope。

## 报告 impact 角度
：泄露个人行程、联系方式、实时可用状态（High）。
：违反 GDPR 等隐私预期。
：High，强调“app password + 路径参数组合绕过对象级授权”。

## 相关案例链接
- [https://hackerone.com/reports/3382343](https://hackerone.com/reports/3382343)

<!-- GROK_EXPANSION_END -->
