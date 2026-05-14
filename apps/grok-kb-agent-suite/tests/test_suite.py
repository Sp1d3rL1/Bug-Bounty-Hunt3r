from __future__ import annotations
import importlib.util, json, py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]


def test_files_exist():
    required = [
        ROOT / 'backend/server.py',
        ROOT / 'backend/workflows.py',
        ROOT / 'frontend/index.html',
        ROOT / 'frontend/styles.css',
        ROOT / 'frontend/app.js',
        ROOT / 'skills/powerups/manifest.json',
        ROOT / 'skills/powerups/tavily_verifier.skill.md',
        ROOT / 'skills/powerups/report_intelligence.skill.md',
        PROJECT / 'scripts/grok_api_agent.py',
        PROJECT / 'scripts/report_intel_agent.py',
        PROJECT / 'scripts/bb_intel_pipeline.py',
        PROJECT / 'docs/intelligence_kb/reports/_index.md',
        PROJECT / 'docs/intelligence_kb/reports/imported_authorized/.gitkeep',
        PROJECT / 'docs/intelligence_kb/reports/manual_channel_sources.md',
        PROJECT / 'data/report_intel/manual_channel_research/trashcan/.gitkeep',
        ROOT / 'tests/fixtures/authorized_newsletter_export.json',
        ROOT / 'tests/fixtures/manual_channel_results.tsv',
    ]
    missing = [str(p) for p in required if not p.exists()]
    assert not missing, missing


def test_python_compile():
    for p in [ROOT / 'backend/server.py', ROOT / 'backend/workflows.py', ROOT / 'backend/state.py', PROJECT / 'scripts/grok_api_agent.py', PROJECT / 'scripts/report_intel_agent.py', PROJECT / 'scripts/bb_intel_pipeline.py']:
        py_compile.compile(str(p), doraise=True)


def test_skill_manifest():
    data = json.loads((ROOT / 'skills/powerups/manifest.json').read_text())
    assert len(data['powerups']) >= 6


def test_evidence_policy_in_api_agent():
    text = (PROJECT / 'scripts/grok_api_agent.py').read_text()
    assert 'BASELINE_EVIDENCE_POLICY' in text
    assert 'verification_status' in text
    assert 'unchanged_verification_only' in text
    assert 'existing_kb_excerpt' in text
    assert 'tavily-verify-run' in text
    assert 'TAVILY_API_KEY' in (PROJECT / '.env.example').read_text()


def load_report_agent():
    spec = importlib.util.spec_from_file_location('report_intel_agent', PROJECT / 'scripts/report_intel_agent.py')
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def test_report_intel_schema_and_clustering():
    mod = load_report_agent()
    assert mod.REPORT_CARD_SCHEMA['properties']['cards']['items']['properties']['type']['enum'] == ['report_cluster']
    for field in ['source_tier', 'source_id', 'access_level', 'license_policy', 'collection_policy', 'risk_flag', 'human_review_required', 'source_reliability', 'legal_risk']:
        assert field in mod.REPORT_CARD_SCHEMA['properties']['cards']['items']['properties']
    sample_a = mod.make_candidate(
        source_platform='hackerone',
        title='Sample disclosed report',
        canonical_report_url='https://hackerone.com/reports/123?utm_source=x',
        vuln_class='IDOR',
        confidence='high',
        evidence=[{'claim': 'public report', 'source_url': 'https://hackerone.com/reports/123', 'verification_notes': 'fixture'}],
    )
    sample_b = mod.make_candidate(
        source_platform='hackerone',
        title='Duplicate sample disclosed report',
        canonical_report_url='https://hackerone.com/reports/123',
        vuln_class='IDOR',
        confidence='medium',
    )
    merged = mod.merge_cluster([sample_a, sample_b], mod.cluster_key(sample_a))
    assert merged['cluster_size'] == 2
    assert merged['confidence'] == 'high'
    assert len(merged['related_urls']) == 1


def test_report_source_catalog_policy():
    mod = load_report_agent()
    catalog = mod.load_source_catalog()
    tiers = {s['tier'] for s in catalog}
    assert 'platform_public' in tiers
    assert 'curated_aggregators' in tiers
    assert 'gray_trade_watchlist' in tiers
    gray = [s for s in catalog if s['tier'] == 'gray_trade_watchlist']
    assert gray
    assert all(s['metadata_only'] and s['legal_risk'] == 'high' and s['blocked_for_content_collection'] for s in gray)
    metadata = mod.source_metadata_snapshot(gray[0])
    assert metadata['type'] == 'channel_metadata'
    assert metadata['collection_policy'] == 'metadata_only'
    assert metadata['blocked_for_content_collection'] is True


def test_manual_import_requires_authorization():
    mod = load_report_agent()
    fixture = ROOT / 'tests/fixtures/authorized_newsletter_export.json'
    rows = mod.normalize_manual_import(fixture)
    assert len(rows) == 1
    assert rows[0]['access_level'] == 'authorized_export'
    assert rows[0]['collection_policy'] == 'summary_links_evidence_only'
    unauth = ROOT / 'tests/fixtures/unauthorized_newsletter_export.json'
    unauth.write_text('{"items":[{"title":"No auth","url":"https://example.com/noauth"}]}')
    try:
        try:
            mod.normalize_manual_import(unauth)
        except PermissionError:
            pass
        else:
            raise AssertionError('expected PermissionError')
    finally:
        unauth.unlink(missing_ok=True)


def test_gray_items_do_not_cluster():
    mod = load_report_agent()
    src = [s for s in mod.load_source_catalog() if s['tier'] == 'gray_trade_watchlist'][0]
    meta = mod.source_metadata_snapshot(src)
    public = mod.make_candidate(title='Public fixture', canonical_report_url='https://hackerone.com/reports/999', source_platform='hackerone')
    buckets = {}
    for row in [public]:
        buckets.setdefault(mod.cluster_key(row), []).append(row)
    assert meta['type'] == 'channel_metadata'
    assert len([mod.merge_cluster(v, k) for k, v in buckets.items()]) == 1


def test_report_markdown_policy():
    mod = load_report_agent()
    text = mod.sanitize_report_markdown('## TL;DR\n摘要，不包含完整原文。')
    assert '不复现' in text
    assert len(text) < 2000


def test_manual_channel_results_import_and_policy():
    mod = load_report_agent()
    fixture = ROOT / 'tests/fixtures/manual_channel_results.tsv'
    rows = mod.read_manual_channel_input(fixture)
    assert len(rows) >= 30
    records = [mod.normalize_manual_channel_row(r, research_topic='fixture', tool_used='grok_expert') for r in rows]
    legal = [r for r in records if r['storage_decision'] != 'redacted_discovery_record_only']
    assert len(legal) >= 30
    assert all(r['legal_acquisition_method'] for r in legal)
    assert all(r['official_or_legitimate_entry'].startswith('https://') for r in legal)
    paid = [r for r in legal if r['requires_payment']]
    assert paid
    assert all(r['collection_policy'] == 'metadata_until_authorized_export' for r in paid)
    src = mod.manual_record_to_source(legal[0])
    assert src['source_id'] == legal[0]['source_id']
    assert src['manual_acquisition_method']


def test_manual_channel_redaction_policy():
    mod = load_report_agent()
    blocked = mod.normalize_manual_channel_row({
        'source_id': 'blocked_fixture',
        'channel_name': 'Blocked fixture',
        'category': 'gray',
        'official_url': 'https://discord.gg/example-fixture',
        'manual_acquisition_method': 'Should be blocked',
        'why_high_value': 'Fixture only',
    })
    assert blocked['storage_decision'] == 'redacted_discovery_record_only'
    assert blocked['redacted_url_hash']
    assert blocked['redaction_reason']
    assert blocked['allowed_url'] == ''
    assert mod.blocked_reason_for_text('https://example.com/checkout/session') == 'direct_payment_or_checkout_url'
    assert mod.blocked_reason_for_text('https://drive.google.com/file/d/example') == 'cloud_drive_or_file_share'
    raw = 'url\thttps://discord.gg/example-fixture\npay\thttps://example.com/checkout/session'
    sanitized = mod.redact_blocked_manual_raw_text(raw)
    assert 'https://discord.gg/example-fixture' not in sanitized
    assert 'https://example.com/checkout/session' not in sanitized
    assert 'TRASHCAN_REDACTED_URL' in sanitized


if __name__ == '__main__':
    test_files_exist(); test_python_compile(); test_skill_manifest(); test_evidence_policy_in_api_agent(); test_report_intel_schema_and_clustering(); test_report_source_catalog_policy(); test_manual_import_requires_authorization(); test_gray_items_do_not_cluster(); test_report_markdown_policy(); test_manual_channel_results_import_and_policy(); test_manual_channel_redaction_policy(); print('ok')
