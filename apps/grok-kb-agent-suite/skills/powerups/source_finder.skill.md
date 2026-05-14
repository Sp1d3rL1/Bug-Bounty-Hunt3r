# source_finder

Purpose: Discover 2025-2026 high-signal Bug Bounty sources from X and web.

Inputs:
- topic
- date window
- preferred target types

Rules:
- Prefer X posts/threads, disclosed reports, researcher blogs, platform newsletters, tool-author posts.
- Confidence is low if no source URL exists.
- Return compact JSON, not prose.
- Do not include instructions for non-authorized use.

Output fields:
`type, title, author, date, source_url, vuln_class, one_line_trick, why_useful, target_type, confidence, notes`

## Evidence baseline

- Every item must include concrete `source_url`, `source_urls`, and `evidence`.
- No source URL means confidence=low and notes must describe what is unverified.
- Do not infer dates/authors from memory; verify with search result metadata or source page.
