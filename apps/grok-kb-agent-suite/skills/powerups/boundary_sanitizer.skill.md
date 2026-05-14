# boundary_sanitizer

Purpose: Keep technical notes clear, compliant, and low false-positive.

Default substitutions:
- real third-party data -> synthetic data
- production DoS -> Lab-only complexity validation
- token theft -> token exposure risk with test accounts
- payment bypass -> sandbox/test-card pricing-state validation
- destructive action -> minimal-impact proof

Never remove important bug bounty learning value; add context and boundary instead.
