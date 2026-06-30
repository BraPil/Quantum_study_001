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

- [x] Each gap analyzed with a documented position — taxonomy, weight-update rule, scenario fidelity
- [x] Each risk assessed (likelihood, impact, blocks-build-or-monitor) — QUBO scaling, latency, loop stability
- [x] Architectural assumptions confirmed or revised in `docs/architecture.md`
- [x] The central question sharpened: *where concretely does quantum add value here*
- [x] Open questions framed as Phase 3 hypothesis candidates

**Status: ✅ COMPLETE — signed off 2026-06-30. Transitioned to Phase 3 (Hypothesis); see [[Phase-3-Hypothesis]].**

## Phase 2 Outcomes (one-line each)

- **Quantum value:** at this domain's scale, no performance value — value is pedagogical/architectural (measured, not assumed).
- **Two QUBOs, two nested optimizers:** only the inner *selection* QUBO is a quantum candidate; the outer *weight update* is continuous search, not a QUBO.
- **Taxonomy:** canonical closed enum (6 scenarios) + thin free-text→enum mapping layer; score classification accuracy separately from response quality.
- **Scenario fidelity:** the bar is decision diversity (different attacks → different optimal chromosomes), not protocol realism.
- **Latency:** critical path ≈ 3 LLM hops (Classifier∥Risk concurrent, GA local, Learner off-path) ≈ 4–5s — inside target. LOW risk, monitor.
- **Loop stability:** MEDIUM risk if naive; mandatory guards = held-out gate + monotonic-or-reject + damping. Does not block.
- **Carried to Phase 3:** policy-QUBO-vs-weight-regression fork; damped-loop convergence experiment (H1/H2).

---

## Method

Mostly thinking and writing — but evidence-driven where possible. Re-run/extend spikes to *measure* a
risk (e.g., scale the QUBO to 12–20 variables and time vs. classical) rather than speculate. Label
those as analysis probes in `spikes/`.

---

## Definition of Done

All criteria checked + Brandt approval → transition to Phase 3 (Hypothesis).
