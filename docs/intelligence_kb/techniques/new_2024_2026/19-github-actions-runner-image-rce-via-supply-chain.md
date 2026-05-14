---
risk_level: high
collected_at: 2026-05-05
id: 19
title: GitHub Actions Runner Image RCE via Supply Chain
type: technique
vuln_class: Actions Runner Compromise
source_author: Adnan Khan
source_date: 2024-01-05
source_url: https://johnstawinski.com/2024/01/05/worse-than-solarwinds-three-steps-to-hack-blockchains-github-and-ml-through-github-actions/
one_line_trick: Abuse runner image build process for persistent RCE (GitHub BB $20k)
why_useful: Full pipeline control in authorized high-profile BB programs
target_types:
  - GitHub Actions
confidence: high
tags: [bug-bounty, github-actions, supply-chain, runner-image, rce]
---
# GitHub Actions Runner Image RCE via Supply Chain
## 核心思路
通过向 GitHub 官方 `actions/runner-images` 等 runner image 构建仓库提交 PR，触发其 CI/CD workflow，利用 non-ephemeral self-hosted runner 或构建流程中的权限，注入持久化 payload，最终污染所有 GitHub-hosted runner 的基础镜像，实现对数百万 CI/CD pipeline 的供应链 RCE。
## 前置条件
- 目标 runner image 仓库（如 actions/runner-images）允许外部 contributor PR 并触发 workflow
- 使用 non-ephemeral runner 或构建过程中存在持久化步骤
- 构建 workflow 拥有足够权限（默认 approval 设置）
## 完整技法细节
1. 成为仓库 contributor（通过其他低危 issue/PR）。
2. 提交恶意 PR 修改构建脚本或 Dockerfile。
3. PR 触发 CI workflow，在 non-ephemeral runner 上执行 payload（写入持久化持久化风险标记）。
4. 后续所有使用该 runner image 的 workflow 均继承持久化风险标记，实现全局 RCE。
**仅限授权 BB 程序**：GitHub 官方程序中 Adnan Khan 已成功报告并获 $20k 奖励。
## 适用目标画像
- GitHub 官方或大型开源项目的 runner image 构建仓库
- 使用 GitHub-hosted runners 的高价值 BB 程序（区块链、ML、基础设施）
- CI/CD 供应链关键节点
## 为什么有效
runner image 是所有 GitHub Actions 的基础，一旦污染即可影响全球数百万 pipeline。2024 年 Adnan Khan & John Stawinski 团队利用此链路成功攻破 PyTorch 等高价值目标。
## 手工验证流程（授权 / Lab only）
1. 在自有 fork 的 runner image 测试仓库中复现构建流程。
2. 模拟 non-ephemeral runner 环境，注入测试 payload（仅 echo 或 log）。
3. 验证新镜像是否携带持久化效果。
4. 立即清理 lab 环境。
**风险边界**：严禁对生产 runner image 进行任何真实修改，仅 lab 验证。
## 可自动化部分
- 监控公开 runner image 仓库的 PR 和 workflow 配置
- 使用 Gato-X 等工具扫描自托管 runner 暴露点
## 误报/失败条件
- 仓库使用 ephemeral runners
- PR 需要 maintainer approval 且无自动触发
- 构建流程已实施严格 code review 和 SBOM 检查
## 授权边界
仅限 GitHub Bug Bounty 官方程序或其他明确授权测试 CI/CD 供应链的 BB 范围。禁止任何未授权仓库操作。
## 报告 impact 角度
- 全球 GitHub-hosted runner 供应链污染
- 可导致下游仓库 secret 泄露、代码篡改、持久化风险标记植入
- 影响数百万开发者 CI/CD 环境，属于 Critical 级别
## 相关案例链接
- https://johnstawinski.com/2024/01/05/worse-than-solarwinds-three-steps-to-hack-blockchains-github-and-ml-through-github-actions/
- https://adnanthekhan.com/2023/12/20/one-supply-chain-attack-to-rule-them-all/


> 安全边界：本卡仅用于授权项目、靶场或自有环境；任何涉及凭证、CI/CD、支付、账号状态或真实用户数据的验证都必须使用合成数据和最小影响证明。
