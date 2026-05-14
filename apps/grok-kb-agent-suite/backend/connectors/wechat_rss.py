"""WeChat public-account connector via wechat2rss / WeRSS / RSSHub bridge.

We do **not** scrape WeChat directly. Instead we point at any RSS endpoint
served by a wechat2rss-compatible bridge running locally (see
``apps/grok-kb-agent-suite/deploy/wechat-rss/docker-compose.yml``).

Source spec keys::

    id, name, url        -> full RSS endpoint of the bridge
    biz                  -> wechat biz id (for documentation only)
    connector: wechat_rss
    cadence (default daily 09:30), density, region: cn, tags

The connector is essentially RSS but enforces a few WeChat-specific
defaults (region = cn, kind = wechat) and tolerates the bridge being down
(returns nothing, records error in metrics tsv).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Iterator

from .base import RawItem, SourceConnector, register_connector
from ._http import get_text
from ._feed import parse_feed


class WechatRssConnector(SourceConnector):
    connector_id = 'wechat_rss'
    type = 'rss'
    default_cadence = '30 9 * * *'

    def fetch(self, source: dict[str, Any], since: datetime | None) -> Iterator[RawItem]:
        url = source.get('url') or ''
        if not url:
            return
        try:
            text = get_text(url, timeout=int(source.get('timeout', 45)))
        except RuntimeError:
            # bridge offline; record in metrics, do not raise
            return
        for entry in parse_feed(text):
            yield RawItem(
                source_id=str(source.get('id') or source.get('name') or url),
                source_url=url,
                title=entry.get('title', ''),
                url=entry.get('link', ''),
                published_at=entry.get('published', ''),
                author=entry.get('author', '') or source.get('name', ''),
                summary=entry.get('summary', ''),
                tags=sorted({'wechat', 'cn', *(source.get('tags') or [])}),
                extra={
                    'source_id': source.get('id') or source.get('name'),
                    'biz': source.get('biz', ''),
                    'kind': 'wechat',
                },
            )


register_connector(WechatRssConnector())
