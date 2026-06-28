# Architecture — Quantum_Study_001

> System design, component map, data flows, and phase roadmap.
> Update this file whenever the architecture changes. Stubs are fine early.

---

## System Overview

A research system exploring where quantum computing fits best within an agentic architecture.
The core insight driving the design: **AI decides what is happening; quantum decides which combination of responses is mathematically best.**

The domain used for experimentation is a simulated cybersecurity environment (small-scale ICS/SCADA-style network), chosen because it produces discrete, combinatorial optimization problems — the natural fit for QUBO formulation.

**Important:** No quantum advantage is expected or claimed at this scale. The value is learning the integration pattern: formulate → encode → solve → extract. See `docs/evaluation.md`.

---

## Hot Path vs. Cold Path

| | Hot Path | Cold Path |
|--|----------|-----------|
| **When** | Real-time, per-event | Batch, every N events |
| **What** | Threat detection → GA response selection | Policy retrospection → QUBO optimization |
| **Latency target** | 5–7s (Haiku fast agents + Sonnet reasoning agents) | Minutes to hours acceptable |
| **Framework** | Raw Anthropic SDK (Layer 1); LangGraph (Layer 2+) | dwave-neal (local) → D-Wave Leap (cloud) |
| **Output** | Best response chromosome for this event | Updated fitness weights → better hot-path GA |

---

## The GA↔QUBO Learning Loop

This is the intellectual core of the system. The two paths are **complementary halves of a learning loop**, not alternatives:

```
GA (Hot Path) asks:  "What's the best response NOW?"  → per-event, seconds
                              ↓ logs (attack, actions, outcome, reward)
QUBO (Cold Path) asks: "What policy would have minimized harm ACROSS HISTORY?"
                              ↓ result: improved fitness weights
GA uses updated weights for better decisions next time
```

The cold-path QUBO result feeds back into the GA fitness function, making the hot path smarter over time.

---

## Component Map

```
┌──────────────────────────────────────────────────────────────┐
│                        HOT PATH                               │
│                                                               │
│  TelemetryEvent → Observer → Classifier → Risk Assessor      │
│                → Response Generator → GA Optimizer           │
│                → Recommended Response                         │
│                                                               │
│  Framework: Raw Anthropic SDK (Layer 1)                       │
│             LangGraph graph (Layer 2+)                        │
│  Models: Haiku 4.5 (Observer, Classifier, Risk Assessor)     │
│          Sonnet 4.6 (Optimizer, Learning Agent)               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                        COLD PATH                              │
│                                                               │
│  Event Buffer (N events) → Feature Extraction                 │
│  → QUBO Builder (Q matrix) → Quantum Solver                  │
│  → Updated Fitness Weights → Learning Agent                   │
│                                                               │
│  Solver: dwave-neal (local) → Qiskit Aer QAOA (Layer 3)      │
│          → D-Wave Leap (Layer 4A) / IBM Quantum (Layer 4B)   │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                      SHARED MEMORY                            │
│                                                               │
│  SQLite  — structured: event logs, GA runs, QUBO results     │
│  ChromaDB — vector: agent memory, policy embeddings          │
│  NetworkX DiGraph — environment topology (live state)        │
└──────────────────────────────────────────────────────────────┘
```

---

## Agent Roster (Experiment Phase Target)

| Agent | Model | Role |
|-------|-------|------|
| Observer | Haiku 4.5 | Ingests TelemetryEvent; detects anomalies |
| Classifier | Haiku 4.5 | Labels event by attack type |
| Risk Assessor | Haiku 4.5 | Scores threat severity and blast radius |
| Response Generator | Sonnet 4.6 | Proposes candidate action chromosomes |
| GA Optimizer | Sonnet 4.6 | Invokes PyGAD; selects best chromosome |
| Learning Agent | Sonnet 4.6 | Feeds cold path; applies QUBO result to fitness weights |
| Quantum Agent *(Layer 3+)* | — | Tool available to GA Optimizer for QUBO solve |

---

## Chromosome Design

6 binary genes representing response actions:

```
[Alert, Quarantine_PLC, Kill_Process, Deploy_Honeypot, Rate_Limit, Rollback]
  1       0               1             0               1           1
```

**Fitness function:** `threat_eliminated - downtime_cost - action_cost - false_pos_risk`

**QUBO formulation:** `Q` matrix encodes the same weights as linear/quadratic terms over the same 6 binary variables. Cold-path Q matrix is retrospectively optimized over N events.

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

**NetworkX DiGraph schema:**
```python
# Node attributes
{"type": "plc", "status": "normal", "vulnerability": 0.3,
 "process_value": 42.7, "zone": "field"}

# Edge attributes
{"protocol": "modbus", "allowed": True, "latency_ms": 2}
```

**Attack scenarios:** Unauthorized PLC write · Credential theft · Process kill · Ransomware · Lateral movement · USB insertion

**TelemetryEvent schema:**
```python
@dataclass
class TelemetryEvent:
    event_id: str          # uuid
    timestamp: datetime
    source_asset: str      # e.g. "PLC_1"
    event_type: str        # "register_write" | "login_attempt" | "process_kill" | ...
    severity: int          # 1 (info) – 5 (critical)
    is_anomalous: bool     # ground truth label
    attack_type: str|None  # None if normal
    payload: dict
```

---

## Experiment Layers (Phase 4 Sub-Phases)

Each layer must work before moving to the next.

| Layer | Name | Framework | Quantum |
|-------|------|-----------|---------|
| 1 | Agentic Security System | Raw Anthropic SDK | None |
| 2 | Evolutionary Optimizer | LangGraph + PyGAD | None (GA is classical) |
| 3 | Quantum Simulator | LangGraph + PyGAD + Qiskit Aer | QAOA local simulation |
| 4A | D-Wave Real Backend | + dwave-ocean-sdk | Native QUBO on QPU |
| 4B | IBM Quantum Real Backend | + qiskit-ibm-runtime | QAOA on gate hardware |

---

## Folder Structure (Target — Experiment Phase)

```
Quantum_Study_001/
├── agents/
│   ├── observer.py
│   ├── classifier.py
│   ├── risk_assessor.py
│   ├── response_generator.py
│   ├── optimizer.py          # invokes ga.py as a tool
│   └── learner.py
├── environment/
│   ├── assets.py             # NetworkX DiGraph definition (10 nodes)
│   ├── simulator.py          # tick() function
│   └── attacks.py            # 6 attack scenario functions
├── optimization/
│   ├── ga.py                 # PyGAD binary chromosome GA
│   ├── qubo.py               # QUBO Q matrix builder
│   ├── qiskit_solver.py      # QAOA solver (Qiskit Aer / IBM)
│   └── dwave_solver.py       # native QUBO solver (neal / D-Wave Leap)
├── memory/
│   ├── graph.py              # NetworkX environment graph wrapper
│   └── vector_store.py       # ChromaDB wrapper
├── pipeline/
│   └── hot_path.py           # Layer 1: sequential async agent pipeline
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
  Collect: (attack_type, actions_taken, outcome_score, cost)
  ↓
  Build Q matrix:
    Minimize: Risk + Downtime + False_Positives - Protection
    Encode conflict penalties as off-diagonal Q terms
  ↓
  Local test:  dwave-neal (classical SA, zero cloud)
  Layer 3:     Qiskit Aer QAOA (gate-based simulation)
  Layer 4A:    D-Wave Leap (native QUBO on real QPU)
  Layer 4B:    IBM Quantum (QAOA on real gate hardware)
  ↓
  Extract best binary solution → update GA fitness weights
  → Learning Agent persists updated weights to SQLite
```

---

*Last updated: 2026-06-28*
