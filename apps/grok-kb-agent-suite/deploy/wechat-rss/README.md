# WeChat RSS Bridge — Local Deployment

Phase 1 deliverable: a local RSS bridge so the ``wechat_rss`` connector can pull
Chinese SRC / red-team / research public accounts without scraping WeChat
directly.

## What gets started

* **RSSHub** at ``http://127.0.0.1:8080`` — converts upstream sources into
  RSS/Atom. RSSHub ships dozens of WeChat routes (``/wechat/ce/{biz}``,
  ``/wechatmp/...``) plus 1000+ other adapters.
* **Redis** — backs RSSHub's cache so we don't hammer upstream sites.

## Quick start

```bash
make wechat-rss-up       # docker-compose up -d
make wechat-rss-status   # show container state
make wechat-rss-down     # docker-compose down
```

Then visit ``http://127.0.0.1:8080`` in a browser to confirm RSSHub is alive.
The default UI lists every available route.

## Wiring real public accounts into sources.yaml

For each WeChat account, find a working RSSHub route. Common patterns:

| Pattern | URL template | Notes |
| --- | --- | --- |
| chuansongme.com proxy | ``/wechat/ce/{biz}`` | Most stable; ``biz`` is the WeChat ``__biz`` query parameter |
| wechat2rss bridge     | ``/wechatmp/wgcce/{author}`` | If RSSHub adapter present |
| custom bridge         | ``/<custom>``                 | Requires self-hosted bridge |

Once you have a route URL like
``http://127.0.0.1:8080/wechat/ce/MzU0OTk0NDY3OQ==``, edit
``docs/intelligence/sources.yaml`` and replace the placeholder ``url`` for the
matching ``id`` (e.g. ``wechat-tsrc``, ``wechat-asrc``, …). The ``biz`` field is
documentation-only.

## If you sit behind a corporate proxy

Uncomment the ``PROXY_*`` env vars in ``docker-compose.yml`` (or set them in a
``.env`` next to it) so RSSHub can reach upstream sites through
``host.docker.internal:7890``.

## Why RSSHub instead of self-built scrapers

* Already maintains adapters for the long tail of CN security publications
  (FreeBuf, anquanke, B 站 UP 主, 知乎话题) — same bridge serves multiple
  connectors in this project.
* Active community keeps WeChat-specific routes alive when upstream rotates.
* Pluggable: when an account stops working we swap the route, not the code.
