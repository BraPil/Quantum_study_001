# Lessons Learned — Quantum_Study_001

> Mistakes, surprises, and preventive lessons.
> Add an entry whenever something unexpected happens — good or bad.

---

## [2026-06-28] "Brute force is infeasible" is not the bar for quantum

**Surprise:** The intuitive trigger for reaching for quantum — "the search space 2^N is too big to
enumerate" — is the wrong test. The Phase 2 scaling probe showed brute force dies around N=22, but a
*classical* simulated-annealing heuristic stays sub-200ms and self-consistent out to N=60 (10¹⁸
states), exactly optimal everywhere checkable. Classical heuristics fill the gap exhaustive search
leaves.

**Lesson:** The real bar for quantum is "even good classical heuristics (SA, tabu) struggle," which
requires structurally *hard* instances (frustrated / spin-glass couplings), not merely *large* ones.
A sparse, well-structured combinatorial problem — which is what this ICS domain naturally produces —
is comfortably classical at every scale it reaches.

**How to apply:** When evaluating whether a problem "needs" quantum, never stop at the size of the
search space. Always ask whether a classical heuristic actually struggles on *that instance's
structure*. Measure it (`spikes/probe_qubo_scaling.py`), don't assume. This reframing is now baked
into `docs/evaluation.md` and `docs/architecture.md`.

---

*Add new entries above this line, newest first.*
