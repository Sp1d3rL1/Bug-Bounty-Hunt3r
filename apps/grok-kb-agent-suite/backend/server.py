#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, mimetypes, os
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

from state import SUITE_ROOT, PROJECT_ROOT, list_jobs, load_job
from workflows import submit_job

FRONTEND = SUITE_ROOT / 'frontend'
SKILLS = SUITE_ROOT / 'skills' / 'powerups'


def env_file_has(*names: str) -> bool:
    env_path = PROJECT_ROOT / '.env'
    if not env_path.exists():
        return False
    try:
        for raw in env_path.read_text(errors='ignore').splitlines():
            line = raw.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            if k.strip() in names and v.strip().strip('"').strip("'") and 'REPLACE_ME' not in v:
                return True
    except Exception:
        return False
    return False


def env_file_has_all(*names: str) -> bool:
    return all(env_file_has(name) for name in names)


def _sources_summary() -> dict:
    """Return enabled sources from sources.yaml plus last-fetch metrics."""
    try:
        import sys as _s
        if str(SUITE_ROOT / 'backend') not in _s.path:
            _s.path.insert(0, str(SUITE_ROOT / 'backend'))
        from connectors.base import load_sources_yaml, _last_metric_for, list_registered  # type: ignore
        # touch each connector module so list_registered is populated
        import connectors.rss_generic  # noqa: F401
        import connectors.youtube_channel  # noqa: F401
        import connectors.github_repo  # noqa: F401
        import connectors.cve_kev  # noqa: F401
        import connectors.wechat_rss  # noqa: F401
        import connectors.cn_forum  # noqa: F401
    except Exception as e:  # noqa: BLE001
        return {'error': f'connectors unavailable: {e}', 'sources': []}
    out = []
    for s in load_sources_yaml():
        sid = s.get('id') or s.get('name', '')
        out.append({
            'id': sid,
            'name': s.get('name', sid),
            'connector': s.get('connector', ''),
            'cadence': s.get('cadence', ''),
            'density': s.get('density', ''),
            'region': s.get('region', ''),
            'tags': s.get('tags') or [],
            'enabled': s.get('enabled', True),
            'last_metric': _last_metric_for(sid),
        })
    return {'count': len(out), 'connectors': list_registered(), 'sources': out}


def _source_health(sid: str) -> dict:
    try:
        import sys as _s
        if str(SUITE_ROOT / 'backend') not in _s.path:
            _s.path.insert(0, str(SUITE_ROOT / 'backend'))
        from connectors.base import _last_metric_for  # type: ignore
    except Exception as e:  # noqa: BLE001
        return {'error': f'connectors unavailable: {e}'}
    return {'id': sid, 'last_metric': _last_metric_for(sid)}


def json_bytes(obj, status=200):
    return status, 'application/json; charset=utf-8', json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8')


class Handler(BaseHTTPRequestHandler):
    server_version = 'GrokKBAgentSuite/0.1'

    def _send(self, status: int, ctype: str, body: bytes):
        self.send_response(status)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(204, 'text/plain', b'')

    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            if path == '/api/health':
                status = {
                    'ok': True,
                    'suite_root': str(SUITE_ROOT),
                    'project_root': str(PROJECT_ROOT),
                    'has_xai_key': bool(os.getenv('XAI_API_KEY') or os.getenv('GROK_API_KEY') or env_file_has('XAI_API_KEY', 'GROK_API_KEY')),
                    'has_tavily_key': bool(os.getenv('TAVILY_API_KEY') or env_file_has('TAVILY_API_KEY')),
                    'has_hackerone_key': bool((os.getenv('HACKERONE_API_USERNAME') and os.getenv('HACKERONE_API_TOKEN')) or env_file_has_all('HACKERONE_API_USERNAME', 'HACKERONE_API_TOKEN')),
                    'has_github_token': bool(os.getenv('GITHUB_TOKEN') or env_file_has('GITHUB_TOKEN')),
                    'has_bugcrowd_token': bool(os.getenv('BUGCROWD_API_TOKEN') or env_file_has('BUGCROWD_API_TOKEN')),
                    'has_report_source_catalog': (PROJECT_ROOT / 'data/report_intel/source_catalog.json').exists(),
                    'has_report_watchlist': (PROJECT_ROOT / 'docs/intelligence_kb/reports/channel_watchlist.md').exists(),
                    'has_manual_channel_index': (PROJECT_ROOT / 'docs/intelligence_kb/reports/manual_channel_sources.md').exists(),
                }
                return self._send(*json_bytes(status))
            if path == '/api/jobs':
                return self._send(*json_bytes({'jobs': list_jobs()}))
            if path.startswith('/api/jobs/'):
                job_id = path.rsplit('/', 1)[-1]
                job = load_job(job_id)
                return self._send(*json_bytes(job or {'error': 'not found'}, 200 if job else 404))
            if path == '/api/sources':
                return self._send(*json_bytes(_sources_summary()))
            if path.startswith('/api/sources/') and path.endswith('/health'):
                src_id = path[len('/api/sources/'):-len('/health')]
                return self._send(*json_bytes(_source_health(src_id)))
            if path == '/api/playbooks':
                return self._send(*json_bytes({
                    'enabled': False,
                    'message': 'Phase 3 — playbooks runtime not yet enabled.',
                    'planned_count': 6,
                }))
            if path == '/api/match':
                return self._send(*json_bytes({
                    'enabled': False,
                    'message': 'Phase 3 — match.py not yet enabled. Provide ?target=<dossier-id> when ready.',
                }))
            if path == '/api/skills':
                skills = []
                for p in sorted(SKILLS.glob('*.skill.md')):
                    skills.append({'name': p.stem.replace('.skill',''), 'path': str(p), 'preview': p.read_text(errors='ignore')[:600]})
                manifest = SKILLS / 'manifest.json'
                return self._send(*json_bytes({'manifest': json.loads(manifest.read_text()) if manifest.exists() else {}, 'skills': skills}))
            return self.serve_static(path)
        except Exception as e:
            return self._send(*json_bytes({'error': str(e)}, 500))

    def do_POST(self):
        try:
            parsed = urlparse(self.path)
            if parsed.path == '/api/jobs':
                n = int(self.headers.get('content-length', '0') or '0')
                payload = json.loads(self.rfile.read(n).decode('utf-8') or '{}')
                action = payload.pop('action', '')
                job = submit_job(action, payload)
                return self._send(*json_bytes({'job': job}, 202))
            if parsed.path.startswith('/api/sources/') and parsed.path.endswith('/trigger'):
                src_id = parsed.path[len('/api/sources/'):-len('/trigger')]
                job = submit_job('connector_trigger', {'source_id': src_id})
                return self._send(*json_bytes({'job': job}, 202))
            return self._send(*json_bytes({'error': 'not found'}, 404))
        except Exception as e:
            return self._send(*json_bytes({'error': str(e)}, 400))

    def serve_static(self, path: str):
        rel = 'index.html' if path in ('/', '') else path.lstrip('/')
        target = (FRONTEND / rel).resolve()
        if not str(target).startswith(str(FRONTEND.resolve())) or not target.exists() or target.is_dir():
            return self._send(*json_bytes({'error': 'not found'}, 404))
        ctype = mimetypes.guess_type(str(target))[0] or 'application/octet-stream'
        self._send(200, ctype, target.read_bytes())

    def log_message(self, fmt, *args):
        print('%s - %s' % (self.address_string(), fmt % args))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--port', type=int, default=8765)
    args = ap.parse_args()
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f'Grok KB Agent Suite listening on http://{args.host}:{args.port}')
    httpd.serve_forever()


if __name__ == '__main__':
    main()
