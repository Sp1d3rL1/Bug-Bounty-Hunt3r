# prompt_compressor

Purpose: Convert verbose batch prompt files into compact API input.

Rules:
- Parse only CARD_DEST, ID, TYPE, TITLE, AUTHOR_DATE, SOURCE_URL, VULN_CLASS, ONE_LINE_TRICK, WHY_USEFUL, TARGET_TYPE, CONFIDENCE.
- Remove browser/DOM artifacts.
- Rewrite high-risk wording into neutral authorized-scope language.
- Keep useful technical specificity.
