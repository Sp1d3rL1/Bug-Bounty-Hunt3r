# API / OAuth / GraphQL Checklist

## API Recon

- [ ] Swagger/OpenAPI/Postman collection
- [ ] JS 中 endpoint/baseURL
- [ ] Mobile API 与 Web API 差异
- [ ] Versioned endpoints: `/v1`, `/v2`, `/internal`, `/mobile`
- [ ] Hidden methods: GET/POST/PUT/PATCH/DELETE/OPTIONS

## Access Control / BOLA / IDOR

- [ ] Object ID belongs to user A, accessed by user B
- [ ] Tenant ID changed while user remains same
- [ ] `/me/resource` vs `/users/{id}/resource`
- [ ] List endpoint filters expose cross-tenant data
- [ ] Export/download endpoints have weaker auth
- [ ] Background jobs/webhooks leak object IDs

## Mass Assignment

- [ ] `role`, `is_admin`, `plan`, `verified`, `owner_id`, `tenant_id`
- [ ] Create vs update payload fields
- [ ] Mobile-only fields accepted by web API
- [ ] PATCH accepts hidden fields from GET response

## JWT / Session

- [ ] alg/typ/kid handling
- [ ] key rotation and JWKS cache
- [ ] token audience/issuer mismatch
- [ ] refresh token reuse/revocation
- [ ] session fixation / logout invalidation

## OAuth / SSO

- [ ] redirect_uri exact matching
- [ ] state/nonce validation
- [ ] code reuse
- [ ] account linking confusion
- [ ] email claim trust boundary
- [ ] organization/tenant assignment after SSO
- [ ] magic link token scope and expiry

## GraphQL

- [ ] Introspection exposed where unexpected
- [ ] Authorization on node/id lookup
- [ ] Batching bypasses rate limits or auth assumptions
- [ ] Mutation side effects across tenant boundary
- [ ] Error messages leak schema/IDs
- [ ] Query depth/complexity limits

## Reporting Angle

- Prove cross-account or cross-tenant impact with your own two accounts.
- Show minimum necessary response fields.
- Redact tokens and personal data.
- Explain why client-side checks are insufficient.
