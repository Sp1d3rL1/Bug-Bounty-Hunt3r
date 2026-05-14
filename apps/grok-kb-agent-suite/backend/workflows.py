from __future__ import annotations
import os, subprocess, threading
from pathlib import Path
from typing import Any
from state import PROJECT_ROOT, RUNS_DIR, new_job, save_job, tail_text

API_AGENT = PROJECT_ROOT / 'scripts/grok_api_agent.py'
REPORT_AGENT = PROJECT_ROOT / 'scripts/report_intel_agent.py'
BUILD_INDEX = PROJECT_ROOT / 'scripts/grok_kb_build_index.py'
VALIDATE = PROJECT_ROOT / 'scripts/grok_kb_validate.py'
PIPELINE = PROJECT_ROOT / 'scripts/bb_intel_pipeline.py'


def _run_subprocess(job: dict[str, Any], cmd: list[str], cwd: Path = PROJECT_ROOT) -> None:
    job['status'] = 'running'
    job['command'] = cmd
    save_job(job)
    env = os.environ.copy()
    # scripts/grok_api_agent.py can load .env itself; preserving env helps shell exports too.
    proc = subprocess.Popen(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    out, err = proc.communicate()
    job['returncode'] = proc.returncode
    job['stdout_tail'] = tail_text(out)
    job['stderr_tail'] = tail_text(err)
    job['status'] = 'succeeded' if proc.returncode == 0 else 'failed'
    save_job(job)


def submit_job(action: str, payload: dict[str, Any]) -> dict[str, Any]:
    job = new_job(action, payload)
    cmd = build_command(action, payload, job)
    t = threading.Thread(target=_run_subprocess, args=(job, cmd), daemon=True)
    t.start()
    return job


def build_command(action: str, payload: dict[str, Any], job: dict[str, Any]) -> list[str]:
    py = 'python3'
    if action == 'intel_pipeline':
        run_dir = payload.get('run_dir') or str(RUNS_DIR / f"bb_pipeline_{job['id']}")
        job['run_dir'] = run_dir
        cmd = [
            py, str(PIPELINE),
            '--mode', str(payload.get('mode') or 'steady'),
            '--from-date', str(payload.get('from_date') or '2025-01-01'),
            '--to-date', str(payload.get('to_date') or '2026-05-09'),
            '--report-limit', str(int(payload.get('report_limit', 10))),
            '--enrich-limit', str(int(payload.get('enrich_limit', 3))),
            '--technique-limit', str(int(payload.get('technique_limit', 8))),
            '--start-batch', str(int(payload.get('start_batch', 201))),
            '--run-root', run_dir,
        ]
        if payload.get('reports_only'): cmd.append('--reports-only')
        if payload.get('techniques_only'): cmd.append('--techniques-only')
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'expand':
        from_batch = int(payload.get('from_batch', 11))
        to_batch = int(payload.get('to_batch', from_batch))
        run_dir = payload.get('run_dir') or str(RUNS_DIR / f"expand_{job['id']}")
        job['run_dir'] = run_dir
        cmd = [py, str(API_AGENT), 'expand-prompts', '--from-batch', str(from_batch), '--to-batch', str(to_batch), '--run-dir', run_dir]
        if payload.get('use_search', True): cmd.append('--use-search')
        if payload.get('tavily_preverify'): cmd.append('--tavily-preverify')
        if payload.get('dry_run'): cmd.append('--dry-run')
        if payload.get('prompt_dir'): cmd += ['--prompt-dir', str(payload['prompt_dir'])]
        return cmd
    if action == 'discover':
        topic = str(payload.get('topic', '')).strip()
        if not topic: raise ValueError('topic required')
        run_dir = payload.get('run_dir') or str(RUNS_DIR / f"discover_{job['id']}")
        job['run_dir'] = run_dir
        cmd = [py, str(API_AGENT), 'discover-topic', '--topic', topic, '--limit', str(int(payload.get('limit', 25))), '--run-dir', run_dir]
        if payload.get('tavily_context'): cmd.append('--tavily-context')
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'apply_run':
        run_dir = str(payload.get('run_dir') or '')
        if not run_dir: raise ValueError('run_dir required')
        job['run_dir'] = run_dir
        return [py, str(API_AGENT), 'apply-run', '--run-dir', run_dir]
    if action == 'validate':
        return ['bash', '-lc', f'python3 "{BUILD_INDEX}" && python3 "{VALIDATE}"']
    if action == 'batch_submit':
        from_batch = int(payload.get('from_batch', 11))
        to_batch = int(payload.get('to_batch', 60))
        run_dir = payload.get('run_dir') or str(RUNS_DIR / f"batch_{job['id']}")
        job['run_dir'] = run_dir
        cmd = [py, str(API_AGENT), 'batch-submit-prompts', '--from-batch', str(from_batch), '--to-batch', str(to_batch), '--run-dir', run_dir, '--name', str(payload.get('name', 'bb-kb-agent-suite'))]
        if payload.get('use_search', True): cmd.append('--use-search')
        if payload.get('tavily_preverify'): cmd.append('--tavily-preverify')
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'tavily_verify':
        run_dir = str(payload.get('run_dir') or '')
        if not run_dir: raise ValueError('run_dir required')
        job['run_dir'] = run_dir
        mode = str(payload.get('mode') or 'default')
        cmd = [py, str(API_AGENT), 'tavily-verify-run', '--run-dir', run_dir, '--mode', mode]
        if payload.get('write_back'): cmd.append('--write-back')
        if payload.get('search_missing'): cmd.append('--search-missing')
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'report_discover':
        run_dir = payload.get('run_dir') or str(RUNS_DIR / f"report_{job['id']}")
        job['run_dir'] = run_dir
        cmd = [
            py, str(REPORT_AGENT), 'discover',
            '--sources', str(payload.get('sources') or 'public_all'),
            '--topic', str(payload.get('topic') or ''),
            '--vuln-class', str(payload.get('vuln_class') or ''),
            '--from-date', str(payload.get('from_date') or '2025-01-01'),
            '--to-date', str(payload.get('to_date') or '2026-05-06'),
            '--limit', str(int(payload.get('limit', 25))),
            '--run-dir', run_dir,
        ]
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'report_catalog_build':
        cmd = [py, str(REPORT_AGENT), 'catalog-build']
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'report_triage_sources':
        cmd = [py, str(REPORT_AGENT), 'triage-sources']
        if payload.get('tier'): cmd += ['--tier', str(payload.get('tier'))]
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'report_discover_source':
        source_id = str(payload.get('source_id') or '').strip()
        if not source_id: raise ValueError('source_id required')
        run_dir = payload.get('run_dir') or str(RUNS_DIR / f"report_source_{job['id']}")
        job['run_dir'] = run_dir
        cmd = [
            py, str(REPORT_AGENT), 'discover-source',
            '--source-id', source_id,
            '--topic', str(payload.get('topic') or ''),
            '--vuln-class', str(payload.get('vuln_class') or ''),
            '--from-date', str(payload.get('from_date') or '2025-01-01'),
            '--to-date', str(payload.get('to_date') or '2026-05-08'),
            '--limit', str(int(payload.get('limit', 25))),
            '--run-dir', run_dir,
        ]
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'report_discover_catalog':
        run_dir = payload.get('run_dir') or str(RUNS_DIR / f"report_catalog_{job['id']}")
        job['run_dir'] = run_dir
        cmd = [
            py, str(REPORT_AGENT), 'discover-catalog',
            '--topic', str(payload.get('topic') or ''),
            '--vuln-class', str(payload.get('vuln_class') or ''),
            '--from-date', str(payload.get('from_date') or '2025-01-01'),
            '--to-date', str(payload.get('to_date') or '2026-05-08'),
            '--limit', str(int(payload.get('limit', 25))),
            '--run-dir', run_dir,
        ]
        if payload.get('preset'): cmd += ['--preset', str(payload.get('preset'))]
        if payload.get('tier'): cmd += ['--tier', str(payload.get('tier'))]
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'report_import_manual':
        inp = str(payload.get('input') or '').strip()
        if not inp: raise ValueError('input required')
        run_dir = payload.get('run_dir') or str(RUNS_DIR / f"report_import_{job['id']}")
        job['run_dir'] = run_dir
        cmd = [py, str(REPORT_AGENT), 'import-manual', '--input', inp, '--run-dir', run_dir]
        if payload.get('authorization_confirmed'): cmd.append('--authorization-confirmed')
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'manual_channel_prompts':
        cmd = [py, str(REPORT_AGENT), 'manual-channel-prompts']
        if payload.get('out_dir'): cmd += ['--out-dir', str(payload.get('out_dir'))]
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'import_manual_channel_results':
        inp = str(payload.get('input') or '').strip()
        if not inp: raise ValueError('input required')
        cmd = [
            py, str(REPORT_AGENT), 'import-manual-channel-results',
            '--input', inp,
            '--research-topic', str(payload.get('research_topic') or ''),
            '--prompt-or-query', str(payload.get('prompt_or_query') or ''),
            '--tool-used', str(payload.get('tool_used') or 'manual'),
        ]
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'validate_discovery_records':
        return [py, str(REPORT_AGENT), 'validate-discovery-records']
    if action == 'apply_manual_channel_catalog':
        cmd = [py, str(REPORT_AGENT), 'apply-manual-channel-catalog']
        if payload.get('input'): cmd += ['--input', str(payload.get('input'))]
        if payload.get('replace'): cmd.append('--replace')
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'export_manual_channel_index':
        cmd = [py, str(REPORT_AGENT), 'export-manual-channel-index']
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'report_cluster':
        run_dir = str(payload.get('run_dir') or '')
        if not run_dir: raise ValueError('run_dir required')
        job['run_dir'] = run_dir
        inp = str(payload.get('input') or str(Path(run_dir) / 'discovery' / 'candidates.jsonl'))
        return [py, str(REPORT_AGENT), 'cluster', '--input', inp, '--run-dir', run_dir]
    if action == 'report_enrich':
        run_dir = str(payload.get('run_dir') or '')
        if not run_dir: raise ValueError('run_dir required')
        job['run_dir'] = run_dir
        inp = str(payload.get('input') or str(Path(run_dir) / 'clusters' / 'clusters.json'))
        cmd = [py, str(REPORT_AGENT), 'enrich', '--input', inp, '--run-dir', run_dir, '--limit', str(int(payload.get('limit', 5)))]
        if payload.get('dry_run'): cmd.append('--dry-run')
        if payload.get('skip_tavily'): cmd.append('--skip-tavily')
        return cmd
    if action == 'report_apply':
        run_dir = str(payload.get('run_dir') or '')
        if not run_dir: raise ValueError('run_dir required')
        job['run_dir'] = run_dir
        cmd = [py, str(REPORT_AGENT), 'apply', '--run-dir', run_dir]
        if payload.get('dry_run'): cmd.append('--dry-run')
        return cmd
    if action == 'connector_trigger':
        sid = str(payload.get('source_id') or '').strip()
        if not sid:
            raise ValueError('source_id required')
        scheduler = PROJECT_ROOT / 'apps/grok-kb-agent-suite/backend/scheduler.py'
        cmd = [py, str(scheduler), '--tick', '--only', sid]
        if payload.get('dry_run'):
            cmd.append('--dry-run')
        return cmd
    raise ValueError(f'unknown action: {action}')
