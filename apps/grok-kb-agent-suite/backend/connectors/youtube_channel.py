"""YouTube channel connector.

Uses the public, key-less RSS endpoint:
    https://www.youtube.com/feeds/videos.xml?channel_id=<UCxxxxxxxxxxxx>

Source spec keys::

    id, name, channel_id (preferred) or url, connector: youtube_channel
    cadence, density, region, tags
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Iterator

from .base import RawItem, SourceConnector, register_connector
from ._http import get_text
from ._feed import parse_feed

YT_FEED = 'https://www.youtube.com/feeds/videos.xml?channel_id={cid}'


class YoutubeChannelConnector(SourceConnector):
    connector_id = 'youtube_channel'
    type = 'rss'
    default_cadence = '15 */4 * * *'

    def fetch(self, source: dict[str, Any], since: datetime | None) -> Iterator[RawItem]:
        cid = source.get('channel_id')
        url = source.get('url') or (YT_FEED.format(cid=cid) if cid else '')
        if not url:
            return
        text = get_text(url, timeout=int(source.get('timeout', 30)))
        for entry in parse_feed(text):
            yield RawItem(
                source_id=str(source.get('id') or source.get('name') or cid or url),
                source_url=url,
                title=entry.get('title', ''),
                url=entry.get('link', ''),
                published_at=entry.get('published', ''),
                author=entry.get('author', '') or source.get('name', ''),
                summary=entry.get('summary', ''),
                tags=sorted({'youtube', *(source.get('tags') or [])}),
                extra={'source_id': source.get('id') or source.get('name'), 'kind': 'video'},
            )


register_connector(YoutubeChannelConnector())
