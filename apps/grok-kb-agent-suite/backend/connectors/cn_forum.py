"""Chinese-community forum connector.

Targets that ship native RSS / Discourse / Discuz feeds — no scraping needed:

  * 看雪 (kanxue) Discuz: ``bbs.kanxue.com/forum-{fid}-rss.xml``
  * 52pojie Discuz:       ``52pojie.cn/forum.php?mod=rss&fid={fid}``
  * 90sec Discourse:      ``forum.90sec.com/latest.rss`` or ``/c/{cat}.rss``
  * linux.do Discourse:   ``linux.do/latest.rss`` or ``/tag/security.rss``
  * 安全客 / FreeBuf:     standard RSS (preferred via ``rss_generic``)

Source spec keys::

    id, name, url, connector: cn_forum
    flavour: discuz | discourse | rss   (default: rss)
    cadence, density, region: cn, tags
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Iterator

from .base import RawItem, SourceConnector, register_connector
from ._http import get_text
from ._feed import parse_feed


class CnForumConnector(SourceConnector):
    connector_id = 'cn_forum'
    type = 'rss'
    default_cadence = '0 */4 * * *'

    def fetch(self, source: dict[str, Any], since: datetime | None) -> Iterator[RawItem]:
        url = source.get('url') or ''
        if not url:
            return
        try:
            text = get_text(url, timeout=int(source.get('timeout', 30)))
        except RuntimeError:
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
                tags=sorted({'cn-forum', source.get('flavour', 'rss'), *(source.get('tags') or [])}),
                extra={
                    'source_id': source.get('id') or source.get('name'),
                    'flavour': source.get('flavour', 'rss'),
                },
            )


register_connector(CnForumConnector())
