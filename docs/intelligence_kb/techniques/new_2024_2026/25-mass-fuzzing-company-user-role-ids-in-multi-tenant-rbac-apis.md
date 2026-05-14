---
risk_level: high
collected_at: 2026-05-05
id: 25
title: Mass Fuzzing Company/User/Role IDs in Multi-Tenant RBAC APIs
type: technique
vuln_class: Assignment
source_author: Multiple Hunters (X threads)
source_date: 2024-2026
source_url: https://x.com/bountywriteups/status/2005673056455246006
one_line_trick: Fuzz combos of company_id + user_id + role in assign-role endpoints
why_useful: Discovers hidden role boundaries and horizontal/vertical escalations
target_types:
  - Multi-tenant Laravel/SaaS
confidence: high
tags: [bug-bounty, multi-tenant, rbac, idor, fuzzing]
---
# Mass Fuzzing Company/User/Role IDs in Multi-Tenant RBAC APIs
## 核心思路
在多租户 RBAC API 的 assign-role / update-role 等端点，通过低速率、授权范围内的组合测试 公司ID、用户ID、角色ID 的各种组合，绕过租户隔离检查，发现隐藏的权限边界，实现跨租户水平/垂直权限提升。
## 前置条件
- API 存在角色分配相关端点（如 `/api/companies/{company_id}/users/{user_id}/roles`）
- 后端未严格验证当前用户是否属于目标 company_id 或 role 范围
- 使用数字/UUID 作为 ID（易于 fuzz）
## 完整技法细节
1. 枚举自身所属的 company_id、user_id、role_id 列表。
2. 使用 Burp Intruder 或 ffuf 构造 payload：company_id + user_id + role_id 笛卡尔积组合。
3. 对 assign-role 端点发送请求，观察是否成功分配超出自身权限的角色。
4. 验证成功后，切换账号确认权限提升效果。
**仅限授权 BB 程序**：在 lab 或明确授权的多租户 SaaS 中测试。
## 适用目标画像
- Laravel、Spring Boot 等框架的多租户 SaaS 平台
- 使用 company_id / tenant_id 进行隔离但角色分配逻辑薄弱的系统
- RBAC 模型复杂的 B2B 业务
## 为什么有效
多数多租户系统在角色分配时仅检查单一参数，而非组合校验，导致 ID 混淆即可突破隔离。2024-2026 年多位 hunter 在 X 上分享此方法发现大量高危跨租户 BAC。
## 手工验证流程（授权 / Lab only）
1. 在授权测试环境中创建多个测试租户/公司账号。
2. 使用 Burp Repeater 手动构造组合 payload 并发送。
3. 记录成功响应的 ID 组合。
4. 用新账号登录验证权限是否越界。
**风险边界**：仅操作自身创建的测试数据，禁止影响真实用户数据。
## 可自动化部分
- ffuf / Burp Intruder 批量 fuzz ID 组合
- 自研脚本生成 company_id × user_id × role_id 笛卡尔积
## 误报/失败条件
- 端点强制校验当前 session 的 tenant_id
- 使用 UUID 且无顺序可猜
- 后端有 rate-limit 或 IP 封禁
## 授权边界
仅在明确授权 Bug Bounty 程序或自有 lab 多租户环境中进行 fuzz 测试。
## 报告 impact 角度
- 跨租户权限提升 → 数据泄露、账号接管
- 影响整个 SaaS 平台的多租户隔离根基
- 通常评为 High/Critical，附上成功越权 PoC（lab 数据）
## 相关案例链接
- https://x.com/bountywriteups/status/2005673056455246006
- 多租户 BAC 相关 Medium 文章（如 mrro0o0tt 的跨租户案例）


> 安全边界：本卡仅用于授权项目、靶场或自有环境；任何涉及凭证、CI/CD、支付、账号状态或真实用户数据的验证都必须使用合成数据和最小影响证明。

<!-- backlink: docs/checklists/api.md -->
