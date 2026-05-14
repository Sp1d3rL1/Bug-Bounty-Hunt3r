"""GitHub repo connector — monitor commits.atom and releases.atom.

Source spec keys::

    id, name, repo (e.g. "projectdiscovery/nuclei-templates"),
    feed: commits | releases  (default: commits)
    branch: optional, only used for commits.atom
    connector: github_repo
    cadence, density, region, tags
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Iterator

from .base import RawItem, SourceConnector, register_connector
from ._http import get_text
from ._feed import parse_feed


class GithubRepoConnector(SourceConnector):
    connector_id = 'github_repo'
    type = 'rss'
    default_cadence = '30 */3 * * *'

    def fetch(self, source: dict[str, Any], since: datetime | None) -> Iterator[RawItem]:
        repo = source.get('repo') or ''
        if not repo:
            return
        feed = (source.get('feed') or 'commits').lower()
        if feed == 'releases':
            url = f'https://github.com/{repo}/releases.atom'
        elif feed == 'tags':
            url = f'https://github.com/{repo}/tags.atom'
        else:
            branch = source.get('branch') or ''
            url = f'https://github.com/{repo}/commits{("/" + branch) if branch else ""}.atom'
        text = get_text(url, timeout=int(source.get('timeout', 30)))
        for entry in parse_feed(text):
            yield RawItem(
                source_id=str(source.get('id') or source.get('name') or repo),
                source_url=url,
                title=entry.get('title', ''),
                url=entry.get('link', ''),
                published_at=entry.get('published', ''),
                author=entry.get('author', ''),
                summary=entry.get('summary', ''),
                tags=sorted({'github', feed, *(source.get('tags') or [])}),
                extra={'source_id': source.get('id') or source.get('name'), 'repo': repo, 'feed': feed},
            )


register_connector(GithubRepoConnector())
