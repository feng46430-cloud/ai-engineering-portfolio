#!/usr/bin/env python3
"""
Clean-Room Five-Layer Card-Break / Gacha Box Probability & Anti-Overissue Simulator
-----------------------------------------------------------------------------------
Demonstrates deterministic probability governance for commercial card/loot-box systems:
  1. Five-layer domain model: Brand -> Line -> Product -> Box (12 Packs x 5 Slots) -> Checklist
  2. mulberry32 bitwise deterministic 32-bit PRNG for 100% reproducible QA seed replay
  3. Box-level guaranteed hit (Pity) vs. naive independent pack rolls
  4. Global 1/1 (One-of-One) serial inventory lock & dynamic weight re-normalization (zero over-issue)

Zero third-party dependencies (Python 3.9+ standard library only).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple


class Mulberry32:
    """Bit-exact Python port of the mulberry32 32-bit deterministic PRNG."""

    def __init__(self, seed: int) -> None:
        self.state = seed & 0xFFFFFFFF

    def next_float(self) -> float:
        self.state = (self.state + 0x6D2B79F5) & 0xFFFFFFFF
        t = self.state
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t = (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) ^ t
        t &= 0xFFFFFFFF
        t = (t ^ (t >> 14)) & 0xFFFFFFFF
        return t / 4294967296.0


@dataclass(frozen=True)
class TierSpec:
    tier_id: str
    label: str
    slot5_weight: float
    is_box_hit: bool = False
    global_cap: int | None = None  # e.g., 1 for 1/1 One-of-One


PRODUCT_CATALOG = {
    "brand": "ApexCollect",
    "line": "2026 Flagship Series",
    "product": "Hobby Box (12 Packs x 5 Cards)",
    "packs_per_box": 12,
    "slots_per_pack": 5,
    "checklist_tiers": [
        TierSpec("BASE_INSERT", "Silver Foil Insert", slot5_weight=0.9190, is_box_hit=False),
        TierSpec("JERSEY_RELIC", "Game-Worn Swatch Relic", slot5_weight=0.0550, is_box_hit=True, global_cap=None),
        TierSpec("AUTO_250", "On-Card Autograph /250", slot5_weight=0.0180, is_box_hit=True, global_cap=250),
        TierSpec("GOLD_99", "Gold Parallel /99", slot5_weight=0.0070, is_box_hit=True, global_cap=99),
        TierSpec("SUPER_1OF1", "Platinum 1/1 Unique", slot5_weight=0.0010, is_box_hit=True, global_cap=1),
    ],
}


def weighted_pick(rng: Mulberry32, choices: List[Tuple[TierSpec, float]]) -> TierSpec:
    total = sum(w for _, w in choices)
    r = rng.next_float() * total
    acc = 0.0
    for spec, weight in choices:
        acc += weight
        if r <= acc:
            return spec
    return choices[-1][0]


def simulate_print_run(num_boxes: int, master_seed: int, guarded: bool) -> Dict[str, object]:
    rng = Mulberry32(master_seed)
    tiers: List[TierSpec] = PRODUCT_CATALOG["checklist_tiers"]  # type: ignore[assignment]
    packs_per_box: int = PRODUCT_CATALOG["packs_per_box"]  # type: ignore[assignment]

    minted: Dict[str, int] = {t.tier_id: 0 for t in tiers}
    zero_hit_boxes = 0
    first_box_trace: List[str] = []

    for box_idx in range(num_boxes):
        box_has_hit = False
        # Pick which pack acts as the deterministic pity anchor if the first 11 packs miss
        pity_pack_idx = packs_per_box - 1

        for pack_idx in range(packs_per_box):
            # Slots 1-4 are deterministic Base checklist cards; Slot 5 is the chase slot
            eligible: List[Tuple[TierSpec, float]] = []
            for t in tiers:
                if guarded and t.global_cap is not None and minted[t.tier_id] >= t.global_cap:
                    continue  # Hard inventory depletion lock: prevents 1/1 or numbered over-issue
                eligible.append((t, t.slot5_weight))

            if guarded and pack_idx == pity_pack_idx and not box_has_hit:
                hit_pool = [(t, w) for t, w in eligible if t.is_box_hit]
                picked = weighted_pick(rng, hit_pool if hit_pool else eligible)
            else:
                picked = weighted_pick(rng, eligible)

            minted[picked.tier_id] += 1
            if picked.is_box_hit:
                box_has_hit = True
            if box_idx == 0:
                first_box_trace.append(picked.tier_id)

        if not box_has_hit:
            zero_hit_boxes += 1

    return {
        "boxes": num_boxes,
        "zero_hit_boxes": zero_hit_boxes,
        "zero_hit_rate_pct": round(zero_hit_boxes * 100.0 / num_boxes, 2),
        "minted": minted,
        "first_box_trace": first_box_trace,
    }


def main() -> None:
    boxes = 5000
    seed = 20261127

    naive = simulate_print_run(boxes, seed, guarded=False)
    guarded_run_1 = simulate_print_run(boxes, seed, guarded=True)
    guarded_run_2 = simulate_print_run(boxes, seed, guarded=True)

    replay_identical = guarded_run_1["first_box_trace"] == guarded_run_2["first_box_trace"]

    print("=" * 74)
    print(f"[Card-Break Probability Audit] {PRODUCT_CATALOG['line']} | {boxes} Boxes | Seed={seed}")
    print("=" * 74)
    print(f"{'Metric':<38} | {'BEFORE (Naive)':<15} | {'AFTER (Guarded)':<15}")
    print("-" * 74)
    print(
        f"{'Empty Boxes (0 Box-Hit Violation)':<38} | "
        f"{naive['zero_hit_boxes']} ({naive['zero_hit_rate_pct']}%)   | "
        f"{guarded_run_1['zero_hit_boxes']} ({guarded_run_1['zero_hit_rate_pct']}%)"
    )
    naive_1of1 = naive["minted"]["SUPER_1OF1"]  # type: ignore[index]
    guard_1of1 = guarded_run_1["minted"]["SUPER_1OF1"]  # type: ignore[index]
    print(f"{'Global 1/1 Unique Minted (Cap = 1)':<38} | {naive_1of1:<15} | {guard_1of1:<15}")
    naive_99 = naive["minted"]["GOLD_99"]  # type: ignore[index]
    guard_99 = guarded_run_1["minted"]["GOLD_99"]  # type: ignore[index]
    print(f"{'Gold Parallel /99 Minted (Cap = 99)':<38} | {naive_99:<15} | {guard_99:<15}")
    naive_250 = naive["minted"]["AUTO_250"]  # type: ignore[index]
    guard_250 = guarded_run_1["minted"]["AUTO_250"]  # type: ignore[index]
    print(f"{'Autograph /250 Minted (Cap = 250)':<38} | {naive_250:<15} | {guard_250:<15}")
    print(f"{'Mulberry32 Seed Replay Identical':<38} | {'N/A':<15} | {str(replay_identical):<15}")
    print("=" * 74)

    assert guarded_run_1["zero_hit_boxes"] == 0, "Box guarantee violated!"
    assert guard_1of1 <= 1, "Global 1/1 unique card over-issued!"
    assert guard_99 <= 99, "Numbered /99 parallel over-issued!"
    assert guard_250 <= 250, "Autograph /250 over-issued!"
    assert replay_identical, "Seed replay mismatch!"
    print("PASS: All box-guarantee, serial-depletion, and deterministic-replay gates green.")


if __name__ == "__main__":
    main()
