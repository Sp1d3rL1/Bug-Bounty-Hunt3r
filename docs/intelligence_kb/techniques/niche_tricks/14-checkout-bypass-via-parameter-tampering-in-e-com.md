---
type: technique
category: trick
derived_from_case: false
vuln_class: Logic
source_url: https://x.com/intigriti/status/2004494400601129247
source_author: intigriti
source_date: 2025-03-07
collected_at: 2026-05-05
freshness: 2025
confidence: high
risk_level: low
target_types:
  - E-commerce platforms
---

# Checkout Bypass via Parameter Tampering in E-com

## 核心思路

Modify checkout params (quantity negative discount codes timing) in 4 documented ways

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `Logic` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：Bypasses payment logic for free/duplicate orders; practical e-com hunting
- 适用场景：E-commerce platforms
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
- 把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。
- 先找 lab/本地靶场复现，再映射到授权目标。

## 适用目标画像

- E-commerce platforms

## 为什么有效

- 现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。
- Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。
- 本条技巧的价值点：Bypasses payment logic for free/duplicate orders; practical e-com hunting

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
author_date: intigriti / 2025-03-07 tags: ["logic-flaw", "checkout", "ecommerce", "parameter-tampering"] confidence: high

# Checkout Bypass via Parameter Tampering in E-com

## 核心思路
在结账流程中篡改quantity、discount code、price、currency等参数，利用后端订单状态或定价逻辑错误，实现免费/低价下单。

## 前置条件
- 授权的电商测试账号或sandbox环境。
- 结账流程使用可篡改的POST/GET参数（非仅客户端验证）。
- 使用测试卡或sandbox支付网关。

## 完整技法细节
- **Quantity tampering**
：设置负数、0、小数或超大数量值，观察总价变化。
- **Currency confusion**
：修改currency参数，利用汇率差异降低价格。
- **Coupon code (race condition)**
：在 Lab 中低并发验证同一优惠码的状态竞争风险。
- **Test cards / param tampering**
：使用项目允许的测试卡/沙箱凭证组合，或篡改price/amount/id_product_feature_set等字段。

## 适用目标画像
电商平台、在线商店、SaaS订阅结账流程。

## 为什么有效
开发者常假设客户端已验证价格/数量，导致服务器端订单状态处理不当。

## 手工验证流程（授权 / Lab only）
- 在授权sandbox环境中添加商品到购物车。
- 进入结账，拦截请求并修改quantity/price/currency等参数。
- 使用测试卡完成支付，确认是否成功下单/价格变更。
- 记录前后总价差异，仅在lab验证。

## 可自动化部分
- Burp 低速率授权并发验证工具并发优惠码测试。
- 自定义脚本批量篡改quantity/price参数。

## 误报/失败条件
- 服务器端严格校验所有参数与会话绑定。
- 价格计算使用不可篡改的后端缓存或HMAC签名。
- 仅客户端JS验证（无服务器端处理）。

## 授权边界
仅限授权bug bounty程序的sandbox或自有测试商店。严禁真实支付或影响生产订单。

## 报告 impact 角度
“逻辑缺陷允许免费获取高价值商品/服务，造成直接财务损失”，附sandbox验证截图。

## 相关案例链接
- [https://x.com/intigriti/status/1897952626932625900](https://x.com/intigriti/status/1897952626932625900)
(Intigriti 4 ways线程)
- Intigriti价格操纵漏洞文章

<!-- GROK_EXPANSION_END -->
