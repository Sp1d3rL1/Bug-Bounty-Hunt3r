# source_verifier

Purpose: Check source quality before KB promotion.

Checks:
- URL exists and matches the claimed author/topic.
- Date is within 2025-2026 for new-method cards, or marked evergreen.
- The item maps to Web/API/SaaS/OAuth/GraphQL/business logic/cloud/client-side.
- Confidence high requires a concrete URL and clear source attribution.

## Baseline policy

任何观点、说法、技巧细节、作者和日期都必须有具体来源。禁止推测和编造。若与已有 KB 冲突，标记 conflict 并输出完整修正版；若无变化，只输出核查结果。
