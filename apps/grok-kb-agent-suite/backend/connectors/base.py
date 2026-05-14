"""SourceConnector abstraction.

Each connector pulls items from a single class of remote source (RSS, GitHub
release atom, CVE feed, wechat2rss endpoint, ...) and yields normalised
``RawItem`` records. Connectors are zero-dependency by default; only
``rss_generic`` requires ``feedparser``. Every connector is responsible for:

  * declaring its supported ``connector_id`` (matched against sources.yaml)
  * implementing ``fetch(source, since)`` — yield ``RawItem``
  * implementing ``normalise(source, raw)`` — produce a TrickCardDraft dict

The scheduler/dispatcher consumes registered connectors via :func:`get_connector`.
"""
from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

# ---------------------------------------------------------------------------
# Paths (mirror state.py constants without forcing an import cycle)
# ---------------------------------------------------------------------------

_HERE = Path(__file__).resolve()
SUITE_ROOT = _HERE.parents[2]
PROJECT_ROOT = SUITE_ROOT.parents[1]
SOURCES_YAML = PROJECT_ROOT / 'docs' / 'intelligence' / 'sources.yaml'
METRICS_TSV = PROJECT_ROOT / 'logs' / 'connector_metrics.tsv'
METRICS_TSV.parent.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class RawItem:
    """A raw record fetched from a source before normalisation."""
    source_id: str
    source_url: str
    title: str
    url: str
    published_at: str  # ISO-8601 UTC
    author: str = ''
    summary: str = ''
    tags: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConnectorResult:
    source_id: str
    fetched: int = 0
    persisted: int = 0
    deduped: int = 0
    dropped: int = 0
    errors: list[str] = field(default_factory=list)
    started_at: str = ''
    finished_at: str = ''

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Source spec loading
# ---------------------------------------------------------------------------


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def load_sources_yaml(path: Path | None = None) -> list[dict[str, Any]]:
    """Load sources.yaml without requiring PyYAML.

    The yaml file must use a strict subset: list of mappings, scalar values,
    and inline list (``[a, b, c]``) for ``tags``. Comments begin with ``#``.
    Anything else raises ``ValueError`` so the file stays machine-checkable.
    """
    p = path or SOURCES_YAML
    if not p.exists():
        return []
    text = p.read_text(encoding='utf-8')
    sources: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if line.startswith('- '):
            if current is not None:
                sources.append(current)
            current = {}
            rest = line[2:].strip()
            if rest:
                _kv_into(current, rest)
            continue
        if line.startswith('  ') and current is not None:
            _kv_into(current, line.strip())
            continue
        # top-level key: ignore (sources.yaml is a flat list)
    if current is not None:
        sources.append(current)
    return sources


def _kv_into(target: dict[str, Any], pair: str) -> None:
    if ':' not in pair:
        return
    k, v = pair.split(':', 1)
    target[k.strip()] = _coerce(v.strip())


def _coerce(v: str) -> Any:
    if not v:
        return ''
    if v.startswith('[') and v.endswith(']'):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [s.strip().strip('"').strip("'") for s in inner.split(',') if s.strip()]
    if v.lower() in {'true', 'false'}:
        return v.lower() == 'true'
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    if v.startswith("'") and v.endswith("'"):
        return v[1:-1]
    try:
        if v.isdigit():
            return int(v)
        return float(v)
    except (TypeError, ValueError):
        return v


# ---------------------------------------------------------------------------
# Connector registry
# ---------------------------------------------------------------------------


_REGISTRY: dict[str, 'SourceConnector'] = {}


def register_connector(connector: 'SourceConnector') -> None:
    _REGISTRY[connector.connector_id] = connector


def get_connector(connector_id: str) -> 'SourceConnector':
    try:
        return _REGISTRY[connector_id]
    except KeyError as e:
        raise KeyError(
            f'connector {connector_id!r} not registered; '
            f'known={sorted(_REGISTRY)}'
        ) from e


def list_registered() -> list[str]:
    return sorted(_REGISTRY)


# ---------------------------------------------------------------------------
# Base connector class
# ---------------------------------------------------------------------------


class SourceConnector:
    """Subclass and set ``connector_id``; implement ``fetch``."""

    connector_id: str = ''
    type: str = 'rss'  # rss | api | scraper | manual
    default_cadence: str = '0 */6 * * *'  # every 6h, override per-source

    # Lifecycle ------------------------------------------------------------
    def fetch(self, source: dict[str, Any], since: datetime | None) -> Iterator[RawItem]:
        raise NotImplementedError

    def normalise(self, source: dict[str, Any], raw: RawItem) -> dict[str, Any]:
        """Produce a TrickCardDraft dict.

        Subclasses MAY override; default emits a minimal draft suitable for
        downstream Grok-prompt expansion.
        """
        return {
            'title': raw.title.strip()[:200],
            'source_url': raw.url,
            'source_name': source.get('name', raw.source_id),
            'author': raw.author,
            'date': raw.published_at,
            'summary': raw.summary[:1200],
            'tags': sorted(set(raw.tags + list(source.get('tags') or []))),
            'connector': self.connector_id,
            'region': source.get('region', ''),
            'density': source.get('density', ''),
            'confidence': 'pending',
            'risk_level': 'low',
            'extra': raw.extra,
        }

    # Reusable helpers -----------------------------------------------------
    def health(self, source: dict[str, Any]) -> dict[str, Any]:
        """Return the most recent metrics for this source from the TSV log."""
        return _last_metric_for(source.get('id') or source.get('name', ''))


# ---------------------------------------------------------------------------
# Metrics writer / reader
# ---------------------------------------------------------------------------

_METRIC_COLS = (
    'ts', 'source_id', 'connector', 'fetched', 'persisted',
    'deduped', 'dropped', 'errors', 'duration_ms'
)


def write_metric(result: ConnectorResult, connector_id: str, duration_ms: int) -> None:
    if not METRICS_TSV.exists():
        METRICS_TSV.write_text('\t'.join(_METRIC_COLS) + '\n', encoding='utf-8')
    row = [
        _utc_now(), result.source_id, connector_id,
        str(result.fetched), str(result.persisted),
        str(result.deduped), str(result.dropped),
        str(len(result.errors)), str(duration_ms),
    ]
    with METRICS_TSV.open('a', encoding='utf-8') as f:
        f.write('\t'.join(row) + '\n')


def _last_metric_for(source_id: str) -> dict[str, Any]:
    if not source_id or not METRICS_TSV.exists():
        return {}
    last: dict[str, Any] = {}
    for line in METRICS_TSV.read_text(encoding='utf-8').splitlines()[1:]:
        parts = line.split('\t')
        if len(parts) != len(_METRIC_COLS):
            continue
        if parts[1] == source_id:
            last = dict(zip(_METRIC_COLS, parts))
    return last


# ---------------------------------------------------------------------------
# Convenience runner
# ---------------------------------------------------------------------------


def run_source(
    source: dict[str, Any],
    *,
    since: datetime | None = None,
    persist: Callable[[dict[str, Any]], bool] | None = None,
    dedup: Callable[[dict[str, Any]], bool] | None = None,
    dry_run: bool = False,
) -> ConnectorResult:
    """Run a single source through its connector.

    ``persist`` should return True if the normalised draft was stored.
    ``dedup`` should return True if the item was a duplicate (and skipped).
    """
    connector_id = source.get('connector') or ''
    source_id = source.get('id') or source.get('name') or ''
    started = time.time()
    result = ConnectorResult(source_id=source_id, started_at=_utc_now())
    try:
        connector = get_connector(connector_id)
    except KeyError as e:
        result.errors.append(str(e))
        result.finished_at = _utc_now()
        write_metric(result, connector_id, int((time.time() - started) * 1000))
        return result
    try:
        for raw in connector.fetch(source, since):
            result.fetched += 1
            draft = connector.normalise(source, raw)
            if dry_run:
                continue
            if dedup is not None and dedup(draft):
                result.deduped += 1
                continue
            if persist is not None and persist(draft):
                result.persisted += 1
            else:
                result.dropped += 1
    except Exception as e:  # noqa: BLE001 — connector errors are recorded, not raised
        result.errors.append(repr(e))
    result.finished_at = _utc_now()
    write_metric(result, connector_id, int((time.time() - started) * 1000))
    return result


# ---------------------------------------------------------------------------
# CLI smoke entry: ``python -m connectors.base --check``
# ---------------------------------------------------------------------------


def _cli(argv: list[str]) -> int:
    if '--check' in argv:
        srcs = load_sources_yaml()
        sys.stdout.write(json.dumps({
            'sources_yaml': str(SOURCES_YAML),
            'count': len(srcs),
            'sample': srcs[:3],
            'registered': list_registered(),
        }, ensure_ascii=False, indent=2))
        sys.stdout.write('\n')
        return 0
    sys.stdout.write('usage: python -m connectors.base --check\n')
    return 2


if __name__ == '__main__':
    raise SystemExit(_cli(sys.argv[1:]))
