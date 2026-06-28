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

## [2026-06-28] Phase 0 Research Outcomes — Revised Experiment-Phase Stack

**Context:** Five parallel research agents surveyed quantum foundations, backends, agent orchestration,
evolutionary optimization, and ICS simulation. The following decisions supersede the "Anticipated
Experiment-Phase Dependencies" entry above.

---

### Layer 4 Backend: D-Wave Leap (Primary) + IBM Quantum (Secondary)

**Decision:** Replace IBM Quantum as the primary Layer 4 backend with D-Wave Leap. IBM Quantum retained as Layer 4B.

**Rationale:**
- D-Wave's native input format is QUBO/Ising — no QAOA circuit construction needed. Hand it a Q dict, get back binary solutions.
- IBM Quantum requires encoding QUBO as a QAOA variational circuit + Hamiltonian formulation — more complex and performs worse on optimization benchmarks vs. D-Wave.
- D-Wave Advantage2 available. Leap LaunchPad offers 3-month free trial; apply at Phase 4 start.
- IBM Quantum retains value for learning gate-based QC fundamentals (QAOA, circuit construction). 10 min/month free.

**Alternatives considered:** Azure Quantum (D-Wave left in 2023, no native annealing), PennyLane (better for quantum ML than QUBO optimization) — both deferred.

---

### Local QUBO Testing: dwave-neal (Included in dwave-ocean-sdk)

**Decision:** Add `dwave-ocean-sdk` as an approved experiment-phase dependency. Includes `dwave-neal` (classical simulated annealing QUBO solver).

**Rationale:**
- `dwave-neal` runs QUBO locally with zero cloud dependency using the identical API as real D-Wave hardware.
- Swap the sampler (`neal.SimulatedAnnealingSampler` → `DWaveSampler`) to move from local testing to real hardware.
- Validates QUBO formulations before spending QPU minutes on cloud hardware.

---

### Hot-Path Optimizer: PyGAD (Replaces DEAP)

**Decision:** Use `pygad` instead of `DEAP` for the evolutionary optimizer.

**Rationale:**
- PyGAD delivers a working binary chromosome GA in ~20 lines vs. DEAP's verbose creator/toolbox setup.
- 4-5x faster execution. Cleaner API. Python 3.12 compatible.
- DEAP reserved as an upgrade if multi-objective optimization (NSGA-II, Pareto fronts across threat/cost/downtime) is needed in a later phase.

---

### Agent Orchestration: Raw Anthropic SDK (Layer 1), LangGraph (Layer 2+)

**Decision:** Start Layer 1 with raw Anthropic SDK + async Python. Introduce LangGraph at Layer 2.

**Rationale:**
- Layer 1 is a fixed sequential 6-agent pipeline. Raw SDK = each agent is a plain async function. No framework overhead, no magic, all logic visible. Maximum educational clarity.
- LangGraph (1.2, stable) justified at Layer 2 when the Evolutionary Optimizer requires conditional branching, retry logic, and state persistence. ~120ms/node overhead, 30-40% fewer tokens than CrewAI.
- Hot path latency reality: 6 sequential Anthropic API calls ≈ 5-7s using Haiku for fast agents + Sonnet for reasoning-heavy agents. Bottleneck is API TTFT, not orchestration.
- Model-per-agent strategy: Haiku 4.5 for Observer/Classifier/Risk Assessor; Sonnet 4.6 for Optimizer/Learning Agent.

**Deferred:** CrewAI (role-based model doesn't fit typed sequential pipeline), AutoGen (conversation-based, harder to reason about), PydanticAI (noted for re-evaluation at Layer 2 as LangGraph alternative).

---

### ICS Simulation: Pure Python + NetworkX DiGraph

**Decision:** Build the simulation environment from scratch in ~200 lines of pure Python using NetworkX for graph modeling.

**Rationale:**
- No existing Python library generates synthetic ICS telemetry with ground-truth labels suitable for this project.
- Heavy tools (ICS-SimLab, pyModbus) are overkill — protocol accuracy isn't needed for synthetic training data.
- NetworkX DiGraph with node attributes (type, status, vulnerability, zone) and edge attributes (protocol, allowed, latency_ms) is sufficient for modeling attack propagation as a graph walk.
- Full control over ground truth labels (`is_anomalous`, `attack_type`) is a feature, not a limitation.
- TelemetryEvent as a Python dataclass with OCSF-inspired field naming.

---

### Quantum Advantage — Honest Framing

**Decision:** Document explicitly that quantum advantage is not expected or claimed at the scale of this project.

**Rationale:**
- For 6-10 binary variables, brute-force classical search checks 64-1024 combinations in microseconds.
- March 2025 Physical Review A paper: no quantum advantage demonstrated in current combinatorial optimization methods.
- The project value is learning the integration pattern (formulate → encode → solve → extract), not outperforming classical solvers.
- This framing must appear in `docs/evaluation.md` and any project presentations.

---

### Formally Approved Experiment-Phase Dependencies

Supersedes the "Anticipated" entry above. These are approved for addition to `requirements.txt` at Phase 4 start.

| Dependency | Phase | Purpose |
|------------|-------|---------|
| `qiskit` + `qiskit-aer` | Phase 4 Layer 3 | Gate-based quantum simulation (QAOA) |
| `dwave-ocean-sdk` | Phase 4 Layer 3–4 | QUBO local testing (neal) + D-Wave hardware |
| `pygad` | Phase 4 Layer 2 | Hot-path binary chromosome GA |
| `networkx` | Phase 4 Layer 1 | ICS environment graph |
| `langgraph` | Phase 4 Layer 2+ | Agent orchestration (conditional branching) |

---

## [2026-06-28] Phase Transition: Exploration → Discovery

**Decision:** Phase 0 (Exploration) marked COMPLETE. Phase 1 (Discovery) is now active. Approved by Brandt.

**Rationale:**
- All five Phase 0 success criteria met (see `runbooks/phase-0-exploration.md`).
- The hot/cold path + quantum optimization architecture is validated as the right learning vehicle.
- The experiment-phase stack is decided and the tools are researched. Discovery now moves from "is this the right approach?" to "how exactly do the pieces connect, and do they actually work?"

**Phase 1 focus:** Pin down integration points (data contracts/interfaces between layers) and build small proof-of-concept spikes for the highest-risk integrations before committing to the full Phase 4 build.

---

## [2026-06-28] Phase Transition: Discovery → Analysis

**Decision:** Phase 1 (Discovery) marked COMPLETE. Phase 2 (Analysis) is now active. Approved by Brandt.
Phase 0 + Phase 1 work merged to `main`; Phase 2 proceeds on branch `phase/2-analysis`.

**Rationale:**
- All seven Phase 1 success criteria met (see `runbooks/phase-1-discovery.md`). Every high-risk
  integration is proven wireable with running code: data contracts, GA, QUBO, the GA↔QUBO learning
  loop, and a live raw-SDK agent pipeline.
- Discovery surfaced concrete gaps and risks that must be analyzed before designing the experiment
  (Phase 3) and building it (Phase 4). Analysis is where we reason about those, not paper over them.

**Phase 2 focus:** Analyze the gaps and risks the spikes revealed — attack-type taxonomy, the
placeholder weight-update rule, toy-vs-real scenario fidelity, 6-agent latency, and QUBO scaling
beyond the toy 6-variable problem — and revise architectural assumptions accordingly.

---

*Add new entries above this line, newest first.*
