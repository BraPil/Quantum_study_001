# Decision Log — Quantum_Study_001

> Chronological record of architectural decisions.
> Every significant choice lives here with its rationale.
> Format: date, decision, rationale, alternatives considered, upgrade path.

---

## [2026-06-28] Initial Technology Stack

**Decision:** Adopt the following stack for the project.

| Layer | Choice |
|-------|--------|
| Language | Python 3.12 |
| Structured store | SQLite |
| Vector search | ChromaDB |
| LLM interface | Anthropic SDK |
| Testing | pytest |
| Observability | structlog JSON |

**Rationale:**
- Python 3.12 is the installed version and has the richest quantum/ML ecosystem.
- SQLite chosen for zero-infrastructure experiment run storage; no server to manage for a research project.
- ChromaDB chosen over FAISS for local persistence and built-in metadata filtering with minimal setup.
- Anthropic SDK is the primary LLM provider.
- pytest is the Python testing standard.
- structlog JSON produces structured, queryable logs with minimal overhead.

**Alternatives considered:**
- Redis alongside SQLite for hot path queuing — deferred; revisit if hot path latency requires it.
- FAISS over ChromaDB — noted for a future phase where vector throughput becomes a bottleneck. FAISS offers higher performance but requires manual persistence scaffolding.
- Postgres — overkill for a single-user research system.

**Upgrade paths documented in CLAUDE.md §7.**

---

## [2026-06-28] Experiment Domain: Simulated ICS/SCADA Security Environment

**Decision:** Use a small-scale simulated industrial control system (ICS) as the experimental domain.

**Rationale:**
- Produces discrete, combinatorial optimization problems — the natural fit for quantum speedup via QUBO.
- Small world (3 PLCs, 2 workstations, etc.) keeps debugging tractable.
- The hot/cold path split maps cleanly: classical agents handle real-time threat response (hot); quantum optimizer evaluates alternative policies in batch (cold).
- Inspired by ChatGPT architectural consultation on 2026-06-28.

**Non-goal:** This is not a real security system. It is a vehicle for studying quantum/agentic integration patterns.

---

## [2026-06-28] Anticipated Experiment-Phase Dependencies (Pending Approval)

**Status:** Not yet approved. Require Brandt confirmation + decision-log entry before adding to requirements.

| Dependency | Purpose |
|------------|---------|
| LangGraph | Agent orchestration / graph-based workflows |
| NetworkX | Environment topology graph and memory |
| DEAP | Genetic algorithms for evolutionary optimizer |
| Qiskit / Qiskit Aer | Quantum circuit simulation and QUBO solving |

These will be evaluated and formally approved when Phase 4 (Experiment) begins.

---

*Add new entries above this line, newest first.*
