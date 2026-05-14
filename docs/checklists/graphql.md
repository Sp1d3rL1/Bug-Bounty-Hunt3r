---
id: clk-graphql
title: GraphQL Security
owasp_anchor: [API1:2023, API4:2023, API5:2023, API6:2023, API8:2023, WSTG-INPV]
cwe: [CWE-639, CWE-285, CWE-770, CWE-200]
severity_typical: P1-P3
playbook: playbooks/graphql.yaml
last_updated: 2026-05-15
sources: []
maturity: stable
---

# GraphQL Security Checklist

> 双语 / Bilingual: GraphQL / Relay / Apollo / Hasura / Subscriptions 全面覆盖。
> REST API 通用项见 `api.md`。OAuth/JWT 见 `oauth.md`。
> Authorization-only：用自己的两个测试账号验证；不要枚举真实用户的 node id。

---

## 1. Recon

- [ ] 端点定位：`/graphql`、`/api/graphql`、`/v1/graphql`、`/index.php?graphql`、Apollo Studio embed
- [ ] Introspection 是否启用？
  ```graphql
  query { __schema { types { name fields { name } } } }
  ```
- [ ] 检查 GET / POST 双协议：很多服务把 mutation 限制在 POST 但 query 允许 GET → CSRF 风险
- [ ] 检查 batched query 支持（Apollo / Sangria）：`[ {query: "..."}, {query: "..."} ]`
- [ ] 是否暴露 `/voyager`、`/playground`、`/altair`、`/graphiql`
- [ ] WebSocket 端点（Subscription）：`wss://target/graphql-ws`、`graphql-transport-ws`、`subscriptions-transport-ws`
- [ ] 工具识别 schema：clairvoyance / graphw00f / inql

## 2. API1:2023 — BOLA / IDOR (节点级)

- [ ] Relay node id：`{ node(id: "...") }` 可跨用户拿对象？
- [ ] 直接 query 拿 owner=other：`{ user(id: "other-uuid") { email tenantId } }`
- [ ] mutation 跨账号：`mutation { updateInvoice(id: "other-uuid", ...) }`
- [ ] viewer pattern 与直接查询不一致：`{ viewer { invoices } }` 限制 OK，`{ invoices(ownerId: "...") }` 没限制
- [ ] field-level：root 限了，但 nested field 没限：`{ org { internalNotes } }`

## 3. API3:2023 — BOPLA / Mass Assignment (Input level)

- [ ] mutation input 接受隐藏字段：`role`、`tenantId`、`isAdmin`、`verified`
- [ ] 同一 type 在 create/update mutation 里允许字段不同
- [ ] enum 类型可被绕过：`role: "admin"` 字符串注入

## 4. API4:2023 — 资源耗尽

### 4.1 Query depth / complexity
- [ ] 嵌套深度无限制：`user { friends { friends { friends ... 50 levels } } }`
- [ ] 字段计算无 cost limit：`{ search(q: "*") { ...100 fields } }`
- [ ] alias 重复同一 field：`{ a:user b:user c:user ... 1000x }`
- [ ] `@stream` / `@defer` directive 滥用

### 4.2 Batching
- [ ] 单 HTTP 请求批量调 1000 个 mutation
- [ ] login mutation 批量 brute-force：`[{login(u,p1)}, {login(u,p2)}, ...]`

### 4.3 Subscription
- [ ] WS 长连接堆积：开 1000 个订阅占资源
- [ ] heartbeat / idle timeout 缺失

## 5. API5:2023 — BFLA (函数级)

- [ ] 普通用户调 admin mutation：`mutation { adminDeleteUser(id: ...) }`
- [ ] 检查每个 mutation 的 directive：`@auth` / `@hasRole` 是否都有
- [ ] Field-level resolver 缺鉴权：根 query 校验 OK，nested resolver 没校验

## 6. API6:2023 — 业务流滥用

- [ ] race condition：同时发两个 `claim_coupon` mutation
- [ ] mutation 顺序错乱：`refund` 后再 `cancel` 是否触发双重退款
- [ ] 通过 GraphQL 走非主流程绕过限制（Web 限购 1，GraphQL 没限）

## 7. API8:2023 — Misconfig

- [ ] error 暴露 schema：trying invalid field 看 "Did you mean ..." 列出真实字段
- [ ] introspection 在生产开启
- [ ] suggestions 开启（即使 introspection 关）
- [ ] Apollo CSRF：default unsafe POST without preflight
- [ ] Hasura admin secret 在客户端 JS

## 8. Subscription / WebSocket

- [ ] WS handshake：缺 origin 校验 → CSWSH（Cross-Site WebSocket Hijacking）
- [ ] 订阅参数注入：`subscription { onMessage(roomId: "other-room") }` 越权读他人消息
- [ ] connection_init 阶段 token 可缺失
- [ ] 跨连接复用 session

## 9. CSRF / Method Confusion

- [ ] mutation 通过 GET 请求执行（content-type: application/json 不强制）
- [ ] 用 form POST 触发 mutation：`<form method=POST enctype=multipart/form-data>`
- [ ] preflight 缺失：自定义 header 也走 simple request 路径

## 10. 自动化辅助

```bash
# Schema 抓取
clairvoyance https://target/graphql -o schema.json
graphw00f -t https://target/graphql -d  # 识别引擎 (Apollo/Hasura/...)

# Burp 扩展
# - InQL Scanner
# - GraphQL Raider

# Caido
# - GraphQL workflow

# nuclei
nuclei -tags graphql -u https://target

# 测试 introspection
curl -X POST https://target/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{__schema{types{name}}}"}'

# 测试 batching
curl -X POST https://target/graphql \
  -H "Content-Type: application/json" \
  -d '[{"query":"{me{id}}"},{"query":"{me{id}}"}]'

# 测试 alias 复用 brute-force
python3 -c "print('{'+''.join([f'a{i}:login(u:\"x\",p:\"p{i}\")\\n' for i in range(100)])+'}')"
```

## 11. Reporting Angle

* **Title 模板**：`GraphQL <flaw> in <type/mutation> allows <attacker role> to <impact>`
  例：`GraphQL BOLA in updateInvoice mutation allows org member to overwrite cross-tenant invoice fields`
* **Severity 自评**：
  * 跨租户数据写 → CVSS ≥ 8.0 / VRT P1
  * 跨租户数据读 → CVSS ≥ 6.0 / VRT P2
  * Introspection 暴露 → CVSS ≥ 4.0 / VRT P4-P5（取决于是否 production）
  * batching brute-force ATO → CVSS ≥ 7.5 / VRT P2
* **CWE 推荐**：CWE-639（IDOR）/ CWE-770（资源消耗）/ CWE-285（不当授权）
* **PoC 必须**：完整 GraphQL query / variables / response，跨账号 token 全脱敏
* **Suggested Fix**：node id 在 resolver 里按 viewer 重新查；强制 query depth/cost limit；禁用生产 introspection；alias 计数限制；mutation 强制 POST + CSRF token；WS handshake 校验 origin
