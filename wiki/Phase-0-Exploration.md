# Phase 0 — Exploration Runbook

> Full runbook: `runbooks/phase-0-exploration.md` in the repository.
> Active branch: `phase/0-exploration`

---

## Goal

Validate the approach before committing to building anything.

---

## Success Criteria

- [ ] Can articulate where quantum computing adds genuine value vs. where classical suffices
- [ ] Surveyed at least 3 quantum frameworks/backends and can compare them for this use case
- [ ] Hot/cold path architecture validated against at least one credible external reference
- [ ] Evolutionary optimizer (DEAP-style) confirmed as viable for combinatorial response selection
- [ ] Decision made on experiment-phase dependencies (LangGraph, NetworkX, DEAP, Qiskit)

---

## Research Agenda

1. **Quantum Foundations** — QUBO formulation, gate-based vs. annealing, quantum advantage at this scale
2. **Agentic + Quantum Integration** — existing patterns, LangGraph evaluation, alternatives
3. **Evolutionary Optimization** — DEAP capabilities, chromosome design, fitness function
4. **Simulation Environment** — minimal ICS sim, NetworkX graph modeling, attack scenario design
5. **Backend Evaluation** — Qiskit Aer, IBM Quantum, D-Wave Leap, Azure Quantum

---

## Key Documents

- `docs/discovery-log.md` — record all research findings here
- `docs/decision-log.md` — record all technology decisions here
- `docs/architecture.md` — update if the architecture changes based on findings

---

## Definition of Done

All success criteria checked + Brandt explicit sign-off → update CLAUDE.md phase status → create Phase 1 runbook.
