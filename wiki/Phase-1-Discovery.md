# Phase 1 — Discovery Runbook

> Full runbook: `runbooks/phase-1-discovery.md` in the repository.
> Active branch: `phase/0-exploration` (Phase 1 work continues here until a new branch is cut)
> Entered 2026-06-28 after Phase 0 sign-off.

---

## Goal

Phase 0 answered *"is this the right approach?"* — yes. Phase 1 answers *"how exactly do the pieces
connect, and do the approved tools actually work as researched?"*

---

## Success Criteria

- [ ] Data contracts defined for every layer boundary (TelemetryEvent → agent state → chromosome → QUBO → fitness update)
- [ ] Minimal QUBO solve works end-to-end with `dwave-neal` locally — proves the cold-path tool
- [ ] Minimal PyGAD binary chromosome GA runs with a toy fitness function — proves the hot-path optimizer
- [ ] Minimal 2-agent raw-SDK pipeline passes a TelemetryEvent through — proves the agent pattern
- [ ] GA↔QUBO handoff demonstrated in a spike
- [ ] Every approved tool installed and confirmed working in this environment
- [ ] Findings recorded in [[Discovery-Log]]

---

## Approach

**Spikes, not production.** Phase 1 builds throwaway proofs that integration points work. The real
build is Phase 4. Keep spikes in `spikes/` or `notebooks/`, clearly labeled. Do NOT build the full
agent roster or simulation here.

**Install-as-needed.** Approved deps were scoped for Phase 4 start, but spikes may need them earlier.
That's fine — the approval exists; this is just earlier timing for proof-of-concept. Note each install.

---

## Definition of Done

All success criteria checked + Brandt approval → transition to Phase 2 (Analysis).
