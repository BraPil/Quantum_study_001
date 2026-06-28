# Security — Quantum_Study_001

> Threat model, injection defense, secret hygiene.

---

## Secret Hygiene

- All secrets and API keys go in `.env` (gitignored — never committed)
- No hardcoded credentials anywhere in `src/` or tests
- `ANTHROPIC_API_KEY` is the only secret currently in use
- Tests must pass without `.env` present (no credential-dependent tests)

## LLM Prompt Injection Defense

- All externally sourced content must be sanitized before inclusion in any LLM prompt
- No exception for "internal" sources — sanitize everything that touches a prompt

## Threat Model

*This is a research system, not a production system. Formal threat modeling deferred to Phase 4 if the simulation requires it.*

Current surface area:
- Anthropic API key (only secret; protect via `.env`)
- No external-facing endpoints in current phases

---

*Last updated: 2026-06-28*
