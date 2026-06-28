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

## 2026-06-28 — Experiment-Phase Dependencies (Pending Approval)

LangGraph, NetworkX, DEAP, Qiskit/Qiskit Aer are anticipated but **not yet approved**. Require Brandt's confirmation before install.

---

*See `docs/decision-log.md` for full rationale on each decision.*
