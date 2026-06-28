# Phase Roadmap

---

## Status

| Phase | Name | Status |
|-------|------|--------|
| 0 | Exploration | ✅ Complete |
| 1 | Discovery | 🔄 IN PROGRESS |
| 2 | Analysis | ⬜ Not Started |
| 3 | Hypothesis | ⬜ Not Started |
| 4 | Experiment | ⬜ Not Started |
| └─ Layer 1 | Agentic Security System | ⬜ |
| └─ Layer 2 | Evolutionary Optimizer | ⬜ |
| └─ Layer 3 | Quantum Simulator | ⬜ |
| └─ Layer 4 | Real Quantum Backend | ⬜ |
| 5 | Results | ⬜ Not Started |
| 6 | Conclusion | ⬜ Not Started |

---

## Phase Descriptions

**Phase 0 — Exploration** ✅
Got informed on industry processes, capabilities, and best practices. Validated the hot/cold path + quantum optimization architecture as the right approach. See [[Discovery-Log]] for outcomes and [[Phase-0-Exploration]] for the completed runbook.

**Phase 1 — Discovery** 🔄
Pin down exact integration points (data contracts between layers) and build small proof-of-concept spikes for the highest-risk integrations (QUBO solve, GA, agent pipeline, GA↔QUBO loop). See [[Phase-1-Discovery]].

**Phase 2 — Analysis**
Analyze what was discovered. Gaps, risks, revised assumptions.

**Phase 3 — Hypothesis**
Form testable hypotheses about where quantum adds value. Define experiment design.

**Phase 4 — Experiment**
Build and test in four layers (see Architecture). This is where ~90% of the implementation work occurs.

**Phase 5 — Results**
Capture and document experiment outcomes objectively.

**Phase 6 — Conclusion**
Draw conclusions about quantum/agentic integration. What worked, what didn't, what's next.

---

## Phase Discipline

Do not implement features belonging to a later phase until the current phase's success criteria are met. Phase transition requires Brandt's explicit sign-off.
