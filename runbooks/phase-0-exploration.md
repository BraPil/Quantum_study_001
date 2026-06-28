# Runbook — Phase 0: Exploration

> Operational guide for the Exploration phase of Quantum_Study_001.
> This phase ends when both success criteria below are met and Brandt signs off on phase transition.

---

## Phase Goal

Validate the approach before committing to building anything. Emerge with:
1. Informed understanding of quantum computing capabilities, limitations, and best-fit use cases in agentic systems
2. Confidence (or redirected plan) that the hot/cold path + quantum optimization architecture is the right learning vehicle

---

## Success Criteria

- [x] Can articulate where quantum computing adds genuine value vs. where classical is sufficient
      → *Finding: no quantum advantage at 6-10 var scale; value is the integration pattern. See discovery-log.*
- [x] Have surveyed at least 3 real quantum frameworks/backends (e.g., Qiskit, Cirq, D-Wave Ocean, PennyLane) and can compare them for this use case
      → *Surveyed Qiskit/IBM, D-Wave Leap/Ocean, Azure Quantum, PennyLane. D-Wave is the native QUBO choice.*
- [x] Hot/cold path architecture validated against at least one credible external reference or practitioner resource
      → *Validated. GA(hot)↔QUBO(cold) confirmed complementary by research (arxiv 2405.09272).*
- [x] Evolutionary optimizer confirmed as a viable approach for combinatorial response selection
      → *Confirmed. PyGAD selected over DEAP for the binary chromosome GA.*
- [x] Decision made on experiment-phase dependencies — approved or replaced
      → *Approved: qiskit/qiskit-aer, dwave-ocean-sdk, pygad, networkx, langgraph. DEAP replaced by PyGAD; PennyLane/Azure deferred.*

---

## Research Agenda

### 1. Quantum Foundations for this Use Case
- What is QUBO? How are problems formulated as QUBO? What types of problems benefit?
- What is the current state of quantum hardware (gate-based vs. annealing)?
- What is "quantum advantage" and is it achievable for problems at this scale?
- Key resources: Qiskit documentation, D-Wave QUBO primer, IBM Quantum Learning

### 2. Agentic + Quantum Integration Patterns
- How have others connected classical agent systems to quantum solvers?
- What does a realistic hot/cold path look like in practice?
- Is LangGraph the right orchestration layer? Alternatives: CrewAI, raw async, custom graph

### 3. Evolutionary Optimization
- DEAP: capabilities, limitations, fit for combinatorial response selection
- What does a "chromosome" representing a security response set look like?
- Fitness function design: threat eliminated + low downtime + low cost + low false positives

### 4. Simulation Environment
- What minimal simulation is needed to generate meaningful training signal?
- Can a NetworkX graph adequately model the small ICS environment?
- What attack scenarios produce the most interesting QUBO structures?

### 5. Backend Evaluation
- Qiskit Aer (local simulator) — capabilities, QUBO support via QAOA
- IBM Quantum (cloud gate-based) — access model, queue times, qubit limits
- D-Wave Leap (cloud annealer) — native QUBO support, access model
- Azure Quantum — hybrid options

---

## Exploration Activities

| Activity | Output | Notes |
|----------|--------|-------|
| Literature / doc survey | Notes in `docs/discovery-log.md` | Cite sources with URLs |
| Framework comparisons | Entries in `docs/decision-log.md` | Record what was evaluated |
| Architecture validation | Updated `docs/architecture.md` | Correct any stubs |
| Dependency approval | Decision-log entry per dep | Required before any install |
| Phase 0 → 1 sign-off | Brandt explicit confirmation | Must meet all success criteria |

---

## Session Protocol for This Phase

1. `git status && git log --oneline -5` — orient
2. Check `docs/discovery-log.md` — don't repeat prior research
3. Define the specific question for this session before starting
4. Record findings in discovery-log immediately — don't lose them
5. If a finding changes the architecture, update `docs/architecture.md`
6. If a finding changes a technology choice, update `docs/decision-log.md`

---

## Definition of Done (Phase 0)

All success criteria above checked. Brandt reviews and explicitly approves transition to Phase 1 (Discovery). At that point:
- Update `CLAUDE.md` Phase Status: Exploration → ✅ COMPLETE, Discovery → 🔄 IN PROGRESS
- Create `runbooks/phase-1-discovery.md`
- Record the phase transition in `docs/decision-log.md`

---

*Created: 2026-06-28 | Owner: Brandt Pileggi*
