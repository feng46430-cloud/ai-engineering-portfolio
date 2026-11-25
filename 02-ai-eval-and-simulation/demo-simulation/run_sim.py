#!/usr/bin/env python3
"""
500-Turn Dynamic State-Machine & Growth Model Simulation Demo
-------------------------------------------------------------
Demonstrates how deterministic simulation testing catches systemic defects
BEFORE deploying rule/prompt systems to live LLM runs:
  1. Cold-start deadlock (base = 0 with pure multiplicative growth)
  2. Compounding decay unit error (-1.8%/turn -> ~39% annual attrition)
  3. Calibrated convergence across 500 turns (~10 simulated years, 50 turns/year)

Zero external dependencies. Run directly with:
    python 02-ai-eval-and-simulation/demo-simulation/run_sim.py
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


TIERS: List[Tuple[str, int, float]] = [
    ("T0", 0, 1.0),
    ("T1", 50_000, 2.0),
    ("T2", 500_000, 10.0),
    ("T3", 3_000_000, 40.0),
    ("T4", 15_000_000, 150.0),
    ("T5", 50_000_000, 500.0),
]

CAP = 120_000_000


def resolve_tier(value: float) -> Tuple[str, float]:
    tier_name, mult = TIERS[0][0], TIERS[0][2]
    for name, threshold, factor in TIERS:
        if value >= threshold:
            tier_name, mult = name, factor
    return tier_name, mult


@dataclass
class SimResult:
    label: str
    start_value: int
    end_value: int
    end_tier: str
    milestones_year: Dict[str, float]
    deadlocked: bool


def simulate_legacy_buggy(start_value: int, turns: int = 500) -> SimResult:
    """Reproduces the pre-audit defects: pure multiplicative growth + -1.8%/turn decay."""
    n = float(start_value)
    milestones: Dict[str, float] = {}
    for t in range(1, turns + 1):
        if t % 100 == 0:
            n += n * 0.25  # major release
        elif t % 36 == 0:
            n += n * 0.12  # breakout
        elif t % 24 == 0:
            n += n * 0.04  # mid event
        elif t % 12 == 0:
            n += n * 0.02  # routine event
        else:
            n -= n * 0.018  # buggy per-turn silent decay (-1.8%/turn -> ~39%/yr)

        n = max(0.0, min(CAP, n))
        tier, _ = resolve_tier(n)
        if tier != "T0" and tier not in milestones:
            milestones[tier] = round(t / 50.0, 1)

    end_tier, _ = resolve_tier(n)
    return SimResult(
        label="Legacy (Pure Multiplicative + -1.8%/turn)",
        start_value=start_value,
        end_value=int(n),
        end_tier=end_tier,
        milestones_year=milestones,
        deadlocked=(int(n) < 5_000),
    )


def simulate_calibrated(start_value: int, turns: int = 500) -> SimResult:
    """Calibrated model: cold-start floor + tier-scaled exposure + -0.5%/turn decay."""
    n = float(start_value)
    milestones: Dict[str, float] = {}
    for t in range(1, turns + 1):
        tier, mult = resolve_tier(n)
        sat = max(0.0, 1.0 - n / CAP)

        if t % 100 == 0:  # major hit
            delta = max(10_000.0, (n * 0.20 + 4_000_000 * mult * 0.012) * sat)
            n += delta
        elif t % 36 == 0:  # breakout
            delta = max(2_000.0, (n * 0.10 + 1_000_000 * mult * 0.010) * sat)
            n += delta
        elif t % 24 == 0:  # mid promo
            delta = max(300.0, (n * 0.03 + 200_000 * mult * 0.010) * sat)
            n += delta
        elif t % 12 == 0:  # routine release
            delta = max(50.0, (n * 0.012 + 30_000 * mult * 0.005) * sat)
            n += delta
        else:
            n -= n * 0.005  # calibrated steady attrition (-0.5%/turn)

        n = max(0.0, min(CAP, n))
        new_tier, _ = resolve_tier(n)
        if new_tier != "T0" and new_tier not in milestones:
            milestones[new_tier] = round(t / 50.0, 1)

    end_tier, _ = resolve_tier(n)
    return SimResult(
        label="Calibrated (Floor Delta + Tier Mult + -0.5%/turn)",
        start_value=start_value,
        end_value=int(n),
        end_tier=end_tier,
        milestones_year=milestones,
        deadlocked=(int(n) < 5_000),
    )


def main() -> None:
    scenarios = [
        simulate_legacy_buggy(start_value=0),
        simulate_legacy_buggy(start_value=890),
        simulate_calibrated(start_value=0),
        simulate_calibrated(start_value=890),
    ]

    print("=" * 88)
    print("500-Turn State-Machine Simulation Report (50 turns = 1 simulated year)")
    print("=" * 88)
    print(f"{'Model Variant':<49} | {'Start':>6} | {'End @500':>11} | {'Tier':<4} | {'Milestones (Yr)'}")
    print("-" * 88)
    for r in scenarios:
        ms = ", ".join(f"{k}@{v}y" for k, v in r.milestones_year.items()) or "NONE (STALLED)"
        print(f"{r.label:<49} | {r.start_value:>6,} | {r.end_value:>11,} | {r.end_tier:<4} | {ms}")
    print("-" * 88)

    # Automated invariant gate assertions
    assert scenarios[0].end_value == 0 and scenarios[0].deadlocked, "Expected 0-start legacy deadlock"
    assert scenarios[1].deadlocked, "Expected low-base legacy stagnation"
    assert not scenarios[2].deadlocked and scenarios[2].end_tier in ("T2", "T3", "T4", "T5"), (
        "Calibrated 0-start model must escape cold-start deadlock and reach T2+"
    )
    assert not scenarios[3].deadlocked and scenarios[3].end_value > 1_000_000, (
        "Calibrated 890-start model must converge cleanly above 1M"
    )
    print("[PASS] All simulation invariants verified: legacy defects reproduced & calibrated fixes confirmed.")


if __name__ == "__main__":
    main()
