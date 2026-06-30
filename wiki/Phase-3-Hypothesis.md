# Phase 3 — Hypothesis Runbook

> Full runbook: `runbooks/phase-3-hypothesis.md` in the repository.
> Active branch: `phase/2-analysis`
> Entered 2026-06-30 after Phase 2 sign-off.

---

## Goal

Phase 2 reasoned about the design and sharpened the central question with measurement. Phase 3 turns
that into **testable hypotheses** and a **Phase 4 experiment design**. The honest Phase 2 finding —
*quantum adds no performance value at this scale; value is pedagogical/architectural* — is the premise
the experiment must demonstrate rigorously and stress-test where it could still bend.

Reasoning and design, not building. **No production code.**

---

## Hypotheses to formalize (carried from Analysis)

- **H1 — Hard-instance distinguishability.** If the cold-path policy QUBO is built with frustrated /
  spin-glass couplings (not the natural sparse structure), classical SA degrades and a quantum annealer
  becomes distinguishable. Define metric (optimality gap / time-to-solution), margin, and falsifier.
- **H2 — Correctness parity (the honest deliverable).** A quantum-solved cold path produces the *same*
  policy update as the classical path. Define "same" (identical chromosome / within-ε regret) and the
  tolerance for sampler stochasticity. This tests the plumbing — the real product.
- **H3 — Hot-path-never.** Per-event selection (N ≤ ~10) never benefits from quantum. Likely settled by
  the scaling probe; decide whether to formally close it or keep a thin confirmation.

## Open forks to resolve

- **Policy-QUBO vs. weight-regression** — one large cold-path policy QUBO, or weight regression feeding
  the per-event QUBO? Choose a Phase 4 baseline or design the comparison.
- **Damped, held-out-gated loop convergence** — make the Risk B guards a measurable claim: does the
  damped, held-out-gated loop converge and stay converged across K cycles with varied batches? Direct
  extension of `spike_loop.py`.

## Experiment design to produce

Layer-by-layer build order, what is measured (per `docs/evaluation.md`), what counts as success, and the
acceptance tests that must pass before any loop result is trusted (sim decision-diversity; loop convergence).

---

## Success Criteria

- [ ] H1, H2, H3 each stated as a falsifiable hypothesis (claim, metric, threshold, refuting observation)
- [ ] The two open forks resolved into a Phase 4 decision
- [ ] A Phase 4 experiment design exists, traceable to the hypotheses and to `docs/evaluation.md`
- [ ] Acceptance tests named for the sim (decision-diversity) and the loop (held-out convergence)
- [ ] Hypotheses + design in `docs/decision-log.md`; surprises in `docs/lessons-learned.md`

---

## Definition of Done

All criteria checked + Brandt approval → transition to Phase 4 (Experiment), where the approved
dependency-install gate finally opens (`requirements.txt`).
