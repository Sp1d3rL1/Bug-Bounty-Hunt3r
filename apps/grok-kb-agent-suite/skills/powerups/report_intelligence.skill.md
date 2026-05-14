# Report Intelligence Powerup

用途：采集、聚类、分析公开披露 Bug Bounty 报告及其关联博客、X 讨论、newsletter、Web3 audit/bounty findings 摘要，并维护 source catalog / gray-channel metadata watchlist。

## 默认边界

- 只采集公开披露内容：平台 public/disclosed report、公开 advisory、公开博客、公开 X 帖、公开 newsletter。
- 不抓取私邀项目、未披露报告、登录墙或付费墙内容。
- KB 只保存摘要、链接、证据短片段、hash 与可迁移学习点；不保存完整报告正文。
- 真实漏洞链路只做已披露高层复盘，不写成真实目标复现手册。
- 付费/私域内容只通过用户确认授权的 export 导入。
- 灰色 report trade 只保存公开元数据与风险标记；不购买、不索要、不下载、不解析附件、不保存报告内容。

## CLI

```bash
python3 scripts/report_intel_agent.py discover --sources public_all --limit 25
python3 scripts/report_intel_agent.py catalog-build --dry-run
python3 scripts/report_intel_agent.py discover-catalog --preset public_only --limit 25 --dry-run
python3 scripts/report_intel_agent.py discover-catalog --tier gray_trade_watchlist --dry-run
python3 scripts/report_intel_agent.py import-manual --input path/to/authorized_export.json --authorization-confirmed --dry-run
python3 scripts/report_intel_agent.py cluster --input data/report_intel/runs/<run>/discovery/candidates.jsonl --run-dir data/report_intel/runs/<run>
python3 scripts/report_intel_agent.py enrich --input data/report_intel/runs/<run>/clusters/clusters.json --run-dir data/report_intel/runs/<run> --dry-run
python3 scripts/report_intel_agent.py apply --run-dir data/report_intel/runs/<run>
```

## 质量门

- `confidence=high`：平台披露报告、官方 advisory、或可核查公开报告原链。
- `confidence=medium`：研究员博客/帖子清晰但无平台报告原链。
- `confidence=low`：newsletter/X 只提及但缺少原始报告，进入 review。


## Manual Channel Research

用于合法付费/私域/小众渠道的完整发现记录：保存官方入口、合法获取方法、质量信号、发现路径和屏蔽原因；不保存私邀、直接付款页、附件、云盘、盗版/泄露内容或报告全文。

CLI:
```bash
python3 scripts/report_intel_agent.py manual-channel-prompts
python3 scripts/report_intel_agent.py import-manual-channel-results --input apps/grok-kb-agent-suite/tests/fixtures/manual_channel_results.tsv
python3 scripts/report_intel_agent.py validate-discovery-records
python3 scripts/report_intel_agent.py apply-manual-channel-catalog
python3 scripts/report_intel_agent.py export-manual-channel-index
```
