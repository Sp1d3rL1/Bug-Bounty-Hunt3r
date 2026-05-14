---
type: technique
category: new_method
derived_from_case: false
vuln_class: IAM Misconfiguration
source_url: https://blogs.jsmon.sh/exploiting-ci-cd-pipelines-aws-account-takeover-via-github-actions-oidc/
source_author: Isha Sangpal
source_date: 2026-04-17
collected_at: 2026-05-05
freshness: 2026
confidence: high
risk_level: low
target_types:
  - GitHub Actions + AWS
---

# AWS Account Takeover via GitHub Actions OIDC Wildcard Trust

## 核心思路

Set IAM role trust policy to repo:* allowing attacker GH repo OIDC assume-role

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `IAM Misconfiguration` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Full AWS account control without static creds in authorized bounty programs
- 适用场景：GitHub Actions + AWS
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。
- 先找 lab/本地靶场复现，再映射到授权目标。

## 适用目标画像

- GitHub Actions + AWS

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Full AWS account control without static creds in authorized bounty programs

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

- https://blogs.jsmon.sh/exploiting-ci-cd-pipelines-aws-account-takeover-via-github-actions-oidc/

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

# 核心思路
GitHub Actions OIDC 信任策略中使用通配符（如 `repo:*`）导致 IAM Role 可被任意仓库（包括测试者控制的仓库）通过 `AssumeRoleWithWebIdentity` 接管。无需泄露静态凭证，仅依赖策略逻辑缺陷即可实现云权限边界突破。
# 前置条件
- 目标组织公开或可枚举的 GitHub Workflow 文件（`.github/workflows/*.yml`）。
- AWS IAM Role 的 Trust Policy 包含 OIDC Provider `token.actions.githubusercontent.com` 且 `sub` 条件为通配符。
- 已授权测试的 AWS/Github Lab 环境（生产仅限 scope 内）。
# 完整技法细节
1. 搜索 GitHub 仓库中引用目标 Role ARN（如 `arn:aws:iam::ACCOUNT:role/ProdDeploymentRole`）。
2. 检查 IAM Trust Policy 是否包含：
```json
"Condition": {
"StringLike": {
"token.actions.githubusercontent.com:sub": "repo:*"
}
}
在测试者控制的公共仓库中创建 Workflow：
YAML
```text
name: AWS-OIDC-Test
on: [push]
permissions:
id-token: write
contents: read
jobs:
assume:
runs-on: ubuntu-latest
steps:
- uses: aws-actions/configure-aws-credentials@v4
with:
role-to-assume: arn:aws:iam::ACCOUNT:role/TargetRole
aws-region: us-east-1
- run: aws sts get-caller-identity
```
- Push 触发 Workflow，观察是否成功 assume 并返回临时凭证（仅读操作）。

# 适用目标画像
使用 GitHub Actions + AWS OIDC 的 SaaS / 开源项目 CI/CD 流水线，尤其是依赖 Terraform / CDK 部署的云原生组织。

# 为什么有效
OIDC 依赖 IAM Trust Policy 进行信任校验，通配符 repo:* 消除了仓库/组织限制，任何持有有效 JWT 的仓库均可 assume Role。GitHub OIDC Provider 公开可访问，无需秘密。

# 手工验证流程（授权 / Lab only）
- 在授权 Lab 中创建测试 AWS Account + GitHub Repo。
- 配置易受攻击的 IAM Role（通配符策略）。
- 使用上述 Workflow 测试 assume。
- 仅执行 aws sts get-caller-identity 和 aws iam get-role 等只读命令验证。
- 记录 Role ARN、Trust Policy 截图及 Workflow 日志作为 PoC。

# 可自动化部分
- GitHub 搜索 role-to-assume + configure-aws-credentials 结合 ARN 模式。
- 自定义脚本解析 Workflow 文件并检查 OIDC 配置。

# 误报/失败条件
- Trust Policy 使用 StringEquals + 精确 repo:org/repo:ref:refs/heads/main。
- 缺少 id-token: write 权限或 aud 检查缺失但 sub 已锁定。

# 授权边界
仅在明确授权的 Bug Bounty scope 或自建 Lab 内测试。禁止对生产 Role 执行任何写操作或数据访问。PoC 完成后立即删除测试 Workflow。

# 报告 impact 角度
- 完整 AWS Account 临时权限接管（S3、SSM、EC2 等）。
- CI/CD 供应链攻击向量，无需凭证泄露即可持久化。
- 高危业务影响：基础设施完全控制。

# 相关案例链接
- [https://blogs.jsmon.sh/exploiting-ci-cd-pipelines-aws-account-takeover-via-github-actions-oidc/](https://blogs.jsmon.sh/exploiting-ci-cd-pipelines-aws-account-takeover-via-github-actions-oidc/)
（Isha Sangpal 原帖）

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/cicd_github_actions.md -->

<!-- backlink: docs/checklists/cloud_aws_metadata_iam.md -->

<!-- backlink: docs/checklists/recon_methodology.md -->

<!-- backlink: docs/checklists/subdomain_takeover.md -->
