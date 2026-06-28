# CLAUDE.md — Quantum_Study_001

> Governs every AI coding session in this repository.
> Read before touching any file. Keep lean — depth lives in companion docs.
> **When this file conflicts with the code, the code wins. Update this file immediately.**

---

## 0. Ecosystem Map

| Companion File | Governs |
|----------------|---------|
| `docs/architecture.md` | System design, component map, data flows, phase roadmap |
| `docs/governance.md` | Protected paths, approval escalation, file ownership |
| `docs/workflows.md` | Dev lifecycle, branching, commit standards, PR process |
| `docs/evaluation.md` | AI/ML eval methodology, benchmark tracking, uncertainty policy |
| `docs/security.md` | Threat model, injection defense, secret hygiene |
| `docs/knowledge.md` | Knowledge types, storage strategy, retrieval patterns |
| `docs/decision-log.md` | Chronological record of architectural decisions |
| `docs/discovery-log.md` | Important findings that affect future work |
| `docs/lessons-learned.md` | Mistakes, surprises, preventive lessons |
| `adr/` | Architecture Decision Records (created on demand) |
| `runbooks/` | Operational procedures (created on demand) |
| `templates/` | Standard document templates |

*Read only the companions relevant to the current session's task.*

---

## 1. Mission

**Purpose:** A personal research study in integrating quantum hot and cold paths with agentic systems — specifically to understand where quantum computing fits best and how to incorporate it meaningfully.

**Users:** Brandt Pileggi (project owner) and his orchestrated agents.

**Success looks like:**
- A working pipeline that feeds data to both hot and cold paths
- A near real-time quantum response system demonstrating the hot/cold split in practice
- A clear, documented answer to: "where does quantum actually add value in this architecture?"

**Non-goals (explicit):**
- This is not an enterprise or production system
- This system will not be hardened for external users, SLAs, or operational reliability requirements

---

## 2. Architectural Constitution

*Values, not rules. When two values conflict, the one ranked higher wins.*
*Derive correct behavior for novel situations from these values rather than asking for a rule.*

| Rank | Value | What it demands |
|------|-------|----------------|
| 1 | **Observability** | If it isn't logged and measurable, it doesn't exist |
| 2 | **Correctness** | Working before fast before elegant. Measure before optimizing |
| 3 | **Simplicity** | Smallest change satisfying the requirement. No future-proofing |
| 4 | **Explainability** | Every decision has a stated reason. No magic |
| 5 | **Testability** | If you can't test it, rethink the design |
| 6 | **Replaceability** | Implementations are swappable; interfaces are stable |
| 7 | **Security** | Sanitize, authenticate, rate-limit from day one |
| 8 | **Evolvability** | Today's choice doesn't lock out tomorrow's option |

> **Example conflict resolution:** Observability vs. Simplicity — adding a log line is rarely
> "too complex." Simplicity vs. Correctness — never skip a test to ship faster.

---

## 3. Governance

*Actions requiring explicit human approval before proceeding:*

| Action | Risk | Default |
|--------|------|---------|
| Delete or overwrite files outside the active task scope | Blast radius | **Block** |
| Change public interfaces, API contracts, or wire schemas | Downstream breakage | **Block** |
| Add new dependencies to requirements / package files | Security + bloat | **Block** |
| Commit anything containing credentials, tokens, or keys | Irreversible leak | **Block** |
| Modify CI/CD pipelines or deployment configuration | Affects all contributors | **Block** |
| Push to main, master, or release branches | Requires human gate | **Block** |
| Make irreversible infrastructure changes (drop tables, etc.) | Disaster recovery | **Block** |
| Refactor code outside the active task's stated scope | Scope creep | **Ask** |
| Reference an API or library without citing its source | Hallucination risk | **Ask** |

**Protected files:** None designated yet. Update `docs/governance.md` when any are established.

**Rule:** When uncertain whether an action falls under a guardrail — pause and ask.

---

## 4. Session Protocol

*Execute in order at the start of every coding session:*

1. **Orient to state**
   ```bash
   git status && git log --oneline -5
   ```

2. **Confirm the baseline is clean**
   ```bash
   pytest tests/ -v
   ```
   Do not begin changes if the baseline is red. Fix first.

3. **Read the relevant companion docs**
   From the Ecosystem Map above, identify which files apply to this session's task.
   Read those before writing any code.

4. **Check institutional memory**
   Scan `docs/decision-log.md` and `docs/discovery-log.md` for entries affecting the
   current task. If something was decided before, honor the decision or explicitly reverse it.

5. **Optional — ingest LLM engineering foundations**
   If working on AI/LLM components or debugging model behavior, read:
   - Karpathy's LLM Wiki: `https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`
   This establishes shared vocabulary for reasoning about neural network engineering.

---

## 5. Definition of Done

*A task is not complete until every applicable box is checked. Binary — not negotiable.*

**Code**
- [ ] Tests pass; new code has at least one happy-path and one failure-path test
- [ ] No new linting warnings introduced
- [ ] No hardcoded secrets, credentials, or API keys
- [ ] External content sanitized before any LLM prompt inclusion

**Documentation**
- [ ] Relevant companion docs updated to reflect changed behavior
- [ ] `docs/decision-log.md` updated if an architectural decision was made
- [ ] `docs/lessons-learned.md` updated if something surprising happened
- [ ] ADR filed in `adr/` if a significant architectural choice was locked in

**Hygiene**
- [ ] No unresolved TODOs within the task's stated scope
- [ ] No dead code or commented-out blocks left behind
- [ ] PR / commit description explains *why*, not just *what*

*If a task is too large to satisfy all applicable criteria in one session, split the task.*

---

## 6. Core Anti-Patterns

*These feel correct but are wrong for this codebase. Recognize them. Refuse them.*

| Pattern | The Trap | The Rule |
|---------|----------|----------|
| **Fat orchestrator** | Business logic added to coordination code | Orchestrators move data; they don't transform it |
| **God module** | One class doing crawling + analysis + storage | Single responsibility. Split at the second job |
| **Inline LLM calls** | LLM call buried in a utility or pipeline function | LLM calls belong in agents; inject the client via config |
| **Bare HTTP** | `requests.get()` without rate limiting or UA header | Rate-limit all external calls; use session with standard UA |
| **Credential-dependent tests** | Tests that fail without `.env` present | All tests pass in a clean environment with no secrets |
| **Print debugging** | `print()` in `src/` or equivalent source directories | Structured logging only; remove before commit |
| **Premature abstraction** | Helper class extracted for a single use case | Three similar lines > one leaky abstraction |
| **Sanitization bypass** | "This source is internal, skip sanitize_text()" | Sanitize everything that touches an LLM prompt |
| **Spec fiction** | Referencing an API or package without verifying it exists | Read the source. Cite the version |
| **Ambiguous ownership** | File modified without declaring which task owns it | Every task declares its file scope upfront |

---

## 7. Technology Stack

| Layer | Choice | Rationale | Upgrade Path |
|-------|--------|-----------|--------------|
| Language | Python 3.12 | Current installed version; rich quantum/ML ecosystem | 3.13 when stable |
| Structured store | SQLite | Zero infrastructure; perfect for experiment run storage and agent logs | Postgres if concurrent writes ever needed |
| Vector search | ChromaDB | Local-first, persistent, easy Python API, built-in metadata filtering | FAISS for performance gains in a future phase (noted: higher throughput, no built-in persistence) |
| LLM interface | Anthropic SDK | Primary model provider | Provider-agnostic wrapper via config if needed |
| Testing | pytest | Standard Python testing; parametrize useful for circuit config sweeps | Add hypothesis for property-based quantum invariant tests |
| Observability | structlog JSON | Structured, queryable logs; low overhead | OpenTelemetry at scale |

**Anticipated experiment-phase dependencies** *(not yet approved — require decision-log entry before adding):*
- `LangGraph` — agent orchestration / graph-based workflows
- `NetworkX` — graph memory and environment modeling
- `DEAP` — genetic algorithms for evolutionary optimizer
- `Qiskit` / `Qiskit Aer` — quantum circuit simulation and QUBO formulation

*Adding any dependency requires a reason here and an entry in `docs/decision-log.md`.*

---

## 8. Phase Status

```
Phase 0 — Exploration        [🔄 IN PROGRESS]
Phase 1 — Discovery          [⬜ NOT STARTED]
Phase 2 — Analysis           [⬜ NOT STARTED]
Phase 3 — Hypothesis         [⬜ NOT STARTED]
Phase 4 — Experiment         [⬜ NOT STARTED]
  └─ Layer 1: Agentic System   (hot path — classical agents)
  └─ Layer 2: Evolutionary Optimizer  (DEAP genetic algorithms)
  └─ Layer 3: Quantum Simulator       (Qiskit Aer)
  └─ Layer 4: Real Quantum Backend    (IBM / Azure / D-Wave)
Phase 5 — Results            [⬜ NOT STARTED]
Phase 6 — Conclusion         [⬜ NOT STARTED]
```

**Current phase priorities (Exploration):**
1. Get informed on industry processes, workflows, capabilities, best practices, and available resources as they pertain to quantum + agentic integration
2. Validate that this architectural approach (hot/cold path split with quantum optimization) is the right way to learn and implement this problem space

**Phase discipline:** do not implement features belonging to a later phase until the current
phase's success criteria are met. Phase definitions live in `docs/architecture.md`.

---

*Maintained by: Brandt Pileggi. Last updated: 2026-06-28.*
*Architecture decisions: `docs/decision-log.md` | Discovery log: `docs/discovery-log.md`*
