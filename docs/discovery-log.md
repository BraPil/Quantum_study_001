# Discovery Log — Quantum_Study_001

> Important findings that affect future work.
> Add an entry whenever you discover something non-obvious that a future session needs to know.

---

## [2026-06-29] Phase 2 Analysis — Gaps & Remaining Risks (closes Phase 2)

Completes the analysis the QUBO-scaling probe started. The probe settled the *quantum-value* question
by measurement; this entry takes a documented position on the three design **gaps** the Discovery
spikes exposed and assesses the two **risks** the probe did not cover (6-agent latency, learning-loop
stability). Method here is reasoning, not building — per the Phase 2 runbook, genuinely open questions
are framed as Phase 3 hypotheses rather than forced to an answer now. **No production code added.**

### Gap 1 — Attack-type taxonomy (inferred vs. ground-truth label comparability)

**The gap.** In `spike_agents.py` the Classifier inferred `unauthorized_command_injection` while the
sim's ground truth (`spike_agents.py:130`) was `unauthorized_plc_write` — semantically the same event,
two different strings. Free-text agent labels and sim labels cannot be compared for scoring as-is.

**Position.** Decouple the two namespaces and score against a *canonical* set, never against raw agent
text:
- **Ground truth is a closed enum** — the 6 attack scenarios already named in `architecture.md`
  (Unauthorized PLC write · Credential theft · Process kill · Ransomware · Lateral movement · USB
  insertion). Promote these into an `AttackType` enum alongside the existing `Action` enum in the
  contracts module. This is the canonical taxonomy.
- **The agent emits free text; a thin mapping layer resolves it to the enum** (or to `UNKNOWN`). Start
  with the cheapest mechanism that works — a synonym/substring table (`"plc write" | "register write"
  | "command injection on a controller" → UNAUTHORIZED_PLC_WRITE`). Only escalate to an
  embedding-nearest-neighbour match (ChromaDB is already in the stack) if the table proves too brittle.
  Resist a second LLM "label-normalizer" agent — that adds latency and a new failure mode to dodge a
  problem a lookup table solves.
- **Granularity = exactly the 6 scenarios, no finer.** The taxonomy only needs to be as granular as the
  *response set* is: two attacks that warrant the same optimal chromosome do not need distinct labels.
  With 6 actions and 6 attack types that is already the right resolution; inventing MITRE-ATT&CK-level
  sub-techniques would add label classes that map to identical responses — taxonomy fiction.

**Why this is safe to defer to Phase 4 build.** It is a small, well-understood mapping component, not an
open research question. The position is recorded; nothing here blocks the build. The one real evaluation
subtlety — that classification *accuracy* (did the agent name the right attack?) must be scored
separately from *response quality* (was the chosen chromosome good?), so a mislabel and a bad response
don't get conflated — is logged in `evaluation.md`.

### Gap 2 — The "real" weight-update rule, and what QUBO is actually for

**The gap.** `spike_loop.py`'s `cold_path_retrospect()` is an honest placeholder: it sweeps six
hand-listed `w_downtime` candidates (`spike_loop.py:88`) and keeps the one minimising true regret on
the logged batch. It recovered the true weight, proving loop *mechanics* — but a six-value coordinate
sweep over one weight is not a learning algorithm.

**Position — separate the two optimization problems; they are not the same kind of problem.**
- **Response/policy *selection* is the QUBO.** Choosing which subset of binary actions to fire — per
  event (hot path, N≤10) or as a policy table (cold path, N≈36–100) — is genuinely a QUBO: binary
  variables, quadratic conflict/redundancy penalties (`scenario.py:34`). This is where the
  formulate→encode→solve→extract pattern lives, and it is the part worth wiring to a quantum backend.
- **The fitness-weight *update* is NOT naturally a QUBO.** The weights (`FitnessWeights`:
  threat/downtime/cost/false_pos) are **continuous**, and the loss "regret of the GA decisions these
  weights induce, summed over history" is a non-convex, non-differentiable function of them (the GA's
  argmax makes it piecewise-constant). Forcing continuous weights into QUBO would require binary
  discretisation that throws away resolution for no benefit. The right tool is **derivative-free
  continuous search over a handful of weights** — Nelder-Mead / coordinate descent / a small CMA-ES,
  or Bayesian optimisation if evaluations get expensive. The spike's coordinate sweep is the degenerate
  1-D case of exactly this; the Phase 4 version is the same idea over all four weights with a real
  search method.
- **Therefore quantum's locus is unambiguous:** the *selection* QUBO (specifically the cold-path policy
  QUBO, the only one that grows), never the weight update. This sharpens the architecture's "two QUBOs"
  framing: the learning loop is `continuous-search(weights)` on the outside wrapping `QUBO(selection)`
  on the inside — two nested optimizers, only the inner one is a QUBO, only the inner one is a quantum
  candidate.

**Open question → Phase 3.** Whether retrospective policy optimization is best expressed as *one* large
cold-path policy QUBO (condition×action table solved once) or as *weight regression* feeding the
existing per-event QUBO is a real fork. It maps onto hypotheses **H1/H2** already framed. Recorded, not
forced.

### Gap 3 — Toy-vs-real scenario fidelity (what makes training signal "meaningful")

**The gap.** `scenario.py` is one fixed threat with hand-picked per-action numbers (`_PROPS`) and three
hand-placed pairwise penalties (`_PAIR_PENALTY`). It proved GA and QUBO agree — but a single static
threat generates no *learning* signal.

**Position — fidelity is defined by signal, not by realism.** The bar a scenario must clear is *not*
protocol accuracy (Modbus byte layouts, real PLC timing); it is **decision diversity**:
1. **Different attack types must induce different optimal chromosomes.** If every attack's best response
   is the same subset, the cold path has nothing to learn and the QUBO is decorative. This is the
   single necessary property — and it is already an `evaluation.md` simulation metric ("are different
   attack types producing meaningfully different optimal response subsets?").
2. **The optimum must be non-obvious** — the quadratic penalties must occasionally make the best subset
   *exclude* a high-benefit action (the spike already shows this: quarantine is individually strong but
   dropped because its pairwise penalties dominate). A problem whose optimum is "take every beneficial
   action" needs neither GA nor QUBO.
3. **Per-attack `_PROPS` must vary enough that a miscalibrated weight produces visibly wrong decisions**
   — otherwise the learning loop (Gap 2) has no regret gradient to descend.

**How much realism is enough:** the minimum that produces properties 1–3. Concretely, the Phase 4 sim
needs (a) the 6 attack types each with a distinct `_PROPS`/penalty profile, and (b) per-event noise so
batches differ — *not* a faithful ICS protocol stack. Heavy tools (ICS-SimLab, pyModbus) remain
overkill, consistent with the Phase 1 finding. **Risk to watch:** hand-authoring 6 profiles that are
"different enough" without being arbitrary — the guard is to *measure* property 1 (distinct optima
across attacks) as an acceptance test on the sim before trusting any loop result.

### Risk A — 6-agent hot-path latency

**Likelihood of missing the 5–7s target: LOW. Impact: LOW (research system, no SLA). → Monitor, does
not block.**

**Reassessment.** The "~7s = 6 × ~1.2s" figure in the runbook assumes six *sequential* LLM hops. That
is the wrong model — two corrections drop it:
- **The critical path is ~4 LLM hops, not 6.** GA Optimizer is local PyGAD (~ms, `spike_ga.py` runs 40
  generations effectively instantly), not an LLM call — it's an LLM-invoked *tool*. The Learning Agent
  is **cold path**, off the per-event critical path entirely. So the hot-path LLM chain is Observer →
  Classifier → Risk Assessor → Response Generator.
- **Classifier and Risk Assessor parallelise.** Both consume only the Observer's output and produce
  independent fields (attack label vs. risk score/blast radius — `contracts.py:58` ResponseContext);
  neither needs the other. Run them concurrently (`asyncio.gather`). Critical path becomes Observer →
  (Classifier ∥ Risk) → Response Generator ≈ **3 sequential hops**.
- At the spike-measured ~1.2s/Haiku-agent (and Sonnet Response Generator a bit more), the realistic
  critical path is **~4–5s, inside the target** — before any streaming. Streaming the final Response
  Generator token-by-token improves *perceived* latency further but doesn't change wall-clock to the GA.

**Guard / what to monitor.** Instrument per-agent time with structlog (already the eval plan), separate
API TTFT from orchestration overhead, and treat the concurrent Classifier∥Risk structure as a design
requirement for the Layer-1 pipeline, not an optimisation. Real measurement waits for Phase 4 (the
agents don't exist yet); this is a *projected* assessment from the 2-agent spike, flagged as such.

**Note for `architecture.md`:** the hot-path latency-target row implies a straight 6-stage line; the
real shape is a small DAG with one concurrent pair and two off-critical-path stages. Documented there.

### Risk B — Learning-loop stability (GA↔QUBO divergence / oscillation / overfit)

**Likelihood of instability if built naively: MEDIUM. Impact: MEDIUM (corrupts the project's central
learning result, though not safety). → Monitor with explicit guards; does not block the build, but the
guards are mandatory, not optional.**

The spike loop is stable only because it is the easy case: one static `W_TRUE`, a single weight, a noise-
free batch, one update. Every one of those simplifications is a real failure mode when relaxed:

| Failure mode | Mechanism | Guard |
|---|---|---|
| **Batch overfit** | Cold path tunes weights to the quirks of one N-event batch; next batch differs | Hold out a validation batch; only accept a weight update if it improves regret on data it wasn't fit to (the spike already gestures at this with separate fit/fresh batches — make it a hard gate) |
| **Oscillation** | Aggressive full-replacement updates over-correct each cycle, weights ping-pong | Damp the update (apply a fraction α of the proposed change — EMA over weight history), not full replacement |
| **Feedback runaway / drift** | GA decisions change the logged distribution, which changes the next QUBO, which changes the GA… a loop with no anchor can drift | Anchor to ground-truth regret (the sim knows true harm), and **gate on monotonic improvement**: reject any update that worsens held-out regret, keep last-good weights |
| **Degenerate signal** | If Gap 3 isn't satisfied (attacks don't induce distinct optima), the loop "learns" noise | Acceptance test on the sim (Gap 3, property 1) *before* trusting loop output |
| **GA stochasticity masquerading as learning** | PyGAD is seeded per-event in the spike; unseeded, run-to-run variance could be misread as a weight effect | Fix/average seeds when attributing a regret change to a weight change |

**The unifying guard** is one principle: **the loop must be evaluated against held-out, ground-truth-
anchored regret, and updates must be monotonic-or-rejected with damping.** That converts an open-loop
amplifier into a controlled one. This is a Phase 3 hypothesis candidate in disguise — "does the damped,
held-out-gated loop converge and stay converged across K cycles?" is exactly an experiment to design,
and a natural extension of `spike_loop.py` (iterate the loop K times, vary the batch, plot regret).

### Net effect on Phase 2 success criteria

All three gaps now have a documented position; both remaining risks are assessed (likelihood, impact,
block-vs-monitor) with named guards. Neither risk blocks the build. Two items are deliberately carried
forward as Phase 3 hypotheses rather than forced shut: the policy-QUBO-vs-weight-regression fork (Gap 2)
and the loop-stability convergence experiment (Risk B). Architecture/evaluation notes updated where the
analysis changed a documented assumption (latency DAG; classification-accuracy-vs-response-quality
scoring split). Phase 2 is ready to close pending Brandt's sign-off.

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
