# Discovery Log

> Authoritative version: `docs/discovery-log.md` in the repository.
> This wiki page summarizes Phase 0 research outcomes.

---

## 2026-06-28 — Phase 0 Five-Agent Research Survey

Five parallel research agents surveyed the problem space. Headline findings:

### Quantum Foundations
- The 6-action response problem is textbook QUBO.
- **No quantum advantage at 6-10 variable scale** — a laptop brute-forces it in microseconds. The project's value is the integration pattern, not beating classical. **This must be framed honestly everywhere.**

### Backends — Revised
- **D-Wave is the honest QUBO backend** — native QUBO input, no QAOA circuit needed. Now Layer 4A (primary).
- **IBM Quantum** → Layer 4B (gate-based learning, QAOA).
- **dwave-neal** enables fully local, offline QUBO testing with the same API as real hardware.
- Azure Quantum and PennyLane deferred.

### Agent Orchestration — Revised
- **Raw Anthropic SDK for Layer 1** (educational clarity), **LangGraph from Layer 2** (when branching/state justify it).
- Hot path realistically 5-7s using Haiku for fast agents + Sonnet for reasoning agents.

### Evolutionary Optimizer — Revised
- **PyGAD replaces DEAP** — working GA in ~20 lines, 4-5x faster. DEAP reserved for multi-objective later.
- The **GA↔QUBO loop is the project's intellectual core**: GA answers "best response now?", QUBO answers "best policy across history?", and QUBO results feed back into GA fitness weights.

### ICS Simulation
- **NetworkX DiGraph** confirmed for the 10-node environment. Attack propagation = graph walk.
- Write our own synthetic telemetry generator (~200 lines) — no suitable library exists, and owning ground-truth labels is a feature.

### Approved Dependencies (Phase 4)
`qiskit` + `qiskit-aer`, `dwave-ocean-sdk`, `pygad`, `networkx`, `langgraph`.
Deferred: DEAP (replaced), PennyLane, Azure Quantum.

---

*See `docs/discovery-log.md` for full detail and source citations.*
