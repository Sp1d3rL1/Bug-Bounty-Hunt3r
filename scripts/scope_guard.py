#!/usr/bin/env python3
"""Allowlist/out-of-scope guard for authorized bug bounty recon.

Input can be domains, URLs, or JSONL lines containing url/host fields.
Only stdout-safe entries that match in_scope and do not match out_of_scope.
"""
from __future__ import annotations
import argparse, fnmatch, json, re, sys
from pathlib import Path
from urllib.parse import urlparse

DOMAIN_RE = re.compile(r"^[a-zA-Z0-9_.:-]+$")

def load_config(path: str) -> dict:
    cfg = json.loads(Path(path).read_text())
    return cfg

def normalize_host(value: str) -> str | None:
    value = value.strip()
    if not value:
        return None
    # JSONL support
    if value.startswith('{'):
        try:
            obj = json.loads(value)
            value = obj.get('url') or obj.get('host') or obj.get('input') or ''
        except Exception:
            return None
    if '://' in value:
        host = urlparse(value).hostname
    else:
        # Strip path if a raw host/path appears
        host = value.split('/')[0]
    if not host:
        return None
    host = host.strip().lower().rstrip('.')
    if ':' in host and not DOMAIN_RE.match(host):
        return None
    return host

def host_matches(host: str, pattern: str) -> bool:
    p = pattern.lower().strip().rstrip('.')
    if not p:
        return False
    if p.startswith('*.'):
        suffix = p[1:]  # .example.com
        return host.endswith(suffix) and host != p[2:]
    return fnmatch.fnmatch(host, p)

def is_allowed(host: str, cfg: dict) -> bool:
    ins = cfg.get('in_scope_domains', [])
    outs = cfg.get('out_of_scope_domains', [])
    if not any(host_matches(host, p) for p in ins):
        return False
    if any(host_matches(host, p) for p in outs):
        return False
    return True

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--input', required=True, help='File with domains/URLs/JSONL, or - for stdin')
    ap.add_argument('--rejected', help='Optional file to write rejected entries')
    args = ap.parse_args()
    cfg = load_config(args.config)
    source = sys.stdin if args.input == '-' else open(args.input, 'r', encoding='utf-8', errors='ignore')
    rejected = open(args.rejected, 'w', encoding='utf-8') if args.rejected else None
    seen = set()
    try:
        for line in source:
            raw = line.strip()
            host = normalize_host(raw)
            if not host:
                continue
            if host in seen:
                continue
            seen.add(host)
            if is_allowed(host, cfg):
                print(host)
            elif rejected:
                rejected.write(raw + '\n')
    finally:
        if source is not sys.stdin:
            source.close()
        if rejected:
            rejected.close()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
