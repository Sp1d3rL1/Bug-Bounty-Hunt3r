"""SimHash-based deduplication for connector inbox drafts.

Connectors emit normalised drafts into ``data/grok_research/connector_inbox/``.
Before any draft is queued for Grok-prompt expansion we check it against
``data/grok_research/dedup_index.sqlite``: if a SimHash within Hamming
distance 3 already exists, mark the draft as duplicate and skip.

SimHash is a 64-bit fingerprint of (title + summary + tags + vuln class).
Stdlib only — no datasketch/simhash deps. The index is small (one row per
persisted draft), and queries are O(N) hamming distance — fine up to
millions of entries which is far beyond what we'll ever store.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / 'data' / 'grok_research' / 'dedup_index.sqlite'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

HAMMING_THRESHOLD = 3   # within 3 of an existing fingerprint -> duplicate
SIMHASH_BITS = 64

# ---------------------------------------------------------------------------
# SimHash
# ---------------------------------------------------------------------------


def _features(draft: dict[str, Any]) -> Iterable[str]:
    """Tokens used as SimHash features. Stable across runs."""
    title = (draft.get('title') or '').lower()
    summary = (draft.get('summary') or '').lower()
    vuln = (draft.get('vuln_class') or draft.get('extra', {}).get('vuln_class') or '').lower()
    tags = ' '.join(sorted(draft.get('tags') or [])).lower()
    text = ' '.join([title, summary, vuln, tags])
    # 3-character shingles, with whitespace collapsed.
    text = ' '.join(text.split())
    if len(text) < 3:
        yield text
        return
    for i in range(0, len(text) - 2, 1):
        yield text[i:i + 3]


def simhash(draft: dict[str, Any]) -> int:
    bits = [0] * SIMHASH_BITS
    for tok in _features(draft):
        h = int(hashlib.blake2b(tok.encode('utf-8'), digest_size=8).hexdigest(), 16)
        for i in range(SIMHASH_BITS):
            if h & (1 << i):
                bits[i] += 1
            else:
                bits[i] -= 1
    out = 0
    for i, b in enumerate(bits):
        if b >= 0:
            out |= 1 << i
    return out


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        'CREATE TABLE IF NOT EXISTS dedup ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'simhash INTEGER NOT NULL, '
        'source_url TEXT, '
        'title TEXT, '
        'first_seen TEXT NOT NULL, '
        'kept INTEGER NOT NULL DEFAULT 1, '
        'merged_into INTEGER'
        ')'
    )
    conn.execute('CREATE INDEX IF NOT EXISTS idx_simhash ON dedup(simhash)')
    return conn


def is_duplicate(draft: dict[str, Any], threshold: int = HAMMING_THRESHOLD) -> tuple[bool, int | None]:
    """Return ``(is_dup, matched_id)`` where matched_id is the existing row id."""
    h = simhash(draft)
    src = draft.get('source_url') or ''
    with _connect() as conn:
        # Fast exact-URL short-circuit; many duplicate fetches share the URL.
        if src:
            row = conn.execute('SELECT id FROM dedup WHERE source_url = ?', (src,)).fetchone()
            if row:
                return True, row[0]
        # Fallback: scan SimHash table (cheap up to millions of rows).
        for row in conn.execute('SELECT id, simhash FROM dedup'):
            if hamming(h, row[1]) <= threshold:
                return True, row[0]
    return False, None


def record(draft: dict[str, Any], *, kept: bool = True, merged_into: int | None = None) -> int:
    h = simhash(draft)
    with _connect() as conn:
        cur = conn.execute(
            'INSERT INTO dedup(simhash, source_url, title, first_seen, kept, merged_into) '
            'VALUES (?, ?, ?, ?, ?, ?)',
            (
                h,
                draft.get('source_url') or '',
                draft.get('title', '')[:300],
                draft.get('date') or draft.get('first_seen') or '',
                int(bool(kept)),
                merged_into,
            ),
        )
        conn.commit()
        return int(cur.lastrowid or 0)


def stats() -> dict[str, Any]:
    if not DB_PATH.exists():
        return {'rows': 0}
    with _connect() as conn:
        total = conn.execute('SELECT COUNT(*) FROM dedup').fetchone()[0]
        kept = conn.execute('SELECT COUNT(*) FROM dedup WHERE kept = 1').fetchone()[0]
        return {'rows': total, 'kept': kept, 'dropped': total - kept}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _cli(argv: list[str]) -> int:
    if not argv or argv[0] in {'-h', '--help'}:
        sys.stdout.write(
            'usage:\n'
            '  python -m backend.dedup --stats\n'
            '  python -m backend.dedup --check <draft.json>\n'
            '  python -m backend.dedup --record <draft.json>\n'
        )
        return 0
    if argv[0] == '--stats':
        sys.stdout.write(json.dumps(stats(), indent=2) + '\n')
        return 0
    if argv[0] in {'--check', '--record'}:
        if len(argv) < 2:
            sys.stdout.write('error: missing draft path\n')
            return 2
        draft = json.loads(Path(argv[1]).read_text(encoding='utf-8'))
        if argv[0] == '--check':
            dup, match = is_duplicate(draft)
            sys.stdout.write(json.dumps({'duplicate': dup, 'matched_id': match}, indent=2) + '\n')
        else:
            new_id = record(draft, kept=True)
            sys.stdout.write(json.dumps({'recorded_id': new_id}, indent=2) + '\n')
        return 0
    sys.stdout.write(f'unknown command: {argv[0]}\n')
    return 2


if __name__ == '__main__':
    raise SystemExit(_cli(sys.argv[1:]))
