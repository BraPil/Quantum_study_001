# Phase 2 — Analysis Runbook

> Full runbook: `runbooks/phase-2-analysis.md` in the repository.
> Active branch: `phase/2-analysis`
> Entered 2026-06-28 after Phase 1 sign-off.

---

## Goal

Phase 1 proved the pieces *connect*. Phase 2 asks: *given what running the spikes taught us, is the
design sound — and what breaks when we scale from a toy to the real thing?*

Analysis is reasoning, not building. **No production code.**

---

## Agenda (driven by what Discovery surfaced)

**Gaps**
- Attack-type taxonomy — inferred labels vs. ground-truth labels must be comparable for scoring
- Placeholder weight-update rule — what's the *real* learning rule, and is QUBO the right tool for it?
- Toy-vs-real scenario fidelity — how much realism generates meaningful training signal?

**Risks**
- 6-agent latency (~7s measured-extrapolated) — acceptable for "near real-time"? What runs concurrently?
- QUBO scaling — at what size does the problem stop being a toy? Does quantum ever get interesting here?
- Learning-loop stability — where could the GA↔QUBO loop diverge or overfit?

**Assumptions to revisit**
- Does the hot/cold split still hold after seeing the spikes run?
- Raw-SDK → LangGraph at Layer 2 still right?
- Is the chromosome the right shared GA/QUBO representation?

---

## Success Criteria

- [ ] Each gap analyzed with a documented position
- [ ] Each risk assessed (likelihood, impact, blocks-build-or-monitor)
- [ ] Architectural assumptions confirmed or revised in `docs/architecture.md`
- [ ] The central question sharpened: *where concretely does quantum add value here*
- [ ] Open questions framed as Phase 3 hypothesis candidates

---

## Method

Mostly thinking and writing — but evidence-driven where possible. Re-run/extend spikes to *measure* a
risk (e.g., scale the QUBO to 12–20 variables and time vs. classical) rather than speculate. Label
those as analysis probes in `spikes/`.

---

## Definition of Done

All criteria checked + Brandt approval → transition to Phase 3 (Hypothesis).
