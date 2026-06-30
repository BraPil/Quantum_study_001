# Phase Roadmap

---

## Status

| Phase | Name | Status |
|-------|------|--------|
| 0 | Exploration | ✅ Complete |
| 1 | Discovery | ✅ Complete |
| 2 | Analysis | ✅ Complete |
| 3 | Hypothesis | 🔄 IN PROGRESS |
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

**Phase 1 — Discovery** ✅
Pinned down layer data contracts and built proof-of-concept spikes for every high-risk integration (QUBO solve, GA, agent pipeline, GA↔QUBO loop). All ran. See [[Phase-1-Discovery]] and [[Discovery-Log]].

**Phase 2 — Analysis** ✅
Analyzed the gaps and risks the spikes surfaced and revised architectural assumptions. Sharpened the central question by measurement: at this domain's scale quantum adds no performance value — value is pedagogical/architectural. See [[Phase-2-Analysis]] and [[Discovery-Log]].

**Phase 3 — Hypothesis** 🔄
Formalize the Analysis-surfaced candidates into testable hypotheses (H1 hard-instance distinguishability, H2 correctness parity, H3 hot-path-never), resolve the two open forks (policy-QUBO vs. weight-regression; damped loop convergence), and produce the Phase 4 experiment design. See [[Phase-3-Hypothesis]].

**Phase 4 — Experiment**
Build and test in four layers (see Architecture). This is where ~90% of the implementation work occurs.

**Phase 5 — Results**
Capture and document experiment outcomes objectively.

**Phase 6 — Conclusion**
Draw conclusions about quantum/agentic integration. What worked, what didn't, what's next.

---

## Phase Discipline

Do not implement features belonging to a later phase until the current phase's success criteria are met. Phase transition requires Brandt's explicit sign-off.
