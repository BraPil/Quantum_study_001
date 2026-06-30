# Runbook — Phase 3: Hypothesis

> Operational guide for the Hypothesis phase of Quantum_Study_001.
> Entered 2026-06-30 after Phase 2 sign-off. Ends when success criteria below are met and Brandt approves transition to Phase 4 (Experiment).

---

## Phase Goal

Phase 2 reasoned about the design and sharpened the central question with measurement. Phase 3 turns
that understanding into **testable hypotheses** and a **concrete experiment design** for Phase 4.

The honest Phase 2 finding — *at this domain's scale quantum adds no performance value; the value is
pedagogical and architectural* — is not a dead end. It is the premise that shapes the experiment:
the experiment must be designed to **demonstrate and measure that conclusion rigorously**, and to test
the few places where the conclusion could still bend (deliberately hard instances, correctness parity).

Hypothesis is still reasoning and designing, not building. The output is a falsifiable hypothesis set
and a Phase 4 build/measure spec. **No production code.**

---

## Hypothesis Agenda — carried forward from Analysis

The three candidates were framed in `docs/discovery-log.md` [2026-06-28] (QUBO scaling) and refined by
the [2026-06-29] gaps/risks entry. Phase 3 makes each one falsifiable — a claim, a metric, a threshold,
and the condition that would prove it wrong.

### Hypotheses to formalize
- **H1 — Hard-instance distinguishability.** *If* the cold-path policy QUBO is deliberately constructed
  with frustrated / spin-glass-like couplings (not the natural sparse structure), *then* classical SA's
  solution quality or time-to-solution degrades measurably and a quantum annealer becomes
  distinguishable. → Define: what coupling structure, what metric (optimality gap? TTS?), what margin
  counts as "distinguishable," and what result would falsify it (SA stays optimal → quantum still
  pointless even when we try to make it matter).
- **H2 — Correctness parity (the honest deliverable).** *A quantum-solved cold path produces the same
  policy update as the classical path.* → Define: same-input → same-output test, tolerance for sampler
  stochasticity, and what "same policy" means operationally (identical chromosome? within-ε regret?).
  This tests the plumbing — the actual Phase 4 product.
- **H3 — Hot-path-never.** *Per-event response selection never benefits from quantum at any realistic
  action-space size (N ≤ ~10).* → Likely already settled by the scaling probe; Phase 3 decides whether
  to formally close it or keep a thin confirmation in the experiment.

### Open forks to resolve (from Analysis)
- **Policy-QUBO vs. weight-regression** (Gap 2). Is retrospective optimization best expressed as *one*
  large cold-path policy QUBO (condition × action table solved once), or as *weight regression* feeding
  the existing per-event QUBO? Pick one as the Phase 4 baseline, or design the experiment to compare them.
- **Damped, held-out-gated loop convergence** (Risk B). Turn the stability guards into a measurable
  claim: *does the damped, held-out-gated loop converge and stay converged across K cycles with varied
  batches?* This is a direct extension of `spike_loop.py`.

### Experiment design to produce
- What gets built in each Phase 4 layer, in what order, and the smallest version that tests each hypothesis.
- What gets measured (metrics already live in `docs/evaluation.md`) and what counts as success/failure.
- Acceptance tests that must pass *before* trusting any learning-loop result (esp. Gap 3 decision-diversity).

---

## Success Criteria

- [ ] Each carried-forward candidate (H1, H2, H3) stated as a falsifiable hypothesis: claim, metric,
      threshold, and the observation that would refute it
- [ ] The two open forks resolved into a Phase 4 decision (chosen baseline, or a comparison designed in)
- [ ] A Phase 4 experiment design exists: layer-by-layer build order, what is measured, what counts as
      success — traceable to the hypotheses and to `docs/evaluation.md` metrics
- [ ] Acceptance tests named for the sim (decision-diversity) and the loop (held-out convergence) before
      any result is trusted
- [ ] Hypotheses + design recorded in `docs/decision-log.md`; any surprise in `docs/lessons-learned.md`
- [ ] `docs/architecture.md` updated if the chosen design changes a documented assumption

---

## Method

- Reasoning and design, evidence-driven where cheap. Existing spikes may be *extended as analysis probes*
  to pin a hypothesis threshold (e.g., construct a frustrated QUBO instance and check whether SA actually
  degrades — that directly informs H1's falsification bar). Keep such probes in `spikes/`, labeled.
- Where a design choice is genuinely open, state it as a decision to make at Phase 4 start with the
  criterion that will decide it — don't force an arbitrary pick now.
- Phase discipline: do NOT build the Phase 4 system (agent roster, full sim, real backend wiring) here.
  Hypothesis produces the spec; Experiment executes it.

---

## Session Protocol for This Phase

1. `git status && git log --oneline -5` — orient
2. `pytest tests/ -v` — confirm baseline green
3. Pick one hypothesis or fork; state the claim and its falsification condition before starting
4. Record the formalized hypothesis / design decision in decision-log immediately
5. If the design changes the architecture, update `docs/architecture.md` and tell Brandt

---

## Definition of Done (Phase 3)

All success criteria checked. Brandt reviews and approves transition to Phase 4 (Experiment). At that point:
- Update `CLAUDE.md` Phase Status: Hypothesis → ✅ COMPLETE, Experiment → 🔄 IN PROGRESS
- Create `runbooks/phase-4-experiment.md`
- Add the approved experiment-phase dependencies to `requirements.txt` (approval already on record in
  `docs/decision-log.md`) — this is the phase where that install gate finally opens
- Record the phase transition in `docs/decision-log.md`
- Sync `wiki/` and GitHub wiki

---

*Created: 2026-06-30 | Owner: Brandt Pileggi*
