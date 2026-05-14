# Tavily Verifier Powerup

用途：把 Tavily Search/Extract 作为 Grok KB Agent 的独立 web 来源核查层，而不是替代 Grok 的 X Search。

## 触发场景

- Grok 生成的卡片为 `needs_review`、`conflict_full_update`、`confidence=low`。
- 卡片 source URL 是普通网页、研究博客、公开报告、官方文档，需要提取正文片段核实。
- Discovery 阶段需要给 Grok 附加少量 web 搜索上下文，以降低幻觉。

## 默认策略

1. 非 X URL：优先 Tavily Extract，保存 snippet、content hash、可提取性状态。
2. X/Twitter URL：默认跳过 Tavily Extract，标记 `x_native_grok_x_search_preferred`。
3. 缺失来源：用 Tavily Search 找候选来源，但候选不自动升为 high confidence。
4. 只写入 evidence metadata，不把 Tavily 摘要当作 primary source；primary source 仍应是原始 URL。
5. 成本控制：默认只核查不确定卡片；需要全量时显式选择 `--mode all`。

## CLI

```bash
python3 scripts/grok_api_agent.py tavily-verify-run \
  --run-dir data/grok_api/runs/<run_id> \
  --mode default \
  --write-back
```

预注入上下文：

```bash
python3 scripts/grok_api_agent.py expand-prompts \
  --from-batch 011 --to-batch 011 --use-search --tavily-preverify
```
