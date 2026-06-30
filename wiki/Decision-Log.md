# Decision Log

> Authoritative version: `docs/decision-log.md` in the repository.
> This wiki page is a summary. Always update the repo file first.

---

## 2026-06-28 — Initial Technology Stack

Approved: Python 3.12, SQLite, ChromaDB, Anthropic SDK, pytest, structlog JSON.

Key trade-offs:
- ChromaDB over FAISS — easier setup; FAISS noted for future performance phase
- SQLite over Postgres — zero infrastructure for a research project
- Redis deferred — revisit if hot path latency requires queuing

---

## 2026-06-28 — Experiment Domain: Simulated ICS Security Environment

Using a small-scale ICS/SCADA simulation as the experimental domain because it produces discrete combinatorial optimization problems — the natural fit for QUBO/quantum speedup.

---

## 2026-06-28 — Phase 0 Research Outcomes (Revised Stack)

Five-agent research survey produced these decisions (supersede the earlier "pending" list):

- **Layer 4 backend:** D-Wave Leap (4A, native QUBO) primary; IBM Quantum (4B, gate-based learning) secondary.
- **Local QUBO testing:** `dwave-ocean-sdk` (includes `dwave-neal` classical SA solver).
- **Hot-path optimizer:** PyGAD replaces DEAP (~20 lines, 4-5x faster).
- **Agent orchestration:** Raw Anthropic SDK at Layer 1; LangGraph from Layer 2.
- **ICS simulation:** Pure Python + NetworkX DiGraph, ~200 lines.
- **Quantum advantage:** Not claimed at this scale — value is the integration pattern.

**Approved for Phase 4:** `qiskit` + `qiskit-aer`, `dwave-ocean-sdk`, `pygad`, `networkx`, `langgraph`.
**Deferred:** DEAP (replaced), PennyLane, Azure Quantum.

---

## 2026-06-30 — Phase Transition: Analysis → Hypothesis

Phase 2 (Analysis) COMPLETE — all six criteria met; central question sharpened by measurement (quantum adds no performance value at this scale; value is pedagogical/architectural). Phase 3 (Hypothesis) now active. Approved by Brandt (delegated, "proceed as you see fit"). No merge to `main` (human gate).

Phase 3 will formalize H1 (hard-instance distinguishability), H2 (correctness parity), H3 (hot-path-never) into falsifiable hypotheses, resolve the policy-QUBO-vs-weight-regression and damped-loop-convergence forks, and produce the Phase 4 experiment design.

---

*See `docs/decision-log.md` for full rationale on each decision.*
