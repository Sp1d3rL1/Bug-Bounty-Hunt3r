#!/usr/bin/env python3
"""Report Intelligence agent for public Bug Bounty report learning.

The module discovers, clusters, enriches, and applies public disclosed report
cards into the Obsidian KB. It stores summaries/links/evidence metadata only;
it does not archive complete copyrighted report bodies or private/undisclosed
program content.
"""
from __future__ import annotations

import argparse
import base64
import csv
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any

# Reuse the existing API/Tavily helpers and evidence policy.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from grok_api_agent import (  # type: ignore
    BASELINE_EVIDENCE_POLICY,
    DEFAULT_API_BASE,
    DEFAULT_MODEL,
    DEFAULT_TAVILY_API_BASE,
    DEFAULT_TAVILY_CONTEXT_CHARS,
    DEFAULT_TAVILY_EXTRACT_DEPTH,
    DEFAULT_TAVILY_SEARCH_DEPTH,
    ROOT,
    SYSTEM_PROMPT,
    api_json,
    compact_text,
    is_x_url,
    load_dotenv,
    parse_json_text,
    response_text,
    safe_filename,
    sha16,
    tavily_extract,
    tavily_search,
)

DEFAULT_FROM_DATE = "2025-01-01"
DEFAULT_TO_DATE = dt.date.today().isoformat()
REPORT_ROOT = ROOT / "docs" / "intelligence_kb" / "reports"
REPORT_DATA = ROOT / "data" / "report_intel"
REPORT_LEDGER = REPORT_DATA / "report_ledger.tsv"
RUNS_DIR = REPORT_DATA / "runs"
DISCOVERY_DIR = REPORT_DATA / "discovery"
CLUSTERS_DIR = REPORT_DATA / "clusters"
EXTRACTED_DIR = REPORT_DATA / "extracted"
REPORT_KB_START = "<!-- REPORT_INTEL_START -->"
REPORT_KB_END = "<!-- REPORT_INTEL_END -->"
SOURCE_CATALOG = REPORT_DATA / "source_catalog.json"
SOURCE_TRIAGE_TSV = REPORT_DATA / "source_triage.tsv"
CHANNEL_WATCHLIST_JSONL = REPORT_DATA / "channel_watchlist.jsonl"
GRAY_RESEARCH_SURFACES_JSON = REPORT_DATA / "gray_research_surfaces.json"
MANUAL_CHANNEL_ROOT = REPORT_DATA / "manual_channel_research"
MANUAL_PROMPTS_DIR = MANUAL_CHANNEL_ROOT / "prompts"
MANUAL_RAW_DIR = MANUAL_CHANNEL_ROOT / "raw_grok_outputs"
MANUAL_DISCOVERY_DIR = MANUAL_CHANNEL_ROOT / "discovery_records"
MANUAL_REJECTED_DIR = MANUAL_CHANNEL_ROOT / "rejected_or_redacted"  # legacy read-only compatibility
MANUAL_TRASHCAN_DIR = MANUAL_CHANNEL_ROOT / "trashcan"
MANUAL_IMPORT_BATCHES_DIR = MANUAL_CHANNEL_ROOT / "import_batches"
SOURCE_CATALOG_MD = REPORT_ROOT / "source_catalog.md"
CHANNEL_WATCHLIST_MD = REPORT_ROOT / "channel_watchlist.md"
GRAY_RESEARCH_PROTOCOL_MD = REPORT_ROOT / "gray_research_protocol.md"
MANUAL_CHANNEL_SOURCES_MD = REPORT_ROOT / "manual_channel_sources.md"
MANUAL_CHANNEL_FIELDS = [
    "record_id", "collected_at", "research_topic", "tool_used", "prompt_or_query",
    "source_title", "source_domain", "allowed_url", "redacted_url_hash",
    "channel_type", "discovery_path_summary", "why_interesting",
    "legal_acquisition_method", "official_or_legitimate_entry", "freshness_signal",
    "quality_signal", "risk_flag", "storage_decision", "redaction_reason",
    "review_status", "source_id", "entry_type", "collection_policy",
    "requires_auth", "requires_payment", "requires_vetting", "source_group",
]
MANUAL_CHANNEL_PROMPTS: list[tuple[str, str]] = [
    ("topic_01_paid_private_communities", "Find 10 high-value paid/private Bug Bounty communities, newsletters, Discords, labs, or courses useful in 2025-2026. Prefer official pages and current access methods."),
    ("topic_02_platform_communities", "Find 10 official platform/community channels for HackerOne, Bugcrowd, Intigriti, YesWeHack, Synack, Secuna, Hacker101, and similar researcher communities. Include manual access paths."),
    ("topic_03_vendor_vrp_sources", "Find 10 vendor Bug Bounty / VRP report-learning sources from Google, Microsoft, Meta, GitHub, Atlassian, Apple, Shopify, Discord, and similar vendors. Include official report/writeup/recognition entry points."),
    ("topic_04_wp_cms_ecosystem", "Find 10 WordPress/CMS/plugin vulnerability intelligence sources with bounty/report learning value, including official databases, APIs, newsletters, and researcher credit fields."),
    ("topic_05_web3_audit_bounty", "Find 10 Web3 audit/bounty report sources with public findings and legitimate contest/private-entry paths. Include Code4rena-like, CodeHawks-like, audit firm report libraries, and bounty platforms."),
    ("topic_06_gray_public_surfaces", "Find 10 gray-adjacent but legitimate public discovery surfaces for locating Bug Bounty learning communities. Only include platform-level discovery/search pages and policy docs, not invite links or trade links."),
]
MANUAL_CHANNEL_BASELINE_PROMPT = """You are researching legitimate, high-value Bug Bounty learning/report-intelligence sources.
Every claim must include a concrete source URL. Do not invent sources.
Prefer official/legal access paths.
Do not include leaked/NDA/private report content, pirated mirrors, invite links, direct purchase links, attachments, or report fulltext.
If a lead points to questionable material, return only domain-level context, redaction reason, and the nearest legitimate official source.
Return compact TSV only with header:
source_id | channel_name | category | official_url | manual_acquisition_method | requires_auth | requires_payment | requires_vetting | freshness_signal | why_high_value | storage_policy | confidence | entry_type | source_group
""".strip()
MANUAL_ENTRY_TYPES = {
    "official_signup", "paid_subscription_landing", "vetted_application", "course_landing",
    "community_discovery", "newsletter_archive", "private_discord_after_subscription",
    "research_blog", "platform_recognition", "redacted_lead_to_legitimate_source",
}
MANUAL_COLLECTION_POLICIES = {
    "metadata_only", "metadata_until_authorized_export", "public_summary_links_only",
    "redacted_discovery_record_only",
}
SOURCE_TIERS = [
    "platform_public",
    "curated_aggregators",
    "newsletter_podcast",
    "web3_audit_bounty",
    "community_social",
    "gray_trade_watchlist",
]
DEFAULT_GRAY_RESEARCH_SURFACES: list[dict[str, Any]] = [
    {
        "surface_id": "telegram_public_discovery_surface",
        "platform": "telegram",
        "purpose": "识别公开可见的频道/群组/帖子目录与描述性元数据，不进入频道、不保存邀请链接、不下载附件。",
        "public_context_urls": [
            "https://telegram.org/faq",
            "https://telegram.org/faq_channels",
            "https://core.telegram.org/api/channel",
            "https://tgstat.com/search",
        ],
        "retainable_info": [
            "平台类型", "公开目录/搜索面的名称", "自然语言入口描述", "主题标签", "公开描述摘要",
            "可见成员/订阅量范围（如公开显示）", "最近可见活跃时间范围", "疑似售卖/泄露/NDA 风险标记",
            "发现日期", "人工复核结论", "是否需要举报/忽略",
        ],
        "prohibited_info": [
            "具体邀请链接", "购买链接", "交易联系方式", "附件", "报告正文", "泄露报告标题清单",
            "私聊内容", "绕过访问限制的方法",
        ],
        "coverage_notes": "覆盖 Telegram 官方公开用户名/频道说明、频道 FAQ、API 中 public username/private invite link 区分，以及一个公开频道搜索面样例；不进行具体关键词拉取。",
    },
    {
        "surface_id": "discord_public_discovery_surface",
        "platform": "discord",
        "purpose": "识别公开 Discord Discovery/App Directory/社区目录层面的元数据，不保存服务器邀请、频道内容或私域材料。",
        "public_context_urls": [
            "https://support.discord.com/hc/en-us/articles/4409308485271-Discovery-Guidelines",
            "https://discord.com/guidelines",
            "https://docs.discord.com/developers/discovery/best-practices",
        ],
        "retainable_info": [
            "公开目录类型", "服务器/社区的自然语言入口描述", "公开标签/分类", "规则/风险提示",
            "是否涉及售卖或疑似未授权材料", "人工复核状态", "发现日期",
        ],
        "prohibited_info": [
            "服务器邀请链接", "购买/付款链接", "频道消息", "成员列表", "附件", "报告正文",
            "私聊记录", "规避平台审核或发现限制的方法",
        ],
        "coverage_notes": "覆盖 Discord Discovery 指南、Community Guidelines 与 App Directory discovery 文档；只记录公开目录层元数据。",
    },
    {
        "surface_id": "reddit_forum_public_discussion_surface",
        "platform": "reddit/forum",
        "purpose": "识别公开社区/论坛讨论中关于 report trade 的存在性、风险和指向性元数据，不保存交易入口或具体报告。",
        "public_context_urls": [
            "https://support.reddithelp.com/hc/en-us/articles/19695647891988-How-does-Reddit-search-work",
            "https://www.redditinc.com/policies/content-policy",
        ],
        "retainable_info": [
            "公开社区/论坛类型", "讨论主题类别", "自然语言入口描述", "风险关键词类别（不保存精确交易词组合）",
            "公开规则/版规提示", "是否疑似售卖泄露/NDA 内容", "人工复核状态", "发现日期",
        ],
        "prohibited_info": [
            "具体交易帖 URL", "卖家/买家联系方式", "价格", "付款方式", "附件", "报告正文",
            "精确可复现搜索词组合",
        ],
        "coverage_notes": "覆盖 Reddit 官方搜索能力说明和内容政策入口；论坛类以人工元数据记录为主。",
    },
    {
        "surface_id": "marketplace_public_ad_surface",
        "platform": "marketplace",
        "purpose": "记录公开市场/资源目录/广告层面的存在性与风险，不保存购买路径、卖家联系或商品内容。",
        "public_context_urls": [
            "https://www.google.com/search/howsearchworks/",
        ],
        "retainable_info": [
            "市场类型", "公开广告/目录的自然语言入口描述", "内容类别", "是否声称包含私有/NDA/付费报告",
            "风险等级", "人工复核状态", "发现日期",
        ],
        "prohibited_info": [
            "购买链接", "卖家账号", "付款方式", "下载链接", "附件", "报告正文", "未授权数据样本",
        ],
        "coverage_notes": "只保留市场/广告层风险画像；不构造或保存可直接定位交易的搜索词与链接。",
    },
]
PRESET_TO_TIERS = {
    "maximum_coverage": [
        "platform_public", "curated_aggregators", "newsletter_podcast",
        "web3_audit_bounty", "community_social", "gray_trade_watchlist",
    ],
    "public_only": ["platform_public", "curated_aggregators", "newsletter_podcast", "community_social"],
    "paid_authorized": ["newsletter_podcast"],
    "gray_metadata_only": ["gray_trade_watchlist"],
    "web3_reports": ["web3_audit_bounty"],
    "legitimate_gated": ["platform_public", "curated_aggregators", "newsletter_podcast", "web3_audit_bounty", "community_social", "gray_trade_watchlist"],
    "vendor_official": ["platform_public"],
    "wp_ecosystem": ["platform_public", "curated_aggregators"],
    "research_blogs": ["curated_aggregators", "community_social"],
    "web3_extended": ["web3_audit_bounty"],
    "gray_public_surfaces": ["gray_trade_watchlist"],
}
PUBLIC_SOURCE_PRESETS = {
    "public_all": ["hackerone", "bugcrowd", "github", "github_security_lab", "blogs_x", "newsletters"],
    "hackerone": ["hackerone"],
    "bugcrowd": ["bugcrowd"],
    "github": ["github", "github_security_lab"],
    "github_security_lab": ["github_security_lab", "github"],
    "blogs_x": ["blogs_x", "newsletters"],
    "newsletters": ["newsletters"],
    "maximum_coverage": ["hackerone", "bugcrowd", "github", "github_security_lab", "blogs_x", "newsletters"],
    "public_only": ["hackerone", "bugcrowd", "github", "github_security_lab", "blogs_x", "newsletters"],
    "paid_authorized": ["newsletters"],
    "gray_metadata_only": [],
    "web3_reports": ["blogs_x"],
}
REPORT_DIR_BY_PLATFORM = {
    "hackerone": "platform_reports",
    "bugcrowd": "platform_reports",
    "github_advisory": "advisory_related",
    "github_security_lab": "advisory_related",
    "x": "x_discussions",
    "newsletter": "newsletter_roundups",
    "blog": "researcher_writeups",
    "web": "researcher_writeups",
    "web3": "advisory_related",
    "manual_import": "imported_authorized",
}

DEFAULT_SOURCE_CATALOG: list[dict[str, Any]] = [
    {
        "source_id": "hackerone_hacktivity_api",
        "name": "HackerOne Hacktivity / Hacker API",
        "tier": "platform_public",
        "url": "https://api.hackerone.com/hacker-resources/",
        "platform": "hackerone",
        "access_level": "public_with_optional_api_key",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_disclosed_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "official",
        "learning_value": "high",
        "legal_risk": "low",
        "risk_flag": "none",
        "blocked_for_content_collection": False,
        "query": "disclosed bug bounty report hackerone 2025 2026",
        "notes": "Prefer API when HACKERONE_API_USERNAME/HACKERONE_API_TOKEN are available; otherwise Tavily search only returns public links.",
    },
    {
        "source_id": "bugcrowd_crowdstream_search",
        "name": "Bugcrowd CrowdStream public disclosures",
        "tier": "platform_public",
        "url": "https://docs.bugcrowd.com/researchers/disclosure/disclosing-submissions/",
        "platform": "bugcrowd",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "official",
        "learning_value": "medium",
        "legal_risk": "low",
        "risk_flag": "none",
        "blocked_for_content_collection": False,
        "query": "site:bugcrowd.com/crowdstream disclosed bug bounty report 2025 2026",
        "notes": "Use web search/extract; do not bypass login or private program gates.",
    },
    {
        "source_id": "github_advisories_api",
        "name": "GitHub Global Security Advisories API",
        "tier": "platform_public",
        "url": "https://docs.github.com/en/rest/security-advisories/global-advisories",
        "platform": "github_advisory",
        "access_level": "public_api_with_optional_token",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_advisory_summary",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "official",
        "learning_value": "medium",
        "legal_risk": "low",
        "risk_flag": "none",
        "blocked_for_content_collection": False,
        "query": "GitHub advisory bug bounty report 2025 2026",
        "notes": "Not every GHSA is a bounty report, but advisories help correlate report/blog clusters.",
    },
    {
        "source_id": "github_security_lab",
        "name": "GitHub Security Lab Advisories",
        "tier": "platform_public",
        "url": "https://securitylab.github.com/advisories/",
        "platform": "github_security_lab",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_advisory_summary",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "official",
        "learning_value": "medium",
        "legal_risk": "low",
        "risk_flag": "none",
        "blocked_for_content_collection": False,
        "query": "site:securitylab.github.com/advisories vulnerability report analysis",
        "notes": "Good source for root-cause analysis and advisory-writing patterns.",
    },
    {
        "source_id": "yeswehack_blog_search",
        "name": "YesWeHack public blog writeups",
        "tier": "platform_public",
        "url": "https://www.yeswehack.com/blog",
        "platform": "blog",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "official",
        "learning_value": "medium",
        "legal_risk": "low",
        "risk_flag": "none",
        "blocked_for_content_collection": False,
        "query": "site:yeswehack.com/blog bug bounty report writeup vulnerability disclosure",
        "notes": "Public blog only; cluster with original researcher/platform links when available.",
    },
    {
        "source_id": "disclose_io_directory",
        "name": "disclose.io disclosure program directory",
        "tier": "platform_public",
        "url": "https://directory.disclose.io/",
        "platform": "web",
        "access_level": "public_directory",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_directory_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "curated",
        "learning_value": "low",
        "legal_risk": "low",
        "risk_flag": "program_policy_context_not_report_source",
        "blocked_for_content_collection": False,
        "query": "site:directory.disclose.io vulnerability disclosure program public reports writeup",
        "notes": "Mainly program/policy context; not treated as report proof unless linked report material exists.",
    },
    {
        "source_id": "pentesterland_writeups",
        "name": "PentesterLand Writeups",
        "tier": "curated_aggregators",
        "url": "https://pentester.land/writeups/",
        "platform": "blog",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "curated_links_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "curated",
        "learning_value": "high",
        "legal_risk": "low",
        "risk_flag": "none",
        "blocked_for_content_collection": False,
        "query": "site:pentester.land/writeups bug bounty writeup 2025 2026",
        "notes": "Aggregator; cluster with original reports/blogs when possible.",
    },
    {
        "source_id": "hackdex",
        "name": "HackDex",
        "tier": "curated_aggregators",
        "url": "https://hack-dex.com/",
        "platform": "blog",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "curated_links_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "curated",
        "learning_value": "medium",
        "legal_risk": "low",
        "risk_flag": "none",
        "blocked_for_content_collection": False,
        "query": "site:hack-dex.com bug bounty writeup report",
        "notes": "Use as discovery source, not sole evidence for high confidence.",
    },
    {
        "source_id": "bugboard",
        "name": "BugBoard",
        "tier": "curated_aggregators",
        "url": "https://bugboard.rsecloud.com/",
        "platform": "blog",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "curated_links_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "curated",
        "learning_value": "medium",
        "legal_risk": "low",
        "risk_flag": "none",
        "blocked_for_content_collection": False,
        "query": "site:bugboard.rsecloud.com bug bounty report writeup",
        "notes": "Aggregator; prefer original link in evidence.",
    },
    {
        "source_id": "google_vrp_writeups_repo",
        "name": "Awesome Google VRP Writeups",
        "tier": "curated_aggregators",
        "url": "https://github.com/xdavidhu/awesome-google-vrp-writeups",
        "platform": "github_advisory",
        "access_level": "public_github_repo",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "github_repo_links_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "curated",
        "learning_value": "high",
        "legal_risk": "low",
        "risk_flag": "none",
        "blocked_for_content_collection": False,
        "query": "site:github.com/xdavidhu/awesome-google-vrp-writeups Google VRP writeup",
        "notes": "Excellent report-writing and impact examples; some older items are evergreen.",
    },
    {
        "source_id": "disclosed_newsletter",
        "name": "Disclosed",
        "tier": "newsletter_podcast",
        "url": "https://getdisclosed.com/",
        "platform": "newsletter",
        "access_level": "public_or_paid_archive",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_archive_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "curated",
        "learning_value": "high",
        "legal_risk": "low",
        "risk_flag": "none",
        "blocked_for_content_collection": False,
        "query": "site:getdisclosed.com bug bounty report disclosed writeup",
        "notes": "If paid/private export is imported later, require user authorization confirmation.",
    },
    {
        "source_id": "bbre_premium_metadata",
        "name": "Bug Bounty Reports Explained / BBRE",
        "tier": "newsletter_podcast",
        "url": "https://premium.bugbountyexplained.com/",
        "platform": "newsletter",
        "access_level": "paid_private_optional",
        "auth_required": True,
        "allow_auto_collect": False,
        "metadata_only": True,
        "license_policy": "paid_metadata_only_until_user_export",
        "collection_policy": "metadata_only",
        "source_reliability": "curated",
        "learning_value": "high",
        "legal_risk": "medium",
        "risk_flag": "paid_content_requires_authorized_import",
        "blocked_for_content_collection": True,
        "query": "Bug Bounty Reports Explained public bug bounty reports",
        "notes": "No automated paid-content collection. Manual import requires authorization checkbox/export.",
    },
    {
        "source_id": "critical_thinking_public",
        "name": "Critical Thinking / Critical Research Lab public materials",
        "tier": "newsletter_podcast",
        "url": "https://www.criticalthinkingpodcast.io/about/",
        "platform": "newsletter",
        "access_level": "public_web_with_optional_private_discord",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "curated",
        "learning_value": "high",
        "legal_risk": "low",
        "risk_flag": "private_discord_requires_authorized_import",
        "blocked_for_content_collection": False,
        "query": "Critical Thinking bug bounty disclosed report writeup 2025 2026",
        "notes": "Public pages/podcast/newsletter only; Discord/private content must be user-authorized export.",
    },
    {
        "source_id": "intigriti_bug_bytes",
        "name": "Intigriti Bug Bytes / Blog",
        "tier": "newsletter_podcast",
        "url": "https://newsletter.intigriti.com/",
        "platform": "newsletter",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "curated",
        "learning_value": "medium",
        "legal_risk": "low",
        "risk_flag": "none",
        "blocked_for_content_collection": False,
        "query": "site:newsletter.intigriti.com bug bounty writeup disclosed report",
        "notes": "Useful for report mentions and technique cross-links.",
    },
    {
        "source_id": "code4rena_reports",
        "name": "Code4rena public reports",
        "tier": "web3_audit_bounty",
        "url": "https://code4rena.com/reports",
        "platform": "web3",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_report_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "official",
        "learning_value": "high",
        "legal_risk": "low",
        "risk_flag": "web3_scope_context",
        "blocked_for_content_collection": False,
        "query": "site:code4rena.com/reports public audit finding report high severity",
        "notes": "Web3 audit findings are treated as report-intelligence; no live target reproduction.",
    },
    {
        "source_id": "solodit_reports",
        "name": "Solodit public findings",
        "tier": "web3_audit_bounty",
        "url": "https://solodit.xyz/",
        "platform": "web3",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "curated",
        "learning_value": "high",
        "legal_risk": "low",
        "risk_flag": "web3_scope_context",
        "blocked_for_content_collection": False,
        "query": "site:solodit.xyz vulnerability report finding audit bounty 2025 2026",
        "notes": "Use as indexed finding source; prefer original audit report as evidence.",
    },
    {
        "source_id": "immunefi_public_reports",
        "name": "Immunefi public reports and postmortems",
        "tier": "web3_audit_bounty",
        "url": "https://immunefi.com/blog/",
        "platform": "web3",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "official",
        "learning_value": "high",
        "legal_risk": "low",
        "risk_flag": "web3_scope_context",
        "blocked_for_content_collection": False,
        "query": "site:immunefi.com/blog bug bounty report vulnerability postmortem",
        "notes": "Focus on impact framing and root cause; no operational replay on live protocols.",
    },
    {
        "source_id": "sherlock_public_reports",
        "name": "Sherlock public audit reports",
        "tier": "web3_audit_bounty",
        "url": "https://audits.sherlock.xyz/",
        "platform": "web3",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_report_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "official",
        "learning_value": "high",
        "legal_risk": "low",
        "risk_flag": "web3_scope_context",
        "blocked_for_content_collection": False,
        "query": "site:audits.sherlock.xyz report high severity finding audit contest",
        "notes": "Public Web3 audit findings; summarize root cause and impact only.",
    },
    {
        "source_id": "cantina_public_reports",
        "name": "Cantina public audit reports",
        "tier": "web3_audit_bounty",
        "url": "https://cantina.xyz/portfolio",
        "platform": "web3",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_report_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "official",
        "learning_value": "high",
        "legal_risk": "low",
        "risk_flag": "web3_scope_context",
        "blocked_for_content_collection": False,
        "query": "site:cantina.xyz audit report finding high severity bounty",
        "notes": "Public portfolio/report discovery; keep KB cards link+summary based.",
    },
    {
        "source_id": "x_report_threads",
        "name": "X report threads and hunter discussions",
        "tier": "community_social",
        "url": "https://x.com/",
        "platform": "x",
        "access_level": "public_social",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_link_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "social",
        "learning_value": "high",
        "legal_risk": "low",
        "risk_flag": "verify_with_primary_source",
        "blocked_for_content_collection": False,
        "query": "bug bounty disclosed report writeup bounty impact from:researcher 2025 2026",
        "notes": "Prefer Grok x_search for X; Tavily is for linked web verification only.",
    },
    {
        "source_id": "reddit_bugbounty_writeups",
        "name": "Reddit public bug bounty discussions",
        "tier": "community_social",
        "url": "https://www.reddit.com/r/bugbounty/",
        "platform": "web",
        "access_level": "public_social",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_link_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "social",
        "learning_value": "medium",
        "legal_risk": "low",
        "risk_flag": "verify_with_primary_source",
        "blocked_for_content_collection": False,
        "query": "site:reddit.com/r/bugbounty disclosed report writeup bug bounty",
        "notes": "Use only as discussion/context unless primary links are present.",
    },
    {
        "source_id": "medium_infosec_writeups",
        "name": "Medium / InfoSec Writeups",
        "tier": "community_social",
        "url": "https://infosecwriteups.com/",
        "platform": "blog",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "researcher",
        "learning_value": "medium",
        "legal_risk": "low",
        "risk_flag": "verify_with_primary_source",
        "blocked_for_content_collection": False,
        "query": "site:infosecwriteups.com bug bounty disclosed report writeup 2025 2026",
        "notes": "Good for researcher narratives; verify claims with original report when possible.",
    },
    {
        "source_id": "researcher_blogs_search",
        "name": "Independent researcher blogs search",
        "tier": "community_social",
        "url": "https://www.google.com/search?q=bug+bounty+writeup+disclosed+report+researcher+blog",
        "platform": "blog",
        "access_level": "public_web",
        "auth_required": False,
        "allow_auto_collect": True,
        "metadata_only": False,
        "license_policy": "public_summary_only",
        "collection_policy": "summary_links_evidence_only",
        "source_reliability": "researcher",
        "learning_value": "high",
        "legal_risk": "low",
        "risk_flag": "verify_with_primary_source",
        "blocked_for_content_collection": False,
        "query": "\"bug bounty\" \"disclosed\" \"report\" \"writeup\" \"impact\" \"2025\" OR \"2026\"",
        "notes": "Catch-all public web query; treat each result as medium confidence until verified.",
    },
    {
        "source_id": "manual_gray_telegram",
        "name": "Manual gray-channel Telegram metadata slot",
        "tier": "gray_trade_watchlist",
        "url": "用户人工记录的公开可见 Telegram 群组、频道、帖子或目录页入口描述；不保存邀请链接、附件或报告内容。",
        "platform": "telegram",
        "access_level": "public_metadata_only",
        "auth_required": True,
        "allow_auto_collect": False,
        "metadata_only": True,
        "license_policy": "metadata_only_no_content_collection",
        "collection_policy": "metadata_only",
        "source_reliability": "gray",
        "learning_value": "low",
        "legal_risk": "high",
        "risk_flag": "suspected_report_trade_or_private_material",
        "blocked_for_content_collection": True,
        "query": "",
        "research_context_urls": [
            "https://telegram.org/faq",
            "https://telegram.org/faq_channels",
            "https://core.telegram.org/api/channel",
            "https://tgstat.com/search",
        ],
        "retainable_info": [
            "公开目录/搜索面名称", "自然语言入口描述", "公开频道/群组描述摘要", "主题标签",
            "风险标记", "发现日期", "人工复核状态",
        ],
        "prohibited_info": ["邀请链接", "购买链接", "交易联系方式", "附件", "报告内容", "私聊内容"],
        "notes": "Do not buy, request, download, parse, or save report contents. Only user-provided public metadata may enter channel_watchlist.",
    },
    {
        "source_id": "manual_gray_discord",
        "name": "Manual gray-channel Discord metadata slot",
        "tier": "gray_trade_watchlist",
        "url": "用户人工记录的公开可见 Discord 服务器介绍页、社区目录页或频道主题描述；不保存邀请链接、私聊内容、附件或报告内容。",
        "platform": "discord",
        "access_level": "public_metadata_only",
        "auth_required": True,
        "allow_auto_collect": False,
        "metadata_only": True,
        "license_policy": "metadata_only_no_content_collection",
        "collection_policy": "metadata_only",
        "source_reliability": "gray",
        "learning_value": "low",
        "legal_risk": "high",
        "risk_flag": "suspected_report_trade_or_private_material",
        "blocked_for_content_collection": True,
        "query": "",
        "research_context_urls": [
            "https://support.discord.com/hc/en-us/articles/4409308485271-Discovery-Guidelines",
            "https://discord.com/guidelines",
            "https://docs.discord.com/developers/discovery/best-practices",
        ],
        "retainable_info": [
            "公开服务器/目录描述", "公开标签/分类", "社区规则提示", "风险标记",
            "发现日期", "人工复核状态",
        ],
        "prohibited_info": ["邀请链接", "购买链接", "频道消息", "成员列表", "附件", "报告内容", "私聊内容"],
        "notes": "No content collection. Manual review required before any legal/authorized export is imported separately.",
    },
    {
        "source_id": "manual_gray_forum",
        "name": "Manual gray-channel forum metadata slot",
        "tier": "gray_trade_watchlist",
        "url": "用户人工记录的公开论坛、市场帖、索引页或讨论串的自然语言入口描述；不保存需要登录/购买/下载后才能看到的内容。",
        "platform": "forum",
        "access_level": "public_metadata_only",
        "auth_required": True,
        "allow_auto_collect": False,
        "metadata_only": True,
        "license_policy": "metadata_only_no_content_collection",
        "collection_policy": "metadata_only",
        "source_reliability": "gray",
        "learning_value": "low",
        "legal_risk": "high",
        "risk_flag": "suspected_report_trade_or_private_material",
        "blocked_for_content_collection": True,
        "query": "",
        "research_context_urls": [
            "https://support.reddithelp.com/hc/en-us/articles/19695647891988-How-does-Reddit-search-work",
            "https://www.redditinc.com/policies/content-policy",
        ],
        "retainable_info": [
            "公开论坛/讨论串类型", "自然语言入口描述", "主题类别", "公开规则/版规提示",
            "风险标记", "发现日期", "人工复核状态",
        ],
        "prohibited_info": ["交易帖直链", "联系方式", "价格", "付款方式", "附件", "报告内容", "精确可复现搜索词组合"],
        "notes": "Only channel name/public entrance/topic tags/risk/manual notes; no attachments or private texts.",
    },
    {
        "source_id": "manual_gray_marketplace",
        "name": "Manual gray-channel marketplace metadata slot",
        "tier": "gray_trade_watchlist",
        "url": "用户人工记录的公开市场、资源目录、课程/报告交易广告的自然语言入口描述；不保存购买链接、交易方式、附件或报告内容。",
        "platform": "marketplace",
        "access_level": "public_metadata_only",
        "auth_required": True,
        "allow_auto_collect": False,
        "metadata_only": True,
        "license_policy": "metadata_only_no_content_collection",
        "collection_policy": "metadata_only",
        "source_reliability": "gray",
        "learning_value": "low",
        "legal_risk": "high",
        "risk_flag": "suspected_report_trade_or_private_material",
        "blocked_for_content_collection": True,
        "query": "",
        "research_context_urls": [
            "https://www.google.com/search/howsearchworks/",
        ],
        "retainable_info": [
            "公开市场/广告类型", "自然语言入口描述", "内容类别", "风险等级",
            "是否声称包含私有/NDA/付费报告", "发现日期", "人工复核状态",
        ],
        "prohibited_info": ["购买链接", "卖家账号", "付款方式", "下载链接", "附件", "报告内容", "未授权样本"],
        "notes": "Only public-facing metadata and risk notes. Do not buy, request, download, parse, or preserve content.",
    },
]

REPORT_CARD_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["cards"],
    "properties": {
        "cards": {
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "destination_path", "type", "title", "source_platform",
                    "canonical_report_url", "related_urls", "program_or_vendor",
                    "reporter_or_author", "disclosed_at", "severity", "bounty",
                    "cwe", "cve", "vuln_class", "target_types", "confidence",
                    "learning_value", "summary", "markdown", "evidence",
                ],
                "properties": {
                    "destination_path": {"type": "string"},
                    "type": {"type": "string", "enum": ["report_cluster"]},
                    "title": {"type": "string"},
                    "source_platform": {"type": "string"},
                    "canonical_report_url": {"type": "string"},
                    "related_urls": {"type": "array", "items": {"type": "string"}},
                    "program_or_vendor": {"type": "string"},
                    "reporter_or_author": {"type": "string"},
                    "disclosed_at": {"type": "string"},
                    "severity": {"type": "string"},
                    "bounty": {"type": "string"},
                    "cwe": {"type": "string"},
                    "cve": {"type": "string"},
                    "vuln_class": {"type": "string"},
                    "target_types": {"type": "array", "items": {"type": "string"}},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                    "learning_value": {"type": "string", "enum": ["high", "medium", "low"]},
                    "source_tier": {"type": "string"},
                    "source_id": {"type": "string"},
                    "access_level": {"type": "string"},
                    "license_policy": {"type": "string"},
                    "collection_policy": {"type": "string"},
                    "risk_flag": {"type": "string"},
                    "human_review_required": {"type": "boolean"},
                    "source_reliability": {"type": "string", "enum": ["official", "curated", "researcher", "social", "gray"]},
                    "legal_risk": {"type": "string", "enum": ["low", "medium", "high"]},
                    "blocked_for_content_collection": {"type": "boolean"},
                    "summary": {"type": "string"},
                    "markdown": {"type": "string"},
                    "evidence": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["claim", "source_url", "verification_notes"],
                            "properties": {
                                "claim": {"type": "string"},
                                "source_url": {"type": "string"},
                                "verification_notes": {"type": "string"},
                            },
                        },
                    },
                },
            },
        }
    },
}

REPORT_SYSTEM_PROMPT = SYSTEM_PROMPT + """

You are now curating PUBLIC disclosed Bug Bounty reports and report-adjacent writeups.
Output is for learning report quality, impact framing, root-cause analysis, and transferable authorized testing ideas.
Do not recreate a real target exploit chain as an operational playbook. Keep reproduction high-level and already-disclosed.
Do not copy full article/report bodies. Save summaries, links, short evidence notes, and source hashes only.
""".strip()

REPORT_ENRICH_TEMPLATE = """Expand the following public disclosed Bug Bounty report clusters into Obsidian report intelligence cards.

{baseline_policy}

Output JSON must match the provided schema exactly.
For every card:
- type must be report_cluster.
- destination_path must equal CARD_DEST from the cluster exactly.
- Use Chinese Markdown body, but keep source titles, CVE/CWE, program names, and URLs unchanged.
- Do not paste full report/article bodies. Use summary + link + short evidence notes only.
- Preserve source_tier, source_id, access_level, license_policy, collection_policy, risk_flag, source_reliability, legal_risk, and blocked_for_content_collection from each cluster when present.
- Do not output cards for type=channel_metadata, collection_policy=metadata_only, legal_risk=high, or blocked_for_content_collection=true items.
- Markdown must include these headings exactly:
  ## TL;DR
  ## 来源与关联材料
  ## 业务/技术背景
  ## 漏洞链路摘要（授权 / 已披露 / 高层复盘）
  ## 根因
  ## Impact 表达方式
  ## 可迁移狩猎思路
  ## 与现有 technique/case 卡关联
  ## 授权边界与不复现说明
  ## Evidence / 核查元数据
- Evidence must cite concrete primary source URLs. Tavily snippets are verification context, not primary sources.
- If a platform/public report URL is verified, confidence can be high. If only blog/X/newsletter mentions exist, use medium or low.

CLUSTERS_JSON:
{clusters_json}
""".strip()


def now_run_id(prefix: str) -> str:
    return f"{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}_{prefix}_{uuid.uuid4().hex[:8]}"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_layout() -> None:
    for d in [
        REPORT_ROOT / "platform_reports",
        REPORT_ROOT / "researcher_writeups",
        REPORT_ROOT / "x_discussions",
        REPORT_ROOT / "newsletter_roundups",
        REPORT_ROOT / "advisory_related",
        REPORT_ROOT / "imported_authorized",
        REPORT_DATA / "discovery",
        REPORT_DATA / "extracted",
        REPORT_DATA / "clusters",
        REPORT_DATA / "runs",
        MANUAL_PROMPTS_DIR,
        MANUAL_RAW_DIR,
        MANUAL_DISCOVERY_DIR,
        MANUAL_REJECTED_DIR,
        MANUAL_TRASHCAN_DIR,
        MANUAL_IMPORT_BATCHES_DIR,
    ]:
        d.mkdir(parents=True, exist_ok=True)
        marker = d / ".gitkeep"
        if not marker.exists():
            marker.write_text("", encoding="utf-8")
    if not REPORT_LEDGER.exists():
        REPORT_LEDGER.write_text(
            "id\ttype\ttitle\tsource_platform\tprogram_or_vendor\treporter_or_author\tdisclosed_at\tcanonical_report_url\tvuln_class\tseverity\tconfidence\tlearning_value\tlocal_path\tapplied_at\n",
            encoding="utf-8",
        )
    if not SOURCE_CATALOG.exists():
        SOURCE_CATALOG.parent.mkdir(parents=True, exist_ok=True)
        SOURCE_CATALOG.write_text(json.dumps([normalize_source_entry(x) for x in DEFAULT_SOURCE_CATALOG], ensure_ascii=False, indent=2), encoding="utf-8")
    if not CHANNEL_WATCHLIST_JSONL.exists():
        CHANNEL_WATCHLIST_JSONL.write_text("", encoding="utf-8")
    if not GRAY_RESEARCH_SURFACES_JSON.exists():
        GRAY_RESEARCH_SURFACES_JSON.write_text(json.dumps(DEFAULT_GRAY_RESEARCH_SURFACES, ensure_ascii=False, indent=2), encoding="utf-8")
    if not SOURCE_CATALOG_MD.exists():
        write_source_catalog_md(DEFAULT_SOURCE_CATALOG)
    if not CHANNEL_WATCHLIST_MD.exists():
        write_channel_watchlist_md([])
    if not GRAY_RESEARCH_PROTOCOL_MD.exists():
        write_gray_research_protocol(DEFAULT_GRAY_RESEARCH_SURFACES)
    if not MANUAL_CHANNEL_SOURCES_MD.exists():
        write_manual_channel_index([], [])


def load_source_catalog(path: Path | None = None) -> list[dict[str, Any]]:
    path = path or SOURCE_CATALOG
    if path.exists():
        data = json.loads(path.read_text(errors="ignore"))
        if isinstance(data, dict) and isinstance(data.get("sources"), list):
            data = data["sources"]
        if not isinstance(data, list):
            raise ValueError(f"source catalog must be a list or {{sources: []}}: {path}")
        out = [normalize_source_entry(x) for x in data if isinstance(x, dict)]
    else:
        out = [normalize_source_entry(x) for x in DEFAULT_SOURCE_CATALOG]
    seen: set[str] = set()
    dedup: list[dict[str, Any]] = []
    for item in out:
        sid = str(item.get("source_id") or "").strip()
        if not sid or sid in seen:
            continue
        seen.add(sid)
        dedup.append(item)
    return dedup


def normalize_source_entry(item: dict[str, Any]) -> dict[str, Any]:
    x = dict(item)
    x.setdefault("source_id", slugify(str(x.get("name") or x.get("url") or "source")))
    x.setdefault("name", x["source_id"])
    x.setdefault("tier", "community_social")
    x.setdefault("url", "")
    x.setdefault("platform", guess_platform(str(x.get("url") or ""), fallback="web"))
    x.setdefault("access_level", "public_web")
    x.setdefault("auth_required", False)
    x.setdefault("allow_auto_collect", False)
    x.setdefault("metadata_only", False)
    x.setdefault("license_policy", "public_summary_only")
    x.setdefault("collection_policy", "summary_links_evidence_only")
    x.setdefault("source_reliability", "social")
    x.setdefault("learning_value", "medium")
    x.setdefault("legal_risk", "low")
    x.setdefault("risk_flag", "none")
    x.setdefault("blocked_for_content_collection", bool(x.get("metadata_only")) or x.get("legal_risk") == "high")
    x.setdefault("research_context_urls", [])
    x.setdefault("retainable_info", [])
    x.setdefault("prohibited_info", [])
    x.setdefault("entry_type", "")
    x.setdefault("manual_acquisition_method", "")
    x.setdefault("manual_entry_url", x.get("url", ""))
    x.setdefault("requires_auth", bool(x.get("auth_required")))
    x.setdefault("requires_payment", False)
    x.setdefault("requires_vetting", False)
    x.setdefault("freshness_signal", "")
    x.setdefault("review_status", "verified" if x.get("url") else "needs_review")
    x.setdefault("source_group", "")
    x.setdefault("query", "")
    x.setdefault("notes", "")
    if x["tier"] == "gray_trade_watchlist":
        x["metadata_only"] = True
        x["allow_auto_collect"] = False
        x["collection_policy"] = "metadata_only"
        x["source_reliability"] = "gray"
        x["legal_risk"] = "high"
        x["blocked_for_content_collection"] = True
        x["risk_flag"] = x.get("risk_flag") or "suspected_report_trade_or_private_material"
        if not x.get("retainable_info"):
            x["retainable_info"] = [
                "自然语言入口描述", "公开主题标签", "公开描述摘要", "风险标记", "发现日期", "人工复核状态",
            ]
        if not x.get("prohibited_info"):
            x["prohibited_info"] = ["邀请链接", "购买链接", "交易联系方式", "附件", "报告内容", "私聊内容"]
    return x


def write_source_catalog_md(catalog: list[dict[str, Any]]) -> None:
    SOURCE_CATALOG_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Report Intelligence Source Catalog\n",
        "> 渠道目录用于公开报告发现、付费/私域授权导入管理，以及灰色报告交易线索的元数据观察。默认不保存完整正文。\n",
        "## Policy\n",
        "- 自动采集仅面向公开网页、公开 API、公开 GitHub repo、公开 newsletter archive 和公开报告目录。\n",
        "- 付费/私域内容只允许用户提供合法授权导出后导入；KB 默认仍只保存摘要、链接、短证据片段与 hash。\n",
        "- 灰色 report trade 线索只进入 watchlist：不购买、不索要、不下载、不解析附件、不保存报告内容。\n",
    ]
    by_tier: dict[str, list[dict[str, Any]]] = {tier: [] for tier in SOURCE_TIERS}
    for src in catalog:
        by_tier.setdefault(str(src.get("tier") or "community_social"), []).append(src)
    for tier in SOURCE_TIERS:
        rows = by_tier.get(tier, [])
        lines.append(f"\n## {tier}\n")
        lines.append("| source_id | name | reliability | legal_risk | collection_policy | entry / URL | research context | notes |")
        lines.append("|---|---|---|---|---|---|---|---|")
        gray_details: list[str] = []
        for s in rows:
            url = str(s.get("url") or "")
            link = f"[link]({url})" if url.startswith(("http://", "https://")) else f"`{url}`"
            ctx_urls = [u for u in (s.get("research_context_urls") or []) if isinstance(u, str)]
            ctx = "<br>".join(f"[ctx{i+1}]({u})" for i, u in enumerate(ctx_urls[:4]) if u.startswith(("http://", "https://"))) or ""
            notes = str(s.get("notes") or "").replace("|", "\\|")
            lines.append(
                f"| `{s.get('source_id')}` | {str(s.get('name') or '').replace('|', '/')} | "
                f"{s.get('source_reliability')} | {s.get('legal_risk')} | {s.get('collection_policy')} | {link} | {ctx} | {notes} |"
            )
            if s.get("tier") == "gray_trade_watchlist":
                retain = ", ".join(str(x) for x in (s.get("retainable_info") or [])[:12])
                prohibited = ", ".join(str(x) for x in (s.get("prohibited_info") or [])[:12])
                gray_details.append(f"### `{s.get('source_id')}`\n\n- 可保留：{retain}\n- 禁止保留：{prohibited}\n")
        if gray_details:
            lines.append("\n### Gray metadata field policy\n")
            lines.extend(gray_details)
    SOURCE_CATALOG_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_gray_research_protocol(surfaces: list[dict[str, Any]]) -> None:
    GRAY_RESEARCH_PROTOCOL_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Gray Channel Research Protocol\n",
        "> 目标：对灰色 Bug Bounty report trade 生态做完整的渠道层调研闭环，同时避免保存邀请链接、购买链接、附件、报告正文、交易联系方式或未授权内容。\n",
        "## 解释\n",
        "- “完整调研”在本库中定义为：覆盖预设平台/渠道类型、记录公开发现面、记录可保留字段与禁止字段、留下核查来源和人工复核状态。",
        "- 不能承诺穷尽隐藏、私密、临时、邀请制或已删除渠道；这些只能标记为 `coverage_gap`，不能通过购买/加入/下载来补齐。",
        "- 任何疑似泄露、NDA、私有报告内容只允许进入 `channel_watchlist` 的风险元数据，不进入 report card。\n",
        "## 允许保留的信息\n",
        "- 平台/渠道类型、自然语言入口描述、公开目录/搜索面名称、公开主题标签、公开描述摘要、风险等级、发现日期、人工复核状态。",
        "- 平台级公开文档、公开搜索/发现面的首页或说明页、合规政策链接。\n",
        "## 禁止保留的信息\n",
        "- 具体邀请链接、购买链接、交易联系方式、价格/付款方式、附件、报告正文、未授权样本、私聊内容、绕过访问限制方法。\n",
    ]
    for s in surfaces:
        lines.append(f"## {s.get('surface_id')}\n")
        lines.append(f"- Platform: `{s.get('platform')}`")
        lines.append(f"- Purpose: {s.get('purpose')}")
        lines.append("- Public context URLs:")
        for u in s.get("public_context_urls") or []:
            lines.append(f"  - [{u}]({u})")
        lines.append("- Retainable info:")
        for x in s.get("retainable_info") or []:
            lines.append(f"  - {x}")
        lines.append("- Prohibited info:")
        for x in s.get("prohibited_info") or []:
            lines.append(f"  - {x}")
        lines.append(f"- Coverage notes: {s.get('coverage_notes')}\n")
    GRAY_RESEARCH_PROTOCOL_MD.write_text("\n".join(lines), encoding="utf-8")


def read_channel_watchlist() -> list[dict[str, Any]]:
    if not CHANNEL_WATCHLIST_JSONL.exists():
        return []
    rows = []
    for line in CHANNEL_WATCHLIST_JSONL.read_text(errors="ignore").splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def append_channel_watchlist(rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    CHANNEL_WATCHLIST_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with CHANNEL_WATCHLIST_JSONL.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    write_channel_watchlist_md(read_channel_watchlist())


def write_channel_watchlist_md(rows: list[dict[str, Any]]) -> None:
    CHANNEL_WATCHLIST_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Report Trade / Gray Channel Watchlist\n",
        "> 仅保存公开可见元数据与风险标记；不购买、不索要、不下载、不解析附件、不保存疑似泄露/NDA/私有报告内容。\n",
        "| collected_at | source_id | channel_name | platform | public_entry | context | legal_risk | suspected_leak_or_nda | blocked | notes |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        public_entry = str(r.get("public_entry") or r.get("url") or "")
        link = f"[link]({public_entry})" if public_entry.startswith(("http://", "https://")) else f"`{public_entry}`"
        ctx_urls = [u for u in (r.get("research_context_urls") or []) if isinstance(u, str)]
        ctx = "<br>".join(f"[ctx{i+1}]({u})" for i, u in enumerate(ctx_urls[:4]) if u.startswith(("http://", "https://"))) or ""
        lines.append(
            f"| {r.get('collected_at', '')} | `{r.get('source_id', '')}` | "
            f"{str(r.get('channel_name') or r.get('name') or '').replace('|', '/')} | "
            f"{r.get('platform', '')} | {link} | {ctx} | {r.get('legal_risk', '')} | "
            f"{r.get('suspected_leak_or_nda', '')} | {r.get('blocked_for_content_collection', True)} | "
            f"{str(r.get('notes') or '').replace('|', '/')} |"
        )
    CHANNEL_WATCHLIST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manual_channel_index(records: list[dict[str, Any]], redacted: list[dict[str, Any]]) -> None:
    MANUAL_CHANNEL_SOURCES_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Manual Channel Sources\n",
        "> 合法付费/私域/小众渠道的完整发现记录索引。这里只保存入口、获取方法、摘要、判断依据和屏蔽原因；不保存私邀、购买/付款页、附件、报告全文或未授权内容。\n",
        "## 合法入口\n",
        "| source_id | title | type | official entry | acquisition | quality | review |",
        "|---|---|---|---|---|---|---|",
    ]
    legal = [r for r in records if r.get("storage_decision") != "redacted_discovery_record_only"]
    for r in sorted(legal, key=lambda x: (str(x.get("source_group", "")), str(x.get("source_title", "")))):
        url = str(r.get("official_or_legitimate_entry") or r.get("allowed_url") or "")
        link = f"[link]({url})" if url.startswith(("http://", "https://")) else "`metadata`"
        lines.append(
            f"| `{r.get('source_id', '')}` | {str(r.get('source_title', '')).replace('|', '/')} | "
            f"{r.get('entry_type', '')} | {link} | {str(r.get('legal_acquisition_method', '')).replace('|', '/')} | "
            f"{str(r.get('quality_signal', '')).replace('|', '/')} | {r.get('review_status', '')} |"
        )
    lines += [
        "\n## Trashcan / 已屏蔽入口\n",
        "> 硬性阻断命中的内容统一进入 `data/report_intel/manual_channel_research/trashcan/`。这里只显示 redacted 元数据：domain/hash/reason/发现路径；不显示原始私邀、付款页、附件或正文。\n",
        "| record_id | domain | redacted hash | reason | discovery path | review |",
        "|---|---|---|---|---|---|",
    ]
    for r in redacted:
        lines.append(
            f"| `{r.get('record_id', '')}` | {r.get('source_domain', '')} | `{r.get('redacted_url_hash', '')}` | "
            f"{str(r.get('redaction_reason', '')).replace('|', '/')} | {str(r.get('discovery_path_summary', '')).replace('|', '/')} | {r.get('review_status', '')} |"
        )
    lines += [
        "\n## 待复核\n",
        "| source_id | title | reason |",
        "|---|---|---|",
    ]
    for r in [x for x in records if x.get("review_status") == "needs_review"]:
        lines.append(f"| `{r.get('source_id', '')}` | {str(r.get('source_title', '')).replace('|', '/')} | {str(r.get('risk_flag', '')).replace('|', '/')} |")
    MANUAL_CHANNEL_SOURCES_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def source_matches_tier(src: dict[str, Any], tier_or_preset: str) -> bool:
    if not tier_or_preset:
        return True
    if tier_or_preset in PRESET_TO_TIERS:
        return str(src.get("tier")) in PRESET_TO_TIERS[tier_or_preset]
    return str(src.get("tier")) == tier_or_preset


def catalog_sources_for(tier_or_preset: str, catalog: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not tier_or_preset or tier_or_preset == "all":
        return catalog
    special_groups = {
        "vendor_official": {"vendor_official"},
        "wp_ecosystem": {"wp_ecosystem"},
        "research_blogs": {"research_blogs", "paid_private_community"},
        "web3_extended": {"web3_extended"},
        "gray_public_surfaces": {"gray_public_surfaces"},
    }
    if tier_or_preset == "legitimate_gated":
        return [
            s for s in catalog
            if bool(s.get("requires_auth") or s.get("requires_payment") or s.get("requires_vetting"))
            or str(s.get("collection_policy")) == "metadata_until_authorized_export"
            or str(s.get("entry_type")) in {"paid_subscription_landing", "vetted_application", "private_discord_after_subscription", "course_landing"}
        ]
    if tier_or_preset == "gray_public_surfaces":
        return [s for s in catalog if str(s.get("source_group") or "") == "gray_public_surfaces" or str(s.get("tier")) == "gray_trade_watchlist"]
    if tier_or_preset in special_groups:
        groups = special_groups[tier_or_preset]
        return [s for s in catalog if str(s.get("source_group") or "") in groups]
    return [s for s in catalog if source_matches_tier(s, tier_or_preset)]


def source_score(src: dict[str, Any]) -> int:
    reliability = {"official": 50, "curated": 40, "researcher": 32, "social": 20, "gray": 0}
    learning = {"high": 30, "medium": 18, "low": 6}
    risk_penalty = {"low": 0, "medium": 20, "high": 60}
    score = reliability.get(str(src.get("source_reliability")), 10)
    score += learning.get(str(src.get("learning_value")), 10)
    score -= risk_penalty.get(str(src.get("legal_risk")), 20)
    if src.get("allow_auto_collect"):
        score += 10
    if src.get("metadata_only"):
        score -= 15
    return score


def source_metadata_snapshot(src: dict[str, Any], *, notes: str = "") -> dict[str, Any]:
    return {
        "id": "channel_" + hashlib.sha256(str(src.get("source_id", "")).encode()).hexdigest()[:12],
        "type": "channel_metadata",
        "source_id": src.get("source_id", ""),
        "source_tier": src.get("tier", ""),
        "channel_name": src.get("name", ""),
        "platform": src.get("platform", ""),
        "public_entry": src.get("url", ""),
        "access_level": src.get("access_level", ""),
        "license_policy": src.get("license_policy", ""),
        "collection_policy": "metadata_only",
        "risk_flag": src.get("risk_flag", ""),
        "source_reliability": src.get("source_reliability", ""),
        "learning_value": src.get("learning_value", "low"),
        "legal_risk": src.get("legal_risk", "high"),
        "research_context_urls": src.get("research_context_urls", []),
        "retainable_info": src.get("retainable_info", []),
        "prohibited_info": src.get("prohibited_info", []),
        "human_review_required": True,
        "suspected_leak_or_nda": src.get("tier") == "gray_trade_watchlist" or src.get("legal_risk") == "high",
        "blocked_for_content_collection": True,
        "notes": notes or src.get("notes", ""),
        "collected_at": utc_now(),
    }


def with_source_metadata(candidate: dict[str, Any], src: dict[str, Any]) -> dict[str, Any]:
    out = dict(candidate)
    out.update({
        "source_tier": src.get("tier", "community_social"),
        "source_id": src.get("source_id", out.get("raw_source", out.get("source_platform", "unknown"))),
        "access_level": src.get("access_level", "public_web"),
        "license_policy": src.get("license_policy", "public_summary_only"),
        "collection_policy": src.get("collection_policy", "summary_links_evidence_only"),
        "risk_flag": src.get("risk_flag", "none"),
        "human_review_required": bool(src.get("legal_risk") in {"medium", "high"} or src.get("metadata_only")),
        "source_reliability": src.get("source_reliability", "social"),
        "legal_risk": src.get("legal_risk", "low"),
        "blocked_for_content_collection": bool(src.get("blocked_for_content_collection", False)),
    })
    if out.get("blocked_for_content_collection") or out.get("legal_risk") == "high":
        out["human_review_required"] = True
    return out


def http_json(url: str, *, headers: dict[str, str] | None = None, timeout: int = 45) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": "bb-report-intel/1.0", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_text(url: str, *, headers: dict[str, str] | None = None, timeout: int = 45) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "bb-report-intel/1.0", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def optional_headers() -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def h1_headers() -> dict[str, str] | None:
    user = os.getenv("HACKERONE_API_USERNAME")
    token = os.getenv("HACKERONE_API_TOKEN")
    if not user or not token:
        return None
    raw = base64.b64encode(f"{user}:{token}".encode()).decode()
    return {"Authorization": f"Basic {raw}", "Accept": "application/json"}


def normalize_url(url: str) -> str:
    if not url:
        return ""
    try:
        p = urllib.parse.urlparse(url.strip())
        q = urllib.parse.parse_qsl(p.query, keep_blank_values=False)
        q = [(k, v) for k, v in q if not k.lower().startswith("utm_") and k.lower() not in {"ref", "source"}]
        p = p._replace(query=urllib.parse.urlencode(q), fragment="")
        return urllib.parse.urlunparse(p).rstrip("/")
    except Exception:
        return url.strip().rstrip("/")


def slugify(text: str, max_len: int = 86) -> str:
    text = text.lower().strip()
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return (text[:max_len].strip("-") or "report")


def unique(seq: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for x in seq:
        s = str(x or "").strip()
        if not s:
            continue
        key = normalize_url(s)
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def guess_platform(url: str, fallback: str = "web") -> str:
    netloc = urllib.parse.urlparse(url).netloc.lower()
    if "hackerone.com" in netloc:
        return "hackerone"
    if "bugcrowd.com" in netloc:
        return "bugcrowd"
    if "github.com" in netloc and "advisories" in url:
        return "github_advisory"
    if "securitylab.github.com" in netloc:
        return "github_security_lab"
    if "x.com" in netloc or "twitter.com" in netloc:
        return "x"
    if any(x in netloc for x in ["intigriti", "bugbytes", "disclosed", "newsletter"]):
        return "newsletter"
    return fallback


def candidate_id(url: str, title: str) -> str:
    src = normalize_url(url) or title
    return hashlib.sha256(src.encode("utf-8", errors="ignore")).hexdigest()[:16]


def destination_for(candidate: dict[str, Any]) -> str:
    platform = str(candidate.get("source_platform") or "web")
    sub = REPORT_DIR_BY_PLATFORM.get(platform, "researcher_writeups")
    title = str(candidate.get("title") or "report")
    date = str(candidate.get("disclosed_at") or "unknown")[:10]
    prefix = date if re.match(r"\d{4}-\d{2}-\d{2}", date) else "undated"
    return str(REPORT_ROOT / sub / f"{prefix}-{slugify(title)}.md")


def make_candidate(**kw: Any) -> dict[str, Any]:
    url = normalize_url(str(kw.get("canonical_report_url") or kw.get("source_url") or ""))
    title = str(kw.get("title") or url or "Untitled public report")
    platform = str(kw.get("source_platform") or guess_platform(url))
    related = unique([url] + list(kw.get("related_urls") or []))
    source_tier = str(kw.get("source_tier") or "platform_public" if platform in {"hackerone", "bugcrowd", "github_advisory", "github_security_lab"} else kw.get("source_tier") or "community_social")
    legal_risk = str(kw.get("legal_risk") or ("high" if source_tier == "gray_trade_watchlist" else "low"))
    collection_policy = str(kw.get("collection_policy") or ("metadata_only" if legal_risk == "high" else "summary_links_evidence_only"))
    blocked = bool(kw.get("blocked_for_content_collection") or collection_policy == "metadata_only" or legal_risk == "high")
    c = {
        "id": kw.get("id") or candidate_id(url, title),
        "type": "report_candidate",
        "source_tier": source_tier,
        "source_id": str(kw.get("source_id") or kw.get("raw_source") or platform),
        "source_platform": platform,
        "title": title.strip(),
        "canonical_report_url": url,
        "related_urls": related,
        "program_or_vendor": str(kw.get("program_or_vendor") or "unknown"),
        "reporter_or_author": str(kw.get("reporter_or_author") or "unknown"),
        "disclosed_at": str(kw.get("disclosed_at") or "unknown"),
        "severity": str(kw.get("severity") or "unknown"),
        "bounty": str(kw.get("bounty") or "unknown"),
        "cwe": str(kw.get("cwe") or "unknown"),
        "cve": str(kw.get("cve") or ""),
        "vuln_class": str(kw.get("vuln_class") or "Unknown"),
        "target_types": kw.get("target_types") or ["Web/API/SaaS"],
        "confidence": str(kw.get("confidence") or "medium"),
        "learning_value": str(kw.get("learning_value") or "medium"),
        "summary": compact_text(str(kw.get("summary") or kw.get("description") or ""), 700),
        "evidence": kw.get("evidence") or [],
        "raw_source": str(kw.get("raw_source") or platform),
        "access_level": str(kw.get("access_level") or "public_web"),
        "license_policy": str(kw.get("license_policy") or "public_summary_only"),
        "collection_policy": collection_policy,
        "risk_flag": str(kw.get("risk_flag") or "none"),
        "human_review_required": bool(kw.get("human_review_required") or blocked or legal_risk == "medium"),
        "source_reliability": str(kw.get("source_reliability") or ("official" if platform in {"hackerone", "bugcrowd", "github_advisory", "github_security_lab"} else "social")),
        "legal_risk": legal_risk,
        "blocked_for_content_collection": blocked,
        "discovered_at": utc_now(),
    }
    c["destination_path"] = destination_for(c)
    return c


def parse_date(s: str) -> str:
    if not s:
        return "unknown"
    m = re.search(r"(20\d{2}-\d{2}-\d{2})", s)
    if m:
        return m.group(1)
    return s[:10]


def discover_github_advisories(limit: int, from_date: str, query: str = "") -> list[dict[str, Any]]:
    params = {
        "per_page": str(min(max(limit, 1), 100)),
        "sort": "published",
        "direction": "desc",
        "type": "reviewed",
        "published": f">={from_date}",
    }
    if query:
        params["ecosystem"] = ""
    url = "https://api.github.com/advisories?" + urllib.parse.urlencode({k: v for k, v in params.items() if v})
    data = http_json(url, headers=optional_headers())
    out = []
    for item in data[:limit] if isinstance(data, list) else []:
        ghsa = item.get("ghsa_id") or ""
        html = item.get("html_url") or (f"https://github.com/advisories/{ghsa}" if ghsa else "")
        cves = item.get("cve_id") or ""
        cwes = item.get("cwes") or []
        cwe = ", ".join(x.get("cwe_id", "") for x in cwes if isinstance(x, dict)) or "unknown"
        severity = item.get("severity") or "unknown"
        title = item.get("summary") or ghsa or "GitHub advisory"
        out.append(make_candidate(
            source_platform="github_advisory",
            title=title,
            canonical_report_url=html,
            related_urls=[html],
            program_or_vendor=(item.get("identifiers") or [{}])[0].get("value", "GitHub Advisory") if isinstance(item.get("identifiers"), list) else "GitHub Advisory",
            reporter_or_author="GitHub Advisory Database",
            disclosed_at=parse_date(item.get("published_at", "")),
            severity=severity,
            cwe=cwe,
            cve=cves or "",
            vuln_class=title,
            confidence="high",
            learning_value="medium",
            summary=item.get("description") or title,
            evidence=[{"claim": "GitHub Global Security Advisory is publicly listed", "source_url": html, "verification_notes": f"GHSA id: {ghsa}"}],
            raw_source="github_advisories_api",
        ))
    return out


def discover_github_security_lab(limit: int) -> list[dict[str, Any]]:
    html = http_text("https://securitylab.github.com/advisories/")
    urls = []
    for m in re.finditer(r'href="(/advisories/[^"]+)"', html):
        href = m.group(1)
        if href.rstrip("/") == "/advisories":
            continue
        full = "https://securitylab.github.com" + href
        if full not in urls:
            urls.append(full)
        if len(urls) >= limit:
            break
    out = []
    for u in urls[:limit]:
        slug = u.rstrip("/").split("/")[-1]
        title = slug.replace("-", " ").strip().title()
        out.append(make_candidate(
            source_platform="github_security_lab",
            title=title,
            canonical_report_url=u,
            related_urls=[u],
            program_or_vendor="GitHub Security Lab advisory",
            reporter_or_author="GitHub Security Lab",
            disclosed_at="unknown",
            severity="unknown",
            vuln_class="Security advisory / report",
            confidence="high",
            learning_value="medium",
            summary=f"Public GitHub Security Lab advisory page: {title}",
            evidence=[{"claim": "GitHub Security Lab advisory is publicly listed", "source_url": u, "verification_notes": "Discovered from GitHub Security Lab advisories index."}],
            raw_source="github_security_lab_index",
        ))
    return out


def discover_hackerone_api(limit: int, from_date: str, topic: str = "") -> list[dict[str, Any]]:
    headers = h1_headers()
    if not headers:
        return []
    query = f"disclosed:true disclosed_at:>={from_date}"
    if topic:
        query += f" {topic}"
    params = urllib.parse.urlencode({"queryString": query, "page[size]": str(min(limit, 100))})
    url = "https://api.hackerone.com/v1/hackers/hacktivity?" + params
    data = http_json(url, headers=headers)
    out = []
    for row in data.get("data", [])[:limit] if isinstance(data, dict) else []:
        attrs = row.get("attributes", {}) if isinstance(row, dict) else {}
        rel = row.get("relationships", {}) if isinstance(row, dict) else {}
        report_id = attrs.get("report_id") or row.get("id")
        url = attrs.get("url") or (f"https://hackerone.com/reports/{report_id}" if report_id else "")
        title = attrs.get("title") or attrs.get("substate") or f"HackerOne report {report_id}"
        out.append(make_candidate(
            source_platform="hackerone",
            title=title,
            canonical_report_url=url,
            related_urls=[url],
            program_or_vendor=str(attrs.get("team", {}).get("name") if isinstance(attrs.get("team"), dict) else attrs.get("team") or "HackerOne program"),
            reporter_or_author=str(attrs.get("reporter", {}).get("username") if isinstance(attrs.get("reporter"), dict) else "unknown"),
            disclosed_at=parse_date(str(attrs.get("disclosed_at") or attrs.get("latest_disclosable_action_at") or "")),
            severity=str(attrs.get("severity_rating") or attrs.get("severity") or "unknown"),
            bounty=str(attrs.get("total_awarded_amount") or "unknown"),
            vuln_class=title,
            confidence="high",
            learning_value="high",
            summary=str(attrs.get("description") or attrs.get("vulnerability_information") or title),
            evidence=[{"claim": "HackerOne API returned a disclosed Hacktivity/report item", "source_url": url, "verification_notes": f"HackerOne API row id: {row.get('id')}"}],
            raw_source="hackerone_api",
        ))
    return out


def tavily_available() -> bool:
    return bool(os.getenv("TAVILY_API_KEY"))


def discover_with_tavily(source: str, topic: str, vuln_class: str, limit: int, from_date: str, to_date: str) -> list[dict[str, Any]]:
    if not tavily_available():
        return []
    source_queries = {
        "hackerone": "site:hackerone.com/reports disclosed bug bounty report",
        "bugcrowd": "site:bugcrowd.com/crowdstream disclosed bug bounty report",
        "blogs_x": "bug bounty disclosed report writeup researcher blog X thread",
        "newsletters": "bug bounty disclosed reports newsletter writeup",
    }
    base = source_queries.get(source, "public disclosed bug bounty report writeup")
    query = " ".join(x for x in [base, topic, vuln_class, "2025 2026"] if x).strip()
    resp = tavily_search(query, max_results=limit, search_depth=DEFAULT_TAVILY_SEARCH_DEPTH, start_date=from_date, end_date=to_date)
    out = []
    for r in resp.get("results", [])[:limit]:
        url = r.get("url") or ""
        title = r.get("title") or url or "Public report result"
        platform = guess_platform(url, fallback="blog" if source == "blogs_x" else source.rstrip("s"))
        conf = "medium" if platform in {"blog", "newsletter", "web", "x"} else "high"
        out.append(make_candidate(
            source_platform=platform,
            title=title,
            canonical_report_url=url,
            related_urls=[url],
            program_or_vendor="unknown",
            reporter_or_author="unknown",
            disclosed_at="unknown",
            severity="unknown",
            vuln_class=vuln_class or "Public disclosed report",
            confidence=conf,
            learning_value="medium",
            summary=r.get("content") or title,
            evidence=[{"claim": "Tavily Search found a public candidate source", "source_url": url, "verification_notes": f"Search query: {query}; score={r.get('score', '')}"}],
            raw_source=f"tavily_search:{source}",
        ))
    return out


def discover_with_tavily_catalog(src: dict[str, Any], topic: str, vuln_class: str, limit: int, from_date: str, to_date: str) -> list[dict[str, Any]]:
    if not tavily_available():
        return []
    base = str(src.get("query") or src.get("name") or "public disclosed bug bounty report writeup")
    query = " ".join(x for x in [base, topic, vuln_class, "2025 2026"] if x).strip()
    resp = tavily_search(query, max_results=limit, search_depth=DEFAULT_TAVILY_SEARCH_DEPTH, start_date=from_date, end_date=to_date)
    out = []
    for r in resp.get("results", [])[:limit]:
        url = r.get("url") or ""
        title = r.get("title") or url or f"{src.get('name')} candidate"
        platform = guess_platform(url, fallback=str(src.get("platform") or "web"))
        reliability = str(src.get("source_reliability") or "social")
        conf = "high" if reliability in {"official", "curated"} and platform not in {"web", "blog", "newsletter", "x"} else "medium"
        out.append(with_source_metadata(make_candidate(
            source_platform=platform,
            source_tier=src.get("tier"),
            source_id=src.get("source_id"),
            title=title,
            canonical_report_url=url,
            related_urls=[url],
            program_or_vendor="unknown",
            reporter_or_author="unknown",
            disclosed_at="unknown",
            severity="unknown",
            vuln_class=vuln_class or "Public disclosed report",
            confidence=conf,
            learning_value=src.get("learning_value") or "medium",
            summary=r.get("content") or title,
            evidence=[{"claim": "Tavily Search found a public candidate source", "source_url": url, "verification_notes": f"Catalog source: {src.get('source_id')}; query: {query}; score={r.get('score', '')}"}],
            raw_source=f"catalog:{src.get('source_id')}",
        ), src))
    return out


def discover_source_from_catalog(src: dict[str, Any], *, topic: str, vuln_class: str, limit: int, from_date: str, to_date: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return (report_candidates, metadata_watchlist_rows)."""
    src = normalize_source_entry(src)
    if src.get("metadata_only") or src.get("collection_policy") == "metadata_only" or src.get("legal_risk") == "high":
        return [], [source_metadata_snapshot(src, notes="metadata-only source; content collection blocked by policy")]
    if not src.get("allow_auto_collect"):
        return [], [source_metadata_snapshot(src, notes="source requires manual authorization/import before content collection")]

    sid = str(src.get("source_id") or "")
    out: list[dict[str, Any]] = []
    try:
        if sid == "github_advisories_api":
            out = discover_github_advisories(limit, from_date, topic or vuln_class)
            out = [with_source_metadata(c, src) for c in out]
        elif sid == "github_security_lab":
            out = discover_github_security_lab(limit)
            out = [with_source_metadata(c, src) for c in out]
        elif sid == "hackerone_hacktivity_api":
            out = discover_hackerone_api(limit, from_date, topic)
            if len(out) < limit:
                out.extend(discover_with_tavily_catalog(src, topic, vuln_class, max(1, limit - len(out)), from_date, to_date))
            out = [with_source_metadata(c, src) for c in out]
        else:
            out = discover_with_tavily_catalog(src, topic, vuln_class, limit, from_date, to_date)
    except Exception as e:
        return [], [source_metadata_snapshot(src, notes=f"discovery_failed: {e}")]
    return out[:limit], []


def boolish(value: Any) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y", "是", "需要", "required"}


def domain_of(url: str) -> str:
    try:
        parsed = urllib.parse.urlparse(url if "://" in url else "https://" + url)
        return parsed.netloc.lower().removeprefix("www.")
    except Exception:
        return ""


def sha256_16(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:16]


BLOCKED_URL_PATTERNS = [
    (re.compile(r"https?://(?:www\.)?discord\.gg/[^\s]+", re.I), "discord_invite_link"),
    (re.compile(r"https?://(?:www\.)?discord(?:app)?\.com/invite/[^\s]+", re.I), "discord_invite_link"),
    (re.compile(r"https?://t\.me/\+[^\s]+", re.I), "telegram_private_invite"),
    (re.compile(r"https?://(?:t\.me|telegram\.me)/joinchat/[^\s]+", re.I), "telegram_private_invite"),
    (re.compile(r"https?://(?:drive\.google\.com|mega\.nz|mediafire\.com|dropbox\.com|gofile\.io|anonfiles\.com)/[^\s]+", re.I), "cloud_drive_or_file_share"),
    (re.compile(r"https?://[^\s]*(?:checkout|payment|payments|cart|invoice|billing|paypal|stripe|lemonsqueezy|paddle)[^\s]*", re.I), "direct_payment_or_checkout_url"),
    (re.compile(r"https?://[^\s]+\.(?:zip|rar|7z|tar|gz|pdf|docx?|xlsx?|pptx?)(?:[?#][^\s]*)?$", re.I), "attachment_or_fulltext_file_url"),
]
BLOCKED_TEXT_TERMS = [
    "pirated", "盗版", "cracked course", "course leak", "leaked report", "泄露报告",
    "nda report", "private report dump", "report trade", "报告交易", "paid report free",
]


def blocked_reason_for_text(text: str) -> str:
    compact = str(text or "")
    for pattern, reason in BLOCKED_URL_PATTERNS:
        if pattern.search(compact):
            return reason
    low = compact.lower()
    for term in BLOCKED_TEXT_TERMS:
        if term.lower() in low:
            return "pirated_or_leaked_material_indicator"
    if len(compact) > 8000:
        return "long_body_possible_fulltext"
    if compact.count("\n") > 80 and any(x in low for x in ["steps to reproduce", "impact", "proof of concept", "漏洞链路"]):
        return "possible_report_fulltext"
    return ""


def redact_blocked_manual_raw_text(text: str) -> str:
    """Redact hard-blocked URLs before preserving imported Grok/browser output.

    The manual channel workflow keeps a raw-output audit trail, but hard-stop
    items must not leave invite/payment/attachment URLs behind. We keep enough
    metadata for later review by replacing each matched URL with its reason and
    a short stable hash.
    """
    sanitized = str(text or "")
    for pattern, reason in BLOCKED_URL_PATTERNS:
        def repl(match: re.Match[str]) -> str:
            raw = match.group(0)
            return f"[TRASHCAN_REDACTED_URL reason={reason} sha256_16={sha256_16(raw)}]"

        sanitized = pattern.sub(repl, sanitized)
    return sanitized


def sanitize_allowed_url(url: str) -> tuple[str, str, str]:
    url = str(url or "").strip()
    if not url:
        return "", "", ""
    reason = blocked_reason_for_text(url)
    if reason:
        return "", sha256_16(url), reason
    return normalize_url(url), "", ""


def manual_channel_record_id(row: dict[str, Any]) -> str:
    src = "|".join(str(row.get(k, "")) for k in ["source_id", "source_title", "allowed_url", "official_or_legitimate_entry", "source_domain"])
    return "mchan_" + sha256_16(src or json.dumps(row, sort_keys=True, ensure_ascii=False))


def normalize_source_id_text(text: str) -> str:
    text = str(text or "").strip().lower()
    text = re.sub(r"[^a-z0-9_-]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_-")
    return text or "manual_channel_source"


def infer_entry_type(row: dict[str, Any]) -> str:
    raw = str(row.get("entry_type") or row.get("channel_type") or row.get("category") or "").lower()
    if str(row.get("storage_policy") or row.get("collection_policy") or "").lower() == "redacted_discovery_record_only":
        return "redacted_lead_to_legitimate_source"
    if "discord" in raw and ("private" in raw or boolish(row.get("requires_payment"))):
        return "private_discord_after_subscription"
    if "newsletter" in raw:
        return "newsletter_archive"
    if "course" in raw or "lab" in raw:
        return "course_landing"
    if boolish(row.get("requires_vetting")) or "vetted" in raw or "application" in raw:
        return "vetted_application"
    if boolish(row.get("requires_payment")) or "paid" in raw or "subscription" in raw:
        return "paid_subscription_landing"
    if "recognition" in raw:
        return "platform_recognition"
    if "research" in raw or "blog" in raw:
        return "research_blog"
    if "community" in raw or "discord" in raw:
        return "community_discovery"
    return "official_signup"


def infer_collection_policy(row: dict[str, Any], entry_type: str, redacted: bool) -> str:
    if redacted or entry_type == "redacted_lead_to_legitimate_source":
        return "redacted_discovery_record_only"
    raw = str(row.get("storage_policy") or row.get("collection_policy") or "").strip()
    if raw in MANUAL_COLLECTION_POLICIES:
        return raw
    if boolish(row.get("requires_payment")) or boolish(row.get("requires_auth")) or boolish(row.get("requires_vetting")):
        return "metadata_until_authorized_export"
    return "public_summary_links_only"


def infer_tier_for_manual_record(record: dict[str, Any]) -> str:
    group = str(record.get("source_group") or "").lower()
    category = str(record.get("channel_type") or "").lower()
    if "web3" in group or "web3" in category:
        return "web3_audit_bounty"
    if "gray" in group or "gray" in category:
        return "gray_trade_watchlist"
    if "newsletter" in category or "paid_private" in group:
        return "newsletter_podcast"
    if "research" in group or "blog" in category:
        return "curated_aggregators"
    return "platform_public"


def normalize_manual_channel_row(row: dict[str, Any], *, research_topic: str = "", prompt_or_query: str = "", tool_used: str = "manual") -> dict[str, Any]:
    title = str(row.get("source_title") or row.get("channel_name") or row.get("title") or row.get("source_id") or "manual channel").strip()
    source_id = normalize_source_id_text(str(row.get("source_id") or title))[:80]
    official_url = str(row.get("official_url") or row.get("allowed_url") or row.get("manual_entry_url") or row.get("url") or "").strip()
    legitimate_entry = str(row.get("official_or_legitimate_entry") or row.get("legal_entry") or official_url or "").strip()
    allowed_url, redacted_hash, url_reason = sanitize_allowed_url(official_url)
    allowed_legit, legit_hash, legit_reason = sanitize_allowed_url(legitimate_entry)
    combined_text = "\n".join(str(v) for v in row.values())
    text_reason = blocked_reason_for_text(combined_text)
    redaction_reason = url_reason or legit_reason or text_reason
    redacted = bool(redaction_reason)
    entry_type = infer_entry_type(row)
    if redacted:
        entry_type = "redacted_lead_to_legitimate_source"
    collection_policy = infer_collection_policy(row, entry_type, redacted)
    source_domain = domain_of(allowed_url or allowed_legit or official_url or legitimate_entry)
    record = {
        "record_id": "",
        "collected_at": str(row.get("collected_at") or utc_now()),
        "research_topic": str(row.get("research_topic") or research_topic or row.get("category") or ""),
        "tool_used": str(row.get("tool_used") or tool_used),
        "prompt_or_query": str(row.get("prompt_or_query") or prompt_or_query),
        "source_title": title,
        "source_domain": source_domain,
        "allowed_url": "" if redacted else allowed_url,
        "redacted_url_hash": redacted_hash or legit_hash or (sha256_16(official_url or legitimate_entry) if redacted else ""),
        "channel_type": str(row.get("channel_type") or row.get("category") or ""),
        "discovery_path_summary": compact_text(str(row.get("discovery_path_summary") or f"Found via {tool_used} research topic: {research_topic or row.get('category', '')}"), 500),
        "why_interesting": compact_text(str(row.get("why_interesting") or row.get("why_high_value") or ""), 700),
        "legal_acquisition_method": compact_text(str(row.get("legal_acquisition_method") or row.get("manual_acquisition_method") or ""), 700),
        "official_or_legitimate_entry": "" if redacted else (allowed_legit or allowed_url),
        "freshness_signal": str(row.get("freshness_signal") or ""),
        "quality_signal": compact_text(str(row.get("quality_signal") or row.get("confidence") or row.get("why_high_value") or ""), 500),
        "risk_flag": str(row.get("risk_flag") or ("redacted_lead" if redacted else "none")),
        "storage_decision": collection_policy if not redacted else "redacted_discovery_record_only",
        "redaction_reason": redaction_reason,
        "review_status": str(row.get("review_status") or ("blocked" if redacted else "verified")),
        "source_id": source_id,
        "entry_type": entry_type,
        "collection_policy": collection_policy,
        "requires_auth": boolish(row.get("requires_auth")),
        "requires_payment": boolish(row.get("requires_payment")),
        "requires_vetting": boolish(row.get("requires_vetting")),
        "source_group": str(row.get("source_group") or row.get("group") or ""),
    }
    record["record_id"] = manual_channel_record_id(record)
    if not record["legal_acquisition_method"] and not redacted:
        record["review_status"] = "needs_review"
        record["risk_flag"] = "missing_legal_acquisition_method"
    return record


def read_manual_channel_input(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(errors="ignore")
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        if isinstance(data, list):
            return data
        for key in ("records", "items", "sources"):
            if isinstance(data, dict) and isinstance(data.get(key), list):
                return data[key]
        return []
    # TSV/CSV with flexible delimiter; prefer tab.
    sample = text[:4096]
    dialect = csv.excel_tab if "\t" in sample else csv.excel
    rows = []
    for row in csv.DictReader(text.splitlines(), dialect=dialect):
        rows.append({str(k or "").strip(): str(v or "").strip() for k, v in row.items()})
    return rows


def load_all_manual_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    redacted: list[dict[str, Any]] = []
    for d, target in [(MANUAL_DISCOVERY_DIR, records), (MANUAL_TRASHCAN_DIR, redacted), (MANUAL_REJECTED_DIR, redacted)]:
        for path in sorted(d.glob("*.jsonl")):
            for line in path.read_text(errors="ignore").splitlines():
                if line.strip():
                    target.append(json.loads(line))
    def dedup(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: set[str] = set()
        out: list[dict[str, Any]] = []
        for row in rows:
            key = str(row.get("record_id") or row.get("redacted_url_hash") or json.dumps(row, sort_keys=True, ensure_ascii=False))
            if key in seen:
                continue
            seen.add(key)
            out.append(row)
        return out
    return dedup(records), dedup(redacted)


def manual_record_to_source(record: dict[str, Any]) -> dict[str, Any]:
    tier = infer_tier_for_manual_record(record)
    legal_risk = "high" if tier == "gray_trade_watchlist" else ("medium" if record.get("requires_payment") or record.get("requires_vetting") else "low")
    collection_policy = str(record.get("collection_policy") or record.get("storage_decision") or "metadata_until_authorized_export")
    metadata_only = collection_policy in {"metadata_only", "metadata_until_authorized_export", "redacted_discovery_record_only"} or legal_risk == "high"
    return normalize_source_entry({
        "source_id": record.get("source_id"),
        "name": record.get("source_title"),
        "tier": tier,
        "url": record.get("official_or_legitimate_entry") or record.get("allowed_url"),
        "platform": guess_platform(str(record.get("official_or_legitimate_entry") or record.get("allowed_url") or ""), fallback="web"),
        "access_level": "manual_legal_entry",
        "auth_required": bool(record.get("requires_auth")),
        "allow_auto_collect": not metadata_only and legal_risk != "high",
        "metadata_only": metadata_only,
        "license_policy": "manual_channel_metadata_summary_only",
        "collection_policy": collection_policy,
        "source_reliability": "curated" if tier != "gray_trade_watchlist" else "gray",
        "learning_value": "high",
        "legal_risk": legal_risk,
        "risk_flag": record.get("risk_flag") or "none",
        "blocked_for_content_collection": metadata_only or legal_risk == "high",
        "entry_type": record.get("entry_type"),
        "manual_acquisition_method": record.get("legal_acquisition_method"),
        "manual_entry_url": record.get("official_or_legitimate_entry") or record.get("allowed_url"),
        "requires_auth": bool(record.get("requires_auth")),
        "requires_payment": bool(record.get("requires_payment")),
        "requires_vetting": bool(record.get("requires_vetting")),
        "freshness_signal": record.get("freshness_signal"),
        "review_status": record.get("review_status"),
        "source_group": record.get("source_group"),
        "query": f"{record.get('source_title', '')} bug bounty report learning writeup",
        "notes": record.get("why_interesting") or record.get("discovery_path_summary"),
    })


def cmd_manual_channel_prompts(args: argparse.Namespace) -> None:
    ensure_layout()
    out_dir = Path(args.out_dir) if args.out_dir else (RUNS_DIR / now_run_id("manual_channel_prompts") if args.dry_run else MANUAL_PROMPTS_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"mode": "manual_channel_prompts", "count": len(MANUAL_CHANNEL_PROMPTS), "created_at": utc_now(), "dry_run": args.dry_run}
    for name, topic in MANUAL_CHANNEL_PROMPTS:
        prompt = f"{MANUAL_CHANNEL_BASELINE_PROMPT}\n\nTASK:\n{topic}\n"
        (out_dir / f"{name}.txt").write_text(prompt, encoding="utf-8")
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[{'dry-run' if args.dry_run else 'ok'}] manual_channel_prompts={len(MANUAL_CHANNEL_PROMPTS)} out_dir={out_dir}")


def cmd_import_manual_channel_results(args: argparse.Namespace) -> None:
    ensure_layout()
    inp = Path(args.input).expanduser()
    if not inp.is_absolute():
        inp = (ROOT / inp).resolve()
    rows = read_manual_channel_input(inp)
    records = [normalize_manual_channel_row(r, research_topic=args.research_topic, prompt_or_query=args.prompt_or_query, tool_used=args.tool_used) for r in rows]
    legal = [r for r in records if r.get("storage_decision") != "redacted_discovery_record_only"]
    redacted = [r for r in records if r.get("storage_decision") == "redacted_discovery_record_only"]
    batch_id = now_run_id("manual_channels")
    batch_dir = RUNS_DIR / batch_id if args.dry_run else MANUAL_IMPORT_BATCHES_DIR / batch_id
    batch_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(batch_dir / "discovery_records.jsonl", legal)
    write_jsonl(batch_dir / "trashcan.jsonl", redacted)
    (batch_dir / "manifest.json").write_text(json.dumps({
        "mode": "import_manual_channel_results",
        "input": str(inp),
        "records": len(records),
        "legal": len(legal),
        "redacted": len(redacted),
        "dry_run": args.dry_run,
        "created_at": utc_now(),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    if not args.dry_run:
        stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        write_jsonl(MANUAL_DISCOVERY_DIR / f"{stamp}_discovery_records.jsonl", legal)
        write_jsonl(MANUAL_TRASHCAN_DIR / f"{stamp}_trashcan.jsonl", redacted)
        MANUAL_RAW_DIR.mkdir(parents=True, exist_ok=True)
        raw_snapshot = redact_blocked_manual_raw_text(inp.read_text(errors="ignore"))
        (MANUAL_RAW_DIR / f"{stamp}_{safe_filename(inp.stem)}{inp.suffix}").write_text(raw_snapshot, encoding="utf-8")
        all_records, all_redacted = load_all_manual_records()
        write_manual_channel_index(all_records, all_redacted)
    print(f"[{'dry-run' if args.dry_run else 'ok'}] imported={len(records)} legal={len(legal)} redacted={len(redacted)} batch_dir={batch_dir}")


def cmd_validate_discovery_records(args: argparse.Namespace) -> None:
    ensure_layout()
    records, redacted = load_all_manual_records()
    issues: list[str] = []
    warnings: list[str] = []
    for r in records:
        combined = json.dumps(r, ensure_ascii=False)
        reason = blocked_reason_for_text(combined)
        if reason:
            issues.append(f"LEGAL_RECORD_HAS_BLOCKED_CONTENT {r.get('record_id')} reason={reason}")
        if not r.get("legal_acquisition_method"):
            issues.append(f"LEGAL_RECORD_MISSING_ACQUISITION {r.get('record_id')}")
        if not (r.get("official_or_legitimate_entry") or r.get("allowed_url")):
            issues.append(f"LEGAL_RECORD_MISSING_ENTRY {r.get('record_id')}")
    for r in redacted:
        if not r.get("redacted_url_hash"):
            issues.append(f"REDACTED_MISSING_HASH {r.get('record_id')}")
        if not r.get("redaction_reason"):
            issues.append(f"REDACTED_MISSING_REASON {r.get('record_id')}")
        if r.get("allowed_url"):
            issues.append(f"REDACTED_HAS_ALLOWED_URL {r.get('record_id')}")
    for raw_path in sorted(MANUAL_RAW_DIR.glob("*")):
        if not raw_path.is_file() or raw_path.name == ".gitkeep":
            continue
        raw_text = raw_path.read_text(errors="ignore")
        for pattern, reason in BLOCKED_URL_PATTERNS:
            if pattern.search(raw_text):
                warnings.append(f"RAW_OUTPUT_HAS_BLOCKED_URL {raw_path.name} reason={reason}")
                break
    print(f"manual_discovery_records={len(records)} redacted={len(redacted)} issues={len(issues)} warnings={len(warnings)}")
    for issue in issues[:50]:
        print("ISSUE", issue)
    for warning in warnings[:50]:
        print("WARNING", warning)
    raise SystemExit(1 if issues else 0)


def cmd_apply_manual_channel_catalog(args: argparse.Namespace) -> None:
    ensure_layout()
    if args.input:
        inp = Path(args.input).expanduser()
        if not inp.is_absolute():
            inp = (ROOT / inp).resolve()
        rows = read_manual_channel_input(inp)
        records = [normalize_manual_channel_row(r, tool_used="manual") for r in rows]
        records = [r for r in records if r.get("storage_decision") != "redacted_discovery_record_only"]
    else:
        records, _ = load_all_manual_records()
    sources = [manual_record_to_source(r) for r in records if r.get("review_status") in {"verified", "needs_review"} and r.get("storage_decision") != "redacted_discovery_record_only"]
    catalog = load_source_catalog()
    by_id = {str(s.get("source_id")): s for s in catalog}
    changed = 0
    for s in sources:
        sid = str(s.get("source_id"))
        if not sid:
            continue
        if sid not in by_id or args.replace:
            by_id[sid] = s
            changed += 1
    merged = list(by_id.values())
    if args.dry_run:
        run_dir = RUNS_DIR / now_run_id("apply_manual_channel_catalog")
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "source_catalog.preview.json").write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[dry-run] manual_sources={len(sources)} changed={changed} preview={run_dir / 'source_catalog.preview.json'}")
        return
    SOURCE_CATALOG.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    write_source_catalog_md(merged)
    print(f"[ok] manual_sources={len(sources)} changed={changed} catalog={SOURCE_CATALOG}")


def cmd_export_manual_channel_index(args: argparse.Namespace) -> None:
    ensure_layout()
    records, redacted = load_all_manual_records()
    if args.dry_run:
        print(f"[dry-run] would write {MANUAL_CHANNEL_SOURCES_MD} legal={len(records)} redacted={len(redacted)}")
        return
    write_manual_channel_index(records, redacted)
    print(f"[ok] wrote {MANUAL_CHANNEL_SOURCES_MD} legal={len(records)} redacted={len(redacted)}")


def write_discovery_run(run_dir: Path, manifest: dict[str, Any], candidates: list[dict[str, Any]], metadata_rows: list[dict[str, Any]], *, dry_run: bool) -> None:
    discovery_dir = run_dir / "discovery"
    discovery_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    if dry_run:
        (discovery_dir / "request_plan.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    write_jsonl(discovery_dir / "candidates.jsonl", candidates)
    (discovery_dir / "candidates.json").write_text(json.dumps({"candidates": candidates}, ensure_ascii=False, indent=2), encoding="utf-8")
    if metadata_rows:
        write_jsonl(discovery_dir / "channel_metadata.jsonl", metadata_rows)
        (discovery_dir / "channel_metadata.json").write_text(json.dumps({"metadata": metadata_rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    if metadata_rows and not dry_run:
        append_channel_watchlist(metadata_rows)


def cmd_catalog_build(args: argparse.Namespace) -> None:
    ensure_layout()
    catalog = [normalize_source_entry(x) for x in DEFAULT_SOURCE_CATALOG]
    default_ids = {str(x.get("source_id")) for x in catalog}
    if SOURCE_CATALOG.exists():
        try:
            for existing in load_source_catalog():
                sid = str(existing.get("source_id") or "")
                if sid and sid not in default_ids and (existing.get("manual_acquisition_method") or existing.get("entry_type") or existing.get("source_group")):
                    catalog.append(normalize_source_entry(existing))
                    default_ids.add(sid)
        except Exception as e:
            print(f"[warn] could not merge existing manual catalog entries: {e}", file=sys.stderr)
    payload = {"sources": catalog, "generated_at": utc_now(), "source_policy": "public_summary_metadata_gray_watchlist"}
    gray_payload = {
        "surfaces": DEFAULT_GRAY_RESEARCH_SURFACES,
        "generated_at": utc_now(),
        "policy": "gray-channel research retains public metadata/context only; no invite/purchase/content artifacts",
    }
    if args.dry_run:
        run_dir = RUNS_DIR / now_run_id("catalog_build")
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "source_catalog.preview.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        (run_dir / "gray_research_surfaces.preview.json").write_text(json.dumps(gray_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[dry-run] catalog_sources={len(catalog)} preview={run_dir / 'source_catalog.preview.json'}")
        return
    SOURCE_CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    GRAY_RESEARCH_SURFACES_JSON.write_text(json.dumps(DEFAULT_GRAY_RESEARCH_SURFACES, ensure_ascii=False, indent=2), encoding="utf-8")
    write_source_catalog_md(catalog)
    write_channel_watchlist_md(read_channel_watchlist())
    write_gray_research_protocol(DEFAULT_GRAY_RESEARCH_SURFACES)
    print(f"[ok] catalog_sources={len(catalog)} json={SOURCE_CATALOG} md={SOURCE_CATALOG_MD} gray_protocol={GRAY_RESEARCH_PROTOCOL_MD}")


def cmd_triage_sources(args: argparse.Namespace) -> None:
    ensure_layout()
    catalog = load_source_catalog()
    rows = sorted(catalog, key=source_score, reverse=True)
    lines = ["source_id\ttier\tscore\treliability\tlearning_value\tlegal_risk\tallow_auto_collect\tmetadata_only\turl"]
    for s in rows:
        if args.tier and not source_matches_tier(s, args.tier):
            continue
        lines.append("\t".join(str(x) for x in [
            s.get("source_id"), s.get("tier"), source_score(s), s.get("source_reliability"),
            s.get("learning_value"), s.get("legal_risk"), s.get("allow_auto_collect"),
            s.get("metadata_only"), s.get("url"),
        ]))
    if args.dry_run:
        print("\n".join(lines))
        return
    SOURCE_TRIAGE_TSV.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[ok] wrote {SOURCE_TRIAGE_TSV} rows={len(lines)-1}")


def cmd_discover_source(args: argparse.Namespace) -> None:
    load_dotenv(ROOT / ".env")
    ensure_layout()
    catalog = load_source_catalog()
    src = next((s for s in catalog if s.get("source_id") == args.source_id), None)
    if not src:
        raise SystemExit(f"Unknown source_id={args.source_id}. Run catalog-build or inspect {SOURCE_CATALOG_MD}.")
    run_dir = Path(args.run_dir) if args.run_dir else RUNS_DIR / now_run_id(f"source_{slugify(args.source_id, 32)}")
    manifest = {
        "mode": "report_discover_source",
        "source_id": args.source_id,
        "source": src,
        "topic": args.topic,
        "vuln_class": args.vuln_class,
        "from_date": args.from_date,
        "to_date": args.to_date,
        "limit": args.limit,
        "dry_run": args.dry_run,
        "created_at": utc_now(),
        "source_policy": "public_auto_collect_or_metadata_only_watchlist",
    }
    if args.dry_run:
        candidates: list[dict[str, Any]] = []
        metadata = [source_metadata_snapshot(src, notes="dry-run preview; no network/content collection")] if (src.get("metadata_only") or not src.get("allow_auto_collect")) else []
    else:
        candidates, metadata = discover_source_from_catalog(src, topic=args.topic, vuln_class=args.vuln_class, limit=args.limit, from_date=args.from_date, to_date=args.to_date)
    write_discovery_run(run_dir, manifest, candidates, metadata, dry_run=args.dry_run)
    print(f"[{'dry-run' if args.dry_run else 'ok'}] source_id={args.source_id} candidates={len(candidates)} metadata={len(metadata)} run_dir={run_dir}")


def cmd_discover_catalog(args: argparse.Namespace) -> None:
    load_dotenv(ROOT / ".env")
    ensure_layout()
    catalog = load_source_catalog()
    selector = args.tier or args.preset or "public_only"
    selected = catalog_sources_for(selector, catalog)
    if not selected:
        raise SystemExit(f"No sources selected for tier/preset={selector}")
    run_dir = Path(args.run_dir) if args.run_dir else RUNS_DIR / now_run_id(f"catalog_{slugify(selector, 32)}")
    manifest = {
        "mode": "report_discover_catalog",
        "selector": selector,
        "preset": args.preset,
        "tier": args.tier,
        "source_ids": [s.get("source_id") for s in selected],
        "topic": args.topic,
        "vuln_class": args.vuln_class,
        "from_date": args.from_date,
        "to_date": args.to_date,
        "limit": args.limit,
        "dry_run": args.dry_run,
        "created_at": utc_now(),
        "source_policy": "coverage_first_but_gray_metadata_only",
    }
    candidates: list[dict[str, Any]] = []
    metadata_rows: list[dict[str, Any]] = []
    if args.dry_run:
        for src in selected:
            if src.get("metadata_only") or src.get("legal_risk") == "high" or not src.get("allow_auto_collect"):
                metadata_rows.append(source_metadata_snapshot(src, notes="dry-run preview; no network/content collection"))
    else:
        per_source = max(1, args.limit)
        for src in selected:
            cs, ms = discover_source_from_catalog(src, topic=args.topic, vuln_class=args.vuln_class, limit=per_source, from_date=args.from_date, to_date=args.to_date)
            candidates.extend(cs)
            metadata_rows.extend(ms)
        seen: set[str] = set()
        unique_rows: list[dict[str, Any]] = []
        for c in candidates:
            key = normalize_url(c.get("canonical_report_url", "")) or c.get("id")
            if not key or key in seen:
                continue
            seen.add(key)
            unique_rows.append(c)
            if len(unique_rows) >= args.limit:
                break
        candidates = unique_rows
    write_discovery_run(run_dir, manifest, candidates, metadata_rows, dry_run=args.dry_run)
    print(f"[{'dry-run' if args.dry_run else 'ok'}] selector={selector} sources={len(selected)} candidates={len(candidates)} metadata={len(metadata_rows)} run_dir={run_dir}")


def load_manual_import(path: Path) -> tuple[bool, list[dict[str, Any]], str]:
    data = json.loads(path.read_text(errors="ignore"))
    if isinstance(data, list):
        return False, data, "unspecified"
    if not isinstance(data, dict):
        raise ValueError("manual import must be a JSON object or array")
    items = data.get("items") or data.get("candidates") or data.get("reports") or []
    if not isinstance(items, list):
        raise ValueError("manual import items/candidates/reports must be a list")
    return bool(data.get("authorization_confirmed")), items, str(data.get("source_id") or "manual_authorized_import")


def normalize_manual_import(path: Path, *, authorization_confirmed: bool = False) -> list[dict[str, Any]]:
    embedded_auth, items, source_id = load_manual_import(path)
    if not (authorization_confirmed or embedded_auth):
        raise PermissionError("manual import requires authorization_confirmed=true in the file or --authorization-confirmed")
    out: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        url = str(item.get("canonical_report_url") or item.get("url") or item.get("source_url") or "")
        title = str(item.get("title") or url or "Authorized imported report")
        out.append(make_candidate(
            source_platform=item.get("source_platform") or "manual_import",
            source_tier=item.get("source_tier") or "paid_authorized",
            source_id=item.get("source_id") or source_id,
            title=title,
            canonical_report_url=url,
            related_urls=item.get("related_urls") or ([url] if url else []),
            program_or_vendor=item.get("program_or_vendor") or item.get("program") or "unknown",
            reporter_or_author=item.get("reporter_or_author") or item.get("author") or "unknown",
            disclosed_at=item.get("disclosed_at") or item.get("date") or "unknown",
            severity=item.get("severity") or "unknown",
            bounty=item.get("bounty") or "unknown",
            cwe=item.get("cwe") or "unknown",
            cve=item.get("cve") or "",
            vuln_class=item.get("vuln_class") or "Authorized imported report",
            confidence=item.get("confidence") or "medium",
            learning_value=item.get("learning_value") or "medium",
            summary=item.get("summary") or item.get("description") or "",
            evidence=item.get("evidence") or [{"claim": "User provided an authorized export item", "source_url": url or str(path), "verification_notes": "Manual import; content storage remains summary/link/hash only."}],
            raw_source=f"manual_import:{source_id}",
            access_level="authorized_export",
            license_policy="user_authorized_import_summary_only",
            collection_policy="summary_links_evidence_only",
            risk_flag="manual_authorized_import",
            human_review_required=True,
            source_reliability=item.get("source_reliability") or "researcher",
            legal_risk=item.get("legal_risk") or "medium",
            blocked_for_content_collection=False,
        ))
    return out


def cmd_import_manual(args: argparse.Namespace) -> None:
    ensure_layout()
    inp = Path(args.input).expanduser()
    if not inp.is_absolute():
        inp = (ROOT / inp).resolve()
    candidates = normalize_manual_import(inp, authorization_confirmed=args.authorization_confirmed)
    run_dir = Path(args.run_dir) if args.run_dir else RUNS_DIR / now_run_id("manual_import")
    manifest = {
        "mode": "report_import_manual",
        "input": str(inp),
        "authorization_confirmed": bool(args.authorization_confirmed),
        "candidate_count": len(candidates),
        "dry_run": args.dry_run,
        "created_at": utc_now(),
        "source_policy": "user_authorized_export_summary_links_hash_only",
    }
    write_discovery_run(run_dir, manifest, candidates, [], dry_run=args.dry_run)
    import_dir = run_dir / "manual_import"
    import_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(import_dir / "candidates.jsonl", candidates)
    if not args.dry_run:
        (REPORT_ROOT / "imported_authorized" / ".last_import_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[{'dry-run' if args.dry_run else 'ok'}] manual_import_candidates={len(candidates)} run_dir={run_dir}")


def parse_sources(raw: str) -> list[str]:
    parts = []
    saw_token = False
    for token in re.split(r"[,\s]+", raw.strip()):
        if not token:
            continue
        saw_token = True
        parts.extend(PUBLIC_SOURCE_PRESETS.get(token, [token]))
    if not parts and saw_token:
        return []
    return list(dict.fromkeys(parts)) or PUBLIC_SOURCE_PRESETS["public_all"]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonish(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(errors="ignore").strip()
    if not text:
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    if isinstance(data, list):
        return data
    for key in ("clusters", "candidates", "cards"):
        if isinstance(data, dict) and isinstance(data.get(key), list):
            return data[key]
    return []


def cmd_discover(args: argparse.Namespace) -> None:
    load_dotenv(ROOT / ".env")
    ensure_layout()
    run_dir = Path(args.run_dir) if args.run_dir else RUNS_DIR / now_run_id("report_discover")
    discovery_dir = run_dir / "discovery"
    discovery_dir.mkdir(parents=True, exist_ok=True)
    sources = parse_sources(args.sources)
    manifest = {
        "mode": "report_discover",
        "sources": sources,
        "topic": args.topic,
        "vuln_class": args.vuln_class,
        "from_date": args.from_date,
        "to_date": args.to_date,
        "limit": args.limit,
        "dry_run": args.dry_run,
        "created_at": utc_now(),
        "source_policy": "public_only_summary_and_links",
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.dry_run:
        (discovery_dir / "request_plan.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        write_jsonl(discovery_dir / "candidates.jsonl", [])
        (discovery_dir / "candidates.json").write_text(json.dumps({"candidates": []}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[dry-run] wrote {discovery_dir / 'request_plan.json'}")
        print(f"run_dir={run_dir}")
        return
    candidates: list[dict[str, Any]] = []
    per_source = max(1, args.limit)
    for source in sources:
        try:
            if source == "github":
                candidates.extend(discover_github_advisories(per_source, args.from_date, args.topic or args.vuln_class))
            elif source == "github_security_lab":
                candidates.extend(discover_github_security_lab(per_source))
            elif source == "hackerone":
                candidates.extend(discover_hackerone_api(per_source, args.from_date, args.topic))
                candidates.extend(discover_with_tavily("hackerone", args.topic, args.vuln_class, per_source, args.from_date, args.to_date))
            elif source in {"bugcrowd", "blogs_x", "newsletters"}:
                candidates.extend(discover_with_tavily(source, args.topic, args.vuln_class, per_source, args.from_date, args.to_date))
        except Exception as e:
            print(f"[warn] source={source} failed: {e}", file=sys.stderr)
    # deterministic de-dup for discovery output
    seen: set[str] = set()
    unique_rows = []
    for c in candidates:
        key = normalize_url(c.get("canonical_report_url", "")) or c.get("id")
        if not key or key in seen:
            continue
        seen.add(key)
        unique_rows.append(c)
        if len(unique_rows) >= args.limit:
            break
    write_jsonl(discovery_dir / "candidates.jsonl", unique_rows)
    (discovery_dir / "candidates.json").write_text(json.dumps({"candidates": unique_rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] candidates={len(unique_rows)} run_dir={run_dir}")


def cluster_key(c: dict[str, Any]) -> str:
    url = normalize_url(c.get("canonical_report_url", ""))
    if url:
        m = re.search(r"hackerone\.com/reports/(\d+)", url)
        if m:
            return "h1:" + m.group(1)
        m = re.search(r"github\.com/advisories/(GHSA-[A-Za-z0-9-]+)", url)
        if m:
            return "ghsa:" + m.group(1).lower()
        return "url:" + url.lower()
    raw = "|".join(str(c.get(k, "")).lower() for k in ["title", "program_or_vendor", "vuln_class"])
    return "fuzzy:" + hashlib.sha256(raw.encode()).hexdigest()[:20]


def merge_cluster(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    base = dict(rows[0])
    urls = []
    evidence = []
    for r in rows:
        urls += [r.get("canonical_report_url", "")] + list(r.get("related_urls") or [])
        evidence += list(r.get("evidence") or [])
        if base.get("confidence") != "high" and r.get("confidence") == "high":
            base["confidence"] = "high"
        if base.get("learning_value") != "high" and r.get("learning_value") == "high":
            base["learning_value"] = "high"
    base["cluster_key"] = key
    base["type"] = "report_cluster"
    base["related_urls"] = unique(urls)
    base["evidence"] = evidence[:20]
    base["cluster_size"] = len(rows)
    base["destination_path"] = destination_for(base)
    return base


def cmd_cluster(args: argparse.Namespace) -> None:
    ensure_layout()
    inp = Path(args.input)
    rows = read_jsonish(inp)
    skipped = [
        r for r in rows
        if r.get("type") == "channel_metadata"
        or r.get("collection_policy") == "metadata_only"
        or r.get("legal_risk") == "high"
        or r.get("blocked_for_content_collection")
    ]
    rows = [r for r in rows if r not in skipped]
    buckets: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        buckets.setdefault(cluster_key(row), []).append(row)
    clusters = [merge_cluster(v, k) for k, v in sorted(buckets.items())]
    run_dir = Path(args.run_dir) if args.run_dir else inp.parents[1] if "discovery" in inp.parts else RUNS_DIR / now_run_id("report_cluster")
    out_dir = run_dir / "clusters"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "clusters.json").write_text(json.dumps({"clusters": clusters}, ensure_ascii=False, indent=2), encoding="utf-8")
    write_jsonl(out_dir / "clusters.jsonl", clusters)
    if skipped:
        write_jsonl(out_dir / "skipped_channel_metadata.jsonl", skipped)
    print(f"[ok] clusters={len(clusters)} skipped_metadata_or_high_risk={len(skipped)} run_dir={run_dir}")


def extract_context_for_cluster(cluster: dict[str, Any], max_urls: int = 5) -> dict[str, Any]:
    urls = [u for u in unique([cluster.get("canonical_report_url", "")] + list(cluster.get("related_urls") or [])) if not is_x_url(u)]
    ctx = {"provider": "tavily", "checked_at": utc_now(), "extracted": [], "skipped_urls": [], "usage": {"credits": 0}}
    if not tavily_available():
        ctx["status"] = "missing_tavily_key"
        return ctx
    if not urls:
        ctx["status"] = "no_non_x_urls"
        return ctx
    try:
        resp = tavily_extract(urls[:max_urls], query=str(cluster.get("title") or ""), extract_depth=DEFAULT_TAVILY_EXTRACT_DEPTH)
        ctx["request_id"] = resp.get("request_id")
        ctx["usage"] = resp.get("usage") or {"credits": 0}
        for r in resp.get("results", []) or []:
            raw = str(r.get("raw_content") or "")
            ctx["extracted"].append({
                "url": r.get("url", ""),
                "raw_content_hash": sha16(raw),
                "raw_content_chars": len(raw),
                "snippet": compact_text(raw, int(DEFAULT_TAVILY_CONTEXT_CHARS)),
            })
        for r in resp.get("failed_results", []) or []:
            ctx["skipped_urls"].append({"url": r.get("url", ""), "reason": "extract_failed", "error": r.get("error", "")})
        ctx["status"] = "ok" if ctx["extracted"] else "needs_review"
    except Exception as e:
        ctx["status"] = "error"
        ctx["error"] = str(e)
    return ctx


def response_request_body(prompt: str, max_output_tokens: int, use_search: bool) -> dict[str, Any]:
    body: dict[str, Any] = {
        "model": DEFAULT_MODEL,
        "input": [
            {"role": "system", "content": REPORT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "store": False,
        "text": {"format": {"type": "json_schema", "name": "public_bug_bounty_report_cards", "schema": REPORT_CARD_SCHEMA, "strict": True}},
        "max_output_tokens": max_output_tokens,
    }
    if use_search:
        body["tools"] = [{"type": "x_search"}, {"type": "web_search"}]
    return body


def cmd_enrich(args: argparse.Namespace) -> None:
    load_dotenv(ROOT / ".env")
    ensure_layout()
    inp = Path(args.input)
    clusters = read_jsonish(inp)
    blocked_clusters = [
        c for c in clusters
        if c.get("type") == "channel_metadata"
        or c.get("collection_policy") == "metadata_only"
        or c.get("legal_risk") == "high"
        or c.get("blocked_for_content_collection")
    ]
    clusters = [c for c in clusters if c not in blocked_clusters]
    if not clusters:
        raise SystemExit(f"No enrichable report clusters found in {inp}; blocked_or_metadata={len(blocked_clusters)}")
    run_dir = Path(args.run_dir) if args.run_dir else inp.parents[1] if "clusters" in inp.parts else RUNS_DIR / now_run_id("report_enrich")
    for sub in ["extracted", "prompts", "raw", "cards"]:
        (run_dir / sub).mkdir(parents=True, exist_ok=True)
    if blocked_clusters:
        write_jsonl(run_dir / "clusters" / "blocked_from_enrich.jsonl", blocked_clusters)
    enriched_clusters = []
    for c in clusters[:args.limit]:
        copy = dict(c)
        copy["CARD_DEST"] = c.get("destination_path") or destination_for(c)
        if not args.skip_tavily:
            copy["tavily_context"] = extract_context_for_cluster(c)
        enriched_clusters.append(copy)
    (run_dir / "extracted" / "clusters_with_context.json").write_text(json.dumps({"clusters": enriched_clusters}, ensure_ascii=False, indent=2), encoding="utf-8")
    prompt = REPORT_ENRICH_TEMPLATE.format(
        baseline_policy=BASELINE_EVIDENCE_POLICY,
        clusters_json=json.dumps(enriched_clusters, ensure_ascii=False, indent=2),
    )
    body = response_request_body(prompt, args.max_output_tokens, args.use_search)
    (run_dir / "prompts" / "report_enrich_prompt.txt").write_text(prompt, encoding="utf-8")
    (run_dir / "raw" / "report_enrich.request.json").write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.dry_run:
        print(f"[dry-run] wrote request for {len(enriched_clusters)} clusters")
        print(f"run_dir={run_dir}")
        return
    if not (os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")):
        raise SystemExit("Missing XAI_API_KEY/GROK_API_KEY. Use --dry-run or add key to .env for Grok report enrichment.")
    resp = api_json("POST", "/responses", body, base_url=args.api_base)
    (run_dir / "raw" / "report_enrich.response.json").write_text(json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8")
    parsed = parse_json_text(response_text(resp))
    (run_dir / "cards" / "report_cards.json").write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] cards={len(parsed.get('cards', []))} run_dir={run_dir}")


def sanitize_report_markdown(text: str) -> str:
    # Keep wording clear/compliant; do not obfuscate technical words.
    banned = ["credential stuffing", "botnet", "malware", "real third-party data"]
    for b in banned:
        text = re.sub(re.escape(b), "高风险内容（仅作已披露风险摘要，不复现）", text, flags=re.I)
    guard = "本卡只用于公开披露报告学习、授权项目复盘与报告写作参考；不保存完整原文，不复现真实目标链路。"
    if "授权边界" not in text and "不复现" not in text:
        text += f"\n\n> 授权边界：{guard}\n"
    return text.strip() + "\n"


def frontmatter(card: dict[str, Any]) -> str:
    lines = ["---"]
    for k in [
        "type", "source_platform", "canonical_report_url", "program_or_vendor", "reporter_or_author", "disclosed_at",
        "severity", "bounty", "cwe", "cve", "vuln_class", "confidence", "learning_value",
        "source_tier", "source_id", "access_level", "license_policy", "collection_policy", "risk_flag",
        "human_review_required", "source_reliability", "legal_risk", "blocked_for_content_collection",
    ]:
        v = card.get(k, "")
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{k}: {str(v).replace(chr(10), ' ')}")
    if card.get("related_urls"):
        lines.append("related_urls:")
        for u in card.get("related_urls") or []:
            lines.append(f"  - {u}")
    lines.append("---\n")
    return "\n".join(lines)


def card_records_from_run(run_dir: Path) -> list[dict[str, Any]]:
    cards_dir = run_dir / "cards"
    cards = []
    for path in sorted(cards_dir.glob("*.json")):
        data = json.loads(path.read_text(errors="ignore"))
        cards.extend(data.get("cards", []))
    return cards


def cmd_apply(args: argparse.Namespace) -> None:
    ensure_layout()
    run_dir = Path(args.run_dir)
    cards = card_records_from_run(run_dir)
    if not cards:
        raise SystemExit(f"No cards found under {run_dir / 'cards'}")
    applied = 0
    existing_urls = set()
    if REPORT_LEDGER.exists():
        for line in REPORT_LEDGER.read_text(errors="ignore").splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) > 7:
                existing_urls.add(normalize_url(parts[7]))
    ledger_rows = []
    for card in cards:
        if (
            card.get("type") == "channel_metadata"
            or card.get("collection_policy") == "metadata_only"
            or card.get("legal_risk") == "high"
            or card.get("blocked_for_content_collection")
        ):
            print(f"[skip blocked/metadata] {card.get('title') or card.get('source_id')}")
            continue
        dest_raw = str(card.get("destination_path") or "")
        if not dest_raw:
            continue
        dest = Path(dest_raw)
        if not dest.is_absolute():
            dest = ROOT / dest
        dest = dest.resolve()
        if not str(dest).startswith(str(ROOT.resolve())):
            print(f"[skip outside root] {dest}")
            continue
        md = sanitize_report_markdown(str(card.get("markdown") or ""))
        body = frontmatter(card) + f"# {card.get('title', dest.stem)}\n\n" + md
        if args.dry_run:
            print(f"[dry-run] would write {dest}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            old = dest.read_text(errors="ignore") if dest.exists() else ""
            if REPORT_KB_START in old and REPORT_KB_END in old:
                new = re.sub(re.escape(REPORT_KB_START) + r"[\s\S]*?" + re.escape(REPORT_KB_END), f"{REPORT_KB_START}\n{body}\n{REPORT_KB_END}", old)
            else:
                new = f"{REPORT_KB_START}\n{body}\n{REPORT_KB_END}\n"
            dest.write_text(new, encoding="utf-8")
            print(f"[write] {dest}")
        applied += 1
        canon = normalize_url(str(card.get("canonical_report_url") or ""))
        if canon and canon not in existing_urls:
            ledger_rows.append([
                hashlib.sha256(canon.encode()).hexdigest()[:12],
                "report_cluster",
                card.get("title", ""),
                card.get("source_platform", ""),
                card.get("program_or_vendor", ""),
                card.get("reporter_or_author", ""),
                card.get("disclosed_at", ""),
                card.get("canonical_report_url", ""),
                card.get("vuln_class", ""),
                card.get("severity", ""),
                card.get("confidence", ""),
                card.get("learning_value", ""),
                str(dest),
                utc_now(),
            ])
            existing_urls.add(canon)
    if ledger_rows and not args.dry_run:
        with REPORT_LEDGER.open("a", encoding="utf-8") as f:
            for row in ledger_rows:
                f.write("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in row) + "\n")
    if not args.dry_run:
        build_report_indexes()
    print(f"applied_report_cards={applied} ledger_added={len(ledger_rows)}")


def title_for(path: Path) -> str:
    for line in path.read_text(errors="ignore").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def rel_link(path: Path) -> str:
    return path.relative_to(ROOT / "docs" / "intelligence_kb").with_suffix("").as_posix()


def build_report_indexes() -> None:
    ensure_layout()
    totals = 0
    lines = ["# Report Intelligence Index\n", "> 公开披露 Bug Bounty 报告、关联博客/X 讨论/newsletter 的摘要型学习库。\n"]
    for sub in ["platform_reports", "researcher_writeups", "x_discussions", "newsletter_roundups", "advisory_related", "imported_authorized"]:
        d = REPORT_ROOT / sub
        files = sorted([p for p in d.glob("*.md") if p.name != "_index.md"])
        totals += len(files)
        idx_lines = [f"# {sub}\n", f"Count: {len(files)}\n"]
        for p in files:
            idx_lines.append(f"- [[{rel_link(p)}|{title_for(p)}]]")
        (d / "_index.md").write_text("\n".join(idx_lines) + "\n", encoding="utf-8")
        lines.append(f"## {sub}\n")
        lines.append(f"Count: {len(files)}\n")
        lines.append(f"- [[reports/{sub}/_index|{sub} index]]\n")
    lines.append(f"\n## 当前状态\n\n- Report cards: {totals}\n- Report ledger: `data/report_intel/report_ledger.tsv`\n")
    (REPORT_ROOT / "_index.md").write_text("\n".join(lines), encoding="utf-8")


def cmd_build_index(args: argparse.Namespace) -> None:
    build_report_indexes()
    print(f"[ok] wrote {REPORT_ROOT / '_index.md'}")


def cmd_validate(args: argparse.Namespace) -> None:
    ensure_layout()
    required = [
        "## TL;DR", "## 来源与关联材料", "## 漏洞链路摘要", "## Impact 表达方式",
        "## 可迁移狩猎思路", "## 授权边界与不复现说明", "## Evidence / 核查元数据",
    ]
    files = [p for p in REPORT_ROOT.glob("*/*.md") if p.name != "_index.md"]
    issues = []
    for p in files:
        t = p.read_text(errors="ignore")
        miss = [x for x in required if x not in t]
        if miss:
            issues.append((p, miss))
        if len(t) > 65000:
            issues.append((p, ["too_large_possible_fulltext_snapshot"]))
    print(f"report_cards={len(files)} report_issues={len(issues)} ledger={REPORT_LEDGER}")
    for p, miss in issues[:30]:
        print(f"ISSUE {p}: missing={miss}")
    raise SystemExit(1 if issues else 0)


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Public Bug Bounty report intelligence agent")
    ap.add_argument("--api-base", default=DEFAULT_API_BASE)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("catalog-build")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_catalog_build)

    p = sub.add_parser("triage-sources")
    p.add_argument("--tier", default="", help="tier or preset selector")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_triage_sources)

    p = sub.add_parser("discover-source")
    p.add_argument("--source-id", required=True)
    p.add_argument("--topic", default="")
    p.add_argument("--vuln-class", default="")
    p.add_argument("--from-date", default=DEFAULT_FROM_DATE)
    p.add_argument("--to-date", default=DEFAULT_TO_DATE)
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--run-dir")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_discover_source)

    p = sub.add_parser("discover-catalog")
    p.add_argument("--tier", default="", help="one of platform_public/curated_aggregators/newsletter_podcast/web3_audit_bounty/community_social/gray_trade_watchlist")
    p.add_argument("--preset", default="", help="maximum_coverage/public_only/paid_authorized/gray_metadata_only/web3_reports")
    p.add_argument("--topic", default="")
    p.add_argument("--vuln-class", default="")
    p.add_argument("--from-date", default=DEFAULT_FROM_DATE)
    p.add_argument("--to-date", default=DEFAULT_TO_DATE)
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--run-dir")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_discover_catalog)

    p = sub.add_parser("import-manual")
    p.add_argument("--input", required=True)
    p.add_argument("--run-dir")
    p.add_argument("--authorization-confirmed", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_import_manual)

    p = sub.add_parser("manual-channel-prompts")
    p.add_argument("--out-dir")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_manual_channel_prompts)

    p = sub.add_parser("import-manual-channel-results")
    p.add_argument("--input", required=True)
    p.add_argument("--research-topic", default="")
    p.add_argument("--prompt-or-query", default="")
    p.add_argument("--tool-used", default="manual", choices=["grok_expert", "browser", "tavily", "manual"])
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_import_manual_channel_results)

    p = sub.add_parser("validate-discovery-records")
    p.set_defaults(func=cmd_validate_discovery_records)

    p = sub.add_parser("apply-manual-channel-catalog")
    p.add_argument("--input")
    p.add_argument("--replace", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_apply_manual_channel_catalog)

    p = sub.add_parser("export-manual-channel-index")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_export_manual_channel_index)

    p = sub.add_parser("discover")
    p.add_argument("--sources", default="public_all", help="public_all/hackerone/bugcrowd/github/github_security_lab/blogs_x/newsletters or comma list")
    p.add_argument("--topic", default="")
    p.add_argument("--vuln-class", default="")
    p.add_argument("--from-date", default=DEFAULT_FROM_DATE)
    p.add_argument("--to-date", default=DEFAULT_TO_DATE)
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--run-dir")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_discover)

    p = sub.add_parser("cluster")
    p.add_argument("--input", required=True)
    p.add_argument("--run-dir")
    p.set_defaults(func=cmd_cluster)

    p = sub.add_parser("enrich")
    p.add_argument("--input", required=True)
    p.add_argument("--run-dir")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--max-output-tokens", type=int, default=9000)
    p.add_argument("--use-search", action="store_true", default=True)
    p.add_argument("--skip-tavily", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_enrich)

    p = sub.add_parser("apply")
    p.add_argument("--run-dir", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_apply)

    p = sub.add_parser("build-index")
    p.set_defaults(func=cmd_build_index)

    p = sub.add_parser("validate")
    p.set_defaults(func=cmd_validate)
    return ap


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
