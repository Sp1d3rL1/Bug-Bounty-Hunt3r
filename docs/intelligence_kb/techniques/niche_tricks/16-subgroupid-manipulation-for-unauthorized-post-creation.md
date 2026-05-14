---
type: technique
category: trick
derived_from_case: false
vuln_class: Broken Access Control
source_url: https://medium.com/@0xyz_/5-bac-bugs-in-one-app-
source_author: 0xyz_
source_date: 2025
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: low
target_types:
  - Group-based apps
---

# SubGroupId Manipulation for Unauthorized Post Creation

## 核心思路

Modify subGroupIds in API to share/create posts in unjoined subgroups

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Broken Access Control` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Exploits missing ownership checks on share/create; timing TOCTOU during removal
- 适用场景：Group-based apps
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。
- 测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。
- 重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。

## 适用目标画像

- Group-based apps

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Exploits missing ownership checks on share/create; timing TOCTOU during removal

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

- https://medium.com/@0xyz_/5-bac-bugs-in-one-app-

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://medium.com/@0xyz_/5-bac-bugs-in-one-app-](https://medium.com/@0xyz_/5-bac-bugs-in-one-app-)
" vuln_class: "Broken Access Control" one_line_trick: "Modify subGroupIds in API to share/create posts in unjoined subgroups" why_useful: "Exploits missing ownership checks on share/create; timing TOCTOU during removal" target_type: "Group-based apps" confidence: "high" type: "technique" tags: ["bac", "idor", "subgroup", "group-apps", "toctou"]

### 核心思路
在群组类应用API中，通过篡改subGroupIds参数绕过加入检查，实现未加入子群组的帖子创建/分享，利用所有权校验缺失和TOCTOU时序漏洞。

### 前置条件
- 目标为支持子群组（subgroups）的群组/论坛/协作应用。
- 已认证用户会话，可访问正常创建/分享帖子API。
- 识别包含subGroupIds数组的POST请求。

### 完整技法细节
- 捕获正常创建/分享帖子的API请求（通常POST /posts或/share）。
- 修改subGroupIds参数为未加入的子群组ID（可从其他用户响应或枚举获取）。
- 重放请求，观察是否成功在目标子群组创建/分享帖子。
- 利用TOCTOU：用户被移除子群组期间，API仍处理请求导致未授权操作。
- 仅在Lab环境验证，不执行真实分享。

### 适用目标画像
- 具有子群组功能的社交、协作、论坛或企业内部工具（如Slack-like、Discord-like群组App）。
- API未严格校验请求用户是否属于目标subGroupId。

### 为什么有效
服务器侧仅依赖客户端提交的subGroupIds进行操作，未进行所有权/成员资格二次校验；移除成员操作与API处理存在时序窗口（TOCTOU）。

### 手工验证流程（授权 / Lab only）
- 在授权Lab环境中创建多个子群组，加入/退出测试账号。
- 使用Burp捕获创建帖子请求，修改subGroupIds为未加入ID。
- 重放并确认响应成功但实际帖子出现在未授权群组。
- 立即删除测试帖子，记录前后截图。
- 仅使用benign测试数据。

### 可自动化部分
- Burp Intruder fuzz subGroupIds参数值（枚举已知群组ID）。
- 自定义Python脚本自动化成员状态切换+API请求测试（Lab only）。

### 误报/失败条件
- 服务器侧强制校验当前用户成员资格。
- subGroupIds被服务器重写或忽略。
- API使用UUID而非可预测ID导致枚举困难。

### 授权边界
仅限授权Bug Bounty程序中的群组应用API。禁止任何真实帖子创建/分享到生产群组或涉及真实用户数据；仅Lab验证。

### 报告 impact 角度
- 水平权限提升：未加入用户可在任意子群组创建内容，违反群组隔离。
- 业务影响：群组隐私泄露、垃圾信息泛滥或内部信息扩散。
- 合规风险：违反数据隔离和访问控制最佳实践。

### 相关案例链接
原Medium文章：
- [https://medium.com/@0xyz_/5-bac-bugs-in-one-app-](https://medium.com/@0xyz_/5-bac-bugs-in-one-app-)

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/api.md -->
