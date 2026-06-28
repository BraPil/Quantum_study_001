# Architecture — Quantum_Study_001

> System design, component map, data flows, and phase roadmap.
> Update this file whenever the architecture changes. Stubs are fine early.

---

## System Overview

A research system exploring where quantum computing fits best within an agentic architecture.
The core insight driving the design: **AI decides what is happening; quantum decides which combination of responses is mathematically best.**

The domain used for experimentation is a simulated cybersecurity environment (small-scale ICS/SCADA-style network), chosen because it produces discrete, combinatorial optimization problems — the natural fit for quantum speedup.

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

## Component Map

```
┌─────────────────────────────────────────────────────┐
│                     HOT PATH                         │
│                                                      │
│  Telemetry → Observer Agent → Classifier Agent       │
│           → Risk Assessor → Response Generator       │
│           → Evolutionary Optimizer → Response        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                     COLD PATH                        │
│                                                      │
│  Event Buffer (N events) → Feature Extraction        │
│  → QUBO Builder → Quantum Solver (Qiskit/Backend)    │
│  → Policy Update → Learning Agent                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                  SHARED MEMORY                       │
│                                                      │
│  SQLite (structured: runs, results, event logs)      │
│  ChromaDB (vector: agent memory, embeddings)         │
│  NetworkX graph (environment topology)               │
└─────────────────────────────────────────────────────┘
```

---

## Agent Roster (Experiment Phase Target)

| Agent | Role |
|-------|------|
| Observer | Ingests telemetry; detects anomalies |
| Classifier | Labels events by attack type |
| Risk Assessor | Scores threat severity and blast radius |
| Response Generator | Proposes action chromosomes |
| Optimizer | Runs evolutionary algorithm; selects best response |
| Learning Agent | Feeds cold path; updates policy from quantum results |
| Quantum Agent *(later)* | Tool available to Optimizer for QUBO solve |

---

## Simulated Environment (Small World)

To keep debugging tractable:

| Asset | Count |
|-------|-------|
| PLCs | 3 |
| Workstations | 2 |
| Historian | 1 |
| HMI | 1 |
| Firewall | 1 |
| Operator (persona) | 1 |

**Attack scenarios modeled:**
- Unauthorized PLC write
- Credential theft
- Process kill
- Ransomware
- Lateral movement
- USB insertion

---

## Experiment Layers (Phase 4 Sub-Phases)

Each layer must work before moving to the next.

| Layer | Name | Description |
|-------|------|-------------|
| 1 | Agentic Security System | Hot path classical agents; no quantum |
| 2 | Evolutionary Optimizer | DEAP genetic algorithm replaces hardcoded priorities |
| 3 | Quantum Simulator | Qiskit Aer solves QUBO locally |
| 4 | Real Quantum Backend | IBM Quantum / Azure Quantum / D-Wave |

---

## Folder Structure (Target — Experiment Phase)

```
Quantum_Study_001/
├── agents/
│   ├── observer.py
│   ├── classifier.py
│   ├── risk_assessor.py
│   ├── response_generator.py
│   ├── optimizer.py
│   └── learner.py
├── environment/
│   ├── simulator.py
│   ├── attacks.py
│   └── assets.py
├── optimization/
│   ├── ga.py           # genetic algorithm (DEAP)
│   ├── qubo.py         # QUBO problem builder
│   └── qiskit_solver.py
├── memory/
│   ├── graph.py        # NetworkX environment graph
│   └── vector_store.py # ChromaDB wrapper
├── docs/
├── tests/
├── notebooks/
└── CLAUDE.md
```

*This structure is aspirational for Phase 4. Implement only what the current phase requires.*

---

## Data Flow (Cold Path Detail)

```
Every N events:
  Collect: attack features + actions taken + result + reward
  ↓
  Bundle → QUBO formulation
  "Could there have been a better policy?"
  ↓
  Minimize: Risk + Downtime + False Positives - Protection
  ↓
  Send to Qiskit Aer (Layer 3) or real backend (Layer 4)
  ↓
  Result → update policy weights → Learning Agent
```

---

*Last updated: 2026-06-28*
