---
id: clk-safe-automation-rules
title: 安全自动化规则
owasp_anchor: []
cwe: []
severity_typical: meta
playbook: ""
last_updated: 2026-05-15
sources: []
maturity: stable
note: meta — 不是漏洞清单而是 RoE 守门规则，被 recon_pipeline.py 强制执行
---

# 安全自动化规则

## 运行前必须确认

- [ ] 已阅读项目 Rules of Engagement。
- [ ] Scope 明确授权域名/API/mobile。
- [ ] `config/scope.<program>.json` 中 `legal_ack=true`。
- [ ] out-of-scope、第三方服务、禁止测试项已经写入配置。
- [ ] 速率低于项目允许范围。
- [ ] 不运行 brute force、DoS、intrusive、destructive、credential stuffing。

## Nuclei 默认策略

- 默认只跑低风险 tag：`exposure, misconfig, takeover, tech`。
- 默认排除：`dos, bruteforce, brute-force, intrusive, fuzz, fuzzing, exploit, rce, lfi, sqli`。
- 不使用 `-headless`、`-fuzz`、`-code`，除非单独确认项目允许且你理解模板行为。
- 所有结果必须手工验证。

## VPS OPSEC

- 每个项目单独目录、单独配置、单独日志。
- 不把 cookies、tokens、报告草稿上传到第三方通知。
- webhook 通知只发 diff 摘要，不发敏感响应体。
- 如果平台要求特定 User-Agent/Header，在配置中记录并统一使用。

## 何时停止

- 发现影响真实用户数据。
- 出现明显异常流量/错误率。
- 页面或项目规则提示禁止当前行为。
- 触碰支付、删除、生产数据修改、隐私数据读取等高风险点但 scope 未明确允许。
