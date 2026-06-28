"""Phase 1 Discovery spike — hot-path optimizer (PyGAD).

Proves: a PyGAD binary chromosome GA finds the best response set for the toy
scenario, and agrees with brute-force ground truth.

Run: python spikes/spike_ga.py
"""
from __future__ import annotations

import pygad

from contracts import NUM_ACTIONS, Chromosome, FitnessWeights
from scenario import brute_force, value

WEIGHTS = FitnessWeights()


def _fitness(ga_instance, solution, solution_idx) -> float:
    bits = tuple(int(b) for b in solution)
    return value(Chromosome(bits), WEIGHTS)


def run_ga(seed: int = 42) -> tuple[Chromosome, float]:
    ga = pygad.GA(
        num_generations=40,
        num_parents_mating=4,
        fitness_func=_fitness,
        sol_per_pop=20,
        num_genes=NUM_ACTIONS,
        gene_type=int,
        gene_space=[0, 1],
        parent_selection_type="tournament",
        crossover_type="single_point",
        mutation_type="random",
        mutation_percent_genes=20,
        random_seed=seed,
        suppress_warnings=True,
    )
    ga.run()
    solution, fitness, _ = ga.best_solution()
    return Chromosome(tuple(int(b) for b in solution)), float(fitness)


if __name__ == "__main__":
    ga_chromo, ga_val = run_ga()
    bf_chromo, bf_val = brute_force(WEIGHTS)

    print("=== Hot-path GA spike (PyGAD) ===")
    print(f"GA best:          {ga_chromo.bits}  value={ga_val:.4f}")
    print(f"  actions:        {[a.value for a in ga_chromo.active_actions]}")
    print(f"brute-force best: {bf_chromo.bits}  value={bf_val:.4f}")
    print(f"  actions:        {[a.value for a in bf_chromo.active_actions]}")

    agree = abs(ga_val - bf_val) < 1e-9
    print(f"\nGA matches ground truth: {'✓ YES' if agree else '✗ NO'}")
    if not agree:
        raise SystemExit("GA did not reach the optimum — spike FAILED")
