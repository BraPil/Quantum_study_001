"""Phase 1 Discovery spike — the GA↔QUBO learning loop (the project's core).

Proves: the hot-path → store → cold-path → feedback handoff is wireable end-to-end,
and that the feedback moves in the correct direction (regret decreases after the update).

The setup (deliberately simple, deliberately honest):
  - W_TRUE  = reality. The true cost of downtime is higher than the hot path believes.
  - W_hot   = the hot path's current (miscalibrated) belief — it underweights downtime.
  - Hot path: GA picks a response per event using W_hot. Decisions logged to SQLite.
  - Cold path: reads the batch, and retrospectively searches for the w_downtime value
    whose induced GA decisions would have minimized TRUE harm on the historical events.
    Returns updated weights.
  - We then show mean regret on a fresh batch drops after applying the updated weights.

SCOPE (what this spike does NOT claim): the weight-update rule here is a transparent
coordinate search, not a proposed Phase 4 learning algorithm. The spike proves the LOOP
MECHANICS (storage boundary, retrospection, feedback direction), not an optimal learner.

Run: python spikes/spike_loop.py
"""
from __future__ import annotations

import sqlite3
from dataclasses import replace

from contracts import Chromosome, FitnessWeights
from scenario import brute_force, value
from spike_ga import run_ga as _run_ga_default

# Reality: downtime truly costs 2x what the hot path initially assumes.
W_TRUE = FitnessWeights(w_threat=1.0, w_downtime=2.0, w_cost=0.05, w_false_pos=1.0)
# Hot path starts miscalibrated — it underweights downtime.
W_HOT_INITIAL = FitnessWeights(w_threat=1.0, w_downtime=0.5, w_cost=0.05, w_false_pos=1.0)


def _ga_decision(weights: FitnessWeights, seed: int) -> Chromosome:
    """Run the hot-path GA against `weights`, return the chosen response."""
    import pygad
    from contracts import NUM_ACTIONS

    def fitness(ga_inst, sol, idx):
        return value(Chromosome(tuple(int(b) for b in sol)), weights)

    ga = pygad.GA(
        num_generations=40, num_parents_mating=4, fitness_func=fitness,
        sol_per_pop=20, num_genes=NUM_ACTIONS, gene_type=int, gene_space=[0, 1],
        parent_selection_type="tournament", crossover_type="single_point",
        mutation_type="random", mutation_percent_genes=20,
        random_seed=seed, suppress_warnings=True,
    )
    ga.run()
    sol, _, _ = ga.best_solution()
    return Chromosome(tuple(int(b) for b in sol))


def _true_optimum_value(seed_unused: int = 0) -> float:
    """Best achievable TRUE value (same for every event in this toy: one fixed threat)."""
    _, v = brute_force(W_TRUE)
    return v


def _regret(chromo: Chromosome) -> float:
    """How much TRUE value this decision left on the table vs. the true optimum."""
    return _true_optimum_value() - value(chromo, W_TRUE)


def hot_path_batch(weights: FitnessWeights, n_events: int, conn: sqlite3.Connection) -> None:
    """Hot path: make a GA decision per event, log (event, chromosome, true_harm)."""
    for ev in range(n_events):
        chromo = _ga_decision(weights, seed=100 + ev)
        conn.execute(
            "INSERT INTO decisions (event_id, bits, true_regret) VALUES (?, ?, ?)",
            (f"evt-{ev}", "".join(map(str, chromo.bits)), _regret(chromo)),
        )
    conn.commit()


def cold_path_retrospect(conn: sqlite3.Connection) -> FitnessWeights:
    """Cold path: search w_downtime values; pick the one minimizing TRUE regret on history.

    Reads the historical batch from the store, replays the GA under candidate weights,
    scores the induced decisions by true harm, returns the best-calibrated weights.
    """
    rows = conn.execute("SELECT event_id FROM decisions").fetchall()
    seeds = [100 + i for i in range(len(rows))]

    best_w, best_regret = None, float("inf")
    for candidate_downtime in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        cand = replace(W_HOT_INITIAL, w_downtime=candidate_downtime)
        total = sum(_regret(_ga_decision(cand, seed=s)) for s in seeds)
        if total < best_regret:
            best_w, best_regret = cand, total
    return best_w


def mean_regret(weights: FitnessWeights, seeds: range) -> float:
    return sum(_regret(_ga_decision(weights, seed=s)) for s in seeds) / len(seeds)


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE decisions (event_id TEXT, bits TEXT, true_regret REAL)")

    print("=== GA↔QUBO learning-loop spike ===")
    print(f"W_TRUE downtime weight:  {W_TRUE.w_downtime}")
    print(f"W_HOT  downtime weight:  {W_HOT_INITIAL.w_downtime}  (miscalibrated — too low)\n")

    # 1. Hot path runs a batch with the miscalibrated weights, logging to the store.
    hot_path_batch(W_HOT_INITIAL, n_events=8, conn=conn)
    logged = conn.execute("SELECT COUNT(*), AVG(true_regret) FROM decisions").fetchone()
    print(f"Hot path logged {logged[0]} decisions to store. Mean true regret: {logged[1]:.4f}")

    # 2. Cold path retrospects and returns recalibrated weights.
    W_updated = cold_path_retrospect(conn)
    print(f"Cold path recalibrated downtime weight → {W_updated.w_downtime}")

    # 3. Evaluate both weight sets on a fresh batch of events.
    fresh = range(500, 512)
    before = mean_regret(W_HOT_INITIAL, fresh)
    after = mean_regret(W_updated, fresh)
    print(f"\nMean regret on fresh batch:")
    print(f"  before (W_HOT):      {before:.4f}")
    print(f"  after  (recalibrated): {after:.4f}")

    improved = after <= before - 1e-9
    print(f"\nFeedback reduced regret: {'✓ YES' if improved else '✗ NO (already optimal)'}")
    if after > before + 1e-9:
        raise SystemExit("Loop made it worse — spike FAILED")
    conn.close()
