# English Vulnerability Report Template

## Title

`[Vulnerability class] allows [attacker role] to [impact] via [affected feature]`

Example:

`IDOR allows a workspace member to download invoices from another tenant via invoice_id parameter`

## Summary

Briefly explain the vulnerability in 3–5 sentences:

- affected feature
- attacker prerequisite
- vulnerable object/action
- business/security impact

## Scope and Authorization

- Program:
- Asset:
- Tested account(s):
- Date/time:
- Testing stayed within scope:

## Steps to Reproduce

1. Create / use Account A as ...
2. Create / use Account B as ...
3. Perform ...
4. Intercept request ...
5. Change ...
6. Observe ...

## Proof of Concept

```http
GET /api/... HTTP/2
Host: ...
Authorization: Bearer <redacted>
```

Expected:

```text
403 Forbidden or resource scoped to current tenant
```

Actual:

```text
200 OK with another tenant's resource metadata
```

## Impact

Explain concrete impact:

- what data/action is exposed
- who can exploit it
- scale of affected resources
- whether it affects confidentiality, integrity, availability, financial loss, or compliance

## Evidence

- Screenshot 1:
- Screenshot 2:
- Video:
- Request/response files:

Redact tokens, cookies, PII, and third-party data.

## Suggested Fix

- Enforce server-side authorization on object access.
- Bind resource lookup to current user/tenant.
- Add integration tests for cross-tenant access.
- Log and alert suspicious cross-tenant object access attempts.

## Timeline / Notes

- Discovery date:
- Report date:
- Additional notes:
