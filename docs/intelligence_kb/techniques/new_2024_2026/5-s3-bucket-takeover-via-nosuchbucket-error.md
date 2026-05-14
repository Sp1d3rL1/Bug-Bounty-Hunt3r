---
type: technique
category: new_method
derived_from_case: false
vuln_class: Bucket Takeover
source_url: https://medium.com/@anas-nady/everything-about-cloud-bucket-hacking-s3-gcs-azure-firebase-c027e9441ff9
source_author: Anas NadY
source_date: 2025-04-30
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: medium
target_types:
  - AWS S3
---

# S3 Bucket Takeover via NoSuchBucket Error

## 核心思路

Claim non-existent bucket after subdomain error reveals target bucket name

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Bucket Takeover` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Direct data exfil/overwrite in authorized BB targets with public S3
- 适用场景：AWS S3
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 使用授权域名、组织名、公开仓库、证书、ASN、存储命名规律建立资产图。
- 对公开暴露只证明可访问性和最小元数据；不要下载大批量文件或读取敏感内容。
- 把 findings 关联回业务资产、权限边界或可利用路径，避免只报低价值暴露。

## 适用目标画像

- AWS S3

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Direct data exfil/overwrite in authorized BB targets with public S3

## 手工验证流程（授权 / Lab only）

1. 确认 scope、禁止项、速率限制与是否允许该功能测试。
2. 准备至少两个自有测试账号；多租户场景准备两个 organization/workspace。
3. 先完整走通正常业务流，记录对象 ID、角色、状态、token、请求路径。
4. 只替换一个变量或一步状态，观察服务端响应和后续副作用。
5. 用最小必要数据证明影响；不读取、不导出第三方真实数据。
6. 使用授权域名、组织名、公开仓库、证书、ASN、存储命名规律建立资产图。
7. 对公开暴露只证明可访问性和最小元数据；不要下载大批量文件或读取敏感内容。
8. 把 findings 关联回业务资产、权限边界或可利用路径，避免只报低价值暴露。

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
" vuln_class: "Bucket Takeover" one_line_trick: "Claim non-existent bucket after subdomain error reveals target bucket name" why_useful: "授权范围内的数据暴露/覆盖风险验证 in authorized BB targets with public S3" target_type: "AWS S3" confidence: "high" type: "technique" tags: ["aws", "s3", "bucket-takeover", "subdomain", "cloud-misconfig"]

### 核心思路
当子域名CNAME指向已删除或不存在的S3桶时，访问会触发NoSuchBucket错误，从而可通过在自己AWS账户创建同名桶实现接管。

### 前置条件
- 目标子域名存在CNAME记录指向*.s3.amazonaws.com。
- 目标桶名可从错误消息或DNS记录推断。
- 仅限授权Bug Bounty程序中的S3资产。

### 完整技法细节
- 访问子域名（例如assets.target.com）。
- 检查响应：出现“NoSuchBucket: The specified bucket does not exist”错误。
- 确认桶名（例如assets-target-com）。
- 在自己AWS账户（Lab环境）创建同名桶。
- 上传benign proof.txt文件作为PoC。
- 仅验证接管成功，不进行任何生产数据操作。

### 适用目标画像
- 使用S3作为静态资产/CDN的Web应用。
- DNS记录指向已废弃或从未创建的S3桶。
- 常见于旧子域名或遗留基础设施。

### 为什么有效
AWS允许任何账户创建未被占用的桶名；CNAME仍指向该桶时，错误消息直接暴露桶名并允许立即接管。

### 手工验证流程（授权 / Lab only）
- 使用dig或浏览器确认CNAME指向S3。
- 访问子域名获取NoSuchBucket错误。
- 在授权Lab AWS账户创建同名桶并上传poc.txt。
- 重新访问子域名确认内容变为PoC。
- 立即删除桶并记录截图。

### 可自动化部分
- 使用subjack或类似工具自动化扫描死CNAME并检查NoSuchBucket。
- 自定义脚本解析DNS + 尝试桶创建（仅Lab）。

### 误报/失败条件
- 桶已存在（返回其他错误）。
- DNS记录已更新或桶处于pending状态。
- AWS账户无创建桶权限。

### 授权边界
仅限授权Bug Bounty程序in-scope的S3桶和关联子域名。禁止任何真实数据上传/覆盖生产桶；仅Lab环境验证接管。

### 报告 impact 角度
- 高危接管风险：未授权第三方可能完全控制子域名内容，实现钓鱼、恶意JS注入或数据覆盖。
- 业务影响：品牌损害、供应链攻击向量。
- 合规风险：暴露遗留基础设施管理不当。

### 相关案例链接
原Medium文章：
- [https://medium.com/@anas-nady/everything-about-cloud-bucket-hacking-s3-gcs-azure-firebase-c027e9441ff9](https://medium.com/@anas-nady/everything-about-cloud-bucket-hacking-s3-gcs-azure-firebase-c027e9441ff9)

<!-- GROK_EXPANSION_END -->
