"""Minimal RSS 2.0 / Atom 1.0 parser.

We avoid feedparser because it pulls a lot of transitive deps and is not in
stdlib. Returns a list of dicts ``{title, link, summary, author, published}``.
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Iterator

_NS = {
    'atom': 'http://www.w3.org/2005/Atom',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
}


def parse_feed(xml_text: str) -> Iterator[dict[str, str]]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return iter(())
    tag = _strip_ns(root.tag).lower()
    if tag == 'rss':
        items = root.findall('.//item')
        return (_rss_item_to_dict(it) for it in items)
    if tag == 'feed':
        entries = root.findall('atom:entry', _NS)
        if not entries:
            entries = root.findall('{http://www.w3.org/2005/Atom}entry')
        return (_atom_entry_to_dict(e) for e in entries)
    return iter(())


def _strip_ns(tag: str) -> str:
    return tag.split('}', 1)[-1]


def _text_of(el: ET.Element | None) -> str:
    if el is None or el.text is None:
        return ''
    return el.text.strip()


def _rss_item_to_dict(item: ET.Element) -> dict[str, str]:
    title = _text_of(item.find('title'))
    link = _text_of(item.find('link'))
    desc = _text_of(item.find('description')) or _text_of(item.find('content:encoded', _NS))
    author = (
        _text_of(item.find('author'))
        or _text_of(item.find('dc:creator', _NS))
    )
    pub_raw = _text_of(item.find('pubDate')) or _text_of(item.find('dc:date', _NS))
    return {
        'title': _strip_html(title),
        'link': link,
        'summary': _strip_html(desc)[:1500],
        'author': author,
        'published': _normalise_date(pub_raw),
    }


def _atom_entry_to_dict(entry: ET.Element) -> dict[str, str]:
    def _atom(name: str) -> ET.Element | None:
        el = entry.find(f'atom:{name}', _NS)
        if el is None:
            el = entry.find(f'{{{_NS["atom"]}}}{name}')
        return el

    title = _text_of(_atom('title'))
    summary_el = _atom('summary') or _atom('content')
    summary = _text_of(summary_el)
    author_el = _atom('author')
    author = ''
    if author_el is not None:
        name_el = author_el.find('atom:name', _NS) or author_el.find(f'{{{_NS["atom"]}}}name')
        author = _text_of(name_el)
    link_el = _atom('link')
    link = link_el.attrib.get('href', '') if link_el is not None else ''
    if not link:
        link = _text_of(_atom('id'))
    pub_raw = _text_of(_atom('published')) or _text_of(_atom('updated'))
    return {
        'title': _strip_html(title),
        'link': link,
        'summary': _strip_html(summary)[:1500],
        'author': author,
        'published': _normalise_date(pub_raw),
    }


_TAG_RE = re.compile(r'<[^>]+>')
_WS_RE = re.compile(r'\s+')


def _strip_html(s: str) -> str:
    return _WS_RE.sub(' ', _TAG_RE.sub(' ', s)).strip()


def _normalise_date(raw: str) -> str:
    if not raw:
        return ''
    try:
        dt = parsedate_to_datetime(raw)
        if dt is None:
            raise ValueError
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(raw.replace('Z', '+00:00'))
        except ValueError:
            return raw
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
