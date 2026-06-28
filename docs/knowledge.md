# Knowledge — Quantum_Study_001

> Knowledge types, storage strategy, retrieval patterns.
> Populate as the memory/vector store architecture takes shape in Phase 4.

---

## Knowledge Types (Target Architecture)

| Type | Description | Storage |
|------|-------------|---------|
| Event log | Raw telemetry from simulated environment | SQLite |
| Agent decisions | What each agent decided and why | SQLite |
| Experiment runs | Circuit configs, QUBO inputs, quantum results | SQLite |
| Semantic memory | Agent embeddings, policy summaries | ChromaDB |
| Environment graph | Network topology, asset relationships | NetworkX (in-memory) |

## Retrieval Patterns

*To be defined in Phase 4 as agents are built. Key questions:*

- What does the Observer agent need to retrieve to contextualize a new event?
- What does the Learning Agent store after each cold path cycle?
- How are QUBO results embedded and retrieved for policy comparison?

---

*Last updated: 2026-06-28*
