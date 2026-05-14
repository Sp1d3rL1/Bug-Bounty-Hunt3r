"""Generic RSS / Atom connector.

Source spec keys consumed::

    id, name, url, connector: rss_generic
    cadence, density, region, tags, enabled
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Iterator

from .base import RawItem, SourceConnector, register_connector
from ._http import get_text
from ._feed import parse_feed


class RssGenericConnector(SourceConnector):
    connector_id = 'rss_generic'
    type = 'rss'
    default_cadence = '0 */6 * * *'

    def fetch(self, source: dict[str, Any], since: datetime | None) -> Iterator[RawItem]:
        url = source.get('url') or ''
        if not url:
            return
        text = get_text(url, timeout=int(source.get('timeout', 30)))
        for entry in parse_feed(text):
            yield RawItem(
                source_id=str(source.get('id') or source.get('name') or url),
                source_url=url,
                title=entry.get('title', ''),
                url=entry.get('link', ''),
                published_at=entry.get('published', ''),
                author=entry.get('author', ''),
                summary=entry.get('summary', ''),
                tags=list(source.get('tags') or []),
                extra={'source_id': source.get('id') or source.get('name')},
            )


register_connector(RssGenericConnector())
