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
| Agent framework | Raw SDK (L1), LangGraph (L2+) | Raw SDK = clarity for sequential pipeline | — |
| Hot-path optimizer | PyGAD | GA in ~20 lines; 4-5x faster than DEAP | DEAP if multi-objective needed |
| Environment graph | NetworkX DiGraph | 10-node ICS graph; attack propagation as graph walk | — |
| Quantum simulation | Qiskit + Qiskit Aer | QAOA on local simulator; no cloud | IBM Quantum (Layer 4B) |
| QUBO solver | dwave-ocean-sdk (incl. neal) | Local classical SA; same API as real D-Wave | D-Wave Leap QPU (Layer 4A) |
| Testing | pytest | Standard Python; parametrize for circuit config sweeps | Add hypothesis for property-based tests |
| Observability | structlog JSON | Structured, queryable logs; low overhead | OpenTelemetry at scale |

---

## Experiment-Phase Dependencies (Approved — Install at Phase 4)

Approved during Phase 0 research. Add to `requirements.txt` at Phase 4 start, not before.

| Dependency | Layer | Purpose |
|------------|-------|---------|
| `networkx` | 1 | ICS environment topology graph |
| `pygad` | 2 | Hot-path binary chromosome GA (replaces DEAP) |
| `langgraph` | 2+ | Agent orchestration with branching |
| `qiskit` + `qiskit-aer` | 3 | Quantum circuit simulation (QAOA) |
| `dwave-ocean-sdk` | 3–4 | Local QUBO (neal) + D-Wave Leap hardware |

**Deferred:** DEAP (replaced by PyGAD), PennyLane (quantum ML, not QUBO), Azure Quantum.

---

## Adding Dependencies

Any new dependency requires:
1. A reason in `CLAUDE.md` §7
2. An entry in `docs/decision-log.md`
3. Brandt's explicit approval
