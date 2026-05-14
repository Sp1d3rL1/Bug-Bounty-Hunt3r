"""Lightweight, dependency-free scheduler for source connectors.

The scheduler reads ``docs/intelligence/sources.yaml``, computes the next
fire time for each enabled source from its ``cadence`` (subset of cron with
fields ``M H D Mon DoW``), and dispatches connectors when due. State is
persisted to ``data/scheduler_state.json`` so crashes / restarts pick up
where they left off.

There is no daemon mode by default: ``python -m backend.scheduler --tick``
runs one pass and exits. A systemd timer / cron entry / Makefile loop
drives the loop. This matches the rest of the suite's "simple subprocess"
design.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Iterable

# Allow ``python -m backend.scheduler`` and direct execution alike.
_HERE = Path(__file__).resolve()
sys.path.insert(0, str(_HERE.parent))

from connectors.base import (  # noqa: E402  (path adjusted above)
    SOURCES_YAML,
    SUITE_ROOT,
    PROJECT_ROOT,
    load_sources_yaml,
    list_registered,
    run_source,
)

STATE_FILE = SUITE_ROOT / 'data' / 'scheduler_state.json'
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Cron-like cadence parser (subset)
# ---------------------------------------------------------------------------


_FIELDS = ('minute', 'hour', 'day', 'month', 'dow')


def _parse_field(spec: str, lo: int, hi: int) -> set[int]:
    out: set[int] = set()
    for token in spec.split(','):
        token = token.strip()
        if not token:
            continue
        step = 1
        if '/' in token:
            head, step_s = token.split('/', 1)
            step = max(int(step_s), 1)
            token = head
        if token == '*':
            for v in range(lo, hi + 1, step):
                out.add(v)
            continue
        if '-' in token:
            a, b = token.split('-', 1)
            for v in range(int(a), int(b) + 1, step):
                out.add(v)
            continue
        out.add(int(token))
    return {v for v in out if lo <= v <= hi}


def _next_fire(cadence: str, after: datetime) -> datetime:
    parts = cadence.split()
    if len(parts) != 5:
        # default: every 6 hours
        parts = ['0', '*/6', '*', '*', '*']
    minutes = _parse_field(parts[0], 0, 59)
    hours = _parse_field(parts[1], 0, 23)
    days = _parse_field(parts[2], 1, 31)
    months = _parse_field(parts[3], 1, 12)
    dows = _parse_field(parts[4], 0, 6)  # 0 = Sunday

    candidate = (after + timedelta(minutes=1)).replace(second=0, microsecond=0)
    for _ in range(60 * 24 * 366):  # cap one year of search
        if (
            candidate.month in months
            and candidate.day in days
            and candidate.weekday() in _dow_to_weekday(dows)
            and candidate.hour in hours
            and candidate.minute in minutes
        ):
            return candidate
        candidate += timedelta(minutes=1)
    return after + timedelta(hours=6)


def _dow_to_weekday(dows: set[int]) -> set[int]:
    # cron Sunday=0; python weekday Monday=0..Sunday=6
    out: set[int] = set()
    for d in dows:
        out.add((d - 1) % 7)
    return out


# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------


def _load_state() -> dict[str, dict[str, str]]:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding='utf-8'))
    except Exception:
        return {}


def _save_state(state: dict[str, dict[str, str]]) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def _iso(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


# ---------------------------------------------------------------------------
# Tick + run helpers
# ---------------------------------------------------------------------------


def _ensure_connectors_imported() -> None:
    """Trigger registration side-effects."""
    # Importing the package registers each known connector.
    import connectors  # noqa: F401
    import connectors.rss_generic  # noqa: F401
    import connectors.youtube_channel  # noqa: F401
    import connectors.github_repo  # noqa: F401
    import connectors.cve_kev  # noqa: F401
    import connectors.wechat_rss  # noqa: F401
    import connectors.cn_forum  # noqa: F401


def tick(*, dry_run: bool = False, only: str | None = None) -> dict[str, Any]:
    _ensure_connectors_imported()
    sources = load_sources_yaml()
    state = _load_state()
    now = _utc_now()
    results: list[dict[str, Any]] = []
    for src in sources:
        sid = src.get('id') or src.get('name')
        if not sid:
            continue
        if only and sid != only and src.get('connector') != only:
            continue
        if not src.get('enabled', True):
            continue
        cadence = src.get('cadence') or '0 */6 * * *'
        st = state.get(sid, {})
        next_fire_iso = st.get('next_fire')
        next_fire = (
            datetime.strptime(next_fire_iso, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            if next_fire_iso else now - timedelta(seconds=1)
        )
        if now < next_fire and not only:
            continue
        result = run_source(src, since=None, persist=_default_persist, dedup=_default_dedup, dry_run=dry_run)
        state[sid] = {
            'last_fire': _iso(now),
            'next_fire': _iso(_next_fire(cadence, now)),
            'connector': src.get('connector', ''),
        }
        results.append({'id': sid, **result.as_dict()})
    if not dry_run:
        _save_state(state)
    return {'now': _iso(now), 'count': len(results), 'results': results}


# ---------------------------------------------------------------------------
# Default persistence: dump to data/grok_research/connector_inbox/<src>/<id>.json
# Downstream Grok pipeline picks them up the same way as expansion batches.
# ---------------------------------------------------------------------------


INBOX = PROJECT_ROOT / 'data' / 'grok_research' / 'connector_inbox'
INBOX.mkdir(parents=True, exist_ok=True)


def _default_persist(draft: dict[str, Any]) -> bool:
    sid = draft.get('extra', {}).get('source_id') or draft.get('source_name') or 'unknown'
    safe = ''.join(c if c.isalnum() or c in '-._' else '_' for c in sid)
    target_dir = INBOX / safe
    target_dir.mkdir(parents=True, exist_ok=True)
    name = f"{draft.get('date', 'undated').replace(':', '').replace('-', '')[:14]}_{abs(hash(draft.get('source_url', ''))) % (10**8)}.json"
    (target_dir / name).write_text(json.dumps(draft, ensure_ascii=False, indent=2), encoding='utf-8')
    try:
        from dedup import record  # type: ignore[import-not-found]
        record(draft, kept=True)
    except Exception:  # noqa: BLE001
        # dedup index is best-effort; never block persistence on it.
        pass
    return True


def _default_dedup(draft: dict[str, Any]) -> bool:
    try:
        from dedup import is_duplicate  # type: ignore[import-not-found]
        dup, _ = is_duplicate(draft)
        return dup
    except Exception:  # noqa: BLE001
        return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description='Connector scheduler.')
    ap.add_argument('--tick', action='store_true', help='Run one scheduling pass and exit.')
    ap.add_argument('--only', default=None, help='Run a single source id or connector id (forces fire).')
    ap.add_argument('--dry-run', action='store_true', help='Do not persist or update state.')
    ap.add_argument('--list', action='store_true', help='List loaded sources.')
    ap.add_argument('--registered', action='store_true', help='List registered connectors.')
    args = ap.parse_args(argv)
    if args.registered:
        _ensure_connectors_imported()
        for cid in list_registered():
            print(cid)
        return 0
    if args.list:
        srcs = load_sources_yaml()
        print(f'sources_yaml={SOURCES_YAML} count={len(srcs)}')
        for s in srcs:
            print(f"- {s.get('id') or s.get('name')} :: {s.get('connector')} :: {s.get('cadence', '')}")
        return 0
    if args.tick:
        out = tick(dry_run=args.dry_run, only=args.only)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    ap.print_help()
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
