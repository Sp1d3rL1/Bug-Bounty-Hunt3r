---
type: technique
category: new_method
derived_from_case: true
vuln_class: cache deception/poisoning
source_url: https://portswigger.net/research/gotta-cache-em-all
source_author: Martin Doyhenard (PortSwigger)
source_date: 2024-08
collected_at: 2026-05-05
freshness: 2024
confidence: high
risk_level: medium
target_types:
  - CDNs (Cloudflare
  - Akamai) and frameworks
---

# Derived technique from case: Gotta Cache 'Em All: Novel Cache Deception and Poisoning via URL Parsing Quirks

## 核心思路

Delimiter (; # %00) and ../ normalization diffs between CDN/origin poison arbitrary paths

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `cache deception/poisoning` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Bypasses cache key logic on Cloudflare/Akamai for deception or poisoning; practical BB testing tricks
- 适用场景：CDNs (Cloudflare, Akamai) and frameworks
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 先识别 CDN、反向代理、cache key、vary header、normalization 和前后端协议差异。
- 只做低频、无破坏的 cache key/响应差异验证；避免影响真实用户缓存。
- 优先使用 PortSwigger lab 复现具体变体，再迁移为授权环境的最小化检测。

## 适用目标画像

- CDNs (Cloudflare
- Akamai) and frameworks

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Bypasses cache key logic on Cloudflare/Akamai for deception or poisoning; practical BB testing tricks

## 手工验证流程（授权 / Lab only）

1. 确认 scope、禁止项、速率限制与是否允许该功能测试。
2. 准备至少两个自有测试账号；多租户场景准备两个 organization/workspace。
3. 先完整走通正常业务流，记录对象 ID、角色、状态、token、请求路径。
4. 只替换一个变量或一步状态，观察服务端响应和后续副作用。
5. 用最小必要数据证明影响；不读取、不导出第三方真实数据。
6. 先识别 CDN、反向代理、cache key、vary header、normalization 和前后端协议差异。
7. 只做低频、无破坏的 cache key/响应差异验证；避免影响真实用户缓存。
8. 优先使用 PortSwigger lab 复现具体变体，再迁移为授权环境的最小化检测。

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

- https://portswigger.net/research/gotta-cache-em-all

<!-- backlink: docs/checklists/cache_deception_poisoning.md -->
