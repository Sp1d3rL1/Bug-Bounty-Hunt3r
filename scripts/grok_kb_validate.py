#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re, csv
ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'docs' / 'intelligence_kb'
LEDGER = ROOT / 'data' / 'grok_research' / 'source_ledger.tsv'
REQUIRED_TECH = ['source_url:', 'source_author:', 'source_date:', 'confidence:', 'risk_level:', '## 核心思路', '## 前置条件', '## 完整技法细节', '## 手工验证流程', '## 授权边界', '## 报告 impact 角度']
REQUIRED_CASE = ['source_url:', 'source_author:', 'source_date:', '## 链接', '## 关键利用链摘要', '## 可迁移技法']
REQUIRED_REPORT = ['canonical_report_url:', 'source_platform:', '## TL;DR', '## 来源与关联材料', '## 漏洞链路摘要', '## Impact 表达方式', '## 可迁移狩猎思路', '## Evidence / 核查元数据']
HIGH_RISK_TERMS = ['credential stuffing', '撞库', 'ddos', 'botnet', 'stealer', 'malware']

def check_file(path, req):
    t = path.read_text(errors='ignore').lower()
    missing = [x for x in req if x.lower() not in t]
    risky = [x for x in HIGH_RISK_TERMS if x in t]
    return missing, risky

techs = [p for p in (KB/'techniques').glob('*/*.md') if p.name != '_index.md']
cases = [p for p in (KB/'cases').glob('*/*.md') if p.name != '_index.md']
reports = [p for p in (KB/'reports').glob('*/*.md') if p.name != '_index.md'] if (KB/'reports').exists() else []
issues=[]
for p in techs:
    m,r = check_file(p, REQUIRED_TECH)
    if m or r: issues.append((p,m,r))
for p in cases:
    m,r = check_file(p, REQUIRED_CASE)
    if m or r: issues.append((p,m,r))
for p in reports:
    m,r = check_file(p, REQUIRED_REPORT)
    if m or r: issues.append((p,m,r))
ledger_rows = 0
if LEDGER.exists():
    with LEDGER.open() as f:
        ledger_rows = max(0, sum(1 for _ in f)-1)
print(f'techniques={len(techs)} cases={len(cases)} reports={len(reports)} total={len(techs)+len(cases)+len(reports)} ledger_rows={ledger_rows} issues={len(issues)}')
for p,m,r in issues[:40]:
    print(f'ISSUE {p}: missing={m} risky={r}')
raise SystemExit(1 if issues else 0)
