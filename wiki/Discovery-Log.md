# Discovery Log

> Authoritative version: `docs/discovery-log.md` in the repository.
> This wiki page summarizes Phase 0 research outcomes.

---

## 2026-06-29 — Phase 2 Analysis: Gaps & Remaining Risks (closes Phase 2)

Documented positions on the three Discovery gaps and the two risks the scaling probe didn't cover. Reasoning, not building — no production code.

**Gaps**
- **Attack-type taxonomy:** ground truth is a closed `AttackType` enum (the 6 scenarios); agent free text resolves to it via a thin synonym/substring (→ ChromaDB if needed) mapping layer — no second LLM normalizer. Granularity = the 6 scenarios, no finer. Score classification accuracy separately from response quality.
- **Weight-update rule:** the loop is **two nested optimizers**. Inner = *selection* (binary + quadratic → a real QUBO, the only quantum candidate). Outer = *weight update* (continuous, non-convex → derivative-free continuous search, **not** a QUBO). The spike's weight sweep is the degenerate 1-D case.
- **Scenario fidelity:** the bar is **decision diversity** (different attacks → different optimal chromosomes, non-obvious optima), not protocol realism. Make "distinct optima across attacks" an acceptance test before trusting the loop.

**Risks**
- **6-agent latency — LOW, monitor.** Critical path is ~3 LLM hops, not 6: GA is local PyGAD, Learner is cold-path, Classifier∥Risk parallelise → Observer → (Classifier ∥ Risk) → Response Generator ≈ 4–5s, inside target.
- **Learning-loop stability — MEDIUM if naive, guards mandatory.** Failure modes: batch overfit, oscillation, feedback drift, degenerate signal. Unifying guard: evaluate on **held-out** ground-truth regret, **monotonic-or-reject** updates (keep last-good), **damp** (EMA/α). Does not block.

**Carried to Phase 3:** policy-QUBO-vs-weight-regression fork; damped-loop convergence experiment.

---

## 2026-06-28 — Phase 2 Analysis: QUBO Scaling

Probe `spikes/probe_qubo_scaling.py` measured brute force vs. classical simulated annealing as variable count N grows.

| N | 2^N | BF time | SA time | SA vs BF |
|---|-----|---------|---------|----------|
| 20 | 1.0M | 0.55s | 0.06s | optimal |
| 24 | 16.8M | infeasible | 0.07s | (2-seed agree) |
| 40 | 1.1T | infeasible | 0.14s | (2-seed agree) |
| 60 | 1.15×10¹⁸ | infeasible | 0.18s | (2-seed agree) |

**Finding:** Brute force dies ~N=22, but *classical* SA stays sub-200ms and self-consistent to N=60, and is exactly optimal everywhere checkable. So **"brute force infeasible" is not the bar for quantum** — the bar is "even classical heuristics struggle," which this sparse, structured domain never reaches.

**Two-QUBO distinction:** per-event response selection is N≤10 forever (trivially classical); cold-path policy retrospection reaches at most N≈100 (SA solves N=60 in 0.18s). Both classical-tractable.

**Sharpened answer to the central question:** at this domain's scale, quantum adds **no performance value** — its value is pedagogical/architectural (the integration pattern + hot/cold plumbing, quantum as a drop-in swap). The honest finding *is* the deliverable. Phase 3 hypotheses framed: H1 (hard-instance construction), H2 (correctness parity), H3 (hot path never benefits).

---

## 2026-06-28 — Phase 1 Discovery Spikes

Throwaway proofs in `spikes/` de-risk the highest-risk integrations. All deterministic spikes pass (`tests/test_spikes.py`).

- **`neal` is deprecated** — sampler moved to `dwave.samplers.SimulatedAnnealingSampler`. Caught by actually running it. *"Researched" ≠ "runs here"* — exactly what Discovery is for.
- **Layer data contracts defined** (`contracts.py`): TelemetryEvent → ResponseContext → Chromosome → FitnessWeights. Agents infer ground truth; the sim knows it.
- **GA and QUBO both match brute force** — both avoid quarantine due to pairwise penalties, confirming the quadratic term does real work.
- **The GA↔QUBO loop closes:** miscalibrated downtime weight (0.5) recovered to truth (2.0) by cold-path retrospection; regret 0.92 → 0.00. Hot → SQLite → cold → feedback handoff proven wireable.
- **Agent spike ran live:** Observer 1.65s + Classifier 0.75s = 2.40s for 2 agents (~1.2s/agent → ~7s for 6, confirming the Phase 0 estimate). Agents inferred the threat correctly *without* seeing ground truth — the contract design works. Raw-SDK pattern confirmed for Layer 1.

**All 7 Phase 1 criteria met.** New Phase 4 to-do: canonical attack-type taxonomy so inferred and ground-truth labels are comparable for scoring.

| Criterion | Status |
|-----------|--------|
| Data contracts | ✅ |
| QUBO solve (dwave) | ✅ |
| PyGAD GA | ✅ |
| 2-agent raw-SDK pipeline | ✅ ran live |
| GA↔QUBO handoff | ✅ |
| Tools confirmed working | ✅ |

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
