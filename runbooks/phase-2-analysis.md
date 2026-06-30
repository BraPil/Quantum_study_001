# Runbook — Phase 2: Analysis

> Operational guide for the Analysis phase of Quantum_Study_001.
> Entered 2026-06-28 after Phase 1 sign-off. Ends when success criteria below are met and Brandt approves transition to Phase 3 (Hypothesis).

---

## Phase Goal

Phase 1 proved the pieces *connect*. Phase 2 asks the harder question: *given what running the
spikes actually taught us, is the design sound — and what will break when we scale from a toy to the
real thing?*

Analysis is reasoning, not building. The output is a clear-eyed assessment of gaps, risks, and
revised assumptions that feeds the Phase 3 hypothesis and experiment design. **No production code.**

---

## Analysis Agenda — driven by what Discovery surfaced

These are the concrete items the spikes exposed. Each needs analysis, not a fix yet.

### Gaps
- **Attack-type taxonomy.** The agent inferred `unauthorized_command_injection` while the sim's
  ground truth was `unauthorized_plc_write` — semantically equivalent, different label. Scoring needs
  a canonical taxonomy so inferred and ground-truth labels are comparable. *Analyze: what's the right
  taxonomy granularity? Map agent free-text → canonical labels how?*
- **Placeholder weight-update rule.** `spike_loop.py` used a transparent coordinate search to recover
  one miscalibrated weight. *Analyze: what's the real learning rule? Is QUBO even the right tool for
  the weight update, or only for per-event response selection? Where exactly does quantum add value —
  response selection, policy retrospection, or both?*
- **Toy-vs-real scenario fidelity.** The 6-action scenario has hand-picked numbers. *Analyze: what
  makes a scenario generate meaningful training signal? How much realism is enough?*

### Risks
- **6-agent latency.** Measured ~1.2s/agent on Haiku → ~7s for the full roster. *Analyze: is 7s
  acceptable for "near real-time"? Which agents can run concurrently? Where does streaming help?*
- **QUBO scaling.** At 6 variables, classical brute force wins and QUBO/SA matches it trivially.
  *Analyze: at what problem size does the QUBO formulation stop being a toy? Does the real problem
  ever reach a scale where quantum is interesting, or is this purely a pattern-learning exercise?*
  (Phase 0 already concluded no advantage at this scale — confirm that holds for the real scenario.)
- **Learning-loop stability.** *Analyze: where could the GA↔QUBO loop diverge, oscillate, or
  overfit to a batch? What guards are needed?*

### Assumptions to revisit
- Does the hot/cold split still make sense after seeing the spikes run?
- Is raw-SDK → LangGraph at Layer 2 still the right call, or did the agent spike suggest otherwise?
- Is the chromosome the right shared representation between GA and QUBO?

---

## Success Criteria

- [x] Each gap above analyzed with a documented position (not necessarily solved — understood)
      → *Done — discovery-log [2026-06-29]: taxonomy (canonical enum + thin mapping layer),
        weight-update rule (nested optimizers; weight update is continuous search, NOT a QUBO),
        scenario fidelity (signal not realism — decision diversity is the bar).*
- [x] Each risk assessed: likelihood, impact, and whether it blocks the build or is monitored
      → *QUBO scaling: **assessed** (probe_qubo_scaling.py) — classical-tractable at all realistic N.
        6-agent latency: **assessed** — critical path is ~3 LLM hops (Classifier∥Risk concurrent, GA
        local, Learner off-path), ~4–5s, LOW risk, monitor. Learning-loop stability: **assessed** —
        MEDIUM likelihood if built naively, guards (held-out gate, monotonic-or-reject, damping)
        mandatory. None blocks the build.*
- [x] Architectural assumptions revised in `docs/architecture.md`
      → *Two-QUBO distinction added; both confirmed classical-tractable. Hot/cold split holds.*
- [x] A clear answer to the project's central question sharpened
      → *At this domain's scale quantum adds no performance value; value is pedagogical/architectural.
        Backed by local measurement, not just research. See discovery-log Phase 2 Analysis.*
- [x] Findings recorded in `docs/discovery-log.md`; surprise recorded in `docs/lessons-learned.md`
- [x] Open questions framed as Phase 3 hypothesis candidates (H1 hard-instance, H2 correctness-parity, H3 hot-path-never)

---

## Method

Analysis is mostly thinking and writing, but it can be evidence-driven:
- Re-run or extend spikes to *measure* a risk (e.g., scale the QUBO to 12/20 variables, time it vs.
  classical) rather than speculate. Keep these in `spikes/` and label them analysis probes.
- Where a question is genuinely open, write it down as a Phase 3 hypothesis candidate rather than
  forcing an answer now.

---

## Session Protocol for This Phase

1. `git status && git log --oneline -5` — orient
2. `pytest tests/ -v` — confirm baseline green
3. Pick one agenda item; state the question being analyzed before starting
4. Record the analysis + any measurement in discovery-log / lessons-learned immediately
5. If analysis changes the architecture, update `docs/architecture.md` and tell Brandt

---

## Definition of Done (Phase 2)

All success criteria checked. Brandt reviews and approves transition to Phase 3 (Hypothesis). At that point:
- Update `CLAUDE.md` Phase Status: Analysis → ✅ COMPLETE, Hypothesis → 🔄 IN PROGRESS
- Create `runbooks/phase-3-hypothesis.md`
- Record the phase transition in `docs/decision-log.md`
- Sync `wiki/` and GitHub wiki

---

*Created: 2026-06-28 | Owner: Brandt Pileggi*
