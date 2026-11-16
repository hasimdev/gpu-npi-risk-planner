"""Command-line runner.

    python -m sim.cli                     # baseline
    python -m sim.cli --scenario all      # baseline plus the scenario memo's options
    python -m sim.cli --benchmark         # time 1M trials on the active backend
"""
from __future__ import annotations

import argparse
import time

from .model import get_xp, load_bom, simulate

# The scenarios behind program/05-scenario-packaging-slip.md.
SCENARIOS = {
    "baseline": {},
    "slip": {"advanced_packaging": {"extra_weeks": 6}},
    # Option B: second-source packaging. The slip goes away, but the new line
    # is less proven, so the disruption odds and the qualification time go up.
    "option_b_second_source": {
        "advanced_packaging": {"lead_time": [5, 7, 10], "p_disrupt": 0.30, "delay_weeks": 4},
    },
    # Option C: phased launch. A small first allocation is pulled from packaging
    # earlier (2 weeks shaved), and HBM is expedited at a premium.
    "option_c_phased": {
        "advanced_packaging": {"extra_weeks": 6 - 2},
        "hbm_stacks": {"lead_time": [9, 10, 14]},
    },
}


def show(name, r):
    lw = r["launch_weeks"]
    print(f"\n== {name}  ({r['samples']:,} trials on {r['backend']})")
    print(f"P(launch by week {r['target_weeks']:.0f}) = {r['p_on_time']:.1%}")
    print(f"P50 {lw['p50']:.1f} wk | P80 {lw['p80']:.1f} wk | P90 {lw['p90']:.1f} wk")
    serial = [c["name"] for c in r["critical_path"] if c["critical_share"] > 0.999]
    print("Always on the critical path: " + ", ".join(serial))
    print("Which input sets the pace (share of trials):")
    for c in [c for c in r["critical_path"] if 0 < c["critical_share"] <= 0.999][:5]:
        print(f"  {c['critical_share']:6.1%}  {c['name']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=100_000)
    ap.add_argument("--target", type=float, default=None)
    ap.add_argument("--scenario", default="baseline", choices=[*SCENARIOS, "all"])
    ap.add_argument("--benchmark", action="store_true")
    a = ap.parse_args()
    bom = load_bom()

    if a.benchmark:
        n = 1_000_000
        simulate(bom, samples=10_000)  # warm-up
        t = time.perf_counter()
        r = simulate(bom, samples=n)
        dt = time.perf_counter() - t
        print(f"{n:,} trials on {get_xp()[1]}: {dt:.2f} s")
        return

    names = list(SCENARIOS) if a.scenario == "all" else [a.scenario]
    for name in names:
        show(name, simulate(bom, samples=a.samples, target_weeks=a.target, overrides=SCENARIOS[name]))


if __name__ == "__main__":
    main()
