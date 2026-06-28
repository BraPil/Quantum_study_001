# Runbook — Phase 1: Discovery

> Operational guide for the Discovery phase of Quantum_Study_001.
> Entered 2026-06-28 after Phase 0 sign-off. Ends when success criteria below are met and Brandt approves transition to Phase 2 (Analysis).

---

## Phase Goal

Phase 0 answered *"is this the right approach?"* — yes. Phase 1 answers *"how exactly do the pieces
connect, and do the approved tools actually work as researched?"*

Move from validated architecture to **proven integration points** and **de-risked proof-of-concept spikes**.

---

## Success Criteria

- [x] Data contracts defined for every layer boundary — `spikes/contracts.py`
- [x] A minimal QUBO solve works end-to-end locally — `spikes/spike_qubo.py` (note: sampler is `dwave.samplers.SimulatedAnnealingSampler`, not the deprecated `neal`)
- [x] A minimal PyGAD binary chromosome GA runs with a toy fitness function — `spikes/spike_ga.py`
- [x] A minimal 2-agent raw-SDK pipeline passes a TelemetryEvent through — `spikes/spike_agents.py` (ran live, 2.40s/2 agents)
- [x] The GA↔QUBO handoff is demonstrated in a spike — `spikes/spike_loop.py` (regret 0.92 → 0.00)
- [x] Every approved tool installed and confirmed working — pygad, dwave-ocean-sdk, anthropic
- [x] Discovery findings recorded in `docs/discovery-log.md`

---

## Discovery Activities

| Activity | Output | Risk de-risked |
|----------|--------|----------------|
| Define layer data contracts | Dataclasses / TypedDicts in `docs/architecture.md` | Interface drift between layers |
| `dwave-neal` QUBO spike | `notebooks/` or `spikes/` proof | Cold-path solver actually works |
| PyGAD GA spike | `spikes/` proof | Hot-path optimizer actually works |
| Raw-SDK agent spike | `spikes/` proof | Agent pattern + latency are realistic |
| GA↔QUBO loop spike | `spikes/` proof | The core learning loop is wireable |
| Tool install verification | Updated `requirements.txt` | "Researched" ≠ "works here" |

**Phase discipline:** Spikes are throwaway proofs, not production code. They prove integration points
work. The real Phase 4 build replaces them. Keep them in a `spikes/` or `notebooks/` directory, clearly
labeled as exploratory. Do NOT build the full agent roster or simulation here — that is Phase 4.

---

## Dependency Installation Gate

The experiment-phase deps are APPROVED (see `docs/decision-log.md`) but were scoped for "Phase 4 start."
Discovery spikes need some of them earlier to prove the integrations. **This is acceptable** — install
what a spike requires, when the spike requires it, and note it. The approval already exists; this is just
earlier timing for proof-of-concept purposes, not new scope.

Suggested install order (as spikes demand them):
1. `networkx` + `pygad` — cheapest, classical, no quantum
2. `dwave-ocean-sdk` — for the local `dwave-neal` QUBO spike
3. `qiskit` + `qiskit-aer` — only if a QAOA simulation spike is attempted in Discovery
4. `langgraph` — defer to Phase 4 Layer 2 unless a branching spike is needed

---

## Session Protocol for This Phase

1. `git status && git log --oneline -5` — orient
2. `pytest tests/ -v` — confirm baseline green
3. Check `docs/discovery-log.md` — don't repeat prior findings
4. Define the specific integration question or spike for this session before starting
5. Record what worked AND what didn't in discovery-log / lessons-learned immediately
6. If a spike reveals the architecture is wrong, update `docs/architecture.md` and tell Brandt

---

## Definition of Done (Phase 1)

All success criteria checked. Brandt reviews and approves transition to Phase 2 (Analysis). At that point:
- Update `CLAUDE.md` Phase Status: Discovery → ✅ COMPLETE, Analysis → 🔄 IN PROGRESS
- Create `runbooks/phase-2-analysis.md`
- Record the phase transition in `docs/decision-log.md`
- Sync `wiki/` and GitHub wiki

---

*Created: 2026-06-28 | Owner: Brandt Pileggi*
