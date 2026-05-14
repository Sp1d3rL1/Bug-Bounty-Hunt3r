#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUITE_RUNS = ROOT / "apps" / "grok-kb-agent-suite" / "data" / "runs"
GLOBAL_LEDGER = ROOT / "data" / "grok_research" / "source_ledger.tsv"

REQUIRED_KEYS = [
    "XAI_API_KEY",
    "TAVILY_API_KEY",
    "GITHUB_TOKEN",
    "HACKERONE_API_USERNAME",
    "HACKERONE_API_TOKEN",
    "BUGCROWD_API_TOKEN",
]

REPORT_TOPICS = "2025-2026 public disclosed bug bounty reports SaaS API OAuth payment GraphQL business logic"
CATALOG_TOPICS = "2025-2026 public disclosed bug bounty reports and writeups Web API SaaS OAuth GraphQL payment business logic client-side cloud AI SaaS"

TECH_TOPICS = {
    "smoke": [
        "OAuth API GraphQL bug bounty techniques 2025 2026 source URLs",
    ],
    "steady": [
        "OAuth API GraphQL authorization bug bounty 2025 2026 source URLs",
        "payment subscription refund business logic bug bounty 2025 2026 source URLs",
        "client-side cloud AI SaaS bug bounty techniques 2025 2026 source URLs",
    ],
    "wide": [
        "OAuth SSO JWT SAML magic link bug bounty 2025 2026 source URLs",
        "API BOLA IDOR GraphQL authorization bug bounty 2025 2026 source URLs",
        "payment subscription invoice coupon refund bug bounty 2025 2026 source URLs",
        "client-side postMessage CSPT DOM web cache bug bounty 2025 2026 source URLs",
        "cloud CI/CD GitHub Actions AI LLM SaaS bug bounty 2025 2026 source URLs",
    ],
}

REPORT_SOURCES = {
    "smoke": ["hackerone"],
    "steady": ["hackerone", "github_security_lab", "blogs_x"],
    "wide": ["public_all", "hackerone", "github", "github_security_lab", "blogs_x"],
}

CATALOG_PRESETS = {
    "smoke": ["public_only"],
    "steady": ["public_only", "research_blogs", "web3_extended", "gray_metadata_only"],
    "wide": ["maximum_coverage", "public_only", "vendor_official", "wp_ecosystem", "research_blogs", "web3_extended", "gray_metadata_only"],
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def now_id(prefix: str) -> str:
    return f"{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}_{prefix}_{hashlib.sha1(os.urandom(16)).hexdigest()[:8]}"


def env_file_values() -> dict[str, str]:
    values: dict[str, str] = {}
    env_path = ROOT / ".env"
    if not env_path.exists():
        return values
    for raw in env_path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        values[k.strip()] = v.strip().strip('"').strip("'")
    return values


def preflight() -> tuple[bool, dict[str, bool]]:
    file_values = env_file_values()
    status = {k: bool(os.getenv(k) or file_values.get(k)) for k in REQUIRED_KEYS}
    return all(status.values()), status


def run_cmd(cmd: list[str], *, cwd: Path = ROOT, dry_run: bool = False, allow_fail: bool = False) -> subprocess.CompletedProcess[str]:
    printable = " ".join(json.dumps(x) if " " in x else x for x in cmd)
    print(f"\n$ {printable}", flush=True)
    if dry_run:
        print("[pipeline dry-run] command not executed", flush=True)
        return subprocess.CompletedProcess(cmd, 0, "", "")
    proc = subprocess.run(cmd, cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.stdout:
        print(proc.stdout[-6000:], flush=True)
    if proc.stderr:
        print(proc.stderr[-6000:], file=sys.stderr, flush=True)
    if proc.returncode != 0 and not allow_fail:
        raise subprocess.CalledProcessError(proc.returncode, cmd, output=proc.stdout, stderr=proc.stderr)
    return proc


def jsonl_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(errors="ignore").splitlines() if line.strip())


def cards_count(run_dir: Path) -> int:
    count = 0
    for p in (run_dir / "cards").glob("*.json"):
        try:
            data = json.loads(p.read_text(errors="ignore"))
            count += len(data.get("cards", []))
        except Exception:
            pass
    return count


def merge_technique_ledger(new_ledger: Path, items_json: Path) -> int:
    if not new_ledger.exists() or not GLOBAL_LEDGER.exists():
        return 0
    existing: list[dict[str, str]] = []
    with GLOBAL_LEDGER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = reader.fieldnames or []
        for row in reader:
            existing.append(row)
    seen = {(r.get("source_url", ""), r.get("local_path", "")) for r in existing}
    max_id = 0
    for row in existing:
        try:
            max_id = max(max_id, int(row.get("id") or 0))
        except ValueError:
            pass
    added = 0
    with new_ledger.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            key = (row.get("source_url", ""), row.get("destination_path", ""))
            if key in seen:
                continue
            max_id += 1
            out = {k: "" for k in fieldnames}
            out.update({
                "id": str(max_id),
                "type": row.get("type", ""),
                "title": row.get("title", ""),
                "author": row.get("author", ""),
                "date": row.get("date", ""),
                "source_url": row.get("source_url", ""),
                "vuln_class": row.get("vuln_class", ""),
                "one_line_trick": row.get("one_line_trick", ""),
                "why_useful": row.get("why_useful", ""),
                "target_type": row.get("target_type", ""),
                "confidence": row.get("confidence", ""),
                "raw_file": str(items_json.relative_to(ROOT)) if str(items_json).startswith(str(ROOT)) else str(items_json),
                "local_path": row.get("destination_path", ""),
            })
            existing.append(out)
            seen.add(key)
            added += 1
    with GLOBAL_LEDGER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(existing)
    return added


def combine_discovery_items(discover_dirs: list[Path], out_json: Path) -> int:
    items: list[dict[str, Any]] = []
    for d in discover_dirs:
        p = d / "items.json"
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(errors="ignore"))
            rows = data.get("items", data if isinstance(data, list) else [])
            if isinstance(rows, list):
                items.extend(rows)
        except Exception as e:
            print(f"[warn] cannot read {p}: {e}", file=sys.stderr)
    seen: set[tuple[str, str]] = set()
    unique: list[dict[str, Any]] = []
    for item in items:
        key = (str(item.get("source_url") or "").strip().lower(), str(item.get("title") or "").strip().lower())
        if not key[0] and not key[1]:
            key = (hashlib.sha256(json.dumps(item, sort_keys=True, ensure_ascii=False).encode()).hexdigest(), "")
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps({"items": unique}, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(unique)


def run_report_pipeline(args: argparse.Namespace, run_root: Path, summary: dict[str, Any]) -> None:
    report_runs: list[Path] = []
    presets = CATALOG_PRESETS[args.mode]
    sources = REPORT_SOURCES[args.mode]

    run_cmd(["python3", "scripts/report_intel_agent.py", "catalog-build"], dry_run=args.dry_run)
    run_cmd(["python3", "scripts/report_intel_agent.py", "manual-channel-prompts"], dry_run=args.dry_run)
    run_cmd(["python3", "scripts/report_intel_agent.py", "export-manual-channel-index"], dry_run=args.dry_run)
    run_cmd(["python3", "scripts/report_intel_agent.py", "validate-discovery-records"], dry_run=args.dry_run)
    run_cmd(["python3", "scripts/report_intel_agent.py", "apply-manual-channel-catalog"], dry_run=args.dry_run)

    for preset in presets:
        rd = run_root / "reports" / f"catalog_{preset}"
        cmd = [
            "python3", "scripts/report_intel_agent.py", "discover-catalog",
            "--preset", preset,
            "--topic", CATALOG_TOPICS,
            "--from-date", args.from_date,
            "--to-date", args.to_date,
            "--limit", str(args.report_limit),
            "--run-dir", str(rd),
        ]
        run_cmd(cmd, dry_run=args.dry_run, allow_fail=True)
        report_runs.append(rd)

    for source in sources:
        rd = run_root / "reports" / f"source_{source}"
        cmd = [
            "python3", "scripts/report_intel_agent.py", "discover",
            "--sources", source,
            "--topic", REPORT_TOPICS,
            "--from-date", args.from_date,
            "--to-date", args.to_date,
            "--limit", str(args.report_limit),
            "--run-dir", str(rd),
        ]
        run_cmd(cmd, dry_run=args.dry_run, allow_fail=True)
        report_runs.append(rd)

    applied = 0
    enriched = 0
    for rd in report_runs:
        candidates = jsonl_count(rd / "discovery" / "candidates.jsonl")
        metadata = jsonl_count(rd / "discovery" / "channel_metadata.jsonl")
        summary["report_runs"].append({"run_dir": str(rd), "candidates": candidates, "metadata": metadata})
        if args.dry_run or candidates <= 0:
            continue
        run_cmd(["python3", "scripts/report_intel_agent.py", "cluster", "--input", str(rd / "discovery" / "candidates.jsonl"), "--run-dir", str(rd)], allow_fail=True)
        proc = run_cmd(["python3", "scripts/report_intel_agent.py", "enrich", "--input", str(rd / "clusters" / "clusters.json"), "--run-dir", str(rd), "--limit", str(args.enrich_limit)], allow_fail=True)
        if proc.returncode != 0:
            continue
        enriched += cards_count(rd)
        proc = run_cmd(["python3", "scripts/report_intel_agent.py", "apply", "--run-dir", str(rd)], allow_fail=True)
        if proc.returncode == 0:
            applied += cards_count(rd)
    summary["report_cards_enriched"] = enriched
    summary["report_cards_applied_attempted"] = applied


def run_technique_pipeline(args: argparse.Namespace, run_root: Path, summary: dict[str, Any]) -> None:
    tech_root = run_root / "techniques"
    discover_dirs: list[Path] = []
    for idx, topic in enumerate(TECH_TOPICS[args.mode], start=1):
        rd = tech_root / f"discover_{idx:02d}"
        cmd = [
            "python3", "scripts/grok_api_agent.py", "discover-topic",
            "--topic", topic,
            "--limit", str(args.technique_limit),
            "--from-date", args.from_date,
            "--to-date", args.to_date,
            "--run-dir", str(rd),
            "--tavily-context",
        ]
        run_cmd(cmd, dry_run=args.dry_run, allow_fail=True)
        discover_dirs.append(rd)
    if args.dry_run:
        return
    items_json = tech_root / "items.json"
    unique_count = combine_discovery_items(discover_dirs, items_json)
    summary["technique_items_unique"] = unique_count
    if unique_count <= 0:
        print("[warn] no technique discovery items to expand", file=sys.stderr)
        return
    prompts_dir = tech_root / "prompts"
    ledger_out = tech_root / "discovery_ledger.tsv"
    batch_size = 5
    end_batch = args.start_batch + ((unique_count - 1) // batch_size)
    run_cmd([
        "python3", "scripts/grok_api_agent.py", "make-prompts-from-discovery",
        "--items-json", str(items_json),
        "--out-dir", str(prompts_dir),
        "--start-batch", str(args.start_batch),
        "--batch-size", str(batch_size),
        "--category", "new_2024_2026",
        "--ledger-out", str(ledger_out),
    ])
    expand_dir = tech_root / "expand"
    run_cmd([
        "python3", "scripts/grok_api_agent.py", "expand-prompts",
        "--from-batch", str(args.start_batch),
        "--to-batch", str(end_batch),
        "--prompt-dir", str(prompts_dir),
        "--run-dir", str(expand_dir),
        "--use-search",
        "--tavily-preverify",
    ])
    run_cmd([
        "python3", "scripts/grok_api_agent.py", "tavily-verify-run",
        "--run-dir", str(expand_dir),
        "--mode", "default",
        "--write-back",
        "--search-missing",
    ], allow_fail=True)
    run_cmd(["python3", "scripts/grok_api_agent.py", "apply-run", "--run-dir", str(expand_dir)])
    added = merge_technique_ledger(ledger_out, items_json)
    summary["technique_cards_applied"] = cards_count(expand_dir)
    summary["technique_ledger_added"] = added


def final_qa(summary: dict[str, Any]) -> None:
    run_cmd(["python3", "scripts/report_intel_agent.py", "validate"])
    run_cmd(["python3", "scripts/grok_kb_build_index.py"])
    run_cmd(["python3", "scripts/grok_kb_validate.py"])
    run_cmd(["python3", "scripts/report_intel_agent.py", "validate-discovery-records"])
    reports = [p for p in (ROOT / "docs/intelligence_kb/reports").glob("*/*.md") if p.name != "_index.md"]
    techs = [p for p in (ROOT / "docs/intelligence_kb/techniques").glob("*/*.md") if p.name != "_index.md"]
    cases = [p for p in (ROOT / "docs/intelligence_kb/cases").glob("*/*.md") if p.name != "_index.md"]
    summary["final_counts"] = {"techniques": len(techs), "cases": len(cases), "reports": len(reports), "total": len(techs) + len(cases) + len(reports)}
    if GLOBAL_LEDGER.exists():
        summary["global_source_ledger_rows"] = max(0, sum(1 for _ in GLOBAL_LEDGER.open()) - 1)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="End-to-end Bug Bounty intelligence pull pipeline")
    p.add_argument("--mode", choices=["smoke", "steady", "wide"], default="steady")
    p.add_argument("--from-date", default="2025-01-01")
    p.add_argument("--to-date", default=dt.date.today().isoformat())
    p.add_argument("--report-limit", type=int, default=10)
    p.add_argument("--enrich-limit", type=int, default=3)
    p.add_argument("--technique-limit", type=int, default=8)
    p.add_argument("--start-batch", type=int, default=201)
    p.add_argument("--run-root")
    p.add_argument("--reports-only", action="store_true")
    p.add_argument("--techniques-only", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    return p


def main() -> None:
    args = build_parser().parse_args()
    ok, key_status = preflight()
    run_root = Path(args.run_root) if args.run_root else SUITE_RUNS / now_id(f"bb_pipeline_{args.mode}")
    run_root.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {
        "mode": args.mode,
        "created_at": utc_now(),
        "run_root": str(run_root),
        "dry_run": args.dry_run,
        "key_status": key_status,
        "report_runs": [],
    }
    (run_root / "pipeline_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[pipeline] run_root={run_root}")
    print("[pipeline] key_status=" + json.dumps(key_status, ensure_ascii=False))
    if not ok and not args.dry_run:
        raise SystemExit("Missing required API keys in .env/environment; use --dry-run or configure keys first.")
    if not args.techniques_only:
        run_report_pipeline(args, run_root, summary)
        (run_root / "pipeline_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    if not args.reports_only:
        run_technique_pipeline(args, run_root, summary)
        (run_root / "pipeline_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    if not args.dry_run:
        final_qa(summary)
    summary["completed_at"] = utc_now()
    (run_root / "pipeline_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[pipeline-summary] " + json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
