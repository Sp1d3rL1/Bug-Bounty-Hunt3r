#!/usr/bin/env python3
"""checklist_llm_helper.py — Thin LLM wrapper for the checklist pipeline.

Two engines, no SDK dependencies (stdlib urllib only):

  * ``sonnet``    — Claude Sonnet 4.6 via the local CCR proxy (uses
                    ANTHROPIC_BASE_URL + ANTHROPIC_AUTH_TOKEN env vars).
                    Used for "杂活": arbitration, skeleton drafting.
                    Alias: ``deepseek`` is accepted for backward compat.
  * ``grok``      — xAI v1/chat/completions (uses XAI_API_KEY env var,
                    optional XAI_MODEL override). Used for knowledge-search
                    tasks where realtime X / web data matters.

The checklist_extend pipeline calls this helper for three narrow tasks:

  * ``arbitrate``  — When a card hits multiple buckets, ask the model
                     which one is dominant. Cheap; defaults to sonnet.
  * ``skeleton``   — Generate H2 outline + frontmatter for a fresh
                     checklist file. Slightly heavier prompt; defaults to
                     sonnet.
  * ``discover``   — Scan recent X / web for emerging vuln classes the
                     static BUCKETS dictionary does not yet name.
                     Defaults to **grok** because it needs realtime data.

CLI examples::

  python3 scripts/checklist_llm_helper.py --task arbitrate \
      --card-title "GraphQL Introspection Enabled Leading to IDOR" \
      --buckets "GraphQL,IDOR/BOLA"

  python3 scripts/checklist_llm_helper.py --task skeleton \
      --vuln-class "Recon" --titles-file /tmp/recon_titles.txt

  python3 scripts/checklist_llm_helper.py --task discover --engine grok
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Engine clients
# ---------------------------------------------------------------------------


def _post_json(url: str, headers: dict[str, str], body: dict[str, Any], timeout: int = 90) -> dict[str, Any]:
    data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))


def call_sonnet(system: str, user: str, *, max_tokens: int = 1024, model: str = 'claude-sonnet-4-5') -> str:
    """Anthropic-compatible call routed through the local CCR proxy.

    The proxy at ANTHROPIC_BASE_URL accepts Anthropic Messages-shaped
    requests and forwards them to Claude Sonnet 4.6 (or whatever the router
    is configured to serve). Default model is `claude-sonnet-4-5`; override
    via the `--model` CLI flag if you want a smaller / faster route.
    """
    base = os.environ.get('ANTHROPIC_BASE_URL', '').rstrip('/')
    token = os.environ.get('ANTHROPIC_AUTH_TOKEN') or os.environ.get('ANTHROPIC_API_KEY', '')
    if not (base and token):
        raise RuntimeError('ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN required for sonnet engine')
    body = {
        'model': model,
        'max_tokens': max_tokens,
        'system': system,
        'messages': [{'role': 'user', 'content': user}],
    }
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': token,
        'anthropic-version': '2023-06-01',
    }
    raw = _post_json(f'{base}/v1/messages', headers, body)
    parts = raw.get('content', [])
    return ''.join(p.get('text', '') for p in parts if p.get('type') == 'text').strip()


def call_grok(system: str, user: str, *, max_tokens: int = 1024, model: str | None = None,
              use_search: bool = False) -> str:
    """xAI Grok call (OpenAI-compatible). Reads XAI_API_KEY + XAI_MODEL."""
    key = os.environ.get('XAI_API_KEY') or os.environ.get('GROK_API_KEY', '')
    if not key:
        raise RuntimeError('XAI_API_KEY required for grok engine')
    model = model or os.environ.get('XAI_MODEL', 'grok-4-latest')
    body = {
        'model': model,
        'max_tokens': max_tokens,
        'messages': [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': user},
        ],
    }
    if use_search:
        body['search_parameters'] = {'mode': 'on'}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {key}',
    }
    raw = _post_json('https://api.x.ai/v1/chat/completions', headers, body, timeout=120)
    choices = raw.get('choices') or []
    if not choices:
        return ''
    return (choices[0].get('message') or {}).get('content', '').strip()


def llm_call(engine: str, system: str, user: str, **kw: Any) -> str:
    if engine in ('sonnet', 'deepseek', 'anthropic'):
        return call_sonnet(system, user, **{k: v for k, v in kw.items() if k != 'use_search'})
    if engine == 'grok':
        return call_grok(system, user, **kw)
    raise ValueError(f'unknown engine: {engine}')


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------


SYSTEM_ARBITRATE = (
    'You are a vulnerability taxonomy classifier. Given a card title and a list '
    'of candidate buckets, return the SINGLE most-relevant bucket as one short line '
    'with no extra prose. Choose only from the candidates provided.'
)


def task_arbitrate(engine: str, card_title: str, buckets: list[str]) -> str:
    user = f'Card title: {card_title}\nCandidate buckets: {", ".join(buckets)}\n\nAnswer with one bucket name only.'
    out = llm_call(engine, SYSTEM_ARBITRATE, user, max_tokens=64)
    out = out.strip().splitlines()[0].strip().strip('"').strip("'") if out else ''
    return out if out in buckets else (buckets[0] if buckets else '')


SYSTEM_SKELETON = (
    'You are writing a YAML+Markdown bug-bounty checklist skeleton. Produce ONLY '
    'a valid frontmatter block followed by H2/H3 outline (no specific test '
    'commands, no -[ ] items). Mirror the structure of sso_oidc_saml.md: '
    'frontmatter (id/title/owasp_anchor/cwe/severity_typical/playbook/'
    'last_updated/sources/maturity), then "## 1. Recon", grouped attack-vector '
    'sections, "## 自动化辅助", "## Reporting Angle", "## 已迁移技法 (来自 KB)". '
    'Leave each section body as `<!-- TODO -->`.'
)


def task_skeleton(engine: str, vuln_class: str, sample_titles: list[str]) -> str:
    titles_block = '\n'.join(f'- {t}' for t in sample_titles[:30])
    user = (
        f'Vuln class: {vuln_class}\n\nSample card titles in this bucket:\n{titles_block}\n\n'
        'Generate the skeleton.'
    )
    return llm_call(engine, SYSTEM_SKELETON, user, max_tokens=1500)


SYSTEM_DISCOVER = (
    'You are a bug-bounty taxonomy researcher. Surface emerging vulnerability '
    'classes from 2025-2026 that are not covered by classic OWASP Top 10. Output '
    'a numbered list of <= 10 candidate buckets, each as `<bucket name> | '
    '<one-line why> | <example trick or CVE family>`. Prefer underrepresented or '
    'recently disclosed classes.'
)


def task_discover(engine: str, hint: str = '') -> str:
    user = (
        'Existing buckets: IDOR/BOLA, OAuth/SSO/JWT/SAML, GraphQL, Cache, HTTP '
        'Smuggling, Prototype Pollution, CSPT, SSTI, Deserialization, File '
        'Upload, Email/SMTP, Subdomain Takeover, CSRF/CORS/postMessage/WS, XSS, '
        'Race Condition, Mass Assignment/BOPLA, Cloud-AWS, Cloud-GCP/Azure, '
        'K8s/Container, CI/CD, Mobile, Web3/Smart Contract, AI/LLM, Recon, '
        'GitHub OSINT, Business Logic, WAF Bypass, SSRF.\n\n'
        + (f'Hint: {hint}\n\n' if hint else '')
        + 'List candidate buckets MISSING from the above list.'
    )
    return llm_call(engine, SYSTEM_DISCOVER, user, max_tokens=1500, use_search=True)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n', 1)[0])
    ap.add_argument('--task', required=True, choices=['arbitrate', 'skeleton', 'discover'])
    ap.add_argument('--engine', default='sonnet',
                    choices=['sonnet', 'deepseek', 'anthropic', 'grok'],
                    help='sonnet/deepseek/anthropic = local CCR proxy (Claude Sonnet 4.6); '
                         'grok = xAI realtime')
    ap.add_argument('--card-title', help='for arbitrate')
    ap.add_argument('--buckets', help='comma-separated; for arbitrate')
    ap.add_argument('--vuln-class', help='for skeleton')
    ap.add_argument('--titles-file', help='for skeleton; one title per line')
    ap.add_argument('--hint', default='', help='optional hint for discover')
    args = ap.parse_args(argv)

    try:
        if args.task == 'arbitrate':
            if not args.card_title or not args.buckets:
                ap.error('--card-title and --buckets required for arbitrate')
            print(task_arbitrate(args.engine, args.card_title, [b.strip() for b in args.buckets.split(',') if b.strip()]))
            return 0
        if args.task == 'skeleton':
            if not args.vuln_class or not args.titles_file:
                ap.error('--vuln-class and --titles-file required for skeleton')
            titles = [t.strip() for t in Path(args.titles_file).read_text().splitlines() if t.strip()]
            print(task_skeleton(args.engine, args.vuln_class, titles))
            return 0
        if args.task == 'discover':
            engine = args.engine
            # Even if user asked for 'sonnet' for discover, a heads-up: Grok with
            # realtime search is the recommended engine for emerging-class hunting.
            print(task_discover(engine, args.hint))
            return 0
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f'ERROR ({args.engine} {args.task}): {e}\n')
        return 1
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
