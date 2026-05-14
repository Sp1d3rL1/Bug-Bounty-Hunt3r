# Vulnerability Report Template (English)

> Bilingual / 双语：通用模板，兼容 HackerOne / Bugcrowd / Intigriti / YesWeHack 提交字段并集。
> Web3 用 `web3_immunefi_template.md`，AI/LLM 用 `ai_llm_template.md`，国内 SRC 用 `cn_src_template.md`。

---

## Title

`[Vulnerability class] in [affected feature] allows [attacker role] to [impact]`

Examples:
- `IDOR in /api/v2/invoices/{id} allows workspace member to download cross-tenant invoices`
- `OAuth redirect_uri loose-match in /authorize allows attacker to steal authorization codes via callback/../`

## Metadata

| Field | Value |
|---|---|
| Program | <H1/Bugcrowd/Intigriti/YesWeHack 上的 program 名称> |
| Asset (in scope) | <从 program 资产列表中复制的精确 URL/范围> |
| Weakness / CWE | CWE-XXX (e.g. CWE-639 Authorization Bypass Through User-Controlled Key) |
| CVSS 3.1 vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` (score: X.X) |
| CVSS 4.0 vector (optional) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N` (score: X.X) |
| Bugcrowd VRT | P1 / P2 / P3 / P4 / P5 |
| Disclosure preference | 30-day / 90-day / 180-day / Last Resort |
| Human-validated | ✅ Yes — I personally reproduced this; AI assisted only with summarisation. |

## Summary

3-5 sentences:
1. What feature is affected
2. Who can exploit it (attacker role / required prerequisites)
3. What the vulnerable action does
4. Business / security impact

## Scope and Authorization

- Program / Bug Bounty page URL:
- Asset (verbatim from in-scope list):
- Tested account(s): A = `tester-a@example.com`, B = `tester-b@example.com` (both registered by me)
- Reproducer Account access: <提供给 triager 时的注释，例如 "Both accounts use the same test card 4242…">
- Date / time tested:
- Confirmation that testing stayed within scope: ✅
- Confirmation that no real user data was accessed: ✅

## Steps to Reproduce

1. Sign in as Account A.
2. Create / use resource X.
3. Sign in as Account B in a separate browser profile.
4. Send the request below from Account B (substituting Account A's resource ID).
5. Observe the response — Account B receives Account A's data.

## Proof of Concept

### HTTP Request

```http
GET /api/v2/invoices/<A_INVOICE_ID> HTTP/2
Host: target.example.com
Authorization: Bearer <B_TOKEN_REDACTED>
Cookie: session=<REDACTED>
Accept: application/json
```

### Expected Response

```http
HTTP/2 403 Forbidden
{"error":"forbidden"}
```

### Actual Response

```http
HTTP/2 200 OK
Content-Type: application/json
{
  "invoice_id": "<A_INVOICE_ID>",
  "owner_id": "<A_USER_ID>",
  "amount_cents": 12345,
  ...
}
```

## Impact

- **Confidentiality**: <e.g. "Any workspace member can read all other members' invoice metadata: amount, vendor, paid date.">
- **Integrity**: <e.g. "PUT method on the same path also lacks authorization (verified)." or "N/A">
- **Availability**: <e.g. "N/A">
- **Financial / compliance**:
  - Affected resource count: <估算行数 - "≈ 50,000 invoices across 3,000 tenants in this region">
  - Direct fraud / refund loss: <如适用>
  - GDPR / SOC2 / PCI 触及面: <如适用>

## Evidence

> 全部脱敏：token / cookie / email / 真实 ID / IP

- Screenshot 1 (`screenshot-01-login-A.png`): Account A logged in, viewing own invoice
- Screenshot 2 (`screenshot-02-login-B.png`): Account B logged in
- Screenshot 3 (`screenshot-03-cross-account.png`): Account B receives Account A's invoice
- Video PoC: `https://drive.google.com/...` (≤ 3 min, password-protected)
- Burp / Caido session export: `request-response.bambda` (attached)

## Suggested Fix

1. Server-side: re-resolve resource ownership from the authenticated user, never trust the URL parameter.
2. Add an integration test that asserts cross-tenant access returns 403/404.
3. Audit log + alert on cross-tenant object access attempts.
4. Consider centralising authorization with an ABAC policy engine.

## References

- OWASP API Security Top 10 (2023) — API1: BOLA — https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
- CWE-639 — https://cwe.mitre.org/data/definitions/639.html
- Related disclosed reports: <列 1-2 个 H1 公开报告链接，证明影响等级>

## Timeline / Notes

- Discovery date:
- Internal verification (me): <date>
- Report submitted: <date>
- Triager response: <date>
- Fix verified: <date>
- CVE / advisory: <if assigned>

---

## 中文要点提示

- 标题尽量精炼，要让 triager 一眼看清"哪个端点 + 什么类问题 + 谁能怎么"
- CVSS / CWE 不要乱填；不确定就在报告里说明你打分的逻辑
- Reproducer Account 必须是你自己注册的两个账号；**绝对不要**用真实用户 cookies 复现
- "Human-validated" 字段是 YesWeHack 等平台的合规要求 — AI 协助 OK，但完全 AI 生成的报告会被拒
- 视频 PoC 控制在 3 分钟以内，加密码保护，不公开
