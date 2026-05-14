---
id: clk-prototype-pollution-xss-chain
title: Prototype Pollution & XSS Chain
owasp_anchor: [WSTG-CLNT, A03:2021]
cwe: [CWE-1321, CWE-79]
severity_typical: P2-P3
playbook: playbooks/proto_pollution.yaml
last_updated: 2026-05-14
sources: []
maturity: stable
---

# Prototype Pollution & XSS Chain Checklist

> 双语 / Bilingual：从 client-side `Object.prototype` 污染（DOM-PP）到 PP-to-XSS 链路 (GALA / sink hunt)。
> 用法：先确认存在污染原语，再用已知 gadget 串到 sink；server-side PP 单独走 SSRF/RCE 路径，不在本清单范围。
> Authorization-only：仅在自己的浏览器会话与测试账号上注入污染；不对其他用户共享缓存/同源 frame 注入污染。

---

## 1. Recon & 框架指纹

- [ ] 抓 `<script src>` 列出第三方库版本：lodash / jQuery / Vue / Angular / Backbone / Marionette / async / mixin-deep / set-value
- [ ] 列出 query / hash / postMessage 的解析点（`URLSearchParams` / `qs` / `query-string` / `JSURL`）
- [ ] 找 `Object.assign` / `_.merge` / `_.defaultsDeep` / `$.extend(true,...)` / `mergeWith` 的调用位置
- [ ] 标记 sink：`innerHTML` / `eval` / `setTimeout(string)` / `Function()` / `<script src>` 注入 / `document.write` / template engines 的不安全模板
- [ ] 标记 framework guard：`Object.freeze(Object.prototype)`、`--disable-proto`、`Object.create(null)` 使用情况

## 2. 触发污染原语 (sources)

### 2.1 Query / Hash / Path
- [ ] `?__proto__[polluted]=1` → 直接污染
- [ ] `?constructor[prototype][polluted]=1` → 等价路径
- [ ] `?__proto__.polluted=1`（dot-notation 解析）
- [ ] hash 路由：`#/path?__proto__[x]=y`、`#__proto__[x]=y`
- [ ] path-based router：`/route/__proto__/x/y`
- [ ] JSON body：`{"__proto__":{"polluted":1}}` 经 `JSON.parse` 不污染，但被 merge 后污染

### 2.2 库与函数
- [ ] `_.merge` / `_.mergeWith` / `_.defaultsDeep` / `_.set` / `_.setWith` / `_.zipObjectDeep`（lodash <4.17.21 类）
- [ ] `$.extend(true, {}, userInput)`（jQuery <3.4 类）
- [ ] `mixin-deep` / `merge-deep` / `defaults-deep` / `set-value` 古老版本类
- [ ] `Object.assign` 浅拷贝不污染，但与 spread 配合 + 嵌套时易出
- [ ] Vue 2 `Object.defineProperty` reactivity setter 触发污染传染
- [ ] `node-postgres` / `mongoose` 反序列化路径上的 PP-to-RCE 类（仅记录，本清单偏前端）

### 2.3 postMessage / WebSocket / cookies
- [ ] postMessage 把对象 merge 进 state → 注入 `__proto__`
- [ ] WebSocket JSON message 走 `Object.assign(state, msg)` 路径
- [ ] cookie JSON 解析 + merge

## 3. PP-to-XSS Gadget Hunt

- [ ] `script-src` CSP 是否允许 `'unsafe-inline'` / `'unsafe-eval'` / 宽松 `nonce` 复用
- [ ] 找 framework gadget：
  - jQuery：污染 `$.htmlPrefilter`、`$.fn.init` 默认参数
  - Vue 2：污染 `template` / `v-html` 默认 / `el` / `delimiters`
  - Vue 3：`compilerOptions` / `template ref`（限定场景）
  - Marionette：`render` 默认值
  - Bootstrap：tooltip / popover `template` / `sanitize` 默认值
  - jQuery UI：`pickerTemplate` 等
- [ ] 找 app 自己的 gadget：搜代码中 `obj.x || default`、`opts.template || ...`、`config.something ?? null` 等
- [ ] 通用 GALA（Gadget-Agnostic）思路：污染 `Object.prototype.src`、`href`、`onload`、`innerHTML`、`tagName`、`nodeName` 等被 framework 读取的字段

## 4. DOMPurify / Sanitizer Bypass 关联

- [ ] 检查 DOMPurify 版本与 hooks：是否禁用了 `mXSS` 防御
- [ ] mutation XSS 类：`<form><math><mtext></form><form><mglyph><style></math><img src onerror=...>`
- [ ] 命名空间切换：SVG / MathML 内 `<style>` / `<script>` 解析差异
- [ ] DOMPurify 配置 `ALLOW_UNKNOWN_PROTOCOLS=true` / `RETURN_DOM_FRAGMENT` 误用
- [ ] Trusted Types 是否启用、是否被自家 policy 绕过

## 5. Vue / React / Angular 专项

- [ ] Vue：`v-bind="$attrs"` + 污染 `Object.prototype.innerHTML` 类 [example: Vue CVE 类]
- [ ] Vue：`Object.defineProperty(obj, '__proto__', {set: ...})` trap 检测
- [ ] React：`dangerouslySetInnerHTML` + 污染 `__html` 默认值
- [ ] React：`createElement(type, props)` 中 `props` 来自 merge 污染
- [ ] Angular：`$sce.trustAsHtml` 误用 + scope 污染（旧版 1.x）
- [ ] Next.js / Nuxt：`__NEXT_DATA__` / `__NUXT__` 注入污染状态

## 6. 防御指纹（不踩雷）

- [ ] 看是否存在 `Object.freeze(Object.prototype)` 早期注入
- [ ] 看是否启用 `--disable-proto=delete`（Node 端）
- [ ] 看是否使用 `Map` / `new Object(null)` 替代普通对象
- [ ] 看是否引入 `eslint-plugin-security` 的 `detect-object-injection`

## 7. 自动化辅助

```bash
# DOM Invader（Burp built-in）：自带 Prototype Pollution 扫描
# 启用方法：Burp → DOM Invader → Settings → Prototype pollution

# ppmap：被动检测页面是否存在 PP 原语
# https://github.com/kleiton0x00/ppmap
ppmap -u https://target

# ppfuzz：query / hash / json fuzzer
# https://github.com/dwisiswant0/ppfuzz
ppfuzz -l urls.txt -c 30

# 手测 query 触发
curl -s "https://target/?__proto__[polluted]=foo" -o /dev/null
# 然后 DevTools console:
# > ({}).polluted   // 若返回 "foo" 即污染成功

# Caido workflow：在 Match&Replace 自动给所有 GET 注入 __proto__[probe]=$RANDOM
# HTTPQL：req.query.cont("__proto__") AND resp.body.cont("probe-marker")

# Nuclei 模板（DOM 类有限，主要靠手测）
nuclei -tags prototype-pollution,xss -u https://target

# 检测 GALA 通用 gadget（dwisiswant0 / s1r1us 维护的列表）
# https://github.com/BlackFan/client-side-prototype-pollution
```

## 8. Reporting Angle

* **Title 模板**：`Client-side Prototype Pollution via <source> chained to XSS via <gadget> on <page>`
* **CVSS 3.1 区间**：
  * PP-to-XSS（无需登录，单击触发 stored 类）：6.1 – 8.1（AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N）
  * 仅 PP 原语，无 sink：3.7 – 5.4
  * 链到 ATO（劫持 session token）：8.0 – 9.0
* **VRT P-level**：PP-to-XSS reflected → P3；stored / DOM-stored → P2；可链 ATO → P2 上界
* **CWE 推荐**：CWE-1321（Improperly Controlled Modification of Object Prototype Attributes）+ CWE-79
* **PoC 必须**：
  - 两个测试账号 A（攻击者）/ B（受害者，浏览器自有 cookie）
  - 完整 URL + 截图 console 中 `({}).polluted` 输出
  - 截图触发 `alert(document.domain)` 或外发 cookie 到自有 collaborator
  - 标记浏览器版本（Chrome / Firefox / Safari），因 mXSS 与浏览器解析相关
* **Suggested Fix**（≥2）：
  1. 启动早期 `Object.freeze(Object.prototype)` 与 `Object.freeze(Array.prototype)`
  2. 升级 lodash / jQuery / mixin-deep 等到已修复版本
  3. 用 `Map` / `Object.create(null)` 替代普通对象做配置容器
  4. 启用 Trusted Types + 严格 CSP（去掉 `unsafe-inline`）
  5. merge 函数加 `__proto__` / `constructor` / `prototype` 黑名单 key

## 9. 已迁移技法（来自 KB）

- [[techniques/dom_pp_query_source|Query / Hash 触发 PP]]
- [[techniques/lodash_merge_pp|lodash merge 类污染]]
- [[techniques/jquery_extend_pp|jQuery extend deep 污染]]
- [[techniques/gala_gadget_hunt|GALA 通用 gadget]]
- [[techniques/dompurify_mxss|DOMPurify mXSS 绕过]]
