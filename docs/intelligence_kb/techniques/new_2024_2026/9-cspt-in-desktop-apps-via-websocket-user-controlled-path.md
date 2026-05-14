---
type: technique
category: new_method
derived_from_case: false
vuln_class: CSPT
source_url: https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-168-client-side-path-traversals-across-every-framework-with-xssdoctor
source_author: Critical Thinking Podcast (XSS Doctor)
source_date: 2026-04
collected_at: 2026-05-05
freshness: 2026
confidence: high
risk_level: medium
target_types:
  - desktop apps
  - IoT
---

# CSPT in Desktop Apps via WebSocket/User-Controlled Path

## 核心思路

Path": - /url: https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-168-client-side-path-traversals-across-every-framework-with-xssdoctor§CSPT§Path - text: traversal in desktop/WebSocket requests (non-web components)

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `CSPT` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Extends CSPT beyond browser to IoT/desktop; real authorized hunting example
- 适用场景：desktop apps/IoT
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 枚举 message listeners、URL fragment/query sink、client-side routing、sanitizer 配置和 trusted origins。
- 优先在本地或授权测试页面复现，真实项目只证明可控 sink 与安全影响。
- 关注 OAuth callback、embed/widget、support chat、docs preview 等富客户端功能。

## 适用目标画像

- desktop apps
- IoT

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Extends CSPT beyond browser to IoT/desktop; real authorized hunting example

## 手工验证流程（授权 / Lab only）

1. 确认 scope、禁止项、速率限制与是否允许该功能测试。
2. 准备至少两个自有测试账号；多租户场景准备两个 organization/workspace。
3. 先完整走通正常业务流，记录对象 ID、角色、状态、token、请求路径。
4. 只替换一个变量或一步状态，观察服务端响应和后续副作用。
5. 用最小必要数据证明影响；不读取、不导出第三方真实数据。
6. 枚举 message listeners、URL fragment/query sink、client-side routing、sanitizer 配置和 trusted origins。
7. 优先在本地或授权测试页面复现，真实项目只证明可控 sink 与安全影响。
8. 关注 OAuth callback、embed/widget、support chat、docs preview 等富客户端功能。

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

- https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-168-client-side-path-traversals-across-every-framework-with-xssdoctor

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-168-client-side-path-traversals-across-every-framework-with-xssdoctor](https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-168-client-side-path-traversals-across-every-framework-with-xssdoctor)
" vuln_class: "CSPT" one_line_trick: "Path traversal in desktop/WebSocket requests beyond browser-only flows" why_useful: "Extends CSPT beyond browser to IoT/desktop; real authorized hunting example" target_type: "desktop apps/IoT" confidence: "high" tags: ["cspt", "desktop-app", "websocket", "bugbounty"]

# CSPT in Desktop Apps via WebSocket/User-Controlled Path

## 核心思路
在桌面应用（Electron 等）或 IoT 设备中使用 WebSocket 或用户可控路径发起请求时，路径遍历（../）可绕过浏览器同源限制，直接访问本地文件系统或内部 API，实现客户端路径遍历攻击。

## 前置条件
- 桌面/IoT 应用使用 WebSocket 或 fetch-like 请求，且路径参数由用户输入控制。
- 应用未对路径进行规范化或过滤（常见于框架 useParams 双重解码等）。
- 应用以高权限运行或可访问本地资源。

## 完整技法细节
- 识别用户可控路径参数（URL 参数、WebSocket 消息字段）。
- 注入 ../ 序列，触发路径遍历。
- 桌面环境无浏览器 fetch 限制，WebSocket 可直接请求本地文件或内部服务。
- 结合 protobuf 或特定框架特性进一步提升影响。

## 适用目标画像
- Electron、Tauri 等桌面应用，或使用 WebSocket 的 IoT/嵌入式设备。
- 任何非纯浏览器环境的客户端应用，存在用户可控路径拼接场景。

## 为什么有效
浏览器 CSPT 受 SOP 限制，而桌面应用/WebSocket 运行在更宽松的环境中，路径遍历可直接影响本地文件系统或内部通信。

## 手工验证流程（授权 / Lab only）
- 在授权 Lab 环境中搭建桌面应用或 IoT 模拟器。
- 构造包含 ../ 的 WebSocket 路径 payload。
- 触发请求，观察是否读取本地测试文件。
- 记录 PoC，仅在自有环境验证。

## 可自动化部分
- 自定义脚本或 Burp 扩展自动化 WebSocket 路径 fuzz（授权 Lab 限定）。
- 框架特定 sink 扫描模板。

## 误报/失败条件
- 应用对路径进行严格规范化或白名单过滤。
- WebSocket 实现已进行路径清理。
- 应用以沙箱模式运行（低权限）。

## 授权边界
仅限授权 Bug Bounty 程序中桌面/IoT 目标或自有 Lab 环境。严禁任何破坏性操作或真实数据访问。

## 报告 impact 角度
- 客户端路径遍历导致本地文件读取、内部 API 滥用或配置泄露。
- 业务影响：在桌面/IoT 场景下可能造成本地数据泄露或设备接管，高危影响。
- 建议修复：框架层路径规范化 + 输入验证。

## 相关案例链接
- [HackerNotes Ep. 168 - Client-Side Path Traversals Across Every Framework, with XSSDoctor](https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-168-client-side-path-traversals-across-every-framework-with-xssdoctor)

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/cors_postmessage_websocket.md -->

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->

<!-- backlink: docs/checklists/prototype_pollution_xss_chain.md -->
