#!/usr/bin/env python3
"""
Multi-Strategy State-Machine Curve Calibration Suite
----------------------------------------------------
Demonstrates how offline deterministic parameter sweeps catch systemic curve defects
BEFORE deploying rule/prompt systems to live LLM runs:
  1. Legacy Multiplicative Formula Audit across 5 distinct player strategies (40 turns, start=890)
  2. Calibrated 5-Track Career Convergence (2 / 3 / 5 / 8 / 12 simulated years = 1,560 steps)
  3. 3-Tier Post-Viral Fade Sensitivity Sweep (demonstrating why decay window must be bounded)
  4. Illustrative Single-Metric Threshold Overlap Counterexample (synthetic normalized scales)

Total simulated volume: 1,820 deterministic steps across multi-strategy & multi-year sweeps.
Zero external dependencies. Run directly with:
    python 02-ai-eval-and-simulation/demo-simulation/run_sim.py
"""

from typing import Dict, List, Tuple

CAP = 150_000_000.0
POOLS = [1e4, 1e5, 1e6, 1e7, 1e8]
TIER_MULT = [1.0, 2.0, 10.0, 40.0, 150.0, 500.0]  # T0-T5 exposure multipliers

# (label, K_factor, base_exposure, conv_rate, delta_rep, min_ach_tier, base_loss, use_pool_cap)
EVENTS: Dict[str, Tuple[str, float, float, float, float, int, float, bool]] = {
    "idle":     ("Silent / Idle",      0.0012,     0.0, 0.000,  0.0, 0, 0.0060, False),
    "release":  ("Routine Release",    0.0120,   3e4,   0.005,  1.0, 0, 0.0030, False),
    "promo":    ("Stage / Variety",    0.0300,   2e5,   0.010,  2.0, 0, 0.0030, False),
    "breakout": ("Cross-Circle Hit",   0.1000,   1e6,   0.010,  4.0, 1, 0.0030, True),
    "smash":    ("Smash Hit",          0.2000,   4e6,   0.012,  7.0, 2, 0.0030, True),
    "viral":    ("Overnight Viral",    0.5000,   2e7,   0.015, 12.0, 3, 0.0030, True),
    "award":    ("Major Award",        0.1200,   5e6,   0.012, 10.0, 4, 0.0030, True),
    "global":   ("Global General Fld", 0.3000,   2e7,   0.015, 15.0, 5, 0.0030, True),
}

# 3-pillar promotion gates: (tier_name, min_fans, min_reputation, min_achievement_tier)
TIERS: List[Tuple[str, float, float, int]] = [
    ("T0 Underground", 0,     0,  0),
    ("T1 Niche",       5e4,   15, 0),
    ("T2 Rising",      5e5,   30, 0),
    ("T3 A-List",      3e6,   50, 0),
    ("T4 National",    1.5e7, 70, 4),
    ("T5 Legend",      8e7,   90, 5),
]


def next_pool(n: float) -> float:
    for p in POOLS:
        if p > n:
            return p
    return CAP


def run_legacy_buggy(strategy_k: float, start_fans: float = 890.0, turns: int = 40) -> Tuple[int, str]:
    """Pre-audit buggy model: pure multiplicative growth + heavy per-turn attrition (-1.8%/turn)."""
    n = float(start_fans)
    for t in range(1, turns + 1):
        d = 0.5 if t % 2 == 0 else 1.0
        n = max(0.0, min(CAP, n + n * strategy_k * d - n * 0.018))
    tier = "T0"
    for name, th, _, _ in TIERS:
        if n >= th:
            tier = name.split()[0]
    return int(n), tier


def run_calibrated(
    seq: List[Tuple[str, float]],
    n0: float = 890.0,
    rep0: float = 9.0,
    fade_loss: float = 0.0,
) -> dict:
    """Calibrated nonlinear model: ΔN = (N*K*D + A*c)*(1 - N/CAP) - N*L with 3-pillar gates."""
    n, rep, ach, tier = float(n0), float(rep0), 0, 0
    promo_turns: Dict[int, int] = {}
    history: List[Tuple[int, str, float, float]] = []

    for i, (key, d) in enumerate(seq, 1):
        label, k, ab, c, drep, dach, base_l, pooled = EVENTS[key]
        exposure = ab * TIER_MULT[tier]
        rep = min(100.0, rep + drep)
        ach = max(ach, dach)
        loss = fade_loss if (fade_loss > 0 and key == "idle") else base_l
        nn = max(0.0, n + (n * k * d + exposure * c) * (1.0 - n / CAP) - n * loss)
        if pooled:
            nn = min(nn, next_pool(n))
        if tier < 5:
            _, min_n, min_rep, min_ach = TIERS[tier + 1]
            if nn >= min_n and rep >= min_rep and ach >= min_ach:
                tier += 1
                promo_turns[tier] = i
        history.append((i, label, nn, rep))
        n = nn

    return {
        "end_fans": int(n),
        "end_rep": int(rep),
        "end_tier": TIERS[tier][0],
        "promo_turns": promo_turns,
        "history": history,
    }


def build_yearly_schedule(
    years: int,
    cadence: List[Tuple[str, int]],
    milestones: Dict[int, str] | None = None,
) -> List[Tuple[str, float]]:
    milestones = milestones or {}
    seq: List[Tuple[str, float]] = []
    for week in range(1, years * 52 + 1):
        if week in milestones:
            seq.append((milestones[week], 1.0))
            continue
        pick = "idle"
        for ev, every in cadence:
            if week % every == 0:
                pick = ev
        seq.append((pick, 1.0))
    return seq


def check_single_metric_overlap() -> Tuple[int, int]:
    """
    Illustrative counterexample using normalized synthetic scale estimates (NOT a scraped
    cross-platform dataset) to demonstrate why a single fan-count threshold collides in the
    ~40M band between high-social-traffic acts and stadium-touring acts, motivating a
    3-pillar (Fans + Reputation + Realized Achievement) promotion gate.
    """
    samples = [
        ("Act-01 (Global Stadium)", 360, 5),
        ("Act-02 (Regional Arena)", 120, 5),
        ("Act-03 (Global Arena)",   100, 5),
        ("Act-04 (Stadium A)",       45, 5),
        ("Act-05 (Stadium B)",       40, 5),
        ("Act-06 (Arena A)",         55, 4),
        ("Act-07 (Arena B)",         40, 4),
        ("Act-08 (Arena C)",         40, 4),
        ("Act-09 (Theater A)",       30, 3),
        ("Act-10 (Theater B)",       15, 3),
        ("Act-11 (Mid-Size)",        12, 3),
        ("Act-12 (Livehouse A)",    1.2, 2),
        ("Act-13 (Livehouse B)",    0.8, 2),
    ]
    overlap_band = [s for s in samples if 40 <= s[1] <= 55]
    distinct_tiers = len({s[2] for s in overlap_band})
    return len(overlap_band), distinct_tiers


def main() -> None:
    total_turns = 0
    print("=" * 94)
    print("PART 1 · Legacy Multiplicative Model Across 5 Strategies (40 turns, start=890)")
    print("=" * 94)
    legacy_strategies = [
        ("1. Routine Release Only (K=0.012)", 0.012),
        ("2. Stage / Promo Heavy  (K=0.030)", 0.030),
        ("3. Continuous Breakout  (K=0.100)", 0.100),
        ("4. Continuous Smash Hit (K=0.200)", 0.200),
        ("5. Continuous Viral     (K=0.500)", 0.500),
    ]
    for name, k in legacy_strategies:
        end_n, tier = run_legacy_buggy(k, start_fans=890.0, turns=40)
        total_turns += 40
        print(f"  {name:<36} | End Fans: {end_n:>11,} | Tier: {tier}")

    print("\n" + "=" * 94)
    print("PART 2 · Calibrated Nonlinear Model Across 5 Career Trajectories (2–12 yrs)")
    print("=" * 94)
    tracks = [
        ("Track A: 2yr Steady Indie (26 rels)",  2, build_yearly_schedule(2, [("release", 4), ("promo", 13)])),
        ("Track B: 3yr + 4 Breakouts",           3, build_yearly_schedule(3, [("release", 3), ("promo", 8)], {39: "breakout", 52: "breakout", 104: "breakout", 117: "breakout"})),
        ("Track C: 5yr + 10 Breakouts + Award",  5, build_yearly_schedule(5, [("release", 3), ("promo", 6)], {i: "breakout" for i in range(30, 260, 26)} | {200: "award"})),
        ("Track D: 8yr A-List + Global Award",   8, build_yearly_schedule(8, [("release", 3), ("promo", 6)], {i: "breakout" for i in range(30, 420, 26)} | {180: "award", 300: "award", 380: "global"})),
        ("Track E: 12yr Legend (2x Global)",    12, build_yearly_schedule(12, [("release", 3), ("promo", 6)], {i: "breakout" for i in range(30, 620, 26)} | {180: "award", 300: "award", 380: "global", 560: "global"})),
    ]
    results = []
    for name, yrs, seq in tracks:
        res = run_calibrated(seq)
        total_turns += len(seq)
        results.append(res)
        promos = ", ".join(f"T{k}@{v/52:.1f}y" for k, v in res["promo_turns"].items()) or "—"
        print(f"  {name:<36} | {yrs:>2}y | {res['end_fans']:>11,} | {res['end_tier']:<14} | {promos}")

    zero_escape = run_calibrated(tracks[1][2], n0=0.0, rep0=0.0)
    assert zero_escape["end_fans"] > 50_000, "Calibrated additive floor must allow 0-start progression"
    assert results[0]["end_fans"] < results[1]["end_fans"] < results[2]["end_fans"] < results[3]["end_fans"] < results[4]["end_fans"]
    assert results[4]["end_tier"].startswith("T5"), "12-year Legend trajectory must reach T5"

    print("\n" + "=" * 94)
    print("PART 3 · Post-Viral Fade Sensitivity Sweep (15 Silent Turns After Viral Peak)")
    print("=" * 94)
    viral_burst = [("viral", 1.0), ("viral", 1.0), ("smash", 0.5), ("breakout", 0.2), ("release", 0.1)] + [("idle", 1.0)] * 15
    retentions = []
    for lf, lbl in ((0.003, "No Extra Fade (L=0.003)"), (0.05, "Moderate Fade (L=0.05)"), (0.10, "Harsh Fade    (L=0.10)")):
        r = run_calibrated(viral_burst, fade_loss=lf)
        total_turns += len(viral_burst)
        peak = max(h[2] for h in r["history"])
        ret = r["end_fans"] / peak
        retentions.append(ret)
        print(f"  {lbl:<26} | Peak: {peak:>10,.0f} | @Turn 20: {r['end_fans']:>10,.0f} | Retention: {ret:>4.0%}")
    assert retentions[0] > 0.85 and retentions[2] < 0.25, "Harsh uncapped fade proves need for bounded fade window"

    print("\n" + "=" * 94)
    print("PART 4 · Illustrative Single-Metric Threshold Overlap (Qualitative Counterexample)")
    print("=" * 94)
    band_cnt, tier_cnt = check_single_metric_overlap()
    print(f"  40M–55M band samples: {band_cnt} | Distinct touring tiers in same band: {tier_cnt}")
    print("  Design takeaway: Single fan-count cutoffs cannot separate high-traffic vs touring acts -> 3-pillar gate.")
    assert band_cnt >= 4 and tier_cnt >= 2

    print(f"\n[PASS] All 4 deterministic curve calibration invariants verified ({total_turns:,} simulated steps).")


if __name__ == "__main__":
    main()
