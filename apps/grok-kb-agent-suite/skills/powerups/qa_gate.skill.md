# qa_gate

Purpose: Block low-quality or unsafe KB updates.

Required checks:
- scripts/grok_kb_build_index.py passes
- scripts/grok_kb_validate.py passes
- no missing required technique headings
- no prohibited terms from validate script
- random sample source checks for large runs

## Evidence QA

- Check `verification_status` exists for API cards.
- `needs_review` cards must not be promoted as high confidence.
- `unchanged_verification_only` cards should not repeat full old content.
- Random source checks should prioritize low-confidence and conflict cards.
