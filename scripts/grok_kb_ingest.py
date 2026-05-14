#!/usr/bin/env python3
"""Ingest SuperGrok TSV/Markdown-table outputs into the Obsidian intelligence KB.

This parser is intentionally tolerant: Grok may output pipe tables, TSV, or bullet-ish rows.
It creates source ledger entries plus first-pass cards. Expanded cards can overwrite/refine later.
"""
from __future__ import annotations
import argparse, csv, re, unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'docs' / 'intelligence_kb'
LEDGER = ROOT / 'data' / 'grok_research' / 'source_ledger.tsv'

HEADERS = ['id','type','title','author','date','source_url','vuln_class','one_line_trick','why_useful','target_type','confidence']

TOPIC_CATEGORIES = {
    'topic_01': 'new_method', 'topic_02': 'new_method', 'topic_03': 'new_method', 'topic_04': 'new_method',
    'topic_05': 'new_method', 'topic_06': 'new_method', 'topic_07': 'new_method', 'topic_08': 'new_method',
    'topic_09': 'new_method', 'topic_10': 'new_method', 'topic_11': 'evergreen', 'topic_12': 'trick',
}

def slugify(s: str, maxlen: int = 88) -> str:
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s.lower()).strip('-')
    return (s[:maxlen].strip('-') or 'untitled')

def clean_cell(s: str) -> str:
    s = s.strip().strip('|').strip()
    s = re.sub(r'\s+', ' ', s)
    return s


def normalize_obj(obj: dict) -> dict:
    """Clean DOM-snapshot artifacts from Grok output."""
    blob = (obj.get('source_url','') + ' ' + obj.get('vuln_class',''))
    urls = re.findall(r'https?://[^\s"<>]+', blob)
    if urls:
        u = urls[0]
        u = u.split('%C2%A7')[0].split('§')[0]
        obj['source_url'] = u.rstrip('.,)')
    # DOM snapshots often render links as: cell6='API": - /url: ... - text: BOLA/IDOR'
    vc = obj.get('vuln_class','')
    m = re.findall(r'- text: ?"?([^"\n]+)', vc)
    if m:
        obj['vuln_class'] = clean_cell(m[-1])
    else:
        obj['vuln_class'] = clean_cell(vc.split('/url:')[0].strip(' "'))
    for k in list(obj):
        obj[k] = clean_cell(str(obj[k]).replace('%C2%A7','§'))
    return obj

def parse_rows(text: str):
    rows = []
    # Preferred Grok-safe format: @@id§type§title§author§date§url§class§trick§why§target§confidence@@
    # DOM snapshots include the user's prompt with @@ID...@@ and an extra '@@' in instructions;
    # start parsing at the first numeric record to avoid prompt pollution.
    m_start = re.search(r'@@\d+§', text)
    text_for_records = text[m_start.start():] if m_start else text
    for rec in re.findall(r'@@(.*?)@@', text_for_records, flags=re.S):
        cells = [clean_cell(x) for x in rec.split('§')]
        if len(cells) >= 6:
            cells = (cells + [''] * len(HEADERS))[:len(HEADERS)]
            obj = normalize_obj(dict(zip(HEADERS, cells)))
            if obj['id'].lower() != 'id' and obj['title']:
                rows.append(obj)
    if rows:
        return rows
    for line in text.splitlines():
        raw = line.strip()
        if not raw or raw.startswith('```'):
            continue
        if raw.lower().startswith('id |') or raw.lower().startswith('id\t'):
            continue
        if set(raw.replace('|','').strip()) <= {'-',' ',':'}:
            continue
        cells = None
        if '\t' in raw:
            cells = [clean_cell(x) for x in raw.split('\t')]
        elif raw.count('|') >= 8:
            cells = [clean_cell(x) for x in raw.strip('|').split('|')]
        if not cells or len(cells) < 6:
            continue
        # pad/truncate
        cells = (cells + [''] * len(HEADERS))[:len(HEADERS)]
        obj = normalize_obj(dict(zip(HEADERS, cells)))
        if obj['id'].lower() == 'id' or not obj['title']:
            continue
        rows.append(obj)
    return rows

def classify_category(raw_file: Path, row: dict) -> str:
    name = raw_file.name.lower()
    for prefix, cat in TOPIC_CATEGORIES.items():
        if prefix in name:
            return cat
    t = (row.get('vuln_class','') + ' ' + row.get('one_line_trick','')).lower()
    if 'old' in t or 'evergreen' in t or 'classic' in t:
        return 'evergreen'
    if 'trick' in t or 'bypass' in t or 'weird' in t:
        return 'trick'
    return 'new_method'

def tech_dir_for(category: str) -> Path:
    if category == 'evergreen': return KB / 'techniques' / 'evergreen_new_context'
    if category == 'trick': return KB / 'techniques' / 'niche_tricks'
    return KB / 'techniques' / 'new_2024_2026'

def case_dir_for(row: dict) -> Path:
    src = (row.get('source_url','') + ' ' + row.get('title','')).lower()
    if 'hackerone' in src or 'bugcrowd' in src or 'intigriti' in src or 'yeswehack' in src:
        return KB / 'cases' / 'public_reports'
    if 'x.com' in src or 'twitter.com' in src:
        return KB / 'cases' / 'x_threads'
    return KB / 'cases' / 'researcher_writeups'

def freshness(d: str) -> str:
    for y in ['2026','2025','2024']:
        if y in d:
            return y
    return 'evergreen'

def target_list(s: str) -> list[str]:
    toks = re.split(r'[,/;]+', s or '')
    vals = [x.strip() for x in toks if x.strip()]
    return vals or ['Web', 'API']

def yaml_list(vals):
    return '\n'.join(f'  - {v}' for v in vals)

def write_tech_card(row: dict, raw_file: Path, category: str) -> Path:
    title = row['title']
    slug = slugify(f"{row.get('id','')}-{title}")
    path = tech_dir_for(category) / f'{slug}.md'
    risk = 'high' if re.search(r'payment|refund|billing|race|token|oauth|sso|jwt|tenant|idor|bola', (row.get('vuln_class','')+' '+row.get('title','')).lower()) else 'medium'
    body = f"""---
type: technique
category: {category}
vuln_class: {row.get('vuln_class','')}
source_url: {row.get('source_url','')}
source_author: {row.get('author','')}
source_date: {row.get('date','')}
collected_at: {date.today().isoformat()}
freshness: {freshness(row.get('date',''))}
confidence: {row.get('confidence','medium') or 'medium'}
risk_level: {risk}
target_types:
{yaml_list(target_list(row.get('target_type','')))}
raw_file: {raw_file.as_posix()}
---

# {title}

## 核心思路

{row.get('one_line_trick','') or '待从 Grok 扩展输出补全。'}

## 前置条件

- 目标在授权范围内。
- 该业务/接口/功能与 `{row.get('vuln_class','')}` 相关。
- 使用自有测试账号、靶场或项目允许的测试数据。

## 完整技法细节

{row.get('why_useful','') or '待扩展。'}

> TODO：用 5 条一组 Grok 扩展 prompt 补充完整细节、失败条件和案例映射。

## 适用目标画像

- {row.get('target_type','Web/API/SaaS')}

## 为什么有效

{row.get('why_useful','') or '待扩展。'}

## 手工验证流程（授权 / Lab only）

1. 确认项目 rules of engagement 明确允许该类别测试。
2. 搭建双账号或 sandbox 测试数据，避免触达真实用户数据。
3. 复现来源中的业务前提，只记录最小必要证据。
4. 证明 server-side impact；不要依赖客户端表现。
5. 截图/保存请求响应时打码 token、cookie、PII、支付信息。

## 可自动化部分

- 资产/endpoint 发现、参数枚举、schema 对比、变更 diff 可自动化。
- 权限、支付、状态机、业务影响必须手工确认。

## 误报/失败条件

- 目标不存在相同业务前提。
- 防护在服务端强校验。
- 只影响自有账号且无跨权限/跨租户/财务/数据影响。

## 授权边界

仅用于授权 Bug Bounty、靶场、自有环境。不得用于越界扫描、爆破、DoS、真实支付损害、非授权读取第三方数据。

## 报告 impact 角度

围绕 `{row.get('vuln_class','')}` 说明可导致的未授权数据访问、权限提升、业务绕过、财务影响或合规风险。

## 相关案例链接

- {row.get('source_url','')}
"""
    path.write_text(body, encoding='utf-8')
    return path

def write_case_card(row: dict, raw_file: Path) -> Path:
    title = row['title']
    slug = slugify(f"{row.get('id','')}-{title}")
    path = case_dir_for(row) / f'{slug}.md'
    body = f"""---
type: case
vuln_class: {row.get('vuln_class','')}
source_url: {row.get('source_url','')}
source_author: {row.get('author','')}
source_date: {row.get('date','')}
collected_at: {date.today().isoformat()}
freshness: {freshness(row.get('date',''))}
confidence: {row.get('confidence','medium') or 'medium'}
target_types:
{yaml_list(target_list(row.get('target_type','')))}
raw_file: {raw_file.as_posix()}
---

# {title}

## 链接

{row.get('source_url','')}

## 漏洞类型

{row.get('vuln_class','')}

## 目标业务场景

{row.get('target_type','')}

## 关键利用链摘要

{row.get('one_line_trick','')}

## 可迁移技法

{row.get('why_useful','')}

## 为什么值得收藏

- 可作为 `{row.get('vuln_class','')}` 的报告 impact / 业务路径参考。
- 只保存链接和描述；完整复现以原文和授权环境为准。
"""
    path.write_text(body, encoding='utf-8')
    return path

def append_ledger(rows, raw_file: Path, local_paths):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    if not LEDGER.exists():
        LEDGER.write_text('\t'.join(HEADERS + ['raw_file','local_path']) + '\n', encoding='utf-8')
    with LEDGER.open('a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        for row, path in zip(rows, local_paths):
            writer.writerow([row.get(h,'') for h in HEADERS] + [raw_file.as_posix(), path.as_posix()])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw-dir', required=True)
    args = ap.parse_args()
    raw_dir = Path(args.raw_dir)
    all_rows = []
    all_paths = []
    for raw_file in sorted(raw_dir.glob('*.md')) + sorted(raw_dir.glob('*.tsv')) + sorted(raw_dir.glob('*.txt')):
        text = raw_file.read_text(encoding='utf-8', errors='ignore')
        rows = parse_rows(text)
        paths = []
        for row in rows:
            typ = row.get('type','').lower()
            if 'case' in typ or 'report' in typ or 'writeup' in typ:
                path = write_case_card(row, raw_file)
            elif 'resource' in typ:
                # resources go to review queue for now
                path = KB / 'review_queue' / (slugify(f"{row.get('id','')}-{row.get('title','')}") + '.md')
                path.write_text(f"# {row.get('title','')}\n\n- Source: {row.get('source_url','')}\n- Author: {row.get('author','')}\n- Why useful: {row.get('why_useful','')}\n", encoding='utf-8')
            else:
                cat = classify_category(raw_file, row)
                path = write_tech_card(row, raw_file, cat)
            paths.append(path)
        if rows:
            append_ledger(rows, raw_file, paths)
            all_rows.extend(rows); all_paths.extend(paths)
            print(f'ingested {len(rows)} from {raw_file}')
    print(f'total {len(all_rows)} rows, {len(all_paths)} cards')

if __name__ == '__main__':
    main()
