# Evaluation — Quantum_Study_001

> AI/ML eval methodology, benchmark tracking, uncertainty policy.

---

## Quantum Advantage — Honest Policy

**This project does not claim quantum advantage. Do not imply it.**

For 6–10 binary variables, brute-force classical search evaluates 64–1024 combinations in microseconds.
A March 2025 Physical Review A paper found no quantum advantage demonstrated in current combinatorial
optimization methods. D-Wave demonstrated advantage specifically for magnetic spin glass problems
(May 2025) — not general QUBO at this scale.

**The project's value is the integration pattern:**
- Formulate a combinatorial problem as QUBO
- Encode and solve it on a quantum or quantum-adjacent solver
- Extract a binary solution and apply it
- Build the plumbing so that when problem scale grows, the quantum path is already wired

This framing must appear consistently in any documentation, notebooks, or presentations.

**Local evidence (Phase 2, `spikes/probe_qubo_scaling.py`):** Exhaustive brute force becomes
infeasible around N≈22 variables, but the *classical* simulated-annealing solver stays sub-200ms and
self-consistent out to N=60 (search space 10¹⁸), and is exactly optimal everywhere ground truth is
checkable (N≤20). So the bar for quantum is **not** "brute force is infeasible" — it is "even good
*classical heuristics* struggle," which does not occur at any scale this domain naturally produces.
The two QUBOs in the architecture both sit comfortably in the classical-heuristic regime: per-event
response selection is N≤10 forever; cold-path policy retrospection reaches at most N≈100 and SA solves
N=60 in 0.18s. **Quantum's value here is therefore correctness-of-integration, not speed.** See
`docs/discovery-log.md` [2026-06-28] Phase 2 Analysis for the full reasoning and limitations.

---

## Metrics — To Be Defined in Phase 3 (Hypothesis)

### Hot Path (GA Optimizer)

Key questions to answer before Phase 4:

- **Fitness convergence:** Does the GA converge to a stable best chromosome within N generations?
  What is N for 6 binary variables? (Likely very fast — monitor to confirm.)
- **Response quality:** Does the recommended chromosome actually reduce the simulated threat score?
  Ground truth: compare threat state before/after applying the response in simulation.
- **Latency:** Does the hot path complete within the 5–7s target?
  Instrument per-agent time via structlog. Break down API TTFT vs. orchestration overhead.

### Cold Path (QUBO Optimizer)

- **Solution quality vs. classical:** Does QUBO output match or improve on brute-force classical search
  for 6 variables? (It should — use this as a sanity check, not a benchmark of quantum superiority.)
- **dwave-neal vs. Qiskit Aer vs. D-Wave Leap:** Compare solution quality and time across all three
  solvers for the same Q matrix. Document differences.
- **Policy improvement:** After applying QUBO-updated fitness weights to the GA, does the next round
  of hot-path decisions score higher? This is the learning loop metric.

### Scoring — keep classification accuracy and response quality separate (Phase 2 analysis)

Two distinct things must be scored independently, never conflated:
- **Classification accuracy** — did the agent's *inferred* attack label resolve to the correct
  ground-truth `AttackType`? Scored against a **canonical closed enum** (the 6 scenarios), not raw agent
  free-text. A thin synonym/substring (→ ChromaDB nearest-neighbour if needed) mapping layer normalises
  the agent's free text to the enum; no second LLM "normalizer" agent. Taxonomy granularity = the 6
  scenarios, no finer (no label class should map to an identical optimal response).
- **Response quality** — was the chosen chromosome good (true threat reduction net of cost)?

A mislabel and a bad response are different failures with different fixes; a combined score hides which
one occurred. See `docs/discovery-log.md` [2026-06-29] Gap 1.

### Simulation Environment

- **Ground truth signal:** Are different attack types producing meaningfully different optimal response subsets?
  If every attack suggests the same chromosome, the simulation isn't generating useful signal.
  **(Phase 2: this is the single necessary "fidelity" property — make it an acceptance test on the sim
  *before* trusting any learning-loop result. Realism beyond this, e.g. protocol accuracy, is not
  required. See discovery-log [2026-06-29] Gap 3.)**
- **What "better policy" means quantitatively:** `sum(threat_eliminated) - sum(downtime_cost) - sum(false_positives)`
  across N events. Cold path goal: improve this score vs. the policy before QUBO update.

---

## Uncertainty Policy

- If a quantum result contradicts the classical brute-force result for the same small problem: **trust classical, investigate quantum**. At 6 variables, brute force is authoritative.
- If a metric can't be measured: **don't claim it**. Log what was observed; defer the claim.
- If quantum hardware introduces noise that corrupts the solution: **document it**, don't paper over it. Noise effects at Layer 4 are expected and interesting.

---

*Last updated: 2026-06-29*
