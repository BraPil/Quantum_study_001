"""Phase 1 Discovery — shared toy scenario for the GA and QUBO spikes.

Both the hot-path GA and the cold-path QUBO must optimize the SAME objective for
their results to be comparable. This module is that single objective, expressed two ways:

    value(chromosome, weights)  → classical fitness (what the GA maximizes)
    build_qubo(weights)         → Q matrix (what the QUBO minimizes: -value)
    brute_force(weights)        → ground-truth optimum over all 64 combinations

The objective is genuinely quadratic (pairwise redundancy/conflict penalties), so it
is a real QUBO and not a trivially separable linear problem.

This is throwaway spike code — a toy threat with hand-picked numbers, NOT the real
Phase 4 model. Its only job is to prove the GA and QUBO machinery agree.
"""
from __future__ import annotations

from contracts import ACTION_ORDER, NUM_ACTIONS, Action, Chromosome, FitnessWeights

# Per-action properties for one fixed toy threat (an "unauthorized PLC write").
# Each tuple: (effectiveness, downtime, cost, false_pos_risk), all roughly 0–1.
_PROPS: dict[Action, tuple[float, float, float, float]] = {
    Action.ALERT:           (0.10, 0.00, 0.05, 0.02),  # cheap, weak, safe
    Action.QUARANTINE_PLC:  (0.70, 0.50, 0.20, 0.10),  # strong, disruptive
    Action.KILL_PROCESS:    (0.55, 0.30, 0.15, 0.15),  # strong, medium downtime
    Action.DEPLOY_HONEYPOT: (0.30, 0.05, 0.25, 0.05),  # moderate, costly setup
    Action.RATE_LIMIT:      (0.25, 0.10, 0.10, 0.08),  # mild mitigation
    Action.ROLLBACK:        (0.60, 0.40, 0.30, 0.12),  # strong, expensive
}

# Pairwise penalties (redundancy/conflict) — the quadratic term. Symmetric; keyed i<j.
# Quarantine + Kill overlap (both stop the process). Quarantine + Honeypot conflict
# (can't both isolate and lure). Rollback + Kill partially redundant.
_PAIR_PENALTY: dict[tuple[Action, Action], float] = {
    (Action.QUARANTINE_PLC, Action.KILL_PROCESS): 0.25,
    (Action.QUARANTINE_PLC, Action.DEPLOY_HONEYPOT): 0.40,
    (Action.KILL_PROCESS, Action.ROLLBACK): 0.20,
}


def _linear_benefit(action: Action, w: FitnessWeights) -> float:
    eff, downtime, cost, fp = _PROPS[action]
    return w.w_threat * eff - w.w_downtime * downtime - w.w_cost * cost - w.w_false_pos * fp


def _pair_penalty(a: Action, b: Action) -> float:
    return _PAIR_PENALTY.get((a, b), _PAIR_PENALTY.get((b, a), 0.0))


def value(chromo: Chromosome, w: FitnessWeights) -> float:
    """Classical objective to MAXIMIZE. Higher = better response set."""
    total = 0.0
    for i, a in enumerate(ACTION_ORDER):
        if chromo.bits[i]:
            total += _linear_benefit(a, w)
            for j in range(i + 1, NUM_ACTIONS):
                if chromo.bits[j]:
                    total -= _pair_penalty(a, ACTION_ORDER[j])
    return total


def build_qubo(w: FitnessWeights) -> dict[tuple[int, int], float]:
    """Q matrix for minimizing -value(x). dimod/dwave consume this dict directly.

    minimize x^T Q x  where  Q_ii = -benefit_i,  Q_ij = +penalty_ij (i<j).
    """
    Q: dict[tuple[int, int], float] = {}
    for i, a in enumerate(ACTION_ORDER):
        Q[(i, i)] = -_linear_benefit(a, w)
        for j in range(i + 1, NUM_ACTIONS):
            p = _pair_penalty(a, ACTION_ORDER[j])
            if p:
                Q[(i, j)] = p
    return Q


def brute_force(w: FitnessWeights) -> tuple[Chromosome, float]:
    """Ground truth: exhaustively maximize value over all 2^6 = 64 combinations."""
    best_bits, best_val = None, float("-inf")
    for n in range(2 ** NUM_ACTIONS):
        bits = tuple((n >> k) & 1 for k in range(NUM_ACTIONS))
        v = value(Chromosome(bits), w)
        if v > best_val:
            best_bits, best_val = bits, v
    return Chromosome(best_bits), best_val
