"""Tiny HTTP helpers used by every connector.

stdlib-only (no requests / httpx). Honours ``HTTPS_PROXY`` / ``HTTP_PROXY``
env vars so users behind a 127.0.0.1:7890 corporate proxy "just work".
Adds a deterministic User-Agent so target sites can identify us.
"""
from __future__ import annotations

import gzip
import io
import json
import os
import socket
import urllib.error
import urllib.request
from typing import Any

USER_AGENT = 'BugBountyOS-Connector/0.1 (+https://github.com/local)'

DEFAULT_TIMEOUT = 30


def _build_opener() -> urllib.request.OpenerDirector:
    handlers: list[urllib.request.BaseHandler] = []
    proxies: dict[str, str] = {}
    for name in ('HTTPS_PROXY', 'HTTP_PROXY', 'https_proxy', 'http_proxy'):
        v = os.getenv(name)
        if v:
            proxies[name.lower().split('_')[0]] = v
    if proxies:
        handlers.append(urllib.request.ProxyHandler(proxies))
    return urllib.request.build_opener(*handlers)


_OPENER = _build_opener()


def get(url: str, *, headers: dict[str, str] | None = None, timeout: int = DEFAULT_TIMEOUT) -> bytes:
    """GET ``url`` and return raw bytes (decompressed if gzip)."""
    req = urllib.request.Request(url)
    req.add_header('User-Agent', USER_AGENT)
    req.add_header('Accept', '*/*')
    req.add_header('Accept-Encoding', 'gzip')
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with _OPENER.open(req, timeout=timeout) as resp:
            data = resp.read()
            if resp.headers.get('Content-Encoding') == 'gzip':
                data = gzip.decompress(data)
            return data
    except (urllib.error.URLError, socket.timeout, ConnectionError) as e:
        raise RuntimeError(f'GET {url!r} failed: {e}') from e


def get_text(url: str, **kw: Any) -> str:
    raw = get(url, **kw)
    for enc in ('utf-8', 'utf-8-sig', 'latin-1'):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode('utf-8', errors='replace')


def get_json(url: str, **kw: Any) -> Any:
    return json.loads(get_text(url, **kw))
