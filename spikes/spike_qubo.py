"""Phase 1 Discovery spike — cold-path optimizer (QUBO via Ocean SDK).

Proves: the toy scenario, expressed as a QUBO Q matrix, solves end-to-end with
the local simulated-annealing sampler and agrees with brute-force ground truth.

NOTE (Discovery finding): the standalone `neal` package the research cited is
deprecated. The simulated-annealing sampler now lives at
`dwave.samplers.SimulatedAnnealingSampler`. Same role, swap-in for DWaveSampler.

Run: python spikes/spike_qubo.py
"""
from __future__ import annotations

import dimod
from dwave.samplers import SimulatedAnnealingSampler

from contracts import Chromosome, FitnessWeights
from scenario import brute_force, build_qubo, value

WEIGHTS = FitnessWeights()


def solve_qubo(seed: int = 42) -> tuple[Chromosome, float]:
    Q = build_qubo(WEIGHTS)
    bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
    # Local classical SA. To go to real hardware: swap for EmbeddingComposite(DWaveSampler()).
    sampler = SimulatedAnnealingSampler()
    result = sampler.sample(bqm, num_reads=200, seed=seed)
    best = result.first.sample
    bits = tuple(int(best[i]) for i in range(len(best)))
    return Chromosome(bits), value(Chromosome(bits), WEIGHTS)


if __name__ == "__main__":
    qubo_chromo, qubo_val = solve_qubo()
    bf_chromo, bf_val = brute_force(WEIGHTS)

    print("=== Cold-path QUBO spike (dwave SimulatedAnnealingSampler) ===")
    print(f"QUBO best:        {qubo_chromo.bits}  value={qubo_val:.4f}")
    print(f"  actions:        {[a.value for a in qubo_chromo.active_actions]}")
    print(f"brute-force best: {bf_chromo.bits}  value={bf_val:.4f}")
    print(f"  actions:        {[a.value for a in bf_chromo.active_actions]}")

    agree = abs(qubo_val - bf_val) < 1e-9
    print(f"\nQUBO matches ground truth: {'✓ YES' if agree else '✗ NO'}")
    if not agree:
        raise SystemExit("QUBO did not reach the optimum — spike FAILED")
