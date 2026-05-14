---
type: technique
category: new_method
vuln_class: CSPT
source_url: https://blog.doyensec.com/2025/01/09/cspt-file-upload.html
source_author: Maxence Schmitt (Doyensec)
source_date: 2025-01
collected_at: 2026-05-04
freshness: 2025
confidence: high
risk_level: medium
target_types:
  - web apps with uploads
raw_file: data/grok_research/raw/2026-05-04/topic_07_client_side_dom_cspt.md
---

# CSPT + File Upload Bypass to Arbitrary File Read

## 核心思路

Traverse": - /url: https://blog.doyensec.com/2025/01/09/cspt-file-upload.html§CSPT§Traverse - text: path in upload handler to read attacker-chosen files via client fetch

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `CSPT` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

Niche file-upload + CSPT chain; high BB payouts in authorized programs

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- web apps with uploads

## 为什么有效

Niche file-upload + CSPT chain; high BB payouts in authorized programs

## 手工验证流程（授权 / Lab only）

1. 确认项目 rules of engagement 明确允许该类别测试。
2. 搭建双账号或 sandbox 测试数据，避免触达真实用户数据。
3. 复现来源中的业务前提，只记录最小必要证据。
4. 证明 server-side impact；不要依赖客户端表现。
5. 截图/保存请求响应时打码 token、cookie、PII、支付信息。

## 可自动化部分

- 资产/endpoint 发现、参数枚举、schema 对比、变更 diff 可自动化。
- 权限、支付、状态机、业务影响必须手工确认。

## 误报/失败条件

- 目标不存在相同业务前提。
- 防护在服务端强校验。
- 只影响自有账号且无跨权限/跨租户/财务/数据影响。

## 授权边界

仅用于授权 Bug Bounty、靶场、自有环境。不得用于越界扫描、爆破、DoS、真实支付损害、非授权读取第三方数据。

## 报告 impact 角度

围绕 `CSPT` 说明可导致的未授权数据访问、权限提升、业务绕过、财务影响或合规风险。

## 相关案例链接

- https://blog.doyensec.com/2025/01/09/cspt-file-upload.html

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://blog.doyensec.com/2025/01/09/cspt-file-upload.html](https://blog.doyensec.com/2025/01/09/cspt-file-upload.html)
" vuln_class: "CSPT" one_line_trick: "Traverse path in upload handler to read tester-chosen files via client fetch" why_useful: "Niche file-upload + CSPT chain; high BB payouts in authorized programs" target_type: "web apps with uploads" confidence: "high" tags: ["cspt", "file-upload-bypass", "path-traversal", "bugbounty"]

# CSPT + File Upload Bypass to Arbitrary File Read

## 核心思路
结合文件上传绕过与客户端路径遍历（CSPT），上传包含路径遍历 payload 的 JSON “gadget” 文件（伪装成 PDF/image），利用前端 JSON.parse 触发 CSPT，实现客户端发起对任意文件的读取或 CSRF 请求。

## 前置条件
- 应用存在文件上传功能且仅进行 MIME/魔术字节验证（mmmagic、pdflib、file-type 等）。
- 前端会以 <script src> 或 JSON.parse 方式加载上传后的文件。
- 存在 CSPT 漏洞点（用户可控路径被拼接进 fetch/请求）。

## 完整技法细节
- 构造 JSON gadget：{ "id": "../CSPT_PAYLOAD" } 并嵌入 PDF/image 魔术字节（如 %PDF 或 WEBP 字节）。
- 利用验证器特性绕过类型检查（mmmagic 检查前 1024 字节、pdflib 允许空格替换等）。
- 上传文件，服务器误判为合法 PDF/image。
- 前端加载文件时触发 JSON.parse，路径遍历生效，客户端 fetch 读取任意文件。

## 适用目标画像
- 支持文件上传且前端动态加载上传文件的 Web 应用。
- 使用弱文件类型验证器的后端 + CSPT 存在的客户端逻辑。

## 为什么有效
多数文件验证器仅检查头部字节或部分结构，而 JSON 结构可兼容嵌入魔术字节；客户端 JSON.parse 忽略服务器类型，直接触发路径遍历。

## 手工验证流程（授权 / Lab only）
- 在授权 Lab 环境中搭建带上传和 CSPT 的测试应用。
- 构造 gadget 文件并上传。
- 触发前端加载，观察是否成功读取测试文件。
- 验证不同验证器绕过方式（仅限 Lab）。
- 记录 PoC 但不执行真实数据读取。

## 可自动化部分
- Burp Suite 或自定义脚本生成 gadget 文件。
- 自动化上传 + 触发加载流程（授权目标限定）。

## 误报/失败条件
- 文件验证器进行完整内容解析或严格 JSON 拒绝。
- 前端未使用 JSON.parse 加载上传文件。
- 服务器端路径规范化或 CSP 阻止客户端遍历。

## 授权边界
仅限授权 Bug Bounty 程序或自有 Lab 环境。严禁真实文件读取或数据外泄。报告时强调“客户端路径遍历结合上传绕过”。

## 报告 impact 角度
- 结合 CSPT 可导致客户端任意文件读取、CSRF 或敏感配置泄露。
- 业务影响：用户数据泄露、会话劫持或内部 API 滥用，高额赏金常见。
- 建议修复：严格内容验证 + 禁止客户端解析未经验证的上传文件。

## 相关案例链接
- [Bypassing File Upload Restrictions To Exploit Client-Side Path Traversal](https://blog.doyensec.com/2025/01/09/cspt-file-upload.html)

<!-- GROK_EXPANSION_END -->

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->

<!-- backlink: docs/checklists/file_upload_parser.md -->
