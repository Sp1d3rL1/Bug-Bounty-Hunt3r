#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import re, csv, urllib.parse, random, json
ROOT=Path(__file__).resolve().parents[1]
KB=ROOT/'docs/intelligence_kb'
LEDGER=ROOT/'data/grok_research/source_ledger.tsv'
OUT=KB/'curated_300.md'

# Freshness decay: confidence is multiplied by FRESHNESS_FACTOR ** (age_days // FRESHNESS_WINDOW_DAYS).
# 90 days × 0.7 was the design target; expressed as constants to keep behaviour visible.
FRESHNESS_WINDOW_DAYS = 90
FRESHNESS_FACTOR = 0.7

def title(p):
    for line in p.read_text(errors='ignore').splitlines():
        if line.startswith('# '): return line[2:].strip()
    return p.stem

def meta(p,key):
    m=re.search(rf'^{re.escape(key)}:\s*(.*)$', p.read_text(errors='ignore'), re.M)
    return m.group(1).strip() if m else ''

def obs_link(p):
    return p.relative_to(KB).with_suffix('').as_posix()

def _parse_date(raw: str):
    if not raw: return None
    raw = raw.strip().split()[0]
    for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S'):
        try: return datetime.strptime(raw, fmt).replace(tzinfo=timezone.utc)
        except ValueError: continue
    return None

def freshness_factor(p):
    """Return decay multiplier in (0, 1]; older cards are penalised."""
    d = _parse_date(meta(p, 'date'))
    if d is None: return 1.0
    age_days = (datetime.now(timezone.utc) - d).days
    if age_days <= FRESHNESS_WINDOW_DAYS: return 1.0
    windows = age_days // FRESHNESS_WINDOW_DAYS
    return FRESHNESS_FACTOR ** windows

def score(p):
    t=p.read_text(errors='ignore').lower()
    s=0
    if 'confidence: high' in t: s+=20
    if 'risk_level: high' in t: s+=8
    for kw in ['api','bola','idor','oauth','sso','jwt','graphql','tenant','payment','billing','subscription','cache','smuggling','cloud','github','ai','llm','postmessage','cspt']:
        if kw in t: s+=2
    if 'derived_from_case: false' in t: s+=5
    return s * freshness_factor(p)

techs=[p for p in (KB/'techniques').glob('*/*.md') if p.name!='_index.md']
cases=[p for p in (KB/'cases').glob('*/*.md') if p.name!='_index.md']
techs=sorted(techs, key=lambda p:(-score(p), str(p)))
cases=sorted(cases, key=lambda p:(-score(p), str(p)))
cur_tech=techs[:210]
cur_case=cases[:90]
lines=['# Curated 300 Bug Bounty Intelligence Records','', '> 这是 v1 精选索引：210 条技法 + 90 条案例。完整扩展库仍保留在 techniques/ 与 cases/ 目录。','',f'- Curated techniques: {len(cur_tech)}',f'- Curated cases: {len(cur_case)}',f'- Full technique cards: {len(techs)}',f'- Full case cards: {len(cases)}','']
from collections import defaultdict
by=defaultdict(list)
for p in cur_tech: by[p.parent.name].append(p)
lines.append('## 210 技法精选')
for group, arr in sorted(by.items()):
    lines += ['', f'### {group} ({len(arr)})']
    for p in arr:
        lines.append(f"- [[{obs_link(p)}|{title(p)}]] — `{meta(p,'vuln_class')}` / `{meta(p,'confidence')}` / `{meta(p,'risk_level')}`")
lines += ['', '## 90 案例精选']
byc=defaultdict(list)
for p in cur_case: byc[p.parent.name].append(p)
for group, arr in sorted(byc.items()):
    lines += ['', f'### {group} ({len(arr)})']
    for p in arr:
        src=meta(p,'source_url')
        lines.append(f"- [[{obs_link(p)}|{title(p)}]] — `{meta(p,'vuln_class')}` — {src}")
OUT.write_text('\n'.join(lines)+'\n')
print(f'wrote {OUT} tech={len(cur_tech)} cases={len(cur_case)}')
