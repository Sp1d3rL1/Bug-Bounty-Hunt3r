SHELL := /bin/bash
.PHONY: check-scope dry-run tree \
	sources-list sources-pull sources-tick sources-health \
	wechat-rss-up wechat-rss-down wechat-rss-status \
	checklist-bucket checklist-diff checklist-extend checklist-extend-commit \
	checklist-validate checklist-report checklist-discover

# ---------------------------------------------------------------------------
# Existing recon-pipeline targets
# ---------------------------------------------------------------------------

check-scope:
	python3 scripts/scope_guard.py --config config/scope.example.json --input config/sample_hosts.txt

dry-run:
	python3 scripts/recon_pipeline.py --config config/scope.example.json --dry-run

tree:
	find . -maxdepth 3 -type f | sort

# ---------------------------------------------------------------------------
# Phase 1: connector pipeline
# ---------------------------------------------------------------------------

SCHED := apps/grok-kb-agent-suite/backend/scheduler.py

sources-list:
	python3 $(SCHED) --list

# Pull every due source (cron-aware). Add SOURCE=<id> for a one-shot tick.
sources-pull:
ifdef SOURCE
	python3 $(SCHED) --tick --only "$(SOURCE)"
else
	python3 $(SCHED) --tick
endif

# Force-fire all sources, ignoring cadence (e.g. fresh install bootstrap).
sources-tick:
	@for sid in $$(python3 $(SCHED) --list | awk -F'::' '/^- /{print $$1}' | sed 's/^- //;s/ *$$//'); do \
		echo "→ tick $$sid"; \
		python3 $(SCHED) --tick --only "$$sid" >/dev/null 2>&1 || echo "  failed $$sid"; \
	done

sources-health:
	@if [ -f logs/connector_metrics.tsv ]; then \
		echo "Last 25 connector runs:"; \
		head -1 logs/connector_metrics.tsv; \
		tail -25 logs/connector_metrics.tsv; \
	else \
		echo "no connector runs recorded yet — run 'make sources-pull' first"; \
	fi

# ---------------------------------------------------------------------------
# Phase 1: WeChat RSS bridge (RSSHub + Redis)
# ---------------------------------------------------------------------------

WECHAT_DIR := apps/grok-kb-agent-suite/deploy/wechat-rss

wechat-rss-up:
	cd $(WECHAT_DIR) && docker compose up -d
	@echo "RSSHub at http://127.0.0.1:8080 — see $(WECHAT_DIR)/README.md"

wechat-rss-down:
	cd $(WECHAT_DIR) && docker compose down

wechat-rss-status:
	cd $(WECHAT_DIR) && docker compose ps

# ---------------------------------------------------------------------------
# Phase 2.5: KB → Checklist source-link pipeline
# ---------------------------------------------------------------------------

EXTEND := scripts/checklist_extend.py
LLM    := scripts/checklist_llm_helper.py

# Step 1 — bucket KB cards by vuln_class
checklist-bucket:
	python3 $(EXTEND) --bucket

# Step 3 — show per-checklist diff (dry)
checklist-diff:
	python3 $(EXTEND) --diff

# Step 4-5 — patch sources + add backlinks (dry-run)
checklist-extend:
	python3 $(EXTEND) --apply

# Step 4-5 — write to disk
checklist-extend-commit:
	python3 $(EXTEND) --apply --commit

# Step 6 — verify all link targets exist
checklist-validate:
	python3 $(EXTEND) --validate

# Coverage report
checklist-report:
	python3 $(EXTEND) --report

# Use Grok with realtime search to surface emerging vuln classes we haven't
# bucketed yet. Engine defaults to grok because this needs realtime data.
checklist-discover:
	python3 $(LLM) --task discover --engine grok
