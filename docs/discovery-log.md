# Discovery Log — Quantum_Study_001

> Important findings that affect future work.
> Add an entry whenever you discover something non-obvious that a future session needs to know.

---

## [2026-06-28] Phase 2 Analysis — QUBO Scaling: Where (and Whether) Quantum Helps

**Probe:** `spikes/probe_qubo_scaling.py` — structured random QUBOs (sparse pairwise terms, like
our scenario writ large) solved at increasing variable count N by exhaustive brute force (where
feasible) and by the local simulated-annealing (SA) sampler. Measured BF time, SA time, SA optimality
gap vs. ground truth, and two-seed SA self-consistency. Guarded by `test_scaling_probe_sa_matches_brute_force`.

### Data

| N | search space 2^N | BF time | SA time | SA vs BF | 2-seed |
|---|------------------|---------|---------|----------|--------|
| 6  | 64                  | 0.000s | 0.02s | optimal | agree |
| 14 | 16,384              | 0.005s | 0.06s | optimal | agree |
| 18 | 262,144             | 0.106s | 0.11s | optimal | agree |
| 20 | 1,048,576           | 0.550s | 0.06s | optimal | agree |
| 24 | 16,777,216          | infeasible | 0.07s | (unverifiable) | agree |
| 30 | 1.07×10⁹            | infeasible | 0.08s | (unverifiable) | agree |
| 40 | 1.10×10¹²           | infeasible | 0.14s | (unverifiable) | agree |
| 60 | 1.15×10¹⁸           | infeasible | 0.18s | (unverifiable) | agree |

### What it shows

1. **Brute force dies fast.** BF time is exponential (~5× per +2 variables): 0.1s at N=18, 0.55s at
   N=20, and beyond ~N=22–25 it is infeasible. This is the naive intuition for "when you need
   something cleverer."
2. **But classical SA fills the gap completely.** SA stays **sub-200ms even at N=60** (a search space
   of 10¹⁸), and where brute force can verify (N≤20) SA is **exactly optimal**. Beyond that, two
   independent SA seeds agree at every size — a (weak) signal that SA has converged, not just guessed.
3. **Therefore "brute force is infeasible" is NOT the bar for quantum.** The bar is "even good
   *classical heuristics* struggle." On the kind of structured, sparse problem this domain produces,
   they don't — SA is cheap and (where checkable) optimal far past where exhaustive search dies.

### The two-QUBO distinction (the key analytical insight)

The architecture has two different optimization problems, and they sit at very different scales:

- **Per-event response selection (hot path).** The action space is ~6–10 actions. This QUBO is
  **N ≤ 10 forever** — there is no growth path. It is trivially classical; quantum is never warranted
  here. (The GA already handles it; QUBO would too. Neither needs to be quantum.)
- **Cold-path policy retrospection.** This is the only place N can grow: a policy of
  "(condition) → (action subset)" over, say, 6 attack-types × ~6 actions reaches N≈36, and a richer
  context could push N to ~100. **This is the project's only candidate for an "interesting" QUBO.**
  But the probe shows classical SA solves N=60 in 0.18s — so even the rich cold-path policy QUBO is
  not, on performance grounds, a problem that needs quantum.

### Sharpened answer to the project's central question

*"Where does quantum actually add value in this architecture?"* — Based on this analysis, the honest
answer is: **at the scale this domain naturally produces, quantum adds no performance value. Its value
here is pedagogical and architectural** — learning the formulate → encode → solve → extract pattern,
and building the hot/cold plumbing so a quantum solver is a drop-in (`SimulatedAnnealingSampler` →
`DWaveSampler`) if a genuinely hard, large instance ever arises. This is consistent with the Phase 0
research conclusion and now backed by local measurement, not just literature.

This is not the exciting answer, but it is the true one, and it directly serves the project's stated
goal ("see where quantum is best used"). The finding *is* the value: for combinatorial response
optimization at ICS scale, the right tool is a classical heuristic; quantum's niche lies in larger or
structurally harder problems than this domain generates.

### Limitations (stated honestly)

- Random sparse QUBOs may be "easy" instances. Quantum advantage is claimed on specific *hard*
  instances (frustrated couplings / spin-glass landscapes), which these are not — and which this
  domain does not naturally produce. That asymmetry is itself the point, but it means the probe shows
  "classical is sufficient *here*," not "classical always wins."
- SA optimality is ground-truth-verified only to N=20. Beyond that we have self-consistency, not proof.
- One solver (SA) on one machine; not a hardware benchmark.

### Candidate hypotheses for Phase 3 (where this points next)

- **H1:** If the cold-path policy QUBO is deliberately constructed with frustrated/spin-glass-like
  couplings (not the natural sparse structure), classical SA degrades and a quantum annealer's
  solution quality or time-to-solution becomes distinguishable. *(Tests whether quantum can be made
  to matter here at all — even if artificially.)*
- **H2:** The pedagogical value is real and measurable: a quantum-solved cold path produces the *same*
  policy update as the classical path (correctness parity), proving the integration is sound. *(Tests
  the plumbing, which is the honest deliverable.)*
- **H3:** Hot-path response selection never benefits from quantum at any realistic action-space size.
  *(Likely already settled by this probe; Phase 3 may simply confirm and close it.)*

---

## [2026-06-28] Phase 1 Discovery — Integration Spikes

Built throwaway proof-of-concept spikes in `spikes/` to de-risk the highest-risk integrations
before the Phase 4 build. All deterministic spikes pass and are guarded by `tests/test_spikes.py`.

### Findings

- **`neal` package is deprecated — API moved.** Phase 0 research cited the standalone `dwave-neal`
  package. Running it revealed `ModuleNotFoundError`. The current Ocean SDK exposes the
  simulated-annealing sampler at `dwave.samplers.SimulatedAnnealingSampler`. Same role, and it's a
  drop-in swap for `EmbeddingComposite(DWaveSampler())` to move to real hardware. **This is exactly
  why Discovery builds spikes — "researched" ≠ "runs here."** Docs updated accordingly.

- **Layer data contracts defined and validated** (`spikes/contracts.py`): TelemetryEvent →
  ResponseContext → Chromosome → FitnessWeights. Key design decision baked in: agents see only
  non-ground-truth fields of an event (they must *infer* `attack_type`/`is_anomalous`, the sim knows
  them). Chromosome is the shared currency of GA and QUBO with a fixed 6-action bit ordering.

- **GA and QUBO agree with brute-force ground truth.** On the toy 6-action problem both independently
  select `[alert, kill_process, deploy_honeypot, rate_limit]` and both correctly *avoid* quarantine
  because its pairwise penalties (with kill_process and honeypot) outweigh its standalone benefit.
  This confirms the quadratic QUBO term does real work — the problem isn't trivially separable.
  Satisfies the `evaluation.md` sanity check (quantum/SA result must match classical at small scale).

- **The GA↔QUBO learning loop closes end-to-end.** Spike (`spike_loop.py`): hot-path GA runs a batch
  with a deliberately miscalibrated downtime weight (0.5 vs. true 2.0), logging decisions to SQLite.
  Cold path reads the batch, retrospectively searches weight candidates, and recovers the true weight
  (2.0) — driving mean regret from 0.92 to 0.00 on a fresh batch. **Proves the hot → store → cold →
  feedback handoff is wireable**, including the SQLite persistence boundary. (Scope: the weight-update
  rule is a transparent coordinate search, not a proposed Phase 4 learning algorithm — the spike
  proves loop mechanics, not an optimal learner.)

- **PyGAD 3.7.0 and dwave-ocean-sdk (dimod 0.12.22) confirmed working** in this environment.
  Installed via `spikes/requirements-spikes.txt` (kept separate from root requirements — spikes are
  throwaway). PyGAD needs `suppress_warnings=True` and `random_seed=` for reproducible runs.

- **Agent-pipeline spike RAN successfully** (`spike_agents.py`, raw-SDK Observer→Classifier on
  Haiku 4.5). Real measured latency: **Observer 1.65s + Classifier 0.75s = 2.40s for 2 agents**
  (~1.2s/agent). Extrapolated to the 6-agent roster ≈ **7s**, consistent with the Phase 0 estimate
  of 5–7s. The raw-SDK + plain-async pattern is confirmed for Layer 1 — no framework needed.
  - **Contract design validated against a live model:** agents were shown only the non-ground-truth
    event fields and correctly inferred the threat (`unauthorized_command_injection`, risk 0.92,
    blast 3) without ever seeing the sim's `attack_type`/`is_anomalous`. The "agents infer, sim
    knows" boundary works.
  - Note: agent's inferred label (`unauthorized_command_injection`) differs in wording from the sim's
    ground-truth label (`unauthorized_plc_write`) though semantically equivalent. Phase 4 will need a
    canonical attack-type taxonomy so inferred and ground-truth labels are comparable for scoring.

### Status vs. Phase 1 Success Criteria

| Criterion | Status |
|-----------|--------|
| Layer data contracts defined | ✅ `contracts.py` |
| QUBO solve works locally (dwave) | ✅ `spike_qubo.py` |
| PyGAD GA runs | ✅ `spike_ga.py` |
| 2-agent raw-SDK pipeline | ✅ `spike_agents.py` — ran live, 2.40s/2 agents |
| GA↔QUBO handoff demonstrated | ✅ `spike_loop.py` |
| Approved tools confirmed working | ✅ pygad, dwave-ocean-sdk, anthropic (live call confirmed) |
| Findings recorded | ✅ this entry |

**All 7 Phase 1 success criteria met.** New Phase 4 to-do surfaced: define a canonical attack-type
taxonomy so agent-inferred labels are comparable to ground-truth labels for scoring.

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
