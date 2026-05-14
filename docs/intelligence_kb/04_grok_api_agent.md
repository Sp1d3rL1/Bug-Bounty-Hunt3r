# Grok API Agent Runbook（替代浏览器采集）

更新时间：2026-05-05

## 目标

把原来的“浏览器 + Grok UI + DOM snapshot”流程改为 **xAI Grok API Agent**：

- 用 `/v1/responses` + `x_search` / `web_search` 做 2025-2026 X/Web 情报发现。
- 可选接入 Tavily Search/Extract 作为 **独立 web 来源核查层**：用于普通网页、研究博客、公开报告、官方文档的提取与候选来源发现；X 帖子仍优先使用 xAI `x_search`。
- 用 Structured Outputs（JSON Schema）强制返回稳定 JSON，避免 DOM 截断、按钮噪声、Markdown comment 丢失。
- 用 Batch API 批量处理 `batch_011` 到 `batch_060`，降低成本并绕开浏览器上下文窗口问题。
- 将输出落到 `data/grok_api/runs/<run_id>/cards/*.json`，再统一应用到 Obsidian KB。

## 官方能力依据

- xAI Chat/Responses API：`/v1/chat/completions` 与 `/v1/responses`；Responses 可用 server-side tools。
- xAI Structured Outputs：`text.format.type=json_schema` 可要求模型按 JSON Schema 输出。
- xAI Web Search：Responses API 上支持 `web_search`，可实时检索网页。
- xAI X Search：Responses API 上支持 `x_search`，可指定 `from_date` / `to_date`、handles 等。
- xAI Batch API：可异步提交大量 requests，通常 24h 内完成，文本模型有批处理折扣。
- xAI Rate Limits：不同模型 RPM/TPM 不同；官方建议 batch、指数退避、分散请求。

## 文件结构

```text
scripts/grok_api_agent.py
config/grok_api_agent.example.json
.env.example
data/grok_api/
  runs/<run_id>/
    manifest.json
    usage.tsv
    prompts/batch_011.txt
    raw/batch_011.json
    cards/batch_011.json
  discovery/<run_id>/
    request.json
    raw.json
    items.json
```

## 环境变量

不要把真实 key 写入 Git：

```bash
cp .env.example .env
# 编辑 .env，或者直接 export：
export XAI_API_KEY='xai-...'
export XAI_MODEL='grok-4.3'
export XAI_API_BASE='https://api.x.ai/v1'
export XAI_CACHE_CONV_ID='稳定 UUID，可提升重复前缀 cache 命中概率'

# 可选：Tavily 二次核查
export TAVILY_API_KEY='tvly-...'
export TAVILY_API_BASE='https://api.tavily.com'
```

## 方案 1：实时 API 处理现有 expansion batches

适合先小批量验证：

```bash
python3 scripts/grok_api_agent.py expand-prompts \
  --from-batch 011 \
  --to-batch 012 \
  --use-search \
  --tavily-preverify \
  --from-date 2025-01-01 \
  --to-date 2026-05-05
```

只生成请求、不调用 API：

```bash
python3 scripts/grok_api_agent.py expand-prompts \
  --from-batch 011 \
  --to-batch 011 \
  --use-search \
  --dry-run \
  --run-dir data/grok_api/runs/dry_run_test
```

应用结果到 KB：

```bash
python3 scripts/grok_api_agent.py apply-run \
  --run-dir data/grok_api/runs/<run_id>

python3 scripts/grok_kb_build_index.py
python3 scripts/grok_kb_validate.py
```

## 方案 2：Batch API 批量处理后续批次

适合 `batch_011` 到 `batch_060`：

```bash
python3 scripts/grok_api_agent.py batch-submit-prompts \
  --from-batch 011 \
  --to-batch 060 \
  --use-search \
  --name bb-kb-expand-2025-2026
```

查看状态：

```bash
python3 scripts/grok_api_agent.py batch-status --batch-id <batch_id>
```

拉取结果：

```bash
python3 scripts/grok_api_agent.py batch-fetch \
  --batch-id <batch_id> \
  --run-dir data/grok_api/runs/<run_id>
```

应用结果：

```bash
python3 scripts/grok_api_agent.py apply-run --run-dir data/grok_api/runs/<run_id>
python3 scripts/grok_kb_build_index.py
python3 scripts/grok_kb_validate.py
```

## 方案 3：直接发现 2025-2026 新情报

示例：

```bash
python3 scripts/grok_api_agent.py discover-topic \
  --topic '2025-2026 bug bounty GraphQL authorization bypass schema batching tenant isolation X posts research reports' \
  --limit 25 \
  --tavily-context \
  --from-date 2025-01-01 \
  --to-date 2026-05-05
```

输出在：

```text
data/grok_api/discovery/<run_id>/items.json
```

下一步可以把 `items.json` 转换成新的 `source_ledger.tsv` 行，或生成新的 expansion prompt。

## Prompt 优化策略

新的 Agent 不再把整段浏览器用 prompt 原样提交，而是：

1. 解析每个 `batch_XXX.prompt.md` 里的 `CARD_DEST / ID / TYPE / TITLE / SOURCE_URL / ONE_LINE_TRICK`。
2. 生成更短的 English prompt + JSON `ITEMS_JSON`。
3. 用固定 system prompt 表达边界：authorized / Lab only / synthetic data / minimal-impact validation。
4. 用 JSON Schema 强制返回 `cards[]`，每张卡含 `destination_path` 与 `markdown`。
5. 本地脚本负责落库，避免模型直接改文件路径造成错误。

## 成本与稳定性优化

- 使用稳定 `x-grok-conv-id` header 增加重复 system/schema prompt 的缓存命中概率。
- 小批验证用实时 `/v1/responses`；大批用 Batch API。
- 对 429/5xx 自动指数退避。
- `usage.tsv` 记录 prompt/completion/total tokens、source 数、cost ticks。
- JSON Schema 限制每批最多 8 张卡，避免过长输出不可解析。
- Web/X search 默认限定 2025-01-01 到当前日期，减少噪声。

## 安全/合规写法

知识库不是攻击脚本库。默认落库要求：

- 所有验证限定授权项目、Lab、自有环境。
- 支付/电商只使用 sandbox/test card/测试订单。
- 云权限只做只读身份/权限证明，不执行写操作。
- 可用性类只写“复杂度/限制验证”，不写生产 DoS 操作。
- 案例卡以链接、摘要、可迁移点为主，不复现真实目标链路。

## 发现结果转成新的 expansion batches

`discover-topic` 得到 `items.json` 后，可以直接生成新的 expansion prompts：

```bash
python3 scripts/grok_api_agent.py make-prompts-from-discovery \
  --items-json data/grok_api/discovery/<run_id>/items.json \
  --out-dir data/grok_api/generated_prompts/2026-05-05 \
  --start-batch 061 \
  --batch-size 5 \
  --category new_2024_2026 \
  --ledger-out data/grok_api/discovery/<run_id>/generated_ledger.tsv
```

然后继续扩展：

```bash
python3 scripts/grok_api_agent.py expand-prompts \
  --prompt-dir data/grok_api/generated_prompts/2026-05-05 \
  --from-batch 061 \
  --to-batch 070 \
  --use-search
```

这样可以形成闭环：

```text
X/Web discovery -> items.json -> generated batch prompts -> structured expansion -> apply-run -> KB
```

## 2026-05-05 Evidence Baseline / 反幻觉基线

从本次更新开始，所有 Grok API 输入都会同时在 system prompt 与 user prompt 中加入以下基线策略：

```text
- Every claim, viewpoint, technique detail, date, author attribution, and usefulness statement MUST have a concrete source URL.
- Do not speculate, infer beyond the source, invent authors/dates/URLs, or fill missing facts from memory.
- Verify search results against the supplied source_url and at least one source-backed search result when available.
- If evidence conflicts with the previously collected KB excerpt, output the complete corrected content and explain the conflict in conflict_notes.
- If evidence shows no substantive change from the existing KB excerpt, do not repeat the old card; return verification_status=unchanged_verification_only and a concise verification result.
- If a source cannot be verified, set confidence=low, verification_status=needs_review, and state exactly what could not be verified.
```

### 结构化输出新增字段

每张 API card 必须包含：

```json
{
  "verification_status": "verified_full_update | conflict_full_update | unchanged_verification_only | needs_review",
  "verification_summary": "source-backed verification result",
  "conflict_notes": "empty if no conflict",
  "evidence": [
    {
      "claim": "specific claim",
      "source_url": "https://...",
      "verification_notes": "how the source supports the claim"
    }
  ]
}
```

### 与旧 KB 的冲突核查

`expand-prompts` 现在会读取目标 `CARD_DEST` 对应的已有卡片摘要，并把以下字段加入 `ITEMS_JSON`：

```json
{
  "existing_kb_status": "present | missing | invalid_path",
  "existing_kb_excerpt": "compact previous card excerpt",
  "existing_kb_sha256": "short digest"
}
```

模型必须据此判断：

- `verified_full_update`：来源已核查，需要补全/扩展。
- `conflict_full_update`：与旧卡冲突，输出完整修正版。
- `unchanged_verification_only`：没有变化，只输出核查结果，不重复旧内容。
- `needs_review`：来源无法核查或证据不足。

### 落库变化

`apply-run` 会把核查状态、source_urls、evidence 追加到 `## Evidence / 核查元数据`，并在 `unchanged_verification_only` 时使用：

```md
## Grok API 核查结果
```

而不是重复写一遍完整技法卡。

## 2026-05-05 Tavily 接入方式

Tavily 在本方案中的定位是 **source verifier / web context provider**，不是替代 Grok，也不是替代 X 原生搜索：

- Grok `x_search`：仍是 X 帖子、线程、账号维度情报的主搜索入口。
- Grok `web_search`：仍用于模型侧实时检索与源引用。
- Tavily `Search`：用于缺失来源、低置信项、冲突项的独立网页候选发现。
- Tavily `Extract`：用于对普通 web URL 提取正文片段、记录 content hash、验证 URL 可访问/可提取。

### 预注入 Tavily 上下文

在 Grok 扩展前，把非 X source URL 的 Tavily Extract 摘要加入 `ITEMS_JSON.tavily_context`：

```bash
python3 scripts/grok_api_agent.py expand-prompts \
  --from-batch 011 \
  --to-batch 011 \
  --use-search \
  --tavily-preverify
```

Discovery 阶段也可以给 Grok 附加少量 Tavily Search 结果，降低“凭空补全来源”的概率：

```bash
python3 scripts/grok_api_agent.py discover-topic \
  --topic '2025-2026 bug bounty OAuth SaaS business logic disclosed reports' \
  --limit 25 \
  --tavily-context
```

### 运行后核查 cards

对已有 `cards/*.json` 做二次校验：

```bash
python3 scripts/grok_api_agent.py tavily-verify-run \
  --run-dir data/grok_api/runs/<run_id> \
  --mode default \
  --write-back
```

`--mode default` 只核查最值得花费 Tavily credits 的卡片：

- `verification_status=needs_review`
- `verification_status=conflict_full_update`
- `confidence=low`
- 缺少 source URL

可选模式：

```text
all | needs_review | conflicts | low_confidence
```

输出位置：

```text
data/grok_api/runs/<run_id>/tavily_verification/
  report.tsv
  cards/*.json
```

如使用 `--write-back`，脚本会把 `tavily_verification` 写回 `cards/*.json`；随后执行 `apply-run` 时，KB 卡片的 `## Evidence / 核查元数据` 会附带 Tavily 核查结果。

### 成本/准确性默认值

- `--tavily-search-depth basic`
- `--tavily-extract-depth basic`
- `--tavily-max-results 5`
- `--tavily-context-chars 1200`
- X/Twitter URL 默认标记为 `x_native_grok_x_search_preferred`，不强行用 Tavily 提取。

### 官方文档依据

- Tavily Search API: https://docs.tavily.com/documentation/api-reference/endpoint/search
- Tavily Extract API: https://docs.tavily.com/documentation/api-reference/endpoint/extract
- xAI X Search: https://docs.x.ai/developers/tools/x-search
- xAI Web Search: https://docs.x.ai/developers/tools/web-search

## 2026-05-06 Report Intelligence / 公开报告情报

新增 `scripts/report_intel_agent.py`，用于将真实公开 Bug Bounty 报告及其相关博客、X 讨论、newsletter 做成摘要型知识库。

### 数据与 KB 位置

```text
docs/intelligence_kb/reports/
  source_catalog.md
  channel_watchlist.md
  platform_reports/
  researcher_writeups/
  x_discussions/
  newsletter_roundups/
  advisory_related/
  imported_authorized/
data/report_intel/
  source_catalog.json
  channel_watchlist.jsonl
  discovery/
  extracted/
  clusters/
  runs/
  report_ledger.tsv
```

### CLI 流程

```bash
python3 scripts/report_intel_agent.py discover \
  --sources public_all \
  --topic 'public disclosed bug bounty reports SaaS API business logic OAuth' \
  --from-date 2025-01-01 \
  --to-date 2026-05-08 \
  --limit 25

python3 scripts/report_intel_agent.py cluster \
  --input data/report_intel/runs/<run>/discovery/candidates.jsonl \
  --run-dir data/report_intel/runs/<run>

python3 scripts/report_intel_agent.py enrich \
  --input data/report_intel/runs/<run>/clusters/clusters.json \
  --run-dir data/report_intel/runs/<run> \
  --dry-run

python3 scripts/report_intel_agent.py apply \
  --run-dir data/report_intel/runs/<run>
```

### 来源策略

- 默认公开来源优先：HackerOne disclosed/Hacktivity、Bugcrowd CrowdStream、GitHub Security Lab/GHSA、研究员博客、X 讨论、newsletter。
- 可选增强 key：`HACKERONE_API_USERNAME`、`HACKERONE_API_TOKEN`、`GITHUB_TOKEN`、`BUGCROWD_API_TOKEN`。
- KB 只保存摘要、链接、证据短片段、hash 与可迁移学习点；不保存完整报告正文。
- 报告链路只做已披露高层复盘，不写真实目标复现手册。

## 2026-05-08 Report Intelligence 渠道扩展

`report_intel_agent.py` 现在支持 source catalog 驱动的多源 pipeline：

```bash
python3 scripts/report_intel_agent.py catalog-build --dry-run
python3 scripts/report_intel_agent.py catalog-build
python3 scripts/report_intel_agent.py discover-catalog --preset public_only --limit 25 --dry-run
python3 scripts/report_intel_agent.py discover-catalog --tier curated_aggregators --limit 25 --dry-run
python3 scripts/report_intel_agent.py discover-catalog --tier gray_trade_watchlist --dry-run
python3 scripts/report_intel_agent.py import-manual --input path/to/authorized_export.json --authorization-confirmed --dry-run
python3 scripts/report_intel_agent.py triage-sources --dry-run
```

新增 source tier：

- `platform_public`：HackerOne、Bugcrowd、GitHub Advisories、GitHub Security Lab 等公开平台/官方 API。
- `curated_aggregators`：PentesterLand、HackDex、BugBoard、Google VRP writeup repo 等聚合源。
- `newsletter_podcast`：Disclosed、Bug Bytes、Critical Thinking/CRL、BBRE 等公开或可授权导出的材料。
- `web3_audit_bounty`：Code4rena、Solodit、Immunefi 等公开 Web3 audit / bounty finding。
- `community_social`：X、Reddit、Medium/InfoSec Writeups、研究员博客。
- `gray_trade_watchlist`：仅做灰色 report trade 渠道元数据观察，不做内容采集。

灰色渠道策略是硬限制：不购买、不索要、不下载、不解析附件、不保存疑似泄露/NDA/私有报告内容；只允许保存渠道名、公开入口、平台、标签、风险等级、发现时间和人工备注到 `channel_watchlist.md`。

## 2026-05-08 Manual Channel Research / 完整发现记录

新增合法付费/私域/小众渠道入口的发现记录层：

```text
data/report_intel/manual_channel_research/
  prompts/
  raw_grok_outputs/
  discovery_records/
  trashcan/
  import_batches/
docs/intelligence_kb/reports/manual_channel_sources.md
```

CLI：

```bash
python3 scripts/report_intel_agent.py manual-channel-prompts
python3 scripts/report_intel_agent.py import-manual-channel-results --input apps/grok-kb-agent-suite/tests/fixtures/manual_channel_results.tsv --tool-used grok_expert
python3 scripts/report_intel_agent.py validate-discovery-records
python3 scripts/report_intel_agent.py apply-manual-channel-catalog
python3 scripts/report_intel_agent.py export-manual-channel-index
```

边界：保存官方 landing page、订阅说明、申请页、社区 discovery 页、公开政策页、公开 API 文档和完整发现判断；不保存私邀、直接付款/checkout、附件、云盘、盗版/泄露资源页、报告全文或私聊内容。硬性阻断命中的条目不再略过，统一写入 `trashcan/`；只保留 domain/hash、屏蔽原因和发现路径摘要。`raw_grok_outputs/` 也会在落盘前替换受限 URL 为 `[TRASHCAN_REDACTED_URL reason=... sha256_16=...]`，避免原始私邀/付款/附件链接残留。
