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

### Simulation Environment

- **Ground truth signal:** Are different attack types producing meaningfully different optimal response subsets?
  If every attack suggests the same chromosome, the simulation isn't generating useful signal.
- **What "better policy" means quantitatively:** `sum(threat_eliminated) - sum(downtime_cost) - sum(false_positives)`
  across N events. Cold path goal: improve this score vs. the policy before QUBO update.

---

## Uncertainty Policy

- If a quantum result contradicts the classical brute-force result for the same small problem: **trust classical, investigate quantum**. At 6 variables, brute force is authoritative.
- If a metric can't be measured: **don't claim it**. Log what was observed; defer the claim.
- If quantum hardware introduces noise that corrupts the solution: **document it**, don't paper over it. Noise effects at Layer 4 are expected and interesting.

---

*Last updated: 2026-06-28*
