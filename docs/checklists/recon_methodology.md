---
id: clk-recon-methodology
title: Reconnaissance Methodology (Recon × OSINT × GitHub)
owasp_anchor: [WSTG-INFO]
cwe: [CWE-200, CWE-540]
severity_typical: P3-P5
playbook: playbooks/recon.yaml
last_updated: 2026-05-15
sources:
  - docs/intelligence_kb/cases/researcher_writeups/1-artipacked-github-actions-artifact-token-leak.md
  - docs/intelligence_kb/cases/researcher_writeups/1-comment-and-control-prompt-injection-to-credential-theft-in-claude-code-gemini-cli-git.md
  - docs/intelligence_kb/cases/researcher_writeups/10-idor-hunting-with-burp-suite-1000-order-api-exposure.md
  - docs/intelligence_kb/cases/researcher_writeups/107-2-comment-and-control-prompt-injection-to-credential-theft-in-claude-code-gemini-c.md
  - docs/intelligence_kb/cases/researcher_writeups/107-4-ai-agents-identity-risk-supply-chain-attacks-trivy-action-compromise.md
  - docs/intelligence_kb/cases/researcher_writeups/11-codeqleaked-debug-artifacts-exposing-github-tokens.md
  - docs/intelligence_kb/cases/researcher_writeups/12-autogpt-ssrf-protection-bypass-to-internal-services.md
  - docs/intelligence_kb/cases/researcher_writeups/16-hackerbot-claw-autonomous-github-actions-exploitation-2026.md
  - docs/intelligence_kb/cases/researcher_writeups/17-5500-recon-only-bug-via-passive-enum-to-internal-config.md
  - docs/intelligence_kb/cases/researcher_writeups/18-prompt-injection-in-github-actions-ai-agents-claude-copilot.md
  - docs/intelligence_kb/cases/researcher_writeups/2-sign-in-as-anyone-bypassing-saml-sso-with-parser-differentials.md
  - docs/intelligence_kb/cases/researcher_writeups/23-azure-storage-account-cheat-sheet-recon-tricks.md
  - docs/intelligence_kb/cases/researcher_writeups/23-permutation-found-staging2-internal-critical-vuln.md
  - docs/intelligence_kb/cases/researcher_writeups/25-cve-2026-3854-github-rce-via-git-push-pipeline.md
  - docs/intelligence_kb/cases/researcher_writeups/3-ci-cd-metadata-tokens-leaked-via-js-files.md
  - docs/intelligence_kb/cases/researcher_writeups/4-github-copilot-config-hijack-via-prompt-injection-month-of-ai-bugs.md
  - docs/intelligence_kb/cases/researcher_writeups/8-github-hidden-unicode-bypass-of-utf-warning-filter.md
  - docs/intelligence_kb/cases/researcher_writeups/8-pwn-request-in-google-s-flank-github-actions-workflow.md
  - docs/intelligence_kb/review_queue/1-bug-bounty-hunting-methodology-2025.md
  - docs/intelligence_kb/review_queue/10-cloudfox-cloud-attack-surface-mapper.md
  - docs/intelligence_kb/review_queue/15-bug-bounty-methodology-2025-ci-cd-cloud-section.md
  - docs/intelligence_kb/review_queue/2-bug-bounty-recon-for-everyone.md
  - docs/intelligence_kb/review_queue/21-graphql-enum-tool-for-juicy-types-and-mutations.md
  - docs/intelligence_kb/review_queue/21-reconninja-v7-1-cloud-bucket-github-osint-plugin.md
  - docs/intelligence_kb/review_queue/21-ultimate-recon-guide-for-bug-bounty-hunters-2025.md
  - docs/intelligence_kb/review_queue/25-critical-thinking-bug-bounty-podcast-attacking-oauth-2-1.md
  - docs/intelligence_kb/review_queue/3-my-complete-recon-workflow-for-bug-bounty-hunting-2025-edition.md
  - docs/intelligence_kb/review_queue/4-2025-github-recon-checklist-for-bug-hunters.md
  - docs/intelligence_kb/review_queue/5-recon-for-bug-bounty-8-essential-tools.md
  - docs/intelligence_kb/review_queue/6-recon-series-recap-ultimate-guide-to-bug-bounty-reconnaissance.md
  - docs/intelligence_kb/review_queue/resource-1-bug-bounty-hunting-methodology-2025.md
  - docs/intelligence_kb/review_queue/resource-10-cloudfox-cloud-attack-surface-mapper.md
  - docs/intelligence_kb/review_queue/resource-15-bug-bounty-methodology-2025-ci-cd-cloud-section.md
  - docs/intelligence_kb/review_queue/resource-2-bug-bounty-recon-for-everyone.md
  - docs/intelligence_kb/review_queue/resource-21-graphql-enum-tool-for-juicy-types-and-mutations.md
  - docs/intelligence_kb/review_queue/resource-21-reconninja-v7-1-cloud-bucket-github-osint-plugin.md
  - docs/intelligence_kb/review_queue/resource-21-ultimate-recon-guide-for-bug-bounty-hunters-2025.md
  - docs/intelligence_kb/review_queue/resource-25-critical-thinking-bug-bounty-podcast-attacking-oauth-2-1.md
  - docs/intelligence_kb/review_queue/resource-3-my-complete-recon-workflow-for-bug-bounty-hunting-2025-edition.md
  - docs/intelligence_kb/review_queue/resource-4-2025-github-recon-checklist-for-bug-hunters.md
  - docs/intelligence_kb/review_queue/resource-5-recon-for-bug-bounty-8-essential-tools.md
  - docs/intelligence_kb/review_queue/resource-6-recon-series-recap-ultimate-guide-to-bug-bounty-reconnaissance.md
  - docs/intelligence_kb/techniques/new_2024_2026/10-authenticated-katana-crawling.md
  - docs/intelligence_kb/techniques/new_2024_2026/12-s3-misconfig-via-aws-s3-ls-no-sign-request-on-403.md
  - docs/intelligence_kb/techniques/new_2024_2026/14-environment-var-exfil-via-ps-auxeww-in-agent-tool-calls-comment-and-control-variant.md
  - docs/intelligence_kb/techniques/new_2024_2026/14-gau-wayback-for-historical-endpoints.md
  - docs/intelligence_kb/techniques/new_2024_2026/14-github-actions-pull-request-target-checkout-without-persist-credentials-false.md
  - docs/intelligence_kb/techniques/new_2024_2026/15-vhost-fuzzing-with-ffuf-on-ips.md
  - docs/intelligence_kb/techniques/new_2024_2026/17-cloud-recon-2-0-ephemeral-resources-multi-cloud-enum.md
  - docs/intelligence_kb/techniques/new_2024_2026/19-github-actions-runner-image-rce-via-supply-chain.md
  - docs/intelligence_kb/techniques/new_2024_2026/19-github-dorking-for-leaked-subs-secrets.md
  - docs/intelligence_kb/techniques/new_2024_2026/2-aws-account-takeover-via-github-actions-oidc-wildcard-trust.md
  - docs/intelligence_kb/techniques/new_2024_2026/20-naabu-httpx-pipeline-after-subfinder.md
  - docs/intelligence_kb/techniques/new_2024_2026/201-5-claude-bug-bounty-hunter-ai-assisted-recon-for-oauth-and-graphql.md
  - docs/intelligence_kb/techniques/new_2024_2026/22-postman-public-workspace-recon-for-apis.md
  - docs/intelligence_kb/techniques/new_2024_2026/23-html-comment-injection-for-invisible-pi-in-markdown-processed-ai-agents.md
  - docs/intelligence_kb/techniques/new_2024_2026/24-github-dorking-for-ci-cd-secrets-in-workflows.md
  - docs/intelligence_kb/techniques/new_2024_2026/24-gowitness-nuclei-for-visual-template-scan.md
  - docs/intelligence_kb/techniques/new_2024_2026/3-clairvoyance-for-schema-extraction-when-introspection-disabled.md
  - docs/intelligence_kb/techniques/new_2024_2026/6-gcs-testpermissions-api-for-permission-enumeration.md
  - docs/intelligence_kb/techniques/new_2024_2026/7-alterx-permutation-scanning.md
  - docs/intelligence_kb/techniques/new_2024_2026/9-amass-track-for-new-subdomains.md
  - docs/intelligence_kb/techniques/new_2024_2026/9-github-actions-cache-poisoning-for-supply-chain.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-1-artipacked-github-actions-artifact-token-leak.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-1-comment-and-control-prompt-injection-to-credential-theft-in-claude-code-g.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-11-codeqleaked-debug-artifacts-exposing-github-tokens.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-16-hackerbot-claw-autonomous-github-actions-exploitation-2026.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-17-5500-recon-only-bug-via-passive-enum-to-internal-config.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-18-prompt-injection-in-github-actions-ai-agents-claude-copilot.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-23-permutation-found-staging2-internal-critical-vuln.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-25-cve-2026-3854-github-rce-via-git-push-pipeline.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-3-ci-cd-metadata-tokens-leaked-via-js-files.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-4-github-copilot-config-hijack-via-prompt-injection-month-of-ai-bugs.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-8-pwn-request-in-google-s-flank-github-actions-workflow.md
  - docs/intelligence_kb/techniques/niche_tricks/101-5-hackerone-graphql-and-oauth-top-reports-2025-2026.md
  - docs/intelligence_kb/techniques/niche_tricks/107-3-what-s-coming-to-our-github-actions-2026-security-roadmap.md
  - docs/intelligence_kb/techniques/niche_tricks/19-pdf-log4shell-payload-crafting-for-processors.md
  - docs/intelligence_kb/techniques/niche_tricks/2-asn-pivot-on-ips-from-js-api-responses.md
  - docs/intelligence_kb/techniques/niche_tricks/3-clairvoyance-for-schema-extraction-when-introspection-disabled.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-2-sign-in-as-anyone-bypassing-saml-sso-with-parser-differentials.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-23-azure-storage-account-cheat-sheet-recon-tricks.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-8-github-hidden-unicode-bypass-of-utf-warning-filter.md
maturity: extending
---

# Reconnaissance Methodology Checklist

> 双语 / Bilingual: 元能力清单 — 不直接对应单一漏洞类，而是给所有其他 checklist
> 提供 "你怎么找到值得测的资产" 的事实库索引。
> Authorization-only：仅扫授权范围内的资产。所有自动化工具都受 `safe_automation_rules.md` 守门。

---

## 1. Subdomain & DNS Recon

### 1.1 Passive
- [ ] 多源被动子域：subfinder + assetfinder + amass intel + chaos
- [ ] 证书透明度：crt.sh / censys / google CT mining
- [ ] DNS 历史：securitytrails / virustotal passive DNS / waybackmachine
- [ ] WHOIS / RDAP 反查同 owner 的其他域
- [ ] 反向 SSL 证书：相同 SAN/CN 的资产

### 1.2 Active (低风险)
- [ ] DNS bruteforce: shuffledns + commonspeak2 wordlist (rate 控制 < 100 qps)
- [ ] vhost fuzzing: 拿到 IP 后用 ffuf -H "Host: FUZZ.target.com"
- [ ] PTR / NS / MX / TXT 记录全收集
- [ ] zone transfer 试一下（很少成功但偶有）

## 2. URL & Endpoint Discovery

- [ ] gau + waybackurls + katana + hakrawler 多源 URL 收集
- [ ] JS 端点抽取：linkfinder + getJS + subjs + xnLinkFinder
- [ ] OpenAPI/Swagger/Postman/GraphQL schema 文件直接 grep
- [ ] 移动 APK/IPA 反编译抓 endpoint：jadx / apktool / mobsf
- [ ] 历史 URL 去重 + URL pattern 抽象：`gau target.com | uro`
- [ ] 参数发现：arjun + paramspider
- [ ] 隐藏路径 fuzz: ffuf + 自定义 wordlist (按 tech_stack 选)

## 3. GitHub OSINT

### 3.1 Code Search
- [ ] `<company> language:python "API_KEY"` 类查询（Github Code Search）
- [ ] `org:<company>` + 关键 keyword: token / secret / private / config
- [ ] gitleaks / trufflehog 扫历史 commit
- [ ] Github Actions workflow 文件：`.github/workflows/*.yml` 找 hardcoded secret
- [ ] Cache poisoning: actions cache key collision (Pwn Request 类)

### 3.2 Org / Member Profile
- [ ] `org:<company>` 所有 member → 个人 repo 找泄露
- [ ] 历史 employee：linkedin → github profile 反查
- [ ] gist 全量扫 (gist.github.com/<user>?tab=gists)
- [ ] 公司域名邮箱出现在哪些仓库的 commits

### 3.3 Dependency / Secret
- [ ] `package.json` / `Gemfile.lock` / `requirements.txt` 看依赖
- [ ] `.npmrc` / `.pypirc` / `.dockerconfigjson` 等配置泄露
- [ ] CI 日志 /artifact 公开下载链接

## 4. Cloud / Storage Enumeration

- [ ] s3scanner / cloud_enum / s3enum 扫 S3 bucket
- [ ] GCS bucket: testIamPermissions API 枚举权限
- [ ] Azure blob: container list with `?restype=container&comp=list`
- [ ] CDN 缓存 origin 暴露：`curl -H "Host: target.com" <cdn-ip>`

## 5. Tech Stack Fingerprinting

- [ ] Wappalyzer / httpx tech detection
- [ ] favicon hash: shodan favicon / `httpx -favicon`
- [ ] HTTP header / Set-Cookie 名字推 backend (PHPSESSID / JSESSIONID / connect.sid)
- [ ] 静态资源 hash 反查：`/assets/main.<hash>.js` 比对已知 framework

## 6. Asset Difference Tracking

- [ ] 用 `recon_pipeline.py` (本项目) 跑日级 diff
- [ ] github diff: 监控 .github/workflows + Dockerfile + iac/ 变更
- [ ] DNS 变更 webhook: certspotter / dnscentral
- [ ] favicon 变更 → 后端可能换技术栈

## 7. 自动化辅助

```bash
# 一次跑通的 pipeline
make sources-pull SOURCE=portswigger-research  # 拉最新研究情报
python3 scripts/recon_pipeline.py --config config/scope.<program>.json --dry-run

# subdomains
subfinder -d target.com -all -recursive | tee subdomains.txt
chaos -d target.com -silent >> subdomains.txt
sort -u subdomains.txt > subdomains.uniq

# URL/endpoint
echo target.com | gau --threads 5 --providers wayback,otx,commoncrawl > urls.txt
echo target.com | katana -d 3 -ef png,jpg,svg,woff,css > endpoints.txt
echo target.com | hakrawler -d 3 >> endpoints.txt

# GitHub OSINT
trufflehog github --org=target --token=$GH_TOKEN
gitleaks detect --source=https://github.com/target/repo

# 资产 diff
diff -u recon-2026-05-14.txt recon-2026-05-15.txt
```

## 8. Reporting Angle

* **Severity**: 单纯 recon 通常 P5；找到具体可利用的（暴露的 staging API、泄露 token）才算 P3-P4
* **Title 模板**：`<exposure type> in <asset> exposes <secret/data>`
  例：`GitHub Actions cache poisoning via untrusted PR allows extraction of CI secrets`
* **CWE 推荐**：CWE-200（信息泄露）/ CWE-540（源码包含敏感信息）
* **PoC 必须**：完整发现路径 + 暴露内容（脱敏后）+ 影响推断
* **Suggested Fix**：撤销暴露 token + audit 历史 commit + 收紧 IAM/secret-scanning
* **不要**：直接尝试用泄露的 secret 登录任何资源 — 这是 OOS 行为；只标"该 secret 仍有效（401 vs 403 vs 200 状态判断）"

## 9. 已迁移技法（来自 KB — 由 checklist_extend.py 自动填充）

<!-- BACKLINKS START -->
<!-- 由 scripts/checklist_extend.py --apply --commit 自动写入 -->
<!-- BACKLINKS END -->
