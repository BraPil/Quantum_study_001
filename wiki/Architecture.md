# Architecture

> Full detail: `docs/architecture.md` in the repository.

---

## Hot Path vs. Cold Path

| | Hot Path | Cold Path |
|--|----------|-----------|
| **When** | Real-time, per-event | Batch, every N events |
| **What** | Threat detection → GA response selection | Policy retrospection → QUBO optimization |
| **Latency target** | 5–7s (Haiku + Sonnet mix) | Minutes to hours acceptable |
| **Framework** | Raw Anthropic SDK (L1); LangGraph (L2+) | dwave-neal (local) → D-Wave Leap |
| **Output** | Best response chromosome | Updated GA fitness weights |

> **The GA↔QUBO loop is the project's core.** GA asks "best response *now*?" (hot, seconds).
> QUBO asks "best policy *across history*?" (cold, batch). QUBO results feed back into GA
> fitness weights — complementary halves of a learning loop, not competitors.

> **No quantum advantage is expected or claimed at this scale.** The value is the integration pattern.

---

## Experiment Layers (Phase 4)

Each layer must work before moving to the next.

| Layer | Name | Framework | Quantum |
|-------|------|-----------|---------|
| 1 | Agentic Security System | Raw Anthropic SDK | None |
| 2 | Evolutionary Optimizer | LangGraph + PyGAD | None (GA is classical) |
| 3 | Quantum Simulator | + Qiskit Aer | QAOA local simulation |
| 4A | D-Wave Real Backend | + dwave-ocean-sdk | Native QUBO on QPU |
| 4B | IBM Quantum Real Backend | + qiskit-ibm-runtime | QAOA on gate hardware |

---

## Agent Roster (Target)

| Agent | Role |
|-------|------|
| Observer | Ingests telemetry; detects anomalies |
| Classifier | Labels events by attack type |
| Risk Assessor | Scores threat severity |
| Response Generator | Proposes action chromosomes |
| GA Optimizer | Invokes PyGAD; selects best chromosome |
| Learning Agent | Feeds cold path; applies QUBO result to fitness weights |
| Quantum Agent *(later)* | Tool for Optimizer QUBO solves |

**Models:** Haiku 4.5 for Observer/Classifier/Risk Assessor; Sonnet 4.6 for Response Generator/Optimizer/Learning Agent.

---

## Simulated Environment

3 PLCs · 2 Workstations · 1 Historian · 1 HMI · 1 Firewall · 1 Operator

Attack scenarios: Unauthorized PLC write · Credential theft · Process kill · Ransomware · Lateral movement · USB insertion
