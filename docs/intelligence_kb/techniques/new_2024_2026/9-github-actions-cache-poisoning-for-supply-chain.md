---
type: technique
category: new_method
derived_from_case: false
vuln_class: Actions Cache Poisoning
source_url: https://adnanthekhan.com/tag/bugbounty/
source_author: Adnan Khan
source_date: 2026-03-03
collected_at: 2026-05-05
freshness: 2026
confidence: high
risk_level: medium
target_types:
  - GitHub Actions
---

# GitHub Actions Cache Poisoning for Supply Chain

## 核心思路

Poison cache key with malicious artifact in shared runner workflows

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Actions Cache Poisoning` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Persistent supply-chain compromise across dependent repos in authorized BB
- 适用场景：GitHub Actions
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 先识别 CDN、反向代理、cache key、vary header、normalization 和前后端协议差异。
- 只做低频、无破坏的 cache key/响应差异验证；避免影响真实用户缓存。
- 优先使用 PortSwigger lab 复现具体变体，再迁移为授权环境的最小化检测。

## 适用目标画像

- GitHub Actions

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Persistent supply-chain compromise across dependent repos in authorized BB

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

- https://adnanthekhan.com/tag/bugbounty/

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://adnanthekhan.com/tag/bugbounty/](https://adnanthekhan.com/tag/bugbounty/)
" author: "Adnan Khan / 2026-03-03" target_type: "GitHub Actions" confidence: "high" tags:
- github-actions
- cache-poisoning
- supply-chain
- ci-cd date: "2026-03-03"

## 核心思路
利用 GitHub Actions 共享 runner 的 cache 机制，通过污染特定 cache key 写入恶意 artifact，后续依赖该 workflow 的仓库在拉取 cache 时执行恶意代码，实现供应链持久化影响。

## 前置条件
- 目标仓库或相邻仓库使用 GitHub Actions 且启用 cache（actions/cache 或类似）。
- 存在可注入 workflow 的入口（如 issue、PR 或公开 fork）。
- 授权 Bug Bounty 程序允许在自有/测试仓库中验证。

## 完整技法细节
- 识别使用 cache 的 workflow（尤其是 checkout 后步骤）。
- 构造污染 cache key 的 payload（预测 key 并覆盖 artifact）。
- 在授权 lab 或测试仓库中注入恶意 action，验证 cache 持久化。
观察依赖仓库是否在后续 run 中拉取并执行污染内容。
：仅在自控测试仓库验证，不针对任何生产供应链执行。

## 适用目标画像
大规模使用 GitHub Actions、依赖共享 runner cache 的开源/企业仓库，尤其多仓库依赖场景（如 Angular 等）。

## 为什么有效
GitHub Actions cache 在 runner 间共享且 key 可预测/覆盖，后续 workflow 无条件信任 cache，导致持久化供应链风险。

## 手工验证流程（授权 / Lab only）
- 在自有 GitHub 测试仓库创建使用 cache 的 workflow。
- 注入污染 payload 并触发 run。
- 创建依赖仓库，运行相同 workflow 确认 cache 被污染并执行。
- 记录 cache key、artifact 差异作为证据。
- 立即清理测试仓库，不留任何恶意 artifact。

## 可自动化部分
使用 Adnan Khan 的 Cacheract 等开源工具（仅 lab 内）自动化 cache key 预测和污染测试。

## 误报/失败条件
- Workflow 未使用 cache 或 cache key 包含唯一随机值。
- 仓库设置了严格 workflow 权限或禁用 fork 运行。
- GitHub 平台已部署针对性防护。

## 授权边界
仅限授权 Bug Bounty 程序的自有测试仓库或完全控制的 lab 环境。严禁任何针对第三方仓库的真实供应链污染或破坏性操作。

## 报告 impact 角度
- 持久化供应链妥协，可影响下游所有依赖仓库的构建和发布流程。
- 低交互、高隐蔽性，属于高危 CI/CD 攻击向量。

## 相关案例链接
- [https://adnanthekhan.com/tag/bugbounty/](https://adnanthekhan.com/tag/bugbounty/)
- Adnan Khan Angular 供应链研究文章

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/cache_deception_poisoning.md -->

<!-- backlink: docs/checklists/cicd_github_actions.md -->

<!-- backlink: docs/checklists/recon_methodology.md -->
