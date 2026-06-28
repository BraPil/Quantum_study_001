# Phase 1 Discovery — Spikes

> **Throwaway proof-of-concept code.** These spikes prove the integration points work
> before the real Phase 4 build. They are NOT production code. Phase 4 promotes the
> proven patterns into `src/` proper and discards these.

---

## What each spike proves

| File | Proves | Needs |
|------|--------|-------|
| `contracts.py` | The layer-boundary data contracts typecheck and chain together | — |
| `scenario.py` | A shared toy objective expressed as both GA fitness and a QUBO Q matrix | — |
| `spike_ga.py` | PyGAD finds the optimal response set; matches brute force | `pygad` |
| `spike_qubo.py` | QUBO solves end-to-end locally; matches brute force | `dwave-ocean-sdk` |
| `spike_loop.py` | The GA↔QUBO learning loop: hot path → SQLite → cold path → recalibrated weights | `pygad`, `dwave-ocean-sdk` |
| `spike_agents.py` | Raw-SDK 2-agent pipeline returns a structured result; per-agent latency | `anthropic` + `ANTHROPIC_API_KEY` |

Run any spike directly: `python spikes/spike_ga.py`
The deterministic spikes (GA, QUBO, loop) are also guarded by `tests/test_spikes.py`.

---

## Install (spike deps)

These are Phase-4-approved deps, installed early for Discovery proofs (see runbook):

```bash
pip install -r spikes/requirements-spikes.txt
```

---

## Findings

- **`neal` is deprecated.** The research cited the standalone `dwave-neal` package, but the
  current Ocean SDK exposes the simulated-annealing sampler at
  `dwave.samplers.SimulatedAnnealingSampler`. Same role; drop-in for `DWaveSampler` to go to hardware.
- **GA and QUBO agree with brute force** on the toy 6-action problem — both pick
  `[alert, kill_process, deploy_honeypot, rate_limit]` and both correctly *avoid* quarantine
  because its pairwise penalties (with kill and honeypot) outweigh its benefit. This confirms the
  quadratic term is doing real work.
- **The learning loop closes.** With downtime deliberately miscalibrated (0.5 vs. true 2.0), the
  cold path retrospects over the logged batch and recovers the true weight (2.0), driving regret to
  zero on a fresh batch. Proves the hot→store→cold→feedback handoff is wireable.
- **Latency:** the agent spike measures real per-agent TTFT — run it once a key is available to
  confirm the 5–7s hot-path estimate from Phase 0 research holds.

See `docs/discovery-log.md` for the full write-up.
