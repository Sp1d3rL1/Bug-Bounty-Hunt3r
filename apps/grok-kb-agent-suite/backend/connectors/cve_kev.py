"""CVE / KEV / OSV / GitHub Advisories early-signal connector.

A single source spec selects the upstream via ``feed`` key:

    feed: nvd_recent       -> NVD 2.0 recent CVEs (last 14 days)
    feed: cisa_kev         -> CISA Known Exploited Vulnerabilities JSON
    feed: osv              -> OSV.dev list (use ``ecosystem`` filter)
    feed: zdi              -> ZDI advisories RSS

For NVD / OSV we hit JSON APIs and emit one RawItem per record.
For CISA KEV we hit the official JSON catalog.
For ZDI we just defer to rss_generic if you want it; this connector does NOT
shell out to it.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any, Iterator

from .base import RawItem, SourceConnector, register_connector
from ._http import get_json, get_text
from ._feed import parse_feed


NVD_RECENT = (
    'https://services.nvd.nist.gov/rest/json/cves/2.0?'
    'pubStartDate={start}&pubEndDate={end}'
)
CISA_KEV_JSON = (
    'https://www.cisa.gov/sites/default/files/feeds/'
    'known_exploited_vulnerabilities.json'
)
OSV_LIST = 'https://api.osv.dev/v1/query'
ZDI_RSS = 'https://www.zerodayinitiative.com/blog?format=rss'


class CveKevConnector(SourceConnector):
    connector_id = 'cve_kev'
    type = 'api'
    default_cadence = '0 */8 * * *'

    def fetch(self, source: dict[str, Any], since: datetime | None) -> Iterator[RawItem]:
        feed = (source.get('feed') or 'nvd_recent').lower()
        if feed == 'nvd_recent':
            yield from self._fetch_nvd(source)
        elif feed == 'cisa_kev':
            yield from self._fetch_cisa_kev(source)
        elif feed == 'osv':
            yield from self._fetch_osv(source)
        elif feed == 'zdi':
            yield from self._fetch_zdi(source)
        else:
            raise ValueError(f'cve_kev: unknown feed {feed!r}')

    # --- per-feed implementations --------------------------------------

    def _fetch_nvd(self, source: dict[str, Any]) -> Iterator[RawItem]:
        days = int(source.get('days', 14))
        end = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000')
        start = (datetime.now(timezone.utc) - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%S.000')
        url = NVD_RECENT.format(start=start, end=end)
        data = get_json(url, timeout=int(source.get('timeout', 60)))
        for entry in data.get('vulnerabilities', []):
            cve = entry.get('cve', {})
            cve_id = cve.get('id') or 'CVE-UNKNOWN'
            descs = cve.get('descriptions') or []
            summary = next((d.get('value', '') for d in descs if d.get('lang') == 'en'), '')
            metrics = cve.get('metrics', {})
            cvss = ''
            for k in ('cvssMetricV40', 'cvssMetricV31', 'cvssMetricV30'):
                if metrics.get(k):
                    cvss = metrics[k][0].get('cvssData', {}).get('baseScore', '')
                    break
            yield RawItem(
                source_id=str(source.get('id') or 'nvd'),
                source_url=url,
                title=f'{cve_id} (CVSS {cvss})' if cvss else cve_id,
                url=f'https://nvd.nist.gov/vuln/detail/{cve_id}',
                published_at=cve.get('published', ''),
                author='NVD',
                summary=summary,
                tags=sorted({'cve', 'nvd', *(source.get('tags') or [])}),
                extra={'source_id': source.get('id') or 'nvd', 'cvss': cvss, 'cve_id': cve_id},
            )

    def _fetch_cisa_kev(self, source: dict[str, Any]) -> Iterator[RawItem]:
        data = get_json(CISA_KEV_JSON, timeout=int(source.get('timeout', 60)))
        for v in data.get('vulnerabilities', []):
            cve_id = v.get('cveID', 'CVE-UNKNOWN')
            yield RawItem(
                source_id=str(source.get('id') or 'cisa-kev'),
                source_url=CISA_KEV_JSON,
                title=f'{cve_id} :: {v.get("vendorProject", "")} {v.get("product", "")}',
                url=f'https://nvd.nist.gov/vuln/detail/{cve_id}',
                published_at=(v.get('dateAdded') or '') + 'T00:00:00Z',
                author='CISA',
                summary=v.get('shortDescription', ''),
                tags=sorted({'cve', 'kev', 'exploited', *(source.get('tags') or [])}),
                extra={
                    'source_id': source.get('id') or 'cisa-kev',
                    'cve_id': cve_id,
                    'product': v.get('product'),
                    'required_action': v.get('requiredAction'),
                    'due_date': v.get('dueDate'),
                },
            )

    def _fetch_osv(self, source: dict[str, Any]) -> Iterator[RawItem]:
        ecosystem = source.get('ecosystem') or 'PyPI'
        body = json.dumps({'package': {'ecosystem': ecosystem}}).encode('utf-8')
        # OSV is POST-only. Fall back to a simple urllib request via _http isn't
        # exposed for POST yet, so do it inline.
        import urllib.request
        req = urllib.request.Request(OSV_LIST, data=body, headers={
            'Content-Type': 'application/json',
            'User-Agent': 'BugBountyOS-Connector/0.1',
        })
        with urllib.request.urlopen(req, timeout=int(source.get('timeout', 60))) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        for vuln in data.get('vulns', [])[:int(source.get('limit', 50))]:
            yield RawItem(
                source_id=str(source.get('id') or f'osv-{ecosystem.lower()}'),
                source_url=OSV_LIST,
                title=vuln.get('summary', vuln.get('id', 'osv')),
                url=f'https://osv.dev/vulnerability/{vuln.get("id", "")}',
                published_at=vuln.get('published', ''),
                author='OSV',
                summary=vuln.get('details', '')[:1500],
                tags=sorted({'cve', 'osv', ecosystem.lower(), *(source.get('tags') or [])}),
                extra={'source_id': source.get('id') or f'osv-{ecosystem.lower()}', 'ecosystem': ecosystem},
            )

    def _fetch_zdi(self, source: dict[str, Any]) -> Iterator[RawItem]:
        text = get_text(ZDI_RSS, timeout=int(source.get('timeout', 30)))
        for entry in parse_feed(text):
            yield RawItem(
                source_id=str(source.get('id') or 'zdi'),
                source_url=ZDI_RSS,
                title=entry.get('title', ''),
                url=entry.get('link', ''),
                published_at=entry.get('published', ''),
                author=entry.get('author', '') or 'ZDI',
                summary=entry.get('summary', ''),
                tags=sorted({'cve', 'zdi', *(source.get('tags') or [])}),
                extra={'source_id': source.get('id') or 'zdi'},
            )


register_connector(CveKevConnector())
