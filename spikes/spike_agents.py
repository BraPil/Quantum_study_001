"""Phase 1 Discovery spike — raw-SDK agent pipeline (hot-path pattern).

Proves: a minimal 2-agent sequential pipeline (Observer → Classifier) built on the
raw Anthropic SDK passes a TelemetryEvent through and returns a structured result,
with real per-agent latency measured.

This validates the Layer 1 decision: raw SDK + plain async functions, no framework.

REQUIRES: ANTHROPIC_API_KEY in the environment (or a .env file). If absent, the
spike prints setup instructions and exits cleanly without failing.

Run: python spikes/spike_agents.py
"""
from __future__ import annotations

import asyncio
import json
import os
import time
from datetime import datetime

from contracts import ACTION_ORDER, ResponseContext, TelemetryEvent

FAST_MODEL = "claude-haiku-4-5-20251001"  # Haiku for fast hot-path agents (per decision-log)


def sanitize(text: str) -> str:
    """Minimal prompt-injection guard. CLAUDE.md: sanitize everything touching a prompt.

    For a spike with synthetic data this is belt-and-suspenders, but the pattern must
    be present from day one — the anti-pattern table forbids 'this source is internal'.
    """
    cleaned = text.replace("```", "").strip()
    # Neutralize the most obvious instruction-override attempts in field values.
    for marker in ("ignore previous", "ignore all previous", "system:", "assistant:"):
        cleaned = cleaned.replace(marker, "[redacted]")
    return cleaned[:2000]


def _event_to_prompt_block(evt: TelemetryEvent) -> str:
    """Render only the non-ground-truth fields — agents must INFER the rest."""
    visible = {
        "event_id": evt.event_id,
        "timestamp": evt.timestamp.isoformat(),
        "source_asset": evt.source_asset,
        "event_type": evt.event_type,
        "severity": evt.severity,
        "payload": evt.payload,
    }
    return sanitize(json.dumps(visible, indent=2))


async def observer_agent(client, evt: TelemetryEvent) -> tuple[str, float]:
    """Observer: produce a short natural-language observation of the event."""
    t0 = time.perf_counter()
    msg = await client.messages.create(
        model=FAST_MODEL,
        max_tokens=256,
        system="You are an ICS security Observer. In 1-2 sentences, describe what this "
               "telemetry event shows. Do not speculate beyond the data.",
        messages=[{"role": "user", "content": _event_to_prompt_block(evt)}],
    )
    return msg.content[0].text, time.perf_counter() - t0


async def classifier_agent(client, observation: str) -> tuple[dict, float]:
    """Classifier: label the attack type and risk as structured JSON."""
    t0 = time.perf_counter()
    msg = await client.messages.create(
        model=FAST_MODEL,
        max_tokens=256,
        system="You are an ICS security Classifier. Given the Observer's note, return ONLY "
               'a JSON object: {"inferred_attack_type": str|null, "risk_score": float 0-1, '
               '"blast_radius": int}. No prose.',
        messages=[{"role": "user", "content": sanitize(observation)}],
    )
    raw = msg.content[0].text.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    return json.loads(raw), time.perf_counter() - t0


async def run_pipeline(evt: TelemetryEvent) -> ResponseContext:
    import anthropic

    client = anthropic.AsyncAnthropic()
    observation, t_obs = await observer_agent(client, evt)
    classification, t_cls = await classifier_agent(client, observation)

    print(f"  Observer ({t_obs:.2f}s): {observation}")
    print(f"  Classifier ({t_cls:.2f}s): {classification}")
    print(f"  --- pipeline latency: {t_obs + t_cls:.2f}s (2 agents) ---")

    return ResponseContext(
        event_id=evt.event_id,
        inferred_attack_type=classification.get("inferred_attack_type"),
        risk_score=float(classification.get("risk_score", 0.0)),
        blast_radius=int(classification.get("blast_radius", 0)),
        candidate_actions=list(ACTION_ORDER),  # Response Generator's job — stubbed here
    )


def _load_dotenv() -> None:
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


if __name__ == "__main__":
    _load_dotenv()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("=== Raw-SDK agent pipeline spike ===")
        print("SKIPPED: ANTHROPIC_API_KEY not set.\n")
        print("To run this spike, provide your key one of these ways:")
        print("  1. Create /workspaces/Quantum_study_001/.env with:")
        print("       ANTHROPIC_API_KEY=sk-ant-...")
        print("     (.env is gitignored — it will not be committed)")
        print("  2. Or export it in your shell:  export ANTHROPIC_API_KEY=sk-ant-...")
        raise SystemExit(0)

    sample = TelemetryEvent(
        event_id="evt-spike-001",
        timestamp=datetime(2026, 6, 28, 14, 30, 0),
        source_asset="PLC_2",
        event_type="register_write",
        severity=5,
        is_anomalous=True,                 # ground truth — NOT shown to agents
        attack_type="unauthorized_plc_write",
        payload={"register": "40001", "old": 120, "new": 9999, "auth_user": None},
    )
    print("=== Raw-SDK agent pipeline spike ===")
    print(f"Input event: {sample.event_type} on {sample.source_asset} (severity {sample.severity})\n")
    result = asyncio.run(run_pipeline(sample))
    print(f"\nResult ResponseContext: inferred={result.inferred_attack_type!r} "
          f"risk={result.risk_score} blast={result.blast_radius}")
    print("\nPipeline returned a structured ResponseContext ✓")
