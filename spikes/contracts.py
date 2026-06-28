"""Phase 1 Discovery — Layer boundary data contracts.

These dataclasses define the interfaces between layers of the hot/cold pipeline.
They are the single source of truth for what data crosses each boundary:

    TelemetryEvent  → (Observer/Classifier/Risk Assessor)
        ResponseContext → (Response Generator)
            Chromosome  → (GA Optimizer / QUBO Builder)
                FitnessWeights → (cold-path QUBO result feeds back to hot-path GA)

This is spike code: throwaway proof that the contracts are coherent and the
handoffs typecheck. The Phase 4 build will promote these into src/ proper.

Run `python spikes/contracts.py` to self-validate the example flow.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


# --- The fixed response action space (the chromosome genes) ---------------

class Action(str, Enum):
    """The 6 binary response actions. Chromosome bit order is the enum order."""
    ALERT = "alert"
    QUARANTINE_PLC = "quarantine_plc"
    KILL_PROCESS = "kill_process"
    DEPLOY_HONEYPOT = "deploy_honeypot"
    RATE_LIMIT = "rate_limit"
    ROLLBACK = "rollback"


ACTION_ORDER: tuple[Action, ...] = tuple(Action)  # canonical bit ordering
NUM_ACTIONS = len(ACTION_ORDER)


# --- Boundary 1: simulation → hot path ------------------------------------

@dataclass
class TelemetryEvent:
    """Emitted by the simulated ICS environment. Entry point to the hot path."""
    event_id: str
    timestamp: datetime
    source_asset: str            # e.g. "PLC_1"
    event_type: str              # "register_write" | "login_attempt" | ...
    severity: int                # 1 (info) – 5 (critical)
    is_anomalous: bool           # ground-truth label (sim knows; agents must infer)
    attack_type: Optional[str]   # None if normal
    payload: dict = field(default_factory=dict)


# --- Boundary 2: agent assessment → optimizer -----------------------------

@dataclass
class ResponseContext:
    """What the agents infer from an event, handed to the optimizer.

    Note: agents do NOT see is_anomalous/attack_type ground truth — these are
    the agents' *inferred* values, which may differ from the sim's truth.
    """
    event_id: str
    inferred_attack_type: Optional[str]
    risk_score: float            # 0.0 – 1.0, from Risk Assessor
    blast_radius: int            # count of assets potentially affected
    candidate_actions: list[Action]  # Response Generator's proposals


# --- Boundary 3: optimizer ↔ QUBO (the chromosome) ------------------------

@dataclass
class Chromosome:
    """A binary response selection. The shared currency of GA and QUBO.

    bits[i] == 1 means ACTION_ORDER[i] is applied.
    """
    bits: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.bits) != NUM_ACTIONS:
            raise ValueError(f"expected {NUM_ACTIONS} bits, got {len(self.bits)}")
        if any(b not in (0, 1) for b in self.bits):
            raise ValueError(f"bits must be 0/1, got {self.bits}")

    @property
    def active_actions(self) -> list[Action]:
        return [ACTION_ORDER[i] for i, b in enumerate(self.bits) if b == 1]

    @classmethod
    def from_actions(cls, actions: list[Action]) -> "Chromosome":
        active = set(actions)
        return cls(tuple(1 if a in active else 0 for a in ACTION_ORDER))


# --- Boundary 4: cold path → hot path (the learning feedback) -------------

@dataclass
class FitnessWeights:
    """Tunable weights for the GA fitness function.

    The cold-path QUBO retrospection produces an improved set of these,
    which the hot-path GA uses on its next run. This is the learning loop.
    """
    w_threat: float = 1.0        # reward for eliminating threat
    w_downtime: float = 1.0      # penalty for downtime
    w_cost: float = 0.05         # penalty per action taken
    w_false_pos: float = 1.0     # penalty for false-positive risk


# --- Self-validation ------------------------------------------------------

def _demo() -> None:
    """Walk one event through the contract chain to prove it typechecks."""
    evt = TelemetryEvent(
        event_id="evt-001",
        timestamp=datetime(2026, 6, 28, 12, 0, 0),
        source_asset="PLC_1",
        event_type="register_write",
        severity=5,
        is_anomalous=True,
        attack_type="unauthorized_plc_write",
    )
    ctx = ResponseContext(
        event_id=evt.event_id,
        inferred_attack_type="unauthorized_plc_write",
        risk_score=0.82,
        blast_radius=3,
        candidate_actions=[Action.ALERT, Action.QUARANTINE_PLC, Action.ROLLBACK],
    )
    chromo = Chromosome.from_actions(ctx.candidate_actions)
    weights = FitnessWeights()

    assert chromo.bits == (1, 1, 0, 0, 0, 1)
    assert chromo.active_actions == [Action.ALERT, Action.QUARANTINE_PLC, Action.ROLLBACK]
    print(f"event {evt.event_id} ({evt.attack_type})")
    print(f"  inferred risk: {ctx.risk_score}, blast radius: {ctx.blast_radius}")
    print(f"  chromosome:    {chromo.bits}")
    print(f"  active:        {[a.value for a in chromo.active_actions]}")
    print(f"  weights:       threat={weights.w_threat} downtime={weights.w_downtime} "
          f"cost={weights.w_cost} fp={weights.w_false_pos}")
    print("contracts.py: all boundary contracts typecheck ✓")


if __name__ == "__main__":
    _demo()
