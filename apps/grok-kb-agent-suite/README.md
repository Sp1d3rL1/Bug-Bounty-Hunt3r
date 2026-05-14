# Grok KB Agent Suite

一个独立的 API-first Agent Suite，用 Grok API/X Search/Web Search，并可选接入 Tavily Search/Extract，批量采集、扩展、核查并落库 Bug Bounty Intelligence KB。新增 Report Intelligence 模块用于公开披露报告、关联博客/X 讨论/newsletter 的摘要型知识库。

设计目标参考 2025-2026 GitHub 上口碑好的 Agent 工程特质：

- **Durable execution**：任务落盘，崩溃后可恢复。
- **Human-in-the-loop**：高风险批次先 dry-run / review，再 apply。
- **Structured outputs**：所有模型输出走 JSON Schema，避免 UI/DOM 噪声。
- **Tool registry / skills**：能力包可插拔，不把所有工具塞进单一 prompt。
- **Observability**：记录 usage、cost、状态、日志、raw response。
- **Evals / QA gates**：落库后强制 build index + validate。
- **Minimal framework magic**：核心用 stdlib + Grok API，降低框架黑盒依赖。

## 快速启动

```bash
cd "/Users/spider/Development/codex_workspace/Bug Bounty Hunting"
cp .env.example .env   # 填入 XAI_API_KEY；如要二次核查，再填 TAVILY_API_KEY
python3 apps/grok-kb-agent-suite/backend/server.py --port 8765
```

打开：

```text
http://127.0.0.1:8765/
```

## CLI 方式

底层仍复用根目录的：

```text
scripts/grok_api_agent.py
```

示例：

```bash
python3 scripts/grok_api_agent.py expand-prompts --from-batch 011 --to-batch 012 --use-search
python3 scripts/grok_api_agent.py tavily-verify-run --run-dir data/grok_api/runs/<run_id> --mode default --write-back
python3 scripts/grok_api_agent.py apply-run --run-dir data/grok_api/runs/<run_id>
python3 scripts/report_intel_agent.py discover --sources public_all --limit 25 --dry-run
python3 scripts/grok_kb_build_index.py && python3 scripts/grok_kb_validate.py
```

## Tavily 定位

Tavily 是可选的独立 web-source verifier：

- 用 `--tavily-preverify` 在 Grok 扩展前提取普通网页来源片段。
- 用 `--tavily-context` 在 Discovery 前给 Grok 少量 web 候选来源。
- 用 `tavily-verify-run` 对 `cards/*.json` 中的低置信、冲突、缺来源项做二次核查。
- 不替代 Grok `x_search`；X/Twitter 链接默认仍交给原生 X 搜索/人工复核。

## Report Intelligence

公开报告采集链路：

```bash
python3 scripts/report_intel_agent.py discover --sources public_all --limit 25
python3 scripts/report_intel_agent.py cluster --input data/report_intel/runs/<run>/discovery/candidates.jsonl --run-dir data/report_intel/runs/<run>
python3 scripts/report_intel_agent.py enrich --input data/report_intel/runs/<run>/clusters/clusters.json --run-dir data/report_intel/runs/<run> --dry-run
python3 scripts/report_intel_agent.py apply --run-dir data/report_intel/runs/<run>
```

默认只采集公开披露内容；KB 只保存摘要、链接、证据短片段和 hash，不保存完整报告正文。

渠道扩展命令：

```bash
python3 scripts/report_intel_agent.py catalog-build --dry-run
python3 scripts/report_intel_agent.py discover-catalog --preset public_only --limit 25 --dry-run
python3 scripts/report_intel_agent.py discover-catalog --tier web3_audit_bounty --limit 25 --dry-run
python3 scripts/report_intel_agent.py discover-catalog --tier gray_trade_watchlist --dry-run
python3 scripts/report_intel_agent.py import-manual --input apps/grok-kb-agent-suite/tests/fixtures/authorized_newsletter_export.json --dry-run
```

灰色 report trade 相关来源强制 `metadata_only`：只写 `docs/intelligence_kb/reports/channel_watchlist.md` 与 `data/report_intel/channel_watchlist.jsonl`，不进入 `enrich/apply`。

## 目录

```text
apps/grok-kb-agent-suite/
  backend/        stdlib HTTP API + job runner
  frontend/       zero-build dashboard
  skills/         suite-local powerup skills
  config/         agent suite config
  docs/           架构、对标、运行说明
  data/           suite-local job state
  tests/          stdlib smoke tests
```

## Manual Channel Research

第二批渠道接入新增“完整发现记录 + 合法获取路径”工作流：

```bash
python3 scripts/report_intel_agent.py manual-channel-prompts --dry-run
python3 scripts/report_intel_agent.py import-manual-channel-results --input apps/grok-kb-agent-suite/tests/fixtures/manual_channel_results.tsv --dry-run
python3 scripts/report_intel_agent.py apply-manual-channel-catalog --dry-run
python3 scripts/report_intel_agent.py export-manual-channel-index --dry-run
```

该模块记录官方入口、合法获取方法、质量信号和屏蔽原因；不保存私邀、购买/付款页、附件、云盘、盗版/泄露内容或报告全文。
