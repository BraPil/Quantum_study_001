# Architecture

> Full detail: `docs/architecture.md` in the repository.

---

## Hot Path vs. Cold Path

| | Hot Path | Cold Path |
|--|----------|-----------|
| **When** | Real-time, per-event | Batch, every N events |
| **What** | Threat detection → response selection | Policy retrospection → quantum optimization |
| **Latency target** | < a few seconds | Minutes to hours acceptable |
| **Technology** | Classical agents (LangGraph) | QUBO formulation → Qiskit / quantum backend |
| **Output** | Recommended response action | Improved policy weights / evolved strategy |

---

## Experiment Layers (Phase 4)

Each layer must work before moving to the next.

| Layer | Name | Description |
|-------|------|-------------|
| 1 | Agentic Security System | Hot path classical agents; no quantum |
| 2 | Evolutionary Optimizer | DEAP genetic algorithm replaces hardcoded priorities |
| 3 | Quantum Simulator | Qiskit Aer solves QUBO locally |
| 4 | Real Quantum Backend | IBM Quantum / Azure Quantum / D-Wave |

---

## Agent Roster (Target)

| Agent | Role |
|-------|------|
| Observer | Ingests telemetry; detects anomalies |
| Classifier | Labels events by attack type |
| Risk Assessor | Scores threat severity |
| Response Generator | Proposes action chromosomes |
| Optimizer | Runs evolutionary algorithm |
| Learning Agent | Feeds cold path; updates policy |
| Quantum Agent *(later)* | Tool for Optimizer QUBO solves |

---

## Simulated Environment

3 PLCs · 2 Workstations · 1 Historian · 1 HMI · 1 Firewall · 1 Operator

Attack scenarios: Unauthorized PLC write · Credential theft · Process kill · Ransomware · Lateral movement · USB insertion
