---
risk_level: high
collected_at: 2026-05-05
id: 14
title: GitHub Actions pull_request_target + checkout without persist-credentials:false
type: technique
vuln_class: Actions Credential Exposure
source_author: Multiple hunters (Adnan Khan et al.)
source_date: 2024-2025
source_url: https://adnanthekhan.com/
one_line_trick: Omit persist-credentials:false in actions/checkout to leak token
why_useful: RCE/secret 验证暴露风险（不导出真实敏感数据） in CI/CD pipelines via authorized BB
target_types:
  - GitHub Actions
confidence: high
tags: [bug-bounty, github-actions, ci-cd, credential-exposure, supply-chain]
---
# GitHub Actions pull_request_target + checkout without persist-credentials:false
## 核心思路
在 `pull_request_target` 事件触发的 workflow 中，GITHUB_TOKEN 默认拥有仓库写权限。如果 `actions/checkout` 步骤未显式设置 `persist-credentials: false`，checkout 操作会将 token 持久化到 `.git/config` 或 credential helper 中。随后 PR 中 attacker-controlled 代码（来自 fork 的 head.sha）即可读取该 token，实现凭证泄露或后续恶意操作。
## 前置条件
- 目标仓库存在使用 `on: pull_request_target` 的 workflow
- workflow 中包含 `uses: actions/checkout` 且未设置 `persist-credentials: false`（默认行为会导致持久化）
- 仓库允许外部 fork 提交 PR（大多数开源仓库默认允许）
- workflow 后续步骤会执行 checkout 后的代码（如 run: 脚本、setup 等）
## 完整技法细节
1. 发现目标仓库的 `.github/workflows/*.yml` 中存在 `pull_request_target` + `checkout` 组合。
2. 创建 fork 并提交包含无害测试 payload 的 PR（例如在后续 run 步骤中 `读取自有 lab 中的合成标记文件 或使用 git credential 提取 token）。
3. PR 触发 workflow：pull_request_target 在 base branch 上下文运行，checkout 使用 attacker 的 head.sha 代码。
4. 因未设置 `persist-credentials: false`，token 被持久化，恶意代码可直接读取并 验证暴露风险（不导出真实敏感数据）（例如 记录到自有 lab 日志端点）或使用 token 进行 push、create release 等操作。
**重要**：仅在授权 BB 程序或自有 lab 仓库中测试，严禁在未授权仓库进行真实 PR 提交。
## 适用目标画像
- 使用 GitHub Actions 的开源/企业仓库
- CI/CD pipeline 依赖 pull_request_target（常见于 label、comment 自动化场景）
- 未遵循 GitHub 官方最佳实践（persist-credentials: false + token 最小权限）
## 为什么有效
`pull_request_target` 赋予 base repo 的高权限 GITHUB_TOKEN，而 checkout 未禁用 credential persist 时，untrusted PR 代码即可直接访问该 token。2024-2025 年多起供应链攻击均利用此模式实现秘密泄露或仓库接管。
## 手工验证流程（授权 / Lab only）
1. 在自有测试仓库或授权 BB 程序中创建测试 workflow（pull_request_target + checkout）。
2. 故意省略 `persist-credentials: false`。
3. 从 fork 提交 PR，PR 中包含读取 `.git/config` 或 credential helper 的 payload。
4. 观察 workflow 日志或 验证暴露风险（不导出真实敏感数据） 结果，确认 token 泄露。
5. 立即修复并验证设置 `persist-credentials: false` 后是否阻断。
**风险边界**：仅限 lab/self-owned repo，严禁真实 验证暴露风险（不导出真实敏感数据） 第三方 secret。
## 可自动化部分
- 使用 Gato 或自研 scanner 批量枚举公开仓库的 workflow YAML，检测 `pull_request_target` + `checkout` 且无 `persist-credentials: false`。
- GitHub API 搜索 workflow 文件内容。
## 误报/失败条件
- workflow 已设置 `persist-credentials: false`
- GITHUB_TOKEN 权限被显式降为 read-only 且无 secrets
- workflow 使用 `ref: github.event.pull_request.base.sha` 而非 head.sha
- 仓库启用 require approval for first-time contributors
## 授权边界
仅在明确授权 Bug Bounty 程序（允许 CI/CD 测试）或自有 lab 环境中验证。禁止向未授权仓库提交真实 PR 进行测试。
## 报告 impact 角度
- 潜在 GITHUB_TOKEN 泄露 → 仓库内容修改、release 篡改、secret 验证暴露风险（不导出真实敏感数据）
- 供应链攻击风险：影响所有使用该 Actions 的下游用户
- 符合高危 CI/CD 凭证暴露，建议 Critical/High 等级
## 相关案例链接
- https://adnanthekhan.com/ （Adnan Khan 系列文章）
- 官方 GitHub Docs: https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions


> 安全边界：本卡仅用于授权项目、靶场或自有环境；任何涉及凭证、CI/CD、支付、账号状态或真实用户数据的验证都必须使用合成数据和最小影响证明。

<!-- backlink: docs/checklists/cicd_github_actions.md -->

<!-- backlink: docs/checklists/recon_methodology.md -->
