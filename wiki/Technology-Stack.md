# Technology Stack

> Full detail and rationale: `docs/decision-log.md` in the repository.

---

## Approved Stack

| Layer | Choice | Rationale | Upgrade Path |
|-------|--------|-----------|--------------|
| Language | Python 3.12 | Installed version; richest quantum/ML ecosystem | 3.13 when stable |
| Structured store | SQLite | Zero infrastructure; perfect for experiment run storage | Postgres if concurrent writes needed |
| Vector search | ChromaDB | Local-first, persistent, easy API, built-in metadata filtering | FAISS for throughput in a future phase |
| LLM interface | Anthropic SDK | Primary model provider | Provider-agnostic wrapper via config |
| Testing | pytest | Standard Python; parametrize for circuit config sweeps | Add hypothesis for property-based tests |
| Observability | structlog JSON | Structured, queryable logs; low overhead | OpenTelemetry at scale |

---

## Pending Approval (Not Yet Installed)

These are anticipated experiment-phase dependencies. Each requires Brandt's explicit confirmation + a decision-log entry before being added.

| Dependency | Purpose |
|------------|---------|
| LangGraph | Agent orchestration / graph-based workflows |
| NetworkX | Environment topology graph and memory |
| DEAP | Genetic algorithms for evolutionary optimizer |
| Qiskit / Qiskit Aer | Quantum circuit simulation and QUBO solving |

---

## Adding Dependencies

Any new dependency requires:
1. A reason in `CLAUDE.md` §7
2. An entry in `docs/decision-log.md`
3. Brandt's explicit approval
