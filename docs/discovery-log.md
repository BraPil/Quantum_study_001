# Discovery Log — Quantum_Study_001

> Important findings that affect future work.
> Add an entry whenever you discover something non-obvious that a future session needs to know.

---

## [2026-06-28] Phase 0 Research — Five-Agent Parallel Survey

Five research agents ran simultaneously covering quantum foundations, backends, agent orchestration,
evolutionary optimization, and ICS simulation. Key findings that change or refine the architecture:

---

### QUBO Foundations

- QUBO (Quadratic Unconstrained Binary Optimization) maps directly to the response selection problem.
  For 6 binary actions `[Alert, Quarantine, KillProcess, Honeypot, RateLimit, Rollback]`, the Q matrix
  encodes threat effectiveness weights, downtime costs, action costs, false-positive risk, and pairwise
  conflict penalties. This is textbook QUBO. Reference: [arxiv 1811.11538](https://arxiv.org/abs/1811.11538)

- **No quantum advantage exists at 6–10 variable scale.** A laptop brute-forces 64 combinations in
  microseconds. Classical solvers win easily. The value of this project is learning the integration
  pattern (formulate → encode → solve → extract), not outperforming classical. A March 2025 Physical
  Review A paper found no quantum advantage in current combinatorial optimization methods.
  **Frame this honestly in all documentation and presentations.**

- The cold-path QUBO formulation is: minimize `Risk + Downtime + False_Positives - Protection`.
  Each term is linear or quadratic in the binary response variables.

---

### Backend Selection — Revised

The originally planned Layer 4 architecture (IBM Quantum as primary) is **revised**:

- **D-Wave is the intellectually honest QUBO backend.** QUBO/Ising is its native input format —
  no circuit construction, no QAOA, no Hamiltonian encoding. You hand it a Q dict and get back
  binary solutions. IBM requires encoding QUBO as a QAOA circuit, which adds significant complexity
  and performs worse on optimization problems in benchmarks.

- **D-Wave Leap LaunchPad** offers 3-month free access for qualified applicants. Apply when Phase 4 begins.
  Free tier on signup is 1 min QPU / 20 min hybrid — thin but enough for initial testing.

- **dwave-neal** (D-Wave's classical simulated annealing solver) enables fully local, offline QUBO
  testing with zero cloud dependency. Same API as real D-Wave hardware — swap the sampler to go live.
  This is the right local testing tool before spending QPU minutes on cloud hardware.

- **IBM Quantum** retains value as **Layer 4 option B** for learning gate-based QC fundamentals
  (QAOA, Hamiltonians, circuit construction). 10 min/month free on real hardware. Queue times are
  the main pain point.

- **Azure Quantum** (D-Wave left in 2023; gate-based providers only) and **PennyLane** (better for
  quantum ML/differentiable programming than QUBO optimization) are deferred.

- **Layer 3 → Layer 4 mapping:**
  - Layer 3: Qiskit Aer (local gate-based simulator) — confirms QAOA circuit works
  - Layer 4A: D-Wave Leap — native QUBO, primary cold-path target
  - Layer 4B: IBM Quantum — gate-based hardware, secondary learning target

---

### Agent Orchestration — Revised

Originally planned to use LangGraph for agent orchestration. **Revised:**

- **Start with raw Anthropic SDK + async Python for Layer 1.** Each agent is a plain async function
  that takes a state dict and calls `client.messages.create()`. No framework overhead, no magic,
  all logic visible. Maximum educational clarity for a research project.

- **LangGraph introduced at Layer 2** when the Evolutionary Optimizer adds conditional branching
  ("escalate to quantum?"), retry logic, and state persistence that justify framework overhead.
  LangGraph 1.2 (stable, May 2026) is in production at Klarna, LinkedIn, Uber. Uses ~30-40% fewer
  tokens than CrewAI-style frameworks because routing is code, not LLM calls. ~120ms/node overhead.

- **Hot path latency reality:** 6 sequential Anthropic API calls:
  - Claude Haiku 4.5: ~4–6s total (recommended for Observer, Classifier, Risk Assessor)
  - Claude Sonnet 4.6: ~7–9s total (use only for Optimizer, Learning Agent)
  - Mix: Haiku for fast agents + Sonnet for reasoning-heavy agents ≈ 5-7s achievable
  - The bottleneck is API TTFT, not orchestration. Framework choice is secondary.

- **PydanticAI** noted as a middle ground — type-safe, Anthropic-native, forces explicit I/O contracts.
  Worth evaluating at Layer 2 as an alternative to LangGraph for this use case.

- **CrewAI**: avoid — role-based mental model doesn't map to a typed sequential pipeline.

---

### Evolutionary Optimizer — Revised

Originally planned to use DEAP. **Revised:**

- **PyGAD** is the better choice for the hot-path optimizer:
  - Working GA in ~20 lines vs DEAP's verbose creator/toolbox setup
  - ~4-5x faster execution in benchmarks
  - Cleaner API, maintained (Python 3.12 compatible)
  - Same flexibility for binary chromosomes with custom fitness functions

- **DEAP** (version 1.4.3, last commit Nov 2025, actively maintained) remains the right choice
  if multi-objective optimization (NSGA-II, Pareto fronts) is needed later.

- **The GA↔QUBO feedback loop is the intellectual core of this project:**
  - GA (hot path): "What's the best response *now*?" — per-event, seconds
  - QUBO (cold path): "What policy would have minimized harm *across history*?" — per N events, batch
  - QUBO cold-path results → update GA fitness function weights → better hot-path decisions
  - These are complementary halves of a learning loop, not competing approaches.
  - Research confirms: evolutionary algorithms can even construct better QUBO problem representations
    (arxiv 2405.09272).

- **Minimal chromosome design:** `[Alert, Quarantine, KillProcess, Honeypot, RateLimit, Rollback]`
  as 6 binary genes. Fitness = `threat_eliminated - downtime_cost - action_cost - false_pos_risk`.
  The fitness function is where all domain logic lives; the GA machinery is ~15 lines.

---

### ICS Simulation Environment

- **NetworkX DiGraph is confirmed as the right tool.** 10 nodes, directed edges, node attributes
  (type, status, vulnerability, process_value, zone), edge attributes (protocol, allowed, latency_ms).
  Attack propagation = graph walk. Lateral movement = compromise node → traverse edges → compromise neighbor.

- **No existing Python library generates suitable synthetic ICS telemetry** — write our own.
  This is a feature: full control over ground truth labels (`is_anomalous`, `attack_type`).
  Borrow field naming from OCSF / Elastic ECS conventions.

- **TelemetryEvent schema:** `event_id, timestamp, source_asset, event_type, severity,
  is_anomalous, attack_type, payload`. Implemented as a Python dataclass.

- **MVP scope = ~200 lines of pure Python across 3 files:**
  - `environment/assets.py` — 10-node NetworkX DiGraph definition
  - `environment/simulator.py` — `tick()` function: choose attack or normal, mutate graph, emit events
  - `environment/attacks.py` — 6 functions (one per attack type), each returning events + mutations

- **What makes training signal "meaningful" for QUBO:** different attack combinations must suggest
  different optimal response subsets. The sim doesn't need protocol realism — just enough variation
  that there's no trivially obvious single best response.

- **Heavy tools like ICS-SimLab (containerized) and pyModbus (protocol-accurate) are overkill** for
  synthetic data generation at this scale. Pure Python is faster to build and easier to debug.

---

### Dependency Decisions (Requires Formal Approval + Decision-Log Entry Before Install)

| Dependency | Purpose | Status |
|------------|---------|--------|
| `qiskit` + `qiskit-aer` | Layer 3 quantum simulation | **Approved — Phase 4** |
| `dwave-ocean-sdk` | D-Wave Ocean SDK incl. `dwave-neal` local solver | **Approved — Phase 4** |
| `pygad` | Hot-path evolutionary optimizer | **Approved — Phase 4** (replaces DEAP) |
| `networkx` | ICS environment graph | **Approved — Phase 4** |
| `langgraph` | Agent orchestration (Layer 2+) | **Approved — Phase 4 Layer 2** |
| `DEAP` | Was planned; replaced by PyGAD | **Deferred** |
| `pennylane` | Quantum ML framework | **Deferred — not needed for QUBO** |
| `azure-quantum` | Cloud quantum provider | **Deferred** |

---

*Add new entries above this line, newest first.*
