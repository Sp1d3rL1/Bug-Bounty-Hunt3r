#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'docs' / 'intelligence_kb'

def title(path):
    for line in path.read_text(errors='ignore').splitlines():
        if line.startswith('# '): return line[2:].strip()
    return path.stem

def rel_link(path):
    return path.relative_to(KB).with_suffix('').as_posix()

def build_dir_index(dir_path: Path):
    files = sorted([p for p in dir_path.glob('*.md') if p.name != '_index.md'])
    lines = [f"# {dir_path.name}\n", f"Count: {len(files)}\n"]
    for p in files:
        lines.append(f"- [[{rel_link(p)}|{title(p)}]]")
    (dir_path / '_index.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')

for d in [
    KB/'techniques/new_2024_2026', KB/'techniques/evergreen_new_context', KB/'techniques/niche_tricks',
    KB/'cases/public_reports', KB/'cases/x_threads', KB/'cases/researcher_writeups',
    KB/'reports/platform_reports', KB/'reports/researcher_writeups', KB/'reports/x_discussions',
    KB/'reports/newsletter_roundups', KB/'reports/advisory_related', KB/'reports/imported_authorized',
]:
    d.mkdir(parents=True, exist_ok=True)
    build_dir_index(d)

# top index stats
techs = list((KB/'techniques').glob('*/*.md'))
techs = [p for p in techs if p.name != '_index.md']
cases = list((KB/'cases').glob('*/*.md'))
cases = [p for p in cases if p.name != '_index.md']
reports = list((KB/'reports').glob('*/*.md')) if (KB/'reports').exists() else []
reports = [p for p in reports if p.name != '_index.md']
report_idx = KB/'reports/_index.md'
if (KB/'reports').exists():
    lines = ["# Report Intelligence Index\n", "> 公开披露 Bug Bounty 报告、关联博客/X 讨论/newsletter 的摘要型学习库。\n"]
    for sub in ['platform_reports', 'researcher_writeups', 'x_discussions', 'newsletter_roundups', 'advisory_related', 'imported_authorized']:
        files = sorted([p for p in (KB/'reports'/sub).glob('*.md') if p.name != '_index.md'])
        lines += [f"## {sub}\n", f"Count: {len(files)}\n", f"- [[reports/{sub}/_index|{sub} index]]\n"]
    lines.append(f"\n## 当前状态\n\n- Report cards: {len(reports)}\n- Report ledger: `data/report_intel/report_ledger.tsv`\n")
    report_idx.write_text('\n'.join(lines), encoding='utf-8')
idx = KB/'00_index.md'
text = idx.read_text(errors='ignore') if idx.exists() else '# Bug Bounty Intelligence KB Index\n'
text = re.sub(r'## 当前状态[\s\S]*$', '', text).rstrip()
if '[[reports/_index|Report Intelligence]]' not in text:
    text = text.rstrip() + "\n\n## 报告情报库\n\n- [[reports/_index|Report Intelligence]]：公开披露报告、关联博客/X 讨论/newsletter 摘要库\n"
text += f"""

## 当前状态

- Technique cards: {len(techs)}
- Case cards: {len(cases)}
- Report cards: {len(reports)}
- Total cards: {len(techs)+len(cases)+len(reports)}
- Source ledger: `data/grok_research/source_ledger.tsv`
- Report ledger: `data/report_intel/report_ledger.tsv`
"""
idx.write_text(text.strip()+'\n', encoding='utf-8')
print(f'techniques={len(techs)} cases={len(cases)} reports={len(reports)} total={len(techs)+len(cases)+len(reports)}')
