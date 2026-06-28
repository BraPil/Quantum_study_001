# Discovery Log

> Authoritative version: `docs/discovery-log.md` in the repository.
> This wiki page summarizes Phase 0 research outcomes.

---

## 2026-06-28 — Phase 1 Discovery Spikes

Throwaway proofs in `spikes/` de-risk the highest-risk integrations. All deterministic spikes pass (`tests/test_spikes.py`).

- **`neal` is deprecated** — sampler moved to `dwave.samplers.SimulatedAnnealingSampler`. Caught by actually running it. *"Researched" ≠ "runs here"* — exactly what Discovery is for.
- **Layer data contracts defined** (`contracts.py`): TelemetryEvent → ResponseContext → Chromosome → FitnessWeights. Agents infer ground truth; the sim knows it.
- **GA and QUBO both match brute force** — both avoid quarantine due to pairwise penalties, confirming the quadratic term does real work.
- **The GA↔QUBO loop closes:** miscalibrated downtime weight (0.5) recovered to truth (2.0) by cold-path retrospection; regret 0.92 → 0.00. Hot → SQLite → cold → feedback handoff proven wireable.
- **Agent spike written, blocked on `ANTHROPIC_API_KEY`** — needs a key via `.env` to run.

| Criterion | Status |
|-----------|--------|
| Data contracts | ✅ |
| QUBO solve (dwave) | ✅ |
| PyGAD GA | ✅ |
| 2-agent raw-SDK pipeline | ⏳ blocked on API key |
| GA↔QUBO handoff | ✅ |
| Tools confirmed working | ✅ (anthropic pending live call) |

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
