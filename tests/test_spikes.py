"""Phase 1 — tests guarding the deterministic Discovery spikes.

The GA, QUBO, and learning-loop spikes are reproducible (fixed seeds), so we assert
their invariants here. The agent-pipeline spike needs a live API key and is not tested.

Happy path: each optimizer reaches the known optimum / the loop reduces regret.
Failure path: a deliberately-wrong chromosome scores below the optimum.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "spikes"))

from contracts import Chromosome, FitnessWeights  # noqa: E402
from scenario import brute_force, value  # noqa: E402


def test_ga_reaches_optimum():
    from spike_ga import run_ga
    _, ga_val = run_ga()
    _, bf_val = brute_force(FitnessWeights())
    assert ga_val == pytest.approx(bf_val)


def test_qubo_reaches_optimum():
    from spike_qubo import solve_qubo
    _, qubo_val = solve_qubo()
    _, bf_val = brute_force(FitnessWeights())
    assert qubo_val == pytest.approx(bf_val)


def test_ga_and_qubo_agree():
    from spike_ga import run_ga
    from spike_qubo import solve_qubo
    ga_chromo, _ = run_ga()
    qubo_chromo, _ = solve_qubo()
    assert ga_chromo.bits == qubo_chromo.bits


def test_learning_loop_reduces_regret():
    import spike_loop
    before = spike_loop.mean_regret(spike_loop.W_HOT_INITIAL, range(500, 512))
    after = spike_loop.mean_regret(
        spike_loop.replace(spike_loop.W_HOT_INITIAL, w_downtime=spike_loop.W_TRUE.w_downtime),
        range(500, 512),
    )
    assert after <= before


def test_failure_path_suboptimal_chromosome_scores_lower():
    """A response that ignores the threat must score below the optimum."""
    w = FitnessWeights()
    _, best_val = brute_force(w)
    do_nothing = Chromosome((0, 0, 0, 0, 0, 0))
    assert value(do_nothing, w) < best_val


def test_chromosome_rejects_bad_length():
    with pytest.raises(ValueError):
        Chromosome((1, 0, 1))
