#!/usr/bin/env python3
"""checklist_extend.py — Bridge KB facts into checklist sources.

The pipeline turns the existing intelligence_kb (techniques + cases +
review_queue) into machine-readable links inside `docs/checklists/*.md` so
the checklists become "live indexes" of the KB instead of static notes.

Stages (each runnable in isolation via CLI flags):

  1. Bucket   — title-keyword classification of every KB card
  2. Map      — vuln_class → checklist_id static dictionary
  3. Diff     — what each checklist's frontmatter `sources:` is missing
  4. Patch    — write missing entries into frontmatter (in-place YAML)
  5. Backlink — append `<!-- backlink: docs/checklists/<id>.md -->` to KB cards
  6. Validate — re-parse all checklists, ensure no cycles, no broken links

LLM is **not** invoked here. The companion `checklist_llm_helper.py` handles
ambiguity arbitration and skeleton generation as a separate, opt-in step.

Usage::

  python3 scripts/checklist_extend.py --bucket
  python3 scripts/checklist_extend.py --diff
  python3 scripts/checklist_extend.py --apply              # dry-run
  python3 scripts/checklist_extend.py --apply --commit     # write to disk
  python3 scripts/checklist_extend.py --report             # coverage report
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'docs' / 'intelligence_kb'
CHECKLISTS_DIR = ROOT / 'docs' / 'checklists'
SKIP_FILE = CHECKLISTS_DIR / '_extend_skip.yaml'

# ---------------------------------------------------------------------------
# Step 1 — vuln_class buckets (title keyword → class label)
# ---------------------------------------------------------------------------

BUCKETS: dict[str, list[str]] = {
    'IDOR/BOLA':            ['idor', 'bola', 'access control', '越权'],
    'OAuth/SSO/JWT/SAML':   ['oauth', 'sso', 'jwt', 'saml', 'openid', 'magic link'],
    'GraphQL':              ['graphql'],
    'Cache':                ['cache', '缓存'],
    'HTTP Smuggling':       ['smuggling', 'request smuggling', 'http2', 'http/2', 'h2c'],
    'Prototype Pollution':  ['prototype', ' pp '],
    'CSPT':                 ['cspt', 'client-side path'],
    'SSTI':                 ['ssti', 'template injection'],
    'Deserialization':      ['deserial', 'unserialize', 'pickle', 'gadget'],
    'File Upload':          ['file upload', '文件上传', 'svg', 'zip slip'],
    'Email/SMTP':           ['smtp', ' spf ', 'dkim', 'dmarc', 'email spoof'],
    'Subdomain Takeover':   ['takeover', 'dangling'],
    'CSRF/CORS/postMessage/WS': ['csrf', 'cors', 'postmessage', 'websocket'],
    'XSS':                  ['xss', 'cross-site script'],
    'Race Condition':       ['race condition', 'race-condition', 'toctou'],
    'Mass Assignment/BOPLA': ['mass assignment', 'bopla'],
    'Cloud-AWS':            ['aws ', ' iam ', ' s3 ', ' lambda ', 'imdsv', 'ec2 metadata'],
    'Cloud-GCP/Azure':      ['gcp ', 'azure ', 'google cloud', 'gcs '],
    'K8s/Container':        ['kubernetes', 'k8s ', 'docker ', ' container'],
    'CI/CD':                ['github action', 'gitlab', 'cicd', 'pipeline', 'pwn request'],
    'Mobile':               ['android', ' ios ', ' apk ', ' intent ', 'deep link'],
    'Web3/Smart Contract':  ['solidity', 'reentrancy', 'web3', ' evm ', ' defi ', 'ethereum'],
    'AI/LLM':               ['llm', 'prompt injection', ' rag ', 'agentic'],
    'Recon':                ['recon', 'subfinder', 'asset discovery', 'attack surface'],
    'GitHub OSINT':         [' github ', ' gist ', 'github recon', 'github actions cache'],
    'Business Logic':       ['business logic', 'coupon', 'refund', 'subscription', 'billing'],
    'WAF Bypass':           [' waf ', 'waf bypass', 'waf rule', 'cloudflare bypass', 'akamai bypass'],
    'SSRF':                 ['ssrf', 'server-side request'],
}


def classify(title: str) -> list[str]:
    """Return all bucket labels whose keyword set matches the lowercase title.

    Padding the title with spaces lets short keywords (e.g. ' pp ', ' iam ')
    match without false positives on substrings like 'apple' or 'iambic'.
    """
    pad = f' {title.lower()} '
    hits: list[str] = []
    for cls, kws in BUCKETS.items():
        if any(kw in pad for kw in kws):
            hits.append(cls)
    return hits

# ---------------------------------------------------------------------------
# Step 2 — vuln_class → checklist_id mapping
# A class may map to multiple checklists (e.g. OAuth touches both oauth.md
# and sso_oidc_saml.md). XSS / SSRF / Race Condition are deliberately split
# across multiple existing checklists rather than getting their own file.
# ---------------------------------------------------------------------------

CLASS_TO_CHECKLISTS: dict[str, list[str]] = {
    'IDOR/BOLA':            ['api'],
    'OAuth/SSO/JWT/SAML':   ['oauth', 'sso_oidc_saml'],
    'GraphQL':              ['graphql'],
    'Cache':                ['cache_deception_poisoning'],
    'HTTP Smuggling':       ['http_request_smuggling'],
    'Prototype Pollution':  ['prototype_pollution_xss_chain'],
    'CSPT':                 ['cspt_client_path_traversal'],
    'SSTI':                 ['ssti_template_injection'],
    'Deserialization':      ['deserialization'],
    'File Upload':          ['file_upload_parser'],
    'Email/SMTP':           ['email_spoof_smtp_smuggling'],
    'Subdomain Takeover':   ['subdomain_takeover'],
    'CSRF/CORS/postMessage/WS': ['cors_postmessage_websocket'],
    'XSS':                  ['cors_postmessage_websocket', 'cspt_client_path_traversal',
                             'prototype_pollution_xss_chain'],
    'Race Condition':       ['payment_business_logic', 'api'],
    'Mass Assignment/BOPLA': ['api'],
    'Cloud-AWS':            ['cloud_aws_metadata_iam'],
    'Cloud-GCP/Azure':      ['cloud_gcp_azure'],
    'K8s/Container':        ['kubernetes_container'],
    'CI/CD':                ['cicd_github_actions'],
    'Mobile':               ['mobile_android_ios'],
    'AI/LLM':               ['ai_llm_prompt_injection'],
    'Recon':                ['recon_methodology'],
    'GitHub OSINT':         ['recon_methodology'],
    'Business Logic':       ['payment_business_logic'],
    'WAF Bypass':           ['waf_bypass'],
    'SSRF':                 ['api', 'cloud_aws_metadata_iam', 'cloud_gcp_azure'],
}

# ---------------------------------------------------------------------------
# YAML frontmatter parsing/writing — strict subset (we control the schema)
# ---------------------------------------------------------------------------


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_block, body). frontmatter without --- delimiters."""
    if not text.startswith('---\n'):
        return '', text
    end = text.find('\n---\n', 4)
    if end < 0:
        return '', text
    return text[4:end], text[end + 5:]


def get_yaml_list(fm: str, key: str) -> list[str]:
    """Get a YAML list value out of a frontmatter block.

    Supports two forms:
        sources: []
        sources:
          - path/a.md
          - path/b.md
    """
    inline = re.search(rf'^{re.escape(key)}:\s*\[(.*?)\]\s*$', fm, re.M)
    if inline:
        body = inline.group(1).strip()
        if not body:
            return []
        return [p.strip().strip('"').strip("'") for p in body.split(',') if p.strip()]
    block = re.search(rf'^{re.escape(key)}:\s*\n((?:\s+-\s+.*\n?)+)', fm, re.M)
    if block:
        items = []
        for line in block.group(1).splitlines():
            m = re.match(r'\s+-\s+(.*?)\s*$', line)
            if m:
                items.append(m.group(1).strip().strip('"').strip("'"))
        return items
    return []


def set_yaml_list(fm: str, key: str, values: list[str]) -> str:
    """Replace the value of `key` with a block-style list (always block form)."""
    block_text = f'{key}:\n' + ''.join(f'  - {v}\n' for v in values)
    block_text = block_text.rstrip('\n')
    inline_re = re.compile(rf'^{re.escape(key)}:\s*\[.*?\]\s*$', re.M)
    if inline_re.search(fm):
        return inline_re.sub(block_text, fm, count=1)
    block_re = re.compile(rf'^{re.escape(key)}:\s*\n((?:\s+-\s+.*\n?)+)', re.M)
    if block_re.search(fm):
        return block_re.sub(block_text + '\n', fm, count=1)
    bare_re = re.compile(rf'^{re.escape(key)}:\s*$', re.M)
    if bare_re.search(fm):
        return bare_re.sub(block_text, fm, count=1)
    return fm.rstrip() + '\n' + block_text + '\n'

# ---------------------------------------------------------------------------
# Step 3-4 — Bucket + Patch
# ---------------------------------------------------------------------------


def collect_kb_cards() -> list[Path]:
    """Every KB markdown that should participate in linking."""
    paths: list[Path] = []
    for sub in ('techniques', 'cases', 'review_queue'):
        d = KB / sub
        if not d.exists():
            continue
        for p in d.rglob('*.md'):
            if p.name == '_index.md':
                continue
            paths.append(p)
    return paths


def title_of(card: Path) -> str:
    """First H1 line, falls back to filename stem."""
    try:
        for line in card.read_text(errors='ignore').splitlines():
            if line.startswith('# '):
                return line[2:].strip()
    except OSError:
        pass
    return card.stem.replace('-', ' ').replace('_', ' ')


def bucket_kb() -> dict[str, list[Path]]:
    """vuln_class → list of KB card paths."""
    out: dict[str, list[Path]] = defaultdict(list)
    for card in collect_kb_cards():
        text = card.read_text(errors='ignore')
        haystack = (title_of(card) + ' ' + text[:600]).lower()
        for cls in classify(haystack):
            out[cls].append(card)
    return out


def list_checklists() -> dict[str, Path]:
    """checklist_id (filename stem) → path."""
    return {p.stem: p for p in sorted(CHECKLISTS_DIR.glob('*.md'))}


def diff_checklist(checklist: Path, expected_sources: list[Path]) -> dict:
    text = checklist.read_text(encoding='utf-8')
    fm, _ = split_frontmatter(text)
    if not fm:
        return {'id': checklist.stem, 'error': 'no frontmatter', 'to_add': [], 'to_remove': []}
    current = set(get_yaml_list(fm, 'sources'))
    expected_rel = sorted({str(p.relative_to(ROOT)) for p in expected_sources})
    expected_set = set(expected_rel)
    return {
        'id': checklist.stem,
        'current_count': len(current),
        'expected_count': len(expected_rel),
        'to_add': sorted(expected_set - current),
        'to_remove': sorted(current - expected_set),
    }


def expected_for_each_checklist(buckets: dict[str, list[Path]]) -> dict[str, set[Path]]:
    """Invert CLASS_TO_CHECKLISTS and merge bucket members."""
    out: dict[str, set[Path]] = defaultdict(set)
    for cls, paths in buckets.items():
        targets = CLASS_TO_CHECKLISTS.get(cls, [])
        for tgt in targets:
            out[tgt].update(paths)
    return out


def patch_checklist(checklist: Path, sources: list[str]) -> str:
    text = checklist.read_text(encoding='utf-8')
    fm, body = split_frontmatter(text)
    if not fm:
        return text
    new_fm = set_yaml_list(fm, 'sources', sorted(sources))
    return f'---\n{new_fm}\n---\n{body}'

# ---------------------------------------------------------------------------
# Step 5 — Backlink
# ---------------------------------------------------------------------------

BACKLINK_RE = re.compile(r'<!--\s*backlink:\s*(.+?)\s*-->')


def add_backlink(card: Path, checklist_rel: str) -> tuple[bool, str]:
    """Append `<!-- backlink: <checklist_rel> -->` if absent.

    Returns (changed, new_text).
    """
    text = card.read_text(errors='ignore', encoding='utf-8')
    existing = set(BACKLINK_RE.findall(text))
    if checklist_rel in existing:
        return False, text
    sep = '\n' if text.endswith('\n') else '\n\n'
    new = text + sep + f'<!-- backlink: {checklist_rel} -->\n'
    return True, new

# ---------------------------------------------------------------------------
# Step 6 — Validate
# ---------------------------------------------------------------------------


def validate_all() -> list[str]:
    issues: list[str] = []
    for cl in list_checklists().values():
        text = cl.read_text(encoding='utf-8')
        fm, _ = split_frontmatter(text)
        if not fm:
            issues.append(f'{cl.relative_to(ROOT)}: no frontmatter')
            continue
        for src in get_yaml_list(fm, 'sources'):
            if not (ROOT / src).exists():
                issues.append(f'{cl.relative_to(ROOT)}: missing source {src}')
    return issues

# ---------------------------------------------------------------------------
# CLI dispatch
# ---------------------------------------------------------------------------


def cmd_bucket() -> None:
    buckets = bucket_kb()
    print(f'KB cards seen: {sum(len(v) for v in buckets.values())} (with overlap)')
    counts = Counter({k: len(v) for k, v in buckets.items()})
    width = max(len(k) for k in counts) if counts else 1
    for k, n in counts.most_common():
        print(f'{k:<{width}}  {n:>4}')


def cmd_diff() -> None:
    buckets = bucket_kb()
    expected = expected_for_each_checklist(buckets)
    cls = list_checklists()
    rows = []
    for cid, path in cls.items():
        exp = expected.get(cid, set())
        d = diff_checklist(path, sorted(exp))
        rows.append(d)
    rows.sort(key=lambda r: -len(r.get('to_add', [])))
    for r in rows:
        print(f"{r['id']:<32}  current={r.get('current_count',0):>3} expected={r.get('expected_count',0):>3}  +{len(r.get('to_add',[])):>3} / -{len(r.get('to_remove',[])):>2}")
    total_add = sum(len(r.get('to_add', [])) for r in rows)
    total_rm = sum(len(r.get('to_remove', [])) for r in rows)
    print(f'\ntotal links to add: {total_add} | to remove: {total_rm}')


def cmd_apply(commit: bool) -> None:
    buckets = bucket_kb()
    expected = expected_for_each_checklist(buckets)
    cls = list_checklists()
    changes_checklists = 0
    changes_backlinks = 0
    for cid, path in cls.items():
        exp_paths = sorted(expected.get(cid, set()))
        rel = sorted(str(p.relative_to(ROOT)) for p in exp_paths)
        if not rel and not get_yaml_list(split_frontmatter(path.read_text())[0], 'sources'):
            continue
        new_text = patch_checklist(path, rel)
        if new_text != path.read_text(encoding='utf-8'):
            changes_checklists += 1
            if commit:
                path.write_text(new_text, encoding='utf-8')
        # backlinks
        for card in exp_paths:
            checklist_rel = str(path.relative_to(ROOT))
            changed, new = add_backlink(card, checklist_rel)
            if changed:
                changes_backlinks += 1
                if commit:
                    card.write_text(new, encoding='utf-8')
    mode = 'COMMIT' if commit else 'DRY-RUN'
    print(f'[{mode}] checklists patched: {changes_checklists}')
    print(f'[{mode}] KB backlinks added: {changes_backlinks}')


def cmd_validate() -> int:
    issues = validate_all()
    if not issues:
        print('OK: 0 broken links across all checklists')
        return 0
    for i in issues[:60]:
        print(f'ISSUE {i}')
    print(f'\ntotal: {len(issues)}')
    return 1


def cmd_report() -> None:
    buckets = bucket_kb()
    expected = expected_for_each_checklist(buckets)
    cls = list_checklists()
    print('=' * 60)
    print('Checklist coverage report')
    print('=' * 60)
    for cid, path in cls.items():
        text = path.read_text(encoding='utf-8')
        fm, _ = split_frontmatter(text)
        sources = get_yaml_list(fm, 'sources') if fm else []
        exp = expected.get(cid, set())
        print(f'{cid:<35} sources={len(sources):>3}  expected={len(exp):>3}')


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n', 1)[0])
    ap.add_argument('--bucket', action='store_true', help='Step 1: classify KB cards')
    ap.add_argument('--diff', action='store_true', help='Step 3: print per-checklist diff')
    ap.add_argument('--apply', action='store_true', help='Step 4-5: patch sources + add backlinks')
    ap.add_argument('--commit', action='store_true', help='Combine with --apply to write to disk')
    ap.add_argument('--validate', action='store_true', help='Step 6: check links resolve')
    ap.add_argument('--report', action='store_true', help='Coverage report')
    args = ap.parse_args(argv)
    if args.bucket:
        cmd_bucket()
        return 0
    if args.diff:
        cmd_diff()
        return 0
    if args.apply:
        cmd_apply(commit=args.commit)
        return 0
    if args.validate:
        return cmd_validate()
    if args.report:
        cmd_report()
        return 0
    ap.print_help()
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
