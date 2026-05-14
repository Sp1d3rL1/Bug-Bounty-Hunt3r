---
type: technique
category: new_method
derived_from_case: false
vuln_class: Permission Recon
source_url: https://medium.com/@anas-nady/everything-about-cloud-bucket-hacking-s3-gcs-azure-firebase-c027e9441ff9
source_author: Anas NadY
source_date: 2025-04-30
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: low
target_types:
  - Google Cloud Storage
---

# GCS testPermissions API for Permission Enumeration

## 核心思路

Call storage.buckets.testPermissions API on discovered bucket to list exact perms

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Permission Recon` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Precise privilege escalation mapping in authorized cloud BB programs
- 适用场景：Google Cloud Storage
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。
- 先找 lab/本地靶场复现，再映射到授权目标。

## 适用目标画像

- Google Cloud Storage

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Precise privilege escalation mapping in authorized cloud BB programs

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

- https://medium.com/@anas-nady/everything-about-cloud-bucket-hacking-s3-gcs-azure-firebase-c027e9441ff9

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://medium.com/@anas-nady/everything-about-cloud-bucket-hacking-s3-gcs-azure-firebase-c027e9441ff9](https://medium.com/@anas-nady/everything-about-cloud-bucket-hacking-s3-gcs-azure-firebase-c027e9441ff9)
vuln_class: Permission Recon target_type: Google Cloud Storage confidence: high type: technique tags: [gcs, cloud, permission-enum, recon]

# GCS testPermissions API for Permission Enumeration
- **核心思路**
直接调用 Google Cloud Storage 的 storage.buckets.testPermissions API，精确列出指定 bucket 对当前调用者（匿名或认证用户）授予的具体 IAM 权限，实现低噪权限枚举。
- **前置条件**
- 已通过 DNS 枚举、JS 泄露、源代码或 Google dork 发现 GCS bucket 名称。
- 仅限授权 Bug Bounty 程序或自有 GCS Lab 环境。
- 具备 curl / gsutil 等基本 HTTP 客户端。
- **完整技法细节**
使用以下 curl 调用测试一组权限（无需实际读写操作）：
```text
curl "https://www.googleapis.com/storage/v1/b/<bucket-name>/iam/testPermissions?permissions=storage.objects.create&permissions=storage.objects.delete&permissions=storage.objects.get&permissions=storage.objects.list"
```
API 返回 JSON 中仅列出已授予的权限，例如：
```text
{"permissions": ["storage.objects.list", "storage.objects.get"]}
```
无需执行任何写/删操作即可完成枚举。
- **适用目标画像**
任何使用 Google Cloud Storage 的 Web/App/移动端项目，尤其在 Bug Bounty 程序中暴露 bucket 名称的云存储服务。
- **为什么有效**
testPermissions 是 Google 官方提供的无副作用 IAM 检查接口，可精确映射 allUsers / allAuthenticatedUsers 等公共权限，而无需触发实际存储操作警报。
- **手工验证流程（授权 / Lab only）**
- 在授权 Lab 或 scope 内替换 <bucket-name> 并执行 curl。
- 解析返回的 permissions 数组。
- 仅记录结果，不进行任何后续读写操作。
- 使用 gsutil（仅授权环境下）交叉验证。
- **可自动化部分**
Python 脚本 + 已知 bucket 列表批量调用 testPermissions；集成到云存储 recon 流水线中。
- **误报/失败条件**
- Bucket 不存在或调用者无任何权限（返回空数组）。
- API 配额限制或网络问题。
- Bucket 已启用 Uniform bucket-level access 且权限严格。
- **授权边界**
仅限于 Bug Bounty 程序明确授权测试的 GCS bucket，或自有 Lab 环境。禁止对任何第三方 bucket 执行测试。
- **报告 impact 角度**
- 权限配置错误导致的信息披露 / 任意文件上传 / 数据删除风险
- 云存储暴露的精确权限映射（Privilege Escalation 路径）
- 合规与数据泄露隐患
- **相关案例链接**
- [https://medium.com/@anas-nady/everything-about-cloud-bucket-hacking-s3-gcs-azure-firebase-c027e9441ff9](https://medium.com/@anas-nady/everything-about-cloud-bucket-hacking-s3-gcs-azure-firebase-c027e9441ff9)

<!-- GROK_EXPANSION_END -->
