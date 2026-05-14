# SuperGrok/X 采集运行手册

## 运行原则

- 每个主题开新 Grok 上下文，避免上下文污染。
- 每轮只采 25 条，TSV 输出，防止窗口截断。
- 每 5 条扩展一次，扩展时只要求 Markdown 卡片，不要解释。
- 原始输出保存到 `data/grok_research/raw/YYYY-MM-DD/`。
- 所有来源进入 `data/grok_research/source_ledger.tsv`。

## Step 1：种子资源

Prompt：

```text
Search X/web for 2024-2026 bug bounty technique sources. Return only high-signal accounts, keywords, hashtags, newsletters, Discord/community names, and query seeds. Focus on Web/API/SaaS, OAuth/SSO/JWT, GraphQL, business logic/payment, multi-tenant access control, client-side, cache, cloud recon, AI/LLM SaaS. No explanations. Output compact Markdown tables with source links.
```

## Step 2：主题候选采集

模板：

```text
Search X and web for 25 high-signal bug bounty items from 2024-2026 about: <TOPIC>.

Return compact TSV only:
ID | type technique/case/resource | title | author | date | source_url | vuln_class | one_line_trick | why_useful | target_type | confidence

Rules:
- Prefer X posts/threads by real hunters, disclosed reports, research blogs.
- Include niche tricks, not generic OWASP summaries.
- Include only items useful for authorized bug bounty.
- If no source URL, mark confidence=low.
- No intro, no conclusion.
```

## Step 3：5 条一组扩展

```text
Expand IDs <ID1-ID5> into detailed bug bounty technique cards.

For each card include:
Title, source URL, author/date, vuln class, target profile, prerequisites, full technique details, why it works, manual authorized validation steps, automation potential, false positives, risk boundary, report impact angle, related cases.

Keep case-only items as link + detailed description, not full reproduction.
Output Markdown, no intro.
```

## Step 4：本地解析

```bash
python3 scripts/grok_kb_ingest.py --raw-dir data/grok_research/raw/$(date +%F)
python3 scripts/grok_kb_validate.py
```
