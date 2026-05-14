from __future__ import annotations
import json, time, uuid
from pathlib import Path
from typing import Any

SUITE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SUITE_ROOT.parents[1]
DATA_DIR = SUITE_ROOT / 'data'
JOBS_DIR = DATA_DIR / 'jobs'
RUNS_DIR = DATA_DIR / 'runs'

JOBS_DIR.mkdir(parents=True, exist_ok=True)
RUNS_DIR.mkdir(parents=True, exist_ok=True)


def utc_ts() -> str:
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def new_job(action: str, payload: dict[str, Any]) -> dict[str, Any]:
    job = {
        'id': uuid.uuid4().hex[:12],
        'action': action,
        'payload': payload,
        'status': 'queued',
        'created_at': utc_ts(),
        'updated_at': utc_ts(),
        'returncode': None,
        'command': [],
        'stdout_tail': '',
        'stderr_tail': '',
        'run_dir': None,
    }
    save_job(job)
    return job


def job_path(job_id: str) -> Path:
    return JOBS_DIR / f'{job_id}.json'


def save_job(job: dict[str, Any]) -> None:
    job['updated_at'] = utc_ts()
    job_path(job['id']).write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding='utf-8')


def load_job(job_id: str) -> dict[str, Any] | None:
    p = job_path(job_id)
    if not p.exists():
        return None
    return json.loads(p.read_text(errors='ignore'))


def list_jobs(limit: int = 100) -> list[dict[str, Any]]:
    jobs = []
    for p in sorted(JOBS_DIR.glob('*.json'), key=lambda x: x.stat().st_mtime, reverse=True)[:limit]:
        try:
            jobs.append(json.loads(p.read_text(errors='ignore')))
        except Exception:
            pass
    return jobs


def tail_text(text: str, n: int = 12000) -> str:
    return text[-n:]
