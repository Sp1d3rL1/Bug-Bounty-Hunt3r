# Bug Bounty Hunting Operating System

这是一个把「进阶 Bug Bounty 计划」落地成可执行工作流的本地作战系统：课程采购、X/Grok 情报、目标档案、报告模板、API/OAuth/支付专项 checklist，以及一套安全默认的 VPS recon pipeline。

## 快速开始

1. 阅读 `00_START_HERE.md`。
2. 复制 `config/scope.example.json` 为 `config/scope.<program>.json`，只填入明确授权 scope。
3. 按 `docs/learning/course_purchase_matrix.md` 购买/排课。
4. 用 `docs/intelligence/x_grok_workflow.md` 建 X Pro/Grok 情报流。
5. VPS 上安装工具后运行：

```bash
python3 scripts/recon_pipeline.py --config config/scope.<program>.json
```

## 安全默认

- 默认只做被动收集 + 低风险探活 + 低风险 nuclei。
- 默认拒绝没有 `legal_ack: true` 的 scope 配置。
- 默认排除 `dos, brute-force, intrusive, fuzz, exploit, rce` 相关 nuclei tag。
- 默认所有候选资产先过 allowlist/out-of-scope guard。
- 自动化输出只作为「变化提醒」，报告前必须手工验证。

## 目录

```text
config/              授权 scope 与工具配置模板
docs/learning/       课程采购、180 天计划、证书路线
docs/intelligence/   X/Grok、Discord、Telegram、博客情报流
docs/targets/        目标档案模板与项目筛选
docs/reports/        英文漏洞报告模板
docs/checklists/     API/OAuth/GraphQL、支付/业务逻辑专项
docs/vps/            VPS 部署和 OPSEC
scripts/             scope guard、recon pipeline、diff、通知、安装脚本
data/                运行输出，默认不进 git
```
