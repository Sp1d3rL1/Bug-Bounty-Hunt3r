#!/usr/bin/env python3
"""Safe-default VPS recon pipeline for authorized bug bounty scopes.

This orchestrates common external tools if they are installed. It refuses to run
unless the scope config explicitly acknowledges authorization.
"""
from __future__ import annotations
import argparse, json, os, random, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
LOGS = ROOT / 'logs'

SAFE_NUCLEI_EXCLUDE_TAGS = ['dos','bruteforce','brute-force','intrusive','fuzz','fuzzing','exploit','rce','lfi','sqli']

def load_config(path: str) -> dict:
    cfg = json.loads(Path(path).read_text())
    if not cfg.get('legal_ack'):
        raise SystemExit('Refusing to run: set legal_ack=true only after confirming official authorization and scope.')
    if not cfg.get('authorized_scope_note'):
        raise SystemExit('Refusing to run: authorized_scope_note is empty.')
    return cfg

def sh(cmd: list[str], log_file: Path, dry_run: bool=False, timeout: int=900) -> int:
    line = ' '.join(cmd)
    print(f'[*] {line}')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open('a') as lf:
        lf.write(f'\n$ {line}\n')
        if dry_run:
            lf.write('[dry-run]\n')
            return 0
        try:
            proc = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT, timeout=timeout)
            return proc.returncode
        except subprocess.TimeoutExpired:
            lf.write('[timeout]\n')
            return 124

def which(name: str) -> bool:
    return shutil.which(name) is not None

def write_lines(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    with path.open('w') as f:
        for r in rows:
            r = str(r).strip()
            if r and r not in seen:
                seen.add(r)
                f.write(r + '\n')

def domains_from_config(cfg: dict) -> list[str]:
    domains = []
    for p in cfg.get('in_scope_domains', []):
        p = p.strip().lower()
        if p.startswith('*.'):
            p = p[2:]
        if '*' not in p:
            domains.append(p)
    return sorted(set(domains))

def urls_from_config(cfg: dict) -> list[str]:
    urls = []
    for u in cfg.get('seed_urls', []):
        if u.startswith('http://') or u.startswith('https://'):
            urls.append(u)
    return sorted(set(urls))

def filter_scope(input_file: Path, output_file: Path, rejected_file: Path, cfg_path: str, dry_run: bool):
    cmd = [sys.executable, str(ROOT / 'scripts' / 'scope_guard.py'), '--config', cfg_path, '--input', str(input_file), '--rejected', str(rejected_file)]
    if dry_run:
        print('[*] ' + ' '.join(cmd))
        return
    with output_file.open('w') as out:
        subprocess.run(cmd, stdout=out, check=True)

def summarize_httpx_jsonl(httpx_file: Path, out_file: Path, urls_file: Path):
    if not httpx_file.exists():
        return
    rows = []
    urls = []
    for line in httpx_file.read_text(errors='ignore').splitlines():
        try:
            obj = json.loads(line)
        except Exception:
            continue
        url = obj.get('url') or obj.get('input') or ''
        status = obj.get('status_code') or obj.get('status-code') or ''
        title = obj.get('title') or ''
        tech = ','.join(obj.get('tech', []) or [])
        if url:
            urls.append(url)
        rows.append(f'{url}\t{status}\t{title}\t{tech}')
    write_lines(out_file, rows)
    write_lines(urls_file, urls)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    cfg_path = str(Path(args.config))
    cfg = load_config(cfg_path)
    program = cfg.get('program_name', 'program').replace('/', '_')
    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    run_dir = DATA / program / ts
    latest_dir = DATA / program / 'latest'
    log_file = LOGS / f'{program}.{ts}.log'
    run_dir.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    timeout = int(cfg.get('limits', {}).get('timeout_seconds', 900))
    delay = cfg.get('limits', {}).get('random_delay_seconds', [1, 4])
    if isinstance(delay, list) and len(delay) == 2:
        time.sleep(random.uniform(float(delay[0]), float(delay[1])))

    seeds_domains = run_dir / 'seed_domains.txt'
    seed_urls = run_dir / 'seed_urls.txt'
    write_lines(seeds_domains, domains_from_config(cfg))
    write_lines(seed_urls, urls_from_config(cfg))

    # Passive subdomain collection
    raw_subs = run_dir / 'subdomains.raw.txt'
    scoped_subs = run_dir / 'subdomains.scoped.txt'
    rejected_subs = run_dir / 'subdomains.rejected.txt'
    write_lines(raw_subs, domains_from_config(cfg))

    if cfg.get('recon', {}).get('passive_subdomain', True) and which('subfinder'):
        for d in domains_from_config(cfg):
            sh(['subfinder', '-silent', '-all', '-d', d, '-o', str(run_dir / f'subfinder.{d}.txt')], log_file, args.dry_run, timeout)
            if not args.dry_run and (run_dir / f'subfinder.{d}.txt').exists():
                with raw_subs.open('a') as out, (run_dir / f'subfinder.{d}.txt').open() as src:
                    out.write(src.read())

    if cfg.get('recon', {}).get('amass_passive', False) and which('amass'):
        for d in domains_from_config(cfg):
            sh(['amass', 'enum', '-passive', '-d', d, '-o', str(run_dir / f'amass.{d}.txt')], log_file, args.dry_run, timeout)
            if not args.dry_run and (run_dir / f'amass.{d}.txt').exists():
                with raw_subs.open('a') as out, (run_dir / f'amass.{d}.txt').open() as src:
                    out.write(src.read())

    filter_scope(raw_subs, scoped_subs, rejected_subs, cfg_path, args.dry_run)

    # DNS resolve
    resolved = run_dir / 'resolved.txt'
    if which('dnsx'):
        sh(['dnsx', '-silent', '-l', str(scoped_subs), '-o', str(resolved)], log_file, args.dry_run, timeout)
    else:
        if not args.dry_run:
            shutil.copyfile(scoped_subs, resolved)

    # HTTP probe
    httpx_jsonl = run_dir / 'httpx.jsonl'
    httpx_summary = run_dir / 'httpx.summary.tsv'
    httpx_urls = run_dir / 'httpx.urls.txt'
    if which('httpx'):
        rate = str(cfg.get('limits', {}).get('httpx_rate', 25))
        sh(['httpx', '-silent', '-l', str(resolved), '-title', '-tech-detect', '-status-code', '-json', '-rl', rate, '-retries', '1', '-timeout', '10', '-o', str(httpx_jsonl)], log_file, args.dry_run, timeout)
        if not args.dry_run:
            summarize_httpx_jsonl(httpx_jsonl, httpx_summary, httpx_urls)

    # Passive URLs from archives
    passive_urls = run_dir / 'passive_urls.raw.txt'
    scoped_url_hosts = run_dir / 'passive_url_hosts.scoped.txt'
    if which('gau'):
        for d in domains_from_config(cfg):
            sh(['gau', '--subs', d], log_file, args.dry_run, timeout)
            # gau stdout is logged; use shell redirection manually if you need full URL capture.
    if which('waybackurls'):
        # Keep passive URL collection manual by default to avoid shell piping; documented in vps guide.
        pass

    # Katana active crawl: off by default
    if cfg.get('recon', {}).get('active_crawl', False) and which('katana'):
        rate = str(cfg.get('limits', {}).get('katana_rate', 10))
        sh(['katana', '-list', str(seed_urls), '-silent', '-rl', rate, '-o', str(run_dir / 'katana.urls.txt')], log_file, args.dry_run, timeout)

    # Nuclei low-risk scan
    if cfg.get('recon', {}).get('nuclei_low_risk', True) and which('nuclei'):
        include_tags = ','.join(cfg.get('nuclei', {}).get('include_tags', ['exposure','misconfig','takeover','tech']))
        exclude_tags = ','.join(sorted(set(cfg.get('nuclei', {}).get('exclude_tags', []) + SAFE_NUCLEI_EXCLUDE_TAGS)))
        exclude_sev = ','.join(cfg.get('nuclei', {}).get('exclude_severity', ['critical']))
        rate = str(cfg.get('limits', {}).get('nuclei_rate', 15))
        sh(['nuclei', '-list', str(httpx_urls if httpx_urls.exists() else resolved), '-tags', include_tags, '-exclude-tags', exclude_tags, '-exclude-severity', exclude_sev, '-rl', rate, '-retries', '1', '-timeout', '8', '-jsonl', '-o', str(run_dir / 'nuclei.lowrisk.jsonl')], log_file, args.dry_run, timeout)

    # Diff latest summaries
    if not args.dry_run:
        latest_dir.mkdir(parents=True, exist_ok=True)
        for name in ['subdomains.scoped.txt', 'resolved.txt', 'httpx.urls.txt', 'httpx.summary.tsv']:
            new = run_dir / name
            old = latest_dir / name
            if new.exists():
                diff = run_dir / f'diff.{name}.md'
                subprocess.run([sys.executable, str(ROOT / 'scripts' / 'diff_assets.py'), '--old', str(old), '--new', str(new), '--out', str(diff)], check=False)
                shutil.copyfile(new, old)
        (latest_dir / 'last_run.txt').write_text(str(run_dir) + '\n')

    print(f'[+] run_dir: {run_dir}')
    print(f'[+] log: {log_file}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
