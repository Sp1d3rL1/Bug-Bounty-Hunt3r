#!/usr/bin/env python3
"""Grok API batch agent for the Bug Bounty intelligence KB.

This replaces browser-driven Grok collection with API-first workflows:
- expand existing batch_XXX.prompt.md files into structured JSON cards
- discover new 2025-2026 X/Web intelligence items with x_search/web_search tools
- optionally submit many requests through the xAI Batch API
- apply structured card markdown into the Obsidian KB

No third-party Python packages are required.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROMPT_DIR = ROOT / "data/grok_research/prompts/2026-05-05/expansion_batches"
DEFAULT_RUNS_DIR = ROOT / "data/grok_api/runs"
DEFAULT_DISCOVERY_DIR = ROOT / "data/grok_api/discovery"
DEFAULT_API_BASE = os.getenv("XAI_API_BASE", "https://api.x.ai/v1").rstrip("/")
DEFAULT_MODEL = os.getenv("XAI_MODEL", "grok-4.3")
DEFAULT_TAVILY_API_BASE = os.getenv("TAVILY_API_BASE", "https://api.tavily.com").rstrip("/")
DEFAULT_TAVILY_SEARCH_DEPTH = os.getenv("TAVILY_SEARCH_DEPTH", "basic")
DEFAULT_TAVILY_EXTRACT_DEPTH = os.getenv("TAVILY_EXTRACT_DEPTH", "basic")
DEFAULT_TAVILY_CONTEXT_CHARS = int(os.getenv("TAVILY_CONTEXT_CHARS", "1200"))
DEFAULT_FROM_DATE = "2025-01-01"
DEFAULT_TO_DATE = dt.date.today().isoformat()
KB_START = "<!-- GROK_API_EXPANSION_START -->"
KB_END = "<!-- GROK_API_EXPANSION_END -->"
X_NETLOCS = {"x.com", "www.x.com", "twitter.com", "www.twitter.com", "mobile.twitter.com"}

BASELINE_EVIDENCE_POLICY = """Baseline evidence policy for every request:
- Every claim, viewpoint, technique detail, date, author attribution, and usefulness statement MUST have a concrete source URL.
- Do not speculate, infer beyond the source, invent authors/dates/URLs, or fill missing facts from memory.
- Verify search results against the supplied source_url and at least one source-backed search result when available.
- If evidence conflicts with the previously collected KB excerpt, output the complete corrected content and explain the conflict in conflict_notes.
- If evidence shows no substantive change from the existing KB excerpt, do not repeat the old card; return verification_status=unchanged_verification_only and a concise verification result.
- If a source cannot be verified, set confidence=low, verification_status=needs_review, and state exactly what could not be verified.
""".strip()

SYSTEM_PROMPT = """You are a careful Bug Bounty intelligence curator.
You only write for authorized bug bounty programs, labs, owned systems, synthetic data, and minimal-impact validation.
Preserve useful public research details, but do not produce instructions for credential stuffing, destructive actions, malware, production DoS, real third-party data extraction, or unauthorized access.
For high-risk classes, describe safe exposure triage, patch/remediation verification, and lab-first validation.
Prefer 2025-2026 sources and cite source URLs. Chinese Markdown body is preferred; keep source titles and URLs unchanged.

""".strip() + "\n\n" + BASELINE_EVIDENCE_POLICY

EXPANSION_USER_TEMPLATE = """Expand or verify the following Bug Bounty intelligence items into Obsidian KB card sections.

{baseline_policy}

Output must match the provided JSON schema exactly.
For every card:
- destination_path must equal the provided CARD_DEST exactly.
- type must be technique/case/resource.
- verification_status must be one of:
  - verified_full_update: sources verified and full card content is useful.
  - conflict_full_update: sources conflict with existing KB excerpt; output complete corrected content and conflict_notes.
  - unchanged_verification_only: sources match existing KB excerpt; markdown must only contain ## 核查结果, source list, and concise verification notes. Do not repeat old content.
  - needs_review: source cannot be verified or attribution/date is uncertain.
- Every non-obvious claim in markdown must be backed by evidence[] and source_urls.
- If an item contains tavily_context, treat it as independent web-source evidence:
  use it to verify URLs/snippets, mention conflicts, and never cite Tavily itself as a primary source when the original URL is available.
- Technique markdown for full updates must include these headings:
  ## 核心思路
  ## 前置条件
  ## 完整技法细节
  ## 适用目标画像
  ## 为什么有效
  ## 手工验证流程（授权 / Lab only）
  ## 可自动化部分
  ## 误报/失败条件
  ## 授权边界
  ## 报告 impact 角度
  ## 相关案例链接
- For case/resource cards, keep reproduction high-level and link-centric.
- Use neutral wording: authorized scope, Lab only, synthetic data, test accounts, test cards/sandbox, minimal-impact proof.
- Avoid browser/UI transcript artifacts. Do not include the prompt itself.

ITEMS_JSON:
{items_json}
""".strip()

DISCOVERY_USER_TEMPLATE = """Search X and the web for high-signal Bug Bounty intelligence from 2025-2026 about this topic:
{topic}

{baseline_policy}

Return compact, source-backed items useful for authorized Web/API/SaaS/OAuth/GraphQL/business-logic/cloud/client-side bug bounty work.
Prefer real hunter X posts/threads, disclosed reports, research blogs, platform newsletters, and tool author posts.
Avoid generic OWASP summaries. If a concrete source URL is missing, confidence must be low and notes must say what is unverified.
Each item must include source_urls and evidence explaining which source supports which claim.
Keep descriptions neutral and authorized-scope oriented.
Limit: {limit} items.
If TAVILY_WEB_CONTEXT_JSON is present below, use it only as independent source discovery/verification context; still cite the primary source URLs.
""".strip()

CARD_SCHEMA: dict[str, Any] = {
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
                    "destination_path", "type", "title", "vuln_class", "source_url",
                    "source_author", "source_date", "confidence", "risk_level",
                    "freshness", "target_types", "summary", "markdown", "source_urls",
                    "verification_status", "verification_summary", "conflict_notes", "evidence"
                ],
                "properties": {
                    "destination_path": {"type": "string"},
                    "type": {"type": "string", "enum": ["technique", "case", "resource"]},
                    "title": {"type": "string"},
                    "vuln_class": {"type": "string"},
                    "source_url": {"type": "string"},
                    "source_author": {"type": "string"},
                    "source_date": {"type": "string"},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                    "risk_level": {"type": "string", "enum": ["low", "medium", "high"]},
                    "freshness": {"type": "string"},
                    "target_types": {"type": "array", "items": {"type": "string"}},
                    "summary": {"type": "string"},
                    "markdown": {"type": "string"},
                    "source_urls": {"type": "array", "items": {"type": "string"}},
                    "verification_status": {
                        "type": "string",
                        "enum": ["verified_full_update", "conflict_full_update", "unchanged_verification_only", "needs_review"]
                    },
                    "verification_summary": {"type": "string"},
                    "conflict_notes": {"type": "string"},
                    "evidence": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["claim", "source_url", "verification_notes"],
                            "properties": {
                                "claim": {"type": "string"},
                                "source_url": {"type": "string"},
                                "verification_notes": {"type": "string"}
                            }
                        }
                    },
                },
            },
        }
    },
}

DISCOVERY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["items"],
    "properties": {
        "items": {
            "type": "array",
            "minItems": 1,
            "maxItems": 50,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "type", "title", "author", "date", "source_url", "vuln_class",
                    "one_line_trick", "why_useful", "target_type", "confidence", "notes",
                    "source_urls", "evidence"
                ],
                "properties": {
                    "type": {"type": "string", "enum": ["technique", "case", "resource"]},
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "date": {"type": "string"},
                    "source_url": {"type": "string"},
                    "vuln_class": {"type": "string"},
                    "one_line_trick": {"type": "string"},
                    "why_useful": {"type": "string"},
                    "target_type": {"type": "string"},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                    "notes": {"type": "string"},
                    "source_urls": {"type": "array", "items": {"type": "string"}},
                    "evidence": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["claim", "source_url", "verification_notes"],
                            "properties": {
                                "claim": {"type": "string"},
                                "source_url": {"type": "string"},
                                "verification_notes": {"type": "string"}
                            }
                        }
                    },
                },
            },
        }
    },
}


def now_run_id(prefix: str = "run") -> str:
    return f"{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}_{prefix}_{uuid.uuid4().hex[:8]}"


def require_api_key() -> str:
    key = os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
    if not key:
        raise SystemExit("Missing XAI_API_KEY or GROK_API_KEY in environment. Put it in your shell env; do not commit it.")
    return key


def require_tavily_key() -> str:
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        raise SystemExit("Missing TAVILY_API_KEY in environment. Put it in .env or shell env; do not commit it.")
    return key


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def safe_filename(s: str, max_len: int = 96) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s.strip())
    return s[:max_len].strip("._-") or "item"


def api_json(method: str, path: str, payload: Any | None = None, *, api_key: str | None = None,
             base_url: str = DEFAULT_API_BASE, headers_extra: dict[str, str] | None = None,
             timeout: int = 240, max_retries: int = 5) -> Any:
    api_key = api_key or require_api_key()
    url = f"{base_url}{path}"
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "bb-grok-api-agent/1.0",
    }
    if headers_extra:
        headers.update(headers_extra)
    for attempt in range(max_retries + 1):
        req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries:
                wait = min(90, (2 ** attempt) + random.random() * 2)
                print(f"[retry] {method} {path} -> HTTP {e.code}; wait {wait:.1f}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise RuntimeError(f"HTTP {e.code} calling {path}: {body[:2000]}") from e
        except urllib.error.URLError as e:
            if attempt < max_retries:
                wait = min(90, (2 ** attempt) + random.random() * 2)
                print(f"[retry] {method} {path} -> {e}; wait {wait:.1f}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise


def tavily_api_json(method: str, path: str, payload: Any | None = None, *, api_key: str | None = None,
                    base_url: str = DEFAULT_TAVILY_API_BASE, timeout: int = 90,
                    max_retries: int = 3) -> Any:
    """Call Tavily REST API with stdlib urllib.

    Tavily is used as an independent web-source verifier/context provider.
    It is intentionally not used for native X search; xAI x_search remains
    the primary source for X posts/threads.
    """
    api_key = api_key or require_tavily_key()
    url = f"{base_url.rstrip('/')}{path}"
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "bb-grok-api-agent-tavily/1.0",
    }
    for attempt in range(max_retries + 1):
        req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            if e.code in (408, 409, 425, 429, 500, 502, 503, 504) and attempt < max_retries:
                wait = min(60, (2 ** attempt) + random.random() * 2)
                print(f"[retry] tavily {method} {path} -> HTTP {e.code}; wait {wait:.1f}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise RuntimeError(f"Tavily HTTP {e.code} calling {path}: {body[:2000]}") from e
        except urllib.error.URLError as e:
            if attempt < max_retries:
                wait = min(60, (2 ** attempt) + random.random() * 2)
                print(f"[retry] tavily {method} {path} -> {e}; wait {wait:.1f}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise


def is_http_url(url: str) -> bool:
    try:
        p = urllib.parse.urlparse(url)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False


def is_x_url(url: str) -> bool:
    try:
        netloc = urllib.parse.urlparse(url).netloc.lower()
        return netloc in X_NETLOCS or netloc.endswith(".x.com") or netloc.endswith(".twitter.com")
    except Exception:
        return False


def unique_urls(urls: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in urls:
        u = str(raw or "").strip()
        if not is_http_url(u):
            continue
        key = u.rstrip("/")
        if key in seen:
            continue
        seen.add(key)
        out.append(u)
    return out


def sha16(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:16]


def compact_text(text: str, max_chars: int = DEFAULT_TAVILY_CONTEXT_CHARS) -> str:
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    return text[:max_chars]


def tavily_search(query: str, *, max_results: int = 5, search_depth: str = DEFAULT_TAVILY_SEARCH_DEPTH,
                  include_raw_content: bool | str = False, start_date: str | None = None,
                  end_date: str | None = None, include_domains: list[str] | None = None,
                  exclude_domains: list[str] | None = None, api_base: str = DEFAULT_TAVILY_API_BASE) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "query": query,
        "search_depth": search_depth,
        "max_results": max(0, min(int(max_results), 20)),
        "include_answer": False,
        "include_raw_content": include_raw_content,
        "include_favicon": True,
    }
    if start_date:
        payload["start_date"] = start_date
    if end_date:
        payload["end_date"] = end_date
    if include_domains:
        payload["include_domains"] = include_domains[:300]
    if exclude_domains:
        payload["exclude_domains"] = exclude_domains[:150]
    return tavily_api_json("POST", "/search", payload, base_url=api_base)


def tavily_extract(urls: list[str], *, query: str | None = None,
                   extract_depth: str = DEFAULT_TAVILY_EXTRACT_DEPTH,
                   chunks_per_source: int = 3, timeout_seconds: float = 20.0,
                   api_base: str = DEFAULT_TAVILY_API_BASE) -> dict[str, Any]:
    clean = unique_urls(urls)
    payload: dict[str, Any] = {
        "urls": clean,
        "extract_depth": extract_depth,
        "include_images": False,
        "include_favicon": True,
        "format": "markdown",
        "timeout": max(1.0, min(float(timeout_seconds), 60.0)),
        "include_usage": True,
    }
    if query:
        payload["query"] = query
        payload["chunks_per_source"] = max(1, min(int(chunks_per_source), 5))
    return tavily_api_json("POST", "/extract", payload, base_url=api_base)


def source_urls_from_card(card: dict[str, Any]) -> list[str]:
    urls = [card.get("source_url", "")]
    urls += list(card.get("source_urls") or [])
    for ev in card.get("evidence") or []:
        if isinstance(ev, dict):
            urls.append(ev.get("source_url", ""))
    return unique_urls([str(u) for u in urls])


def source_urls_from_item(item: dict[str, Any]) -> list[str]:
    urls = [item.get("source_url", "")]
    urls += list(item.get("source_urls") or [])
    return unique_urls([str(u) for u in urls])


def tavily_options_from_args(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "api_base": getattr(args, "tavily_api_base", DEFAULT_TAVILY_API_BASE),
        "search_depth": getattr(args, "tavily_search_depth", DEFAULT_TAVILY_SEARCH_DEPTH),
        "extract_depth": getattr(args, "tavily_extract_depth", DEFAULT_TAVILY_EXTRACT_DEPTH),
        "max_results": int(getattr(args, "tavily_max_results", 5)),
        "context_chars": int(getattr(args, "tavily_context_chars", DEFAULT_TAVILY_CONTEXT_CHARS)),
        "from_date": getattr(args, "from_date", DEFAULT_FROM_DATE),
        "to_date": getattr(args, "to_date", DEFAULT_TO_DATE),
    }


def tavily_context_for_item(item: dict[str, Any], options: dict[str, Any]) -> dict[str, Any]:
    """Return compact Tavily evidence context for a prompt item.

    Non-X URLs are extracted directly. X/Twitter URLs are left for xAI x_search,
    but Tavily may still supply web candidates by title when source_url is absent.
    """
    title = str(item.get("title") or "").strip()
    vuln = str(item.get("vuln_class") or "").strip()
    author_date = str(item.get("author_date") or item.get("author") or "").strip()
    query = " ".join(x for x in [title, vuln, author_date, "bug bounty"] if x).strip()
    urls = source_urls_from_item(item)
    web_urls = [u for u in urls if not is_x_url(u)]
    x_urls = [u for u in urls if is_x_url(u)]
    ctx: dict[str, Any] = {
        "provider": "tavily",
        "checked_at": dt.datetime.now().isoformat(),
        "query": query,
        "extracted": [],
        "search_candidates": [],
        "skipped_urls": [{"url": u, "reason": "x_native_grok_x_search_preferred"} for u in x_urls],
        "usage": {"credits": 0},
    }
    if web_urls:
        resp = tavily_extract(
            web_urls[:5], query=query or None, extract_depth=options["extract_depth"],
            chunks_per_source=3, api_base=options["api_base"],
        )
        ctx["raw_extract_request_id"] = resp.get("request_id")
        ctx["usage"]["credits"] += int((resp.get("usage") or {}).get("credits") or 0)
        for r in resp.get("results", []) or []:
            raw = str(r.get("raw_content") or "")
            ctx["extracted"].append({
                "url": r.get("url", ""),
                "raw_content_hash": sha16(raw),
                "raw_content_chars": len(raw),
                "snippet": compact_text(raw, options["context_chars"]),
                "favicon": r.get("favicon", ""),
            })
        for r in resp.get("failed_results", []) or []:
            ctx["skipped_urls"].append({"url": r.get("url", ""), "reason": "tavily_extract_failed", "error": r.get("error", "")})
    if not web_urls and query:
        resp = tavily_search(
            query, max_results=options["max_results"], search_depth=options["search_depth"],
            include_raw_content=False, start_date=options.get("from_date"), end_date=options.get("to_date"),
            api_base=options["api_base"],
        )
        ctx["raw_search_request_id"] = resp.get("request_id")
        ctx["usage"]["credits"] += int((resp.get("usage") or {}).get("credits") or 0)
        for r in resp.get("results", []) or []:
            ctx["search_candidates"].append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "score": r.get("score", ""),
                "content": compact_text(r.get("content", ""), options["context_chars"]),
            })
    return ctx


def tavily_context_for_discovery(topic: str, options: dict[str, Any]) -> dict[str, Any]:
    query = f"{topic} 2025 2026 bug bounty research disclosed report"
    resp = tavily_search(
        query, max_results=options["max_results"], search_depth=options["search_depth"],
        include_raw_content=False, start_date=options.get("from_date"), end_date=options.get("to_date"),
        api_base=options["api_base"],
    )
    return {
        "provider": "tavily",
        "checked_at": dt.datetime.now().isoformat(),
        "query": query,
        "request_id": resp.get("request_id"),
        "usage": resp.get("usage", {}),
        "results": [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "score": r.get("score", ""),
                "content": compact_text(r.get("content", ""), options["context_chars"]),
            }
            for r in (resp.get("results", []) or [])
        ],
    }


def response_text(resp: Any) -> str:
    """Extract final output_text from Responses API or nested batch result shapes."""
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        # OpenAI/xAI Responses API direct shape
        out = resp.get("output")
        if isinstance(out, list):
            chunks = []
            for item in out:
                if isinstance(item, dict) and item.get("type") == "message":
                    for c in item.get("content", []) or []:
                        if isinstance(c, dict) and c.get("type") in ("output_text", "text"):
                            chunks.append(c.get("text", ""))
                elif isinstance(item, dict):
                    txt = response_text(item)
                    if txt:
                        chunks.append(txt)
            if chunks:
                return "\n".join(chunks)
        # Chat completions direct or nested batch shape
        choices = resp.get("choices")
        if isinstance(choices, list) and choices:
            msg = choices[0].get("message", {}) if isinstance(choices[0], dict) else {}
            if isinstance(msg, dict) and isinstance(msg.get("content"), str):
                return msg["content"]
        # Batch result variants
        for key in ("responses", "chat_get_completion", "completion_response", "response", "batch_result"):
            if key in resp:
                txt = response_text(resp[key])
                if txt:
                    return txt
        # Last resort: find JSON-looking strings
        for v in resp.values():
            txt = response_text(v)
            if txt and ('"cards"' in txt or '"items"' in txt):
                return txt
    if isinstance(resp, list):
        for v in resp:
            txt = response_text(v)
            if txt:
                return txt
    return ""


def parse_json_text(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        for match in re.finditer(r"\{", text):
            try:
                obj, _ = decoder.raw_decode(text[match.start():])
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict) and ("cards" in obj or "items" in obj):
                return obj
        m = re.search(r"(\{[\s\S]*\})", text)
        if m:
            return json.loads(m.group(1))
        raise


def parse_prompt_items(prompt_path: Path) -> list[dict[str, str]]:
    text = prompt_path.read_text(errors="ignore")
    starts = [m.start() for m in re.finditer(r"^CARD_DEST:\s*", text, flags=re.M)]
    items = []
    for i, st in enumerate(starts):
        block = text[st: starts[i + 1] if i + 1 < len(starts) else len(text)]
        # Trim separator of previous/next item if present.
        block = re.split(r"\n---\s*\n", block)[0]
        item: dict[str, str] = {}
        for line in block.splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k = k.strip().lower()
            v = v.strip()
            if k in {
                "card_dest", "id", "type", "title", "author_date", "source_url", "vuln_class",
                "one_line_trick", "why_useful", "target_type", "confidence"
            }:
                item[k] = v
        if item.get("card_dest"):
            item.setdefault("type", "technique")
            items.append(item)
    return items


def kb_excerpt_for_destination(dest: str, max_chars: int = 1800) -> dict[str, str]:
    """Return a compact existing-card excerpt so Grok can verify conflicts/no-change."""
    p = Path(dest)
    if not p.is_absolute():
        p = ROOT / dest
    try:
        p = p.resolve()
    except Exception:
        return {"existing_kb_status": "invalid_path", "existing_kb_excerpt": "", "existing_kb_sha256": ""}
    if not str(p).startswith(str(ROOT.resolve())) or not p.exists():
        return {"existing_kb_status": "missing", "existing_kb_excerpt": "", "existing_kb_sha256": ""}
    text = p.read_text(errors="ignore")
    digest = hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:16]
    # Keep the parts most useful for conflict detection while controlling tokens.
    lines = []
    keep_prefixes = ("title:", "type:", "category:", "vuln_class:", "source_url:", "source_author:", "source_date:", "confidence:", "risk_level:", "freshness:")
    in_frontmatter = False
    for line in text.splitlines():
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            lines.append(line)
            continue
        if in_frontmatter and line.lower().startswith(keep_prefixes):
            lines.append(line)
        elif line.startswith("#") or line.startswith("## 核心思路") or line.startswith("## 相关案例链接") or line.startswith("## 授权边界"):
            lines.append(line)
        elif len("\n".join(lines)) < max_chars and any(k in line for k in ["source", "http", "作者", "日期", "核心", "授权"]):
            lines.append(line[:240])
        if len("\n".join(lines)) >= max_chars:
            break
    excerpt = "\n".join(lines).strip()[:max_chars]
    return {"existing_kb_status": "present", "existing_kb_excerpt": excerpt, "existing_kb_sha256": digest}


def optimized_expansion_prompt(prompt_path: Path, tavily_options: dict[str, Any] | None = None) -> str:
    items = parse_prompt_items(prompt_path)
    if not items:
        # Fallback to compacting original prompt rather than failing silently.
        raw = prompt_path.read_text(errors="ignore")
        return BASELINE_EVIDENCE_POLICY + "\n\n" + raw[:24000]
    enriched = []
    for item in items:
        copy = dict(item)
        copy.update(kb_excerpt_for_destination(copy.get("card_dest", "")))
        if tavily_options:
            try:
                copy["tavily_context"] = tavily_context_for_item(copy, tavily_options)
            except Exception as e:
                copy["tavily_context"] = {
                    "provider": "tavily",
                    "status": "error",
                    "error": str(e),
                    "note": "Tavily context failed; rely on xAI x_search/web_search and mark uncertain facts as needs_review.",
                }
        enriched.append(copy)
    return EXPANSION_USER_TEMPLATE.format(
        baseline_policy=BASELINE_EVIDENCE_POLICY,
        items_json=json.dumps(enriched, ensure_ascii=False, indent=2),
    )


def responses_request_body(prompt: str, *, model: str, schema: dict[str, Any], schema_name: str,
                           use_search: bool, x_search: bool, web_search: bool,
                           from_date: str, to_date: str, max_output_tokens: int | None = None) -> dict[str, Any]:
    tools: list[dict[str, Any]] = []
    if use_search and x_search:
        tools.append({"type": "x_search", "from_date": from_date, "to_date": to_date})
    if use_search and web_search:
        tools.append({"type": "web_search"})
    body: dict[str, Any] = {
        "model": model,
        "input": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "store": False,
        "text": {
            "format": {
                "type": "json_schema",
                "name": schema_name,
                "schema": schema,
                "strict": True,
            }
        },
    }
    if tools:
        body["tools"] = tools
    if max_output_tokens:
        body["max_output_tokens"] = max_output_tokens
    return body


def usage_line(request_id: str, resp: dict[str, Any]) -> str:
    usage = resp.get("usage", {}) if isinstance(resp, dict) else {}
    ticks = usage.get("cost_in_usd_ticks", "")
    cost = ""
    if isinstance(ticks, int):
        cost = f"{ticks / 1e10:.8f}"
    return "\t".join([
        request_id,
        str(usage.get("prompt_tokens", "")),
        str(usage.get("completion_tokens", "")),
        str(usage.get("total_tokens", "")),
        str(usage.get("num_sources_used", "")),
        str(ticks),
        cost,
    ])


def write_run_manifest(run_dir: Path, meta: dict[str, Any]) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "manifest.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_expand_prompts(args: argparse.Namespace) -> None:
    load_dotenv(ROOT / ".env")
    api_key = None if args.dry_run else require_api_key()
    prompt_dir = Path(args.prompt_dir)
    run_dir = Path(args.run_dir) if args.run_dir else DEFAULT_RUNS_DIR / now_run_id("expand")
    for sub in ("raw", "cards", "prompts"):
        (run_dir / sub).mkdir(parents=True, exist_ok=True)
    write_run_manifest(run_dir, {
        "mode": "expand-prompts", "model": args.model, "from_batch": args.from_batch,
        "to_batch": args.to_batch, "created_at": dt.datetime.now().isoformat(),
        "use_search": args.use_search, "x_search": args.x_search, "web_search": args.web_search,
        "tavily_preverify": bool(getattr(args, "tavily_preverify", False)),
    })
    usage_path = run_dir / "usage.tsv"
    usage_path.write_text("request_id\tprompt_tokens\tcompletion_tokens\ttotal_tokens\tnum_sources_used\tcost_ticks\tcost_usd\n", encoding="utf-8")
    for n in range(args.from_batch, args.to_batch + 1):
        bid = f"batch_{n:03d}"
        prompt_path = prompt_dir / f"{bid}.prompt.md"
        if not prompt_path.exists():
            print(f"[skip] missing {prompt_path}")
            continue
        tavily_options = tavily_options_from_args(args) if getattr(args, "tavily_preverify", False) and not args.dry_run else None
        prompt = optimized_expansion_prompt(prompt_path, tavily_options=tavily_options)
        (run_dir / "prompts" / f"{bid}.txt").write_text(prompt, encoding="utf-8")
        body = responses_request_body(
            prompt, model=args.model, schema=CARD_SCHEMA, schema_name="bug_bounty_kb_cards",
            use_search=args.use_search, x_search=args.x_search, web_search=args.web_search,
            from_date=args.from_date, to_date=args.to_date, max_output_tokens=args.max_output_tokens,
        )
        if args.dry_run:
            (run_dir / "raw" / f"{bid}.request.json").write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[dry-run] wrote request for {bid}")
            continue
        print(f"[api] expanding {bid} ...")
        resp = api_json("POST", "/responses", body, api_key=api_key, base_url=args.api_base, headers_extra={"x-grok-conv-id": args.cache_id})
        (run_dir / "raw" / f"{bid}.json").write_text(json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8")
        txt = response_text(resp)
        parsed = parse_json_text(txt)
        (run_dir / "cards" / f"{bid}.json").write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
        with usage_path.open("a", encoding="utf-8") as f:
            f.write(usage_line(bid, resp) + "\n")
        print(f"[ok] {bid}: cards={len(parsed.get('cards', []))}")
        if args.sleep:
            time.sleep(args.sleep)
    print(f"run_dir={run_dir}")


def cmd_discover(args: argparse.Namespace) -> None:
    load_dotenv(ROOT / ".env")
    api_key = None if args.dry_run else require_api_key()
    run_dir = Path(args.run_dir) if args.run_dir else DEFAULT_DISCOVERY_DIR / now_run_id("discover")
    run_dir.mkdir(parents=True, exist_ok=True)
    prompt = DISCOVERY_USER_TEMPLATE.format(topic=args.topic, limit=args.limit, baseline_policy=BASELINE_EVIDENCE_POLICY)
    if getattr(args, "tavily_context", False) and not args.dry_run:
        ctx = tavily_context_for_discovery(args.topic, tavily_options_from_args(args))
        (run_dir / "tavily_context.json").write_text(json.dumps(ctx, ensure_ascii=False, indent=2), encoding="utf-8")
        prompt += "\n\nTAVILY_WEB_CONTEXT_JSON:\n" + json.dumps(ctx, ensure_ascii=False, indent=2)
    body = responses_request_body(
        prompt, model=args.model, schema=DISCOVERY_SCHEMA, schema_name="bug_bounty_discovery_items",
        use_search=True, x_search=True, web_search=True, from_date=args.from_date, to_date=args.to_date,
        max_output_tokens=args.max_output_tokens,
    )
    (run_dir / "request.json").write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.dry_run:
        print(f"[dry-run] wrote {run_dir / 'request.json'}")
        return
    resp = api_json("POST", "/responses", body, api_key=api_key, base_url=args.api_base, headers_extra={"x-grok-conv-id": args.cache_id})
    (run_dir / "raw.json").write_text(json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8")
    parsed = parse_json_text(response_text(resp))
    (run_dir / "items.json").write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] discovered {len(parsed.get('items', []))} items in {run_dir}")


def cmd_apply_run(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir)
    cards_dir = run_dir / "cards"
    if not cards_dir.exists():
        raise SystemExit(f"No cards dir: {cards_dir}")
    count = 0
    for f in sorted(cards_dir.glob("*.json")):
        data = json.loads(f.read_text(errors="ignore"))
        for card in data.get("cards", []):
            dest_raw = card.get("destination_path") or ""
            if not dest_raw:
                continue
            dest = Path(dest_raw)
            if not dest.is_absolute():
                dest = ROOT / dest
            dest = dest.resolve()
            if not str(dest).startswith(str(ROOT.resolve())):
                print(f"[skip outside root] {dest}")
                continue
            md = sanitize_markdown(card.get("markdown", ""), card)
            md = append_verification_metadata(md, card)
            if not md.strip():
                continue
            old = dest.read_text(errors="ignore") if dest.exists() else ""
            status = card.get("verification_status", "verified_full_update")
            section_title = "Grok API 核查结果" if status == "unchanged_verification_only" else "Grok API 扩展补充"
            section = f"\n\n{KB_START}\n\n## {section_title}\n\n{md.strip()}\n\n{KB_END}\n"
            if KB_START in old and KB_END in old:
                new = re.sub(re.escape(KB_START) + r"[\s\S]*?" + re.escape(KB_END), section.strip(), old)
            else:
                new = old.rstrip() + section
            new = ensure_required_scaffold(new, card, dest)
            if args.dry_run:
                print(f"[dry-run] would update {dest}")
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(new, encoding="utf-8")
                print(f"[write] {dest}")
            count += 1
    print(f"applied_cards={count}")


def should_tavily_verify(card: dict[str, Any], mode: str) -> bool:
    status = str(card.get("verification_status") or "")
    confidence = str(card.get("confidence") or "").lower()
    urls = source_urls_from_card(card)
    if mode == "all":
        return True
    if mode == "needs_review":
        return status == "needs_review"
    if mode == "conflicts":
        return status == "conflict_full_update"
    if mode == "low_confidence":
        return confidence == "low"
    # default: spend Tavily credits only where it can reduce uncertainty.
    return status in {"needs_review", "conflict_full_update"} or confidence == "low" or not urls


def verify_card_with_tavily(card: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    options = tavily_options_from_args(args)
    title = str(card.get("title") or "").strip()
    vuln = str(card.get("vuln_class") or "").strip()
    query = " ".join(x for x in [title, vuln, "bug bounty source verification"] if x).strip()
    urls = source_urls_from_card(card)
    x_urls = [u for u in urls if is_x_url(u)]
    web_urls = [u for u in urls if not is_x_url(u)]
    verified: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    skipped = [{"url": u, "reason": "x_native_grok_x_search_preferred"} for u in x_urls]
    raw_requests: list[dict[str, Any]] = []
    credits = 0
    min_chars = int(getattr(args, "min_content_chars", 80))

    for i in range(0, len(web_urls), int(getattr(args, "max_urls_per_call", 5))):
        chunk = web_urls[i:i + int(getattr(args, "max_urls_per_call", 5))]
        if not chunk:
            continue
        try:
            resp = tavily_extract(
                chunk, query=query or None, extract_depth=options["extract_depth"],
                chunks_per_source=3, api_base=options["api_base"],
            )
            raw_requests.append({"type": "extract", "urls": chunk, "request_id": resp.get("request_id")})
            credits += int((resp.get("usage") or {}).get("credits") or 0)
            for r in resp.get("results", []) or []:
                raw = str(r.get("raw_content") or "")
                entry = {
                    "url": r.get("url", ""),
                    "raw_content_chars": len(raw),
                    "raw_content_hash": sha16(raw),
                    "snippet": compact_text(raw, options["context_chars"]),
                    "favicon": r.get("favicon", ""),
                }
                if len(raw) >= min_chars:
                    verified.append(entry)
                else:
                    entry["reason"] = "content_too_short"
                    failed.append(entry)
            for r in resp.get("failed_results", []) or []:
                failed.append({"url": r.get("url", ""), "reason": "tavily_extract_failed", "error": r.get("error", "")})
        except Exception as e:
            for u in chunk:
                failed.append({"url": u, "reason": "tavily_extract_exception", "error": str(e)})

    search_candidates: list[dict[str, Any]] = []
    if (not urls or getattr(args, "search_missing", False)) and query:
        try:
            resp = tavily_search(
                query, max_results=options["max_results"], search_depth=options["search_depth"],
                include_raw_content=False, start_date=options.get("from_date"), end_date=options.get("to_date"),
                api_base=options["api_base"],
            )
            raw_requests.append({"type": "search", "query": query, "request_id": resp.get("request_id")})
            credits += int((resp.get("usage") or {}).get("credits") or 0)
            for r in resp.get("results", []) or []:
                search_candidates.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "score": r.get("score", ""),
                    "content": compact_text(r.get("content", ""), options["context_chars"]),
                })
        except Exception as e:
            failed.append({"url": "", "reason": "tavily_search_exception", "error": str(e)})

    if verified and not failed:
        status = "verified_extractable"
    elif verified and failed:
        status = "partial"
    elif search_candidates and not urls:
        status = "source_candidates_found"
    elif skipped and not web_urls:
        status = "skipped_x_native_preferred"
    else:
        status = "needs_review"

    return {
        "provider": "tavily",
        "checked_at": dt.datetime.now().isoformat(),
        "mode": getattr(args, "mode", "default"),
        "status": status,
        "summary": f"verified_urls={len(verified)} failed_urls={len(failed)} skipped_urls={len(skipped)} search_candidates={len(search_candidates)}",
        "query": query,
        "usage": {"credits": credits},
        "verified_urls": verified,
        "failed_urls": failed,
        "skipped_urls": skipped,
        "search_candidates": search_candidates,
        "raw_requests": raw_requests,
        "note": "Tavily verifies extractability and supplies source snippets for web URLs. X/Twitter URLs remain better verified through xAI x_search or direct browser review.",
    }


def cmd_tavily_verify_run(args: argparse.Namespace) -> None:
    load_dotenv(ROOT / ".env")
    if not args.dry_run:
        require_tavily_key()
    run_dir = Path(args.run_dir)
    cards_dir = run_dir / "cards"
    if not cards_dir.exists():
        raise SystemExit(f"No cards dir: {cards_dir}")
    out_dir = run_dir / "tavily_verification"
    raw_dir = out_dir / "cards"
    raw_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "report.tsv"
    rows = ["file\tcard_title\tmode\tstatus\tconfidence\tverified_urls\tfailed_urls\tskipped_urls\tsearch_candidates\tcredits\n"]
    checked = skipped_count = 0
    for f in sorted(cards_dir.glob("*.json")):
        data = json.loads(f.read_text(errors="ignore"))
        changed = False
        out_cards: list[dict[str, Any]] = []
        for card in data.get("cards", []):
            if not should_tavily_verify(card, args.mode):
                skipped_count += 1
                continue
            if args.dry_run:
                tv = {
                    "provider": "tavily",
                    "status": "dry_run_would_verify",
                    "summary": "No API call made.",
                    "source_urls": source_urls_from_card(card),
                }
            else:
                tv = verify_card_with_tavily(card, args)
            card["tavily_verification"] = tv
            changed = True
            checked += 1
            out_cards.append(card)
            rows.append("\t".join([
                f.name,
                str(card.get("title", "")).replace("\t", " "),
                str(args.mode),
                str(tv.get("status", "")),
                str(card.get("confidence", "")),
                str(len(tv.get("verified_urls") or [])),
                str(len(tv.get("failed_urls") or [])),
                str(len(tv.get("skipped_urls") or [])),
                str(len(tv.get("search_candidates") or [])),
                str((tv.get("usage") or {}).get("credits", "")),
            ]) + "\n")
        if changed:
            (raw_dir / f.name).write_text(json.dumps({"cards": out_cards}, ensure_ascii=False, indent=2), encoding="utf-8")
            if args.write_back and not args.dry_run:
                f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"[write-back] {f}")
            else:
                print(f"[write] {raw_dir / f.name}")
    report_path.write_text("".join(rows), encoding="utf-8")
    print(f"tavily_checked={checked} skipped={skipped_count} report={report_path}")


def append_verification_metadata(text: str, card: dict[str, Any] | None = None) -> str:
    if not card:
        return text
    lines = [text.rstrip()]
    status = card.get("verification_status")
    summary = card.get("verification_summary")
    conflict = card.get("conflict_notes")
    evidence = card.get("evidence") or []
    urls = card.get("source_urls") or []
    tavily = card.get("tavily_verification") or {}
    if status or summary or conflict or evidence or urls or tavily:
        lines.append("\n## Evidence / 核查元数据")
    if status:
        lines.append(f"- verification_status: `{status}`")
    if summary:
        lines.append(f"- verification_summary: {summary}")
    if conflict:
        lines.append(f"- conflict_notes: {conflict}")
    if urls:
        lines.append("- source_urls:")
        for u in urls:
            lines.append(f"  - {u}")
    if evidence:
        lines.append("- evidence:")
        for ev in evidence:
            claim = str(ev.get("claim", "")).strip()
            url = str(ev.get("source_url", "")).strip()
            note = str(ev.get("verification_notes", "")).strip()
            lines.append(f"  - claim: {claim}")
            if url:
                lines.append(f"    source: {url}")
            if note:
                lines.append(f"    verification: {note}")
    if isinstance(tavily, dict) and tavily:
        lines.append("- tavily_verification:")
        for key in ("status", "summary", "checked_at", "mode"):
            if tavily.get(key):
                lines.append(f"  - {key}: {tavily.get(key)}")
        usage = tavily.get("usage") or {}
        if usage:
            lines.append(f"  - usage: {usage}")
        verified = tavily.get("verified_urls") or []
        failed = tavily.get("failed_urls") or []
        skipped = tavily.get("skipped_urls") or []
        if verified:
            lines.append("  - verified_urls:")
            for item in verified[:10]:
                lines.append(f"    - {item.get('url', '')} (chars={item.get('raw_content_chars', '')}, hash={item.get('raw_content_hash', '')})")
        if failed:
            lines.append("  - failed_urls:")
            for item in failed[:10]:
                lines.append(f"    - {item.get('url', '')} ({item.get('reason', '')})")
        if skipped:
            lines.append("  - skipped_urls:")
            for item in skipped[:10]:
                lines.append(f"    - {item.get('url', '')} ({item.get('reason', '')})")
    return "\n".join(lines).strip() + "\n"


def sanitize_markdown(text: str, card: dict[str, Any] | None = None) -> str:
    replacements = [
        (r"credential stuffing", "认证速率限制验证（授权 / Lab only）"),
        (r"DDoS|DoS", "可用性影响风险（仅 Lab/限速验证）"),
        (r"exfil(?:trate|tration)?", "验证暴露风险（不导出真实敏感数据）"),
        (r"attacker-controlled", "tester-controlled"),
        (r"malware", "恶意代码风险样本（不执行）"),
        (r"destructive", "有破坏性风险的"),
        (r"real third-party data", "真实第三方数据"),
        (r"WAF bypass", "WAF rule-difference validation"),
        (r"payload", "测试载荷"),
    ]
    for pat, repl in replacements:
        text = re.sub(pat, repl, text, flags=re.I)
    guard = "> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。"
    if "安全边界" not in text and "授权边界" not in text:
        text = text.rstrip() + "\n\n" + guard + "\n"
    return text


def yaml_quote(value: Any) -> str:
    return json.dumps(str(value or ""), ensure_ascii=False)


def card_doc_kind(card: dict[str, Any], dest: Path) -> str:
    parts = {p.lower() for p in dest.parts}
    if "cases" in parts or str(card.get("type") or "").lower() == "case":
        return "case"
    return "technique"


def card_scaffold(card: dict[str, Any], dest: Path) -> str:
    """Create the stable KB scaffold required by validators for new API cards."""
    kind = card_doc_kind(card, dest)
    title = str(card.get("title") or dest.stem)
    source_url = str(card.get("source_url") or "")
    source_author = str(card.get("source_author") or "unknown")
    source_date = str(card.get("source_date") or "unknown")
    confidence = str(card.get("confidence") or "medium")
    risk_level = str(card.get("risk_level") or "medium")
    vuln_class = str(card.get("vuln_class") or "unknown")
    freshness = str(card.get("freshness") or "2025-2026")
    summary = str(card.get("summary") or "见下方 Grok API 扩展补充与 Evidence。")
    target_types = card.get("target_types") or []
    if not isinstance(target_types, list):
        target_types = [str(target_types)]
    target_text = "、".join(str(x) for x in target_types if str(x).strip()) or "Web/API/SaaS"
    fm_type = "case" if kind == "case" else "technique"
    fm_lines = [
        "---",
        f"type: {fm_type}",
        f"title: {yaml_quote(title)}",
        f"vuln_class: {yaml_quote(vuln_class)}",
        f"source_url: {yaml_quote(source_url)}",
        f"source_author: {yaml_quote(source_author)}",
        f"source_date: {yaml_quote(source_date)}",
        f"confidence: {yaml_quote(confidence)}",
        f"risk_level: {yaml_quote(risk_level)}",
        f"freshness: {yaml_quote(freshness)}",
        "target_types:",
    ]
    for tt in target_types or ["Web/API/SaaS"]:
        fm_lines.append(f"  - {yaml_quote(tt)}")
    fm_lines.append("---")
    if kind == "case":
        body = f"""# {title}

## 链接
- {source_url or "来源待复核"}

## 漏洞类型
{vuln_class}

## 目标业务场景
{target_text}

## 关键利用链摘要
{summary}

## 可迁移技法
仅迁移到授权项目、靶场或自有环境；优先提炼前置条件、权限边界、状态机或集成点，不复现真实第三方目标。

## 为什么值得收藏
用于学习公开案例的根因、impact 表达、报告结构与授权范围内的验证思路。
"""
    else:
        body = f"""# {title}

## 核心思路
{summary}

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
{target_text}

## 为什么有效
围绕 {vuln_class} 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

## 手工验证流程
在授权范围内以只读或最小影响方式验证：确认前置条件、构造合成数据/测试账号、观察授权边界或状态差异、记录证据并停止在安全影响证明处。

## 可自动化部分
可自动化收集公开入口、参数、JS/API schema、配置差异和变更信号；实际漏洞确认保留人工复核。

## 误报/失败条件
目标无对应功能、权限模型不同、补丁已生效、测试账号权限不足、来源无法复核或影响无法用最小证明表达。

## 授权边界
不访问非授权目标；不导出真实敏感数据；不进行破坏性、DoS、爆破、认证批量尝试或真实支付损害测试。

## 报告 impact 角度
说明可影响的资产、权限边界、业务状态、数据类别、可复现前置条件和最小影响证据。

## 相关案例链接
- {source_url or "来源待复核"}
"""
    return "\n".join(fm_lines) + "\n\n" + body.strip() + "\n\n"


def ensure_required_scaffold(text: str, card: dict[str, Any], dest: Path) -> str:
    marker = "<!-- GROK_API_SCAFFOLD_START -->"
    if marker in text:
        return text
    kind = card_doc_kind(card, dest)
    required = [
        "source_url:", "source_author:", "source_date:",
        "## 链接", "## 关键利用链摘要", "## 可迁移技法",
    ] if kind == "case" else [
        "source_url:", "source_author:", "source_date:", "confidence:", "risk_level:",
        "## 核心思路", "## 前置条件", "## 完整技法细节", "## 手工验证流程",
        "## 授权边界", "## 报告 impact 角度",
    ]
    low = text.lower()
    if all(x.lower() in low for x in required):
        return text
    scaffold = f"{marker}\n{card_scaffold(card, dest).rstrip()}\n<!-- GROK_API_SCAFFOLD_END -->\n\n"
    return scaffold + text.lstrip()


def make_batch_requests(args: argparse.Namespace) -> list[dict[str, Any]]:
    prompt_dir = Path(args.prompt_dir)
    reqs = []
    tavily_options = tavily_options_from_args(args) if getattr(args, "tavily_preverify", False) and not args.dry_run else None
    for n in range(args.from_batch, args.to_batch + 1):
        bid = f"batch_{n:03d}"
        prompt_path = prompt_dir / f"{bid}.prompt.md"
        if not prompt_path.exists():
            print(f"[skip] missing {prompt_path}")
            continue
        prompt = optimized_expansion_prompt(prompt_path, tavily_options=tavily_options)
        body = responses_request_body(
            prompt, model=args.model, schema=CARD_SCHEMA, schema_name="bug_bounty_kb_cards",
            use_search=args.use_search, x_search=args.x_search, web_search=args.web_search,
            from_date=args.from_date, to_date=args.to_date, max_output_tokens=args.max_output_tokens,
        )
        reqs.append({"batch_request_id": bid, "batch_request": {"responses": body}})
    return reqs


def cmd_batch_submit(args: argparse.Namespace) -> None:
    load_dotenv(ROOT / ".env")
    api_key = None if args.dry_run else require_api_key()
    run_dir = Path(args.run_dir) if args.run_dir else DEFAULT_RUNS_DIR / now_run_id("xai_batch")
    run_dir.mkdir(parents=True, exist_ok=True)
    reqs = make_batch_requests(args)
    (run_dir / "batch_requests.json").write_text(json.dumps({"batch_requests": reqs}, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.dry_run:
        print(f"[dry-run] wrote {run_dir / 'batch_requests.json'} requests={len(reqs)}")
        return
    batch = api_json("POST", "/batches", {"name": args.name or f"bb_kb_{now_run_id('batch')}"}, api_key=api_key, base_url=args.api_base)
    batch_id = batch.get("batch_id") or batch.get("id")
    if not batch_id:
        raise RuntimeError(f"Cannot find batch id in response: {batch}")
    add = api_json("POST", f"/batches/{batch_id}/requests", {"batch_requests": reqs}, api_key=api_key, base_url=args.api_base)
    meta = {"batch": batch, "add_response": add, "batch_id": batch_id, "request_count": len(reqs), "created_at": dt.datetime.now().isoformat()}
    write_run_manifest(run_dir, meta)
    print(f"batch_id={batch_id}\nrun_dir={run_dir}\nrequests={len(reqs)}")


def cmd_batch_status(args: argparse.Namespace) -> None:
    load_dotenv(ROOT / ".env")
    resp = api_json("GET", f"/batches/{args.batch_id}", base_url=args.api_base)
    print(json.dumps(resp, ensure_ascii=False, indent=2))


def cmd_batch_fetch(args: argparse.Namespace) -> None:
    load_dotenv(ROOT / ".env")
    run_dir = Path(args.run_dir)
    (run_dir / "raw").mkdir(parents=True, exist_ok=True)
    (run_dir / "cards").mkdir(parents=True, exist_ok=True)
    token = None
    success = fail = 0
    while True:
        q = f"limit={args.limit}"
        if token:
            q += "&pagination_token=" + urllib.parse.quote(token)
        page = api_json("GET", f"/batches/{args.batch_id}/results?{q}", base_url=args.api_base)
        (run_dir / "raw" / f"results_{len(list((run_dir / 'raw').glob('results_*.json'))):03d}.json").write_text(
            json.dumps(page, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        for result in page.get("results", []):
            rid = result.get("batch_request_id") or result.get("custom_id") or safe_filename(hashlib.sha1(json.dumps(result, sort_keys=True).encode()).hexdigest()[:12])
            txt = response_text(result)
            if not txt:
                fail += 1
                (run_dir / "raw" / f"{rid}.error.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
                continue
            try:
                parsed = parse_json_text(txt)
                (run_dir / "cards" / f"{rid}.json").write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
                success += 1
            except Exception as e:
                fail += 1
                (run_dir / "raw" / f"{rid}.parse_error.txt").write_text(str(e) + "\n\n" + txt, encoding="utf-8")
        token = page.get("pagination_token")
        if not token:
            break
    print(f"fetched success={success} fail={fail} run_dir={run_dir}")


def cmd_list_missing(args: argparse.Namespace) -> None:
    prompt_dir = Path(args.prompt_dir)
    expanded_dir = Path(args.expanded_dir)
    missing = []
    for p in sorted(prompt_dir.glob("batch_*.prompt.md")):
        m = re.search(r"batch_(\d+)\.prompt\.md$", p.name)
        if not m:
            continue
        out = expanded_dir / f"batch_{m.group(1)}.md"
        api_out = Path(args.api_run_dir) / "cards" / f"batch_{m.group(1)}.json" if args.api_run_dir else None
        if not out.exists() and not (api_out and api_out.exists()):
            missing.append(int(m.group(1)))
    print("missing_batches=" + ",".join(f"{x:03d}" for x in missing))



def slugify(text: str, max_len: int = 80) -> str:
    text = text.lower().strip()
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return (text[:max_len].strip("-") or "item")


def category_dir_for(item: dict[str, Any], default_category: str) -> tuple[str, str]:
    typ = item.get("type", "technique")
    vc = (item.get("vuln_class") or "").lower()
    title = (item.get("title") or "").lower()
    if typ == "case":
        return "cases", "researcher_writeups"
    if typ == "resource":
        return "techniques", "niche_tricks"
    if "old" in title or "evergreen" in title:
        return "techniques", "evergreen_new_context"
    if any(x in vc for x in ["trick", "recon", "disclosure"]):
        return "techniques", default_category
    return "techniques", default_category


def cmd_make_prompts_from_discovery(args: argparse.Namespace) -> None:
    data = json.loads(Path(args.items_json).read_text(errors="ignore"))
    items = data.get("items", data if isinstance(data, list) else [])
    if not isinstance(items, list) or not items:
        raise SystemExit("No discovery items found. Expected {'items':[...]} or a JSON array.")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    batch_no = args.start_batch
    for offset in range(0, len(items), args.batch_size):
        chunk = items[offset:offset + args.batch_size]
        lines = [
            "Use Expert mode. Expand the following 5 Bug Bounty intelligence items into detailed Obsidian Markdown cards. Search X/web if needed to verify the source and fill missing details.",
            "",
            "Important rules:",
            "- Authorized bug bounty / lab / owned environments only.",
            "- Use synthetic data, test accounts, sandbox/test cards, and minimal-impact proof.",
            "- For high-risk classes, write safe lab-first validation and risk boundary.",
            "- Case-only items: keep as link + detailed description + transferable lessons, not real-target reproduction steps.",
            "- Chinese body text is preferred; keep source titles/URLs unchanged.",
            "",
            "ITEMS:",
        ]
        for idx, item in enumerate(chunk, start=1):
            title = str(item.get("title") or f"item-{batch_no}-{idx}")
            typ = str(item.get("type") or "technique")
            root_name, cat = category_dir_for(item, args.category)
            slug = slugify(title)
            if root_name == "cases":
                dest = ROOT / "docs/intelligence_kb" / root_name / cat / f"{batch_no}-{idx}-{slug}.md"
            else:
                dest = ROOT / "docs/intelligence_kb" / root_name / cat / f"{batch_no}-{idx}-{slug}.md"
            author = str(item.get("author") or item.get("source_author") or "unknown")
            date = str(item.get("date") or item.get("source_date") or "2025-2026")
            source_url = str(item.get("source_url") or "")
            vuln_class = str(item.get("vuln_class") or "Unknown")
            one = str(item.get("one_line_trick") or item.get("summary") or "")
            useful = str(item.get("why_useful") or item.get("notes") or "")
            target = str(item.get("target_type") or ", ".join(item.get("target_types", [])) or "Web/API")
            confidence = str(item.get("confidence") or "medium")
            lines += [
                f"CARD_DEST: {dest}",
                f"ID: {batch_no}-{idx}",
                f"TYPE: {typ}",
                f"TITLE: {title}",
                f"AUTHOR_DATE: {author} / {date}",
                f"SOURCE_URL: {source_url}",
                f"VULN_CLASS: {vuln_class}",
                f"ONE_LINE_TRICK: {one}",
                f"WHY_USEFUL: {useful}",
                f"TARGET_TYPE: {target}",
                f"CONFIDENCE: {confidence}",
                "",
                "---",
                "",
            ]
            rows.append([typ, title, author, date, source_url, vuln_class, one, useful, target, confidence, str(dest)])
        path = out_dir / f"batch_{batch_no:03d}.prompt.md"
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        print(f"[write] {path} items={len(chunk)}")
        batch_no += 1
    if args.ledger_out:
        ledger = Path(args.ledger_out)
        ledger.parent.mkdir(parents=True, exist_ok=True)
        header = "type\ttitle\tauthor\tdate\tsource_url\tvuln_class\tone_line_trick\twhy_useful\ttarget_type\tconfidence\tdestination_path\n"
        with ledger.open("w", encoding="utf-8") as f:
            f.write(header)
            for row in rows:
                f.write("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in row) + "\n")
        print(f"[write] {ledger} rows={len(rows)}")


def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Grok API agent for Bug Bounty intelligence KB")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--api-base", default=DEFAULT_API_BASE)
    ap.add_argument("--tavily-api-base", default=DEFAULT_TAVILY_API_BASE)
    ap.add_argument("--cache-id", default=os.getenv("XAI_CACHE_CONV_ID", "4f3b4c46-5fd2-48fd-ae51-0bb000000001"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common_tavily(p: argparse.ArgumentParser) -> None:
        p.add_argument("--tavily-api-base", default=DEFAULT_TAVILY_API_BASE)
        p.add_argument("--tavily-search-depth", choices=["basic", "advanced"], default=DEFAULT_TAVILY_SEARCH_DEPTH)
        p.add_argument("--tavily-extract-depth", choices=["basic", "advanced"], default=DEFAULT_TAVILY_EXTRACT_DEPTH)
        p.add_argument("--tavily-max-results", type=int, default=5)
        p.add_argument("--tavily-context-chars", type=int, default=DEFAULT_TAVILY_CONTEXT_CHARS)

    def common_expand(p: argparse.ArgumentParser) -> None:
        p.add_argument("--prompt-dir", default=str(DEFAULT_PROMPT_DIR))
        p.add_argument("--from-batch", type=int, required=True)
        p.add_argument("--to-batch", type=int, required=True)
        p.add_argument("--from-date", default=DEFAULT_FROM_DATE)
        p.add_argument("--to-date", default=DEFAULT_TO_DATE)
        p.add_argument("--max-output-tokens", type=int, default=7000)
        p.add_argument("--use-search", action="store_true", help="Enable server-side X/Web search tools")
        p.add_argument("--x-search", action=argparse.BooleanOptionalAction, default=True)
        p.add_argument("--web-search", action=argparse.BooleanOptionalAction, default=True)
        p.add_argument("--tavily-preverify", action="store_true", help="Pre-fetch compact Tavily Extract/Search context for prompt items before calling Grok")
        p.add_argument("--dry-run", action="store_true")
        common_tavily(p)

    p = sub.add_parser("expand-prompts")
    common_expand(p)
    p.add_argument("--run-dir")
    p.add_argument("--sleep", type=float, default=0)
    p.set_defaults(func=cmd_expand_prompts)

    p = sub.add_parser("discover-topic")
    p.add_argument("--topic", required=True)
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--from-date", default=DEFAULT_FROM_DATE)
    p.add_argument("--to-date", default=DEFAULT_TO_DATE)
    p.add_argument("--max-output-tokens", type=int, default=5000)
    p.add_argument("--tavily-context", action="store_true", help="Attach compact Tavily web-search context before Grok discovery")
    p.add_argument("--run-dir")
    p.add_argument("--dry-run", action="store_true")
    common_tavily(p)
    p.set_defaults(func=cmd_discover)

    p = sub.add_parser("apply-run")
    p.add_argument("--run-dir", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_apply_run)

    p = sub.add_parser("batch-submit-prompts")
    common_expand(p)
    p.add_argument("--run-dir")
    p.add_argument("--name")
    p.set_defaults(func=cmd_batch_submit)

    p = sub.add_parser("batch-status")
    p.add_argument("--batch-id", required=True)
    p.set_defaults(func=cmd_batch_status)

    p = sub.add_parser("batch-fetch")
    p.add_argument("--batch-id", required=True)
    p.add_argument("--run-dir", required=True)
    p.add_argument("--limit", type=int, default=100)
    p.set_defaults(func=cmd_batch_fetch)

    p = sub.add_parser("list-missing")
    p.add_argument("--prompt-dir", default=str(DEFAULT_PROMPT_DIR))
    p.add_argument("--expanded-dir", default="data/grok_research/expanded/2026-05-05")
    p.add_argument("--api-run-dir")
    p.set_defaults(func=cmd_list_missing)

    p = sub.add_parser("tavily-verify-run")
    p.add_argument("--run-dir", required=True)
    p.add_argument("--mode", choices=["default", "all", "needs_review", "conflicts", "low_confidence"], default="default")
    p.add_argument("--write-back", action="store_true", help="Attach tavily_verification to cards/*.json so apply-run includes it")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--search-missing", action="store_true", help="Run Tavily Search even when source URLs exist, useful for finding alternates")
    p.add_argument("--max-urls-per-call", type=int, default=5)
    p.add_argument("--min-content-chars", type=int, default=80)
    p.add_argument("--from-date", default=DEFAULT_FROM_DATE)
    p.add_argument("--to-date", default=DEFAULT_TO_DATE)
    common_tavily(p)
    p.set_defaults(func=cmd_tavily_verify_run)

    p = sub.add_parser("make-prompts-from-discovery")
    p.add_argument("--items-json", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--start-batch", type=int, default=61)
    p.add_argument("--batch-size", type=int, default=5)
    p.add_argument("--category", default="new_2024_2026")
    p.add_argument("--ledger-out")
    p.set_defaults(func=cmd_make_prompts_from_discovery)
    return ap


def main() -> None:
    ap = build_arg_parser()
    args = ap.parse_args()
    # Propagate global model/cache/base into subcommand args when argparse namespaces shadow not.
    if not hasattr(args, "model") or args.model is None:
        args.model = DEFAULT_MODEL
    args.func(args)


if __name__ == "__main__":
    main()
