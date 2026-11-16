"""Monte Carlo lead-time model for a multi-tier GPU board BOM.

Each simulated trial samples a duration for every part, adds any disruption
delay, and rolls finish times up the BOM: a part finishes at
max(finish of everything it needs) + its own duration. The launch date is the
root's finish time.

Runs on the GPU with CuPy when it is installed, otherwise on NumPy. Set
SIM_BACKEND=numpy to force the CPU path.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import yaml

BOM_PATH = Path(__file__).with_name("bom.yaml")


def get_xp():
    """Return (array module, backend name)."""
    if os.environ.get("SIM_BACKEND", "").lower() != "numpy":
        try:
            import cupy as cp  # noqa: F401

            cp.cuda.runtime.getDeviceCount()
            return cp, "cupy"
        except Exception:
            pass
    return np, "numpy"


@dataclass
class Part:
    key: str
    name: str
    tier: int
    lead_time: tuple[float, float, float]
    needs: list[str] = field(default_factory=list)
    p_disrupt: float = 0.0
    delay_weeks: float = 0.0


def load_bom(path: Path | str = BOM_PATH) -> dict:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    parts = {}
    for key, p in raw["parts"].items():
        d = p.get("disruption") or {}
        parts[key] = Part(
            key=key,
            name=p["name"],
            tier=p["tier"],
            lead_time=tuple(float(v) for v in p["lead_time"]),
            needs=list(p.get("needs", [])),
            p_disrupt=float(d.get("p", 0.0)),
            delay_weeks=float(d.get("delay_weeks", 0.0)),
        )
    for part in parts.values():
        for n in part.needs:
            if n not in parts:
                raise ValueError(f"{part.key} needs unknown part {n!r}")
    return {"target_weeks": float(raw["target_weeks"]), "root": raw["root"], "parts": parts}


def topo_order(parts: dict[str, Part]) -> list[str]:
    order, state = [], {}

    def visit(k):
        if state.get(k) == "done":
            return
        if state.get(k) == "active":
            raise ValueError(f"cycle in BOM at {k}")
        state[k] = "active"
        for n in parts[k].needs:
            visit(n)
        state[k] = "done"
        order.append(k)

    for k in parts:
        visit(k)
    return order


def _triangular(xp, rng, lo, mode, hi, n):
    if hi == lo:
        return xp.full(n, lo, dtype=xp.float32)
    u = rng.random(n, dtype=xp.float32)
    c = (mode - lo) / (hi - lo)
    left = lo + xp.sqrt(u * (hi - lo) * (mode - lo))
    right = hi - xp.sqrt((1 - u) * (hi - lo) * (hi - mode))
    return xp.where(u < c, left, right)


def simulate(
    bom: dict,
    samples: int = 100_000,
    target_weeks: float | None = None,
    overrides: dict[str, dict] | None = None,
    seed: int = 7,
):
    """Run the simulation.

    overrides: {part_key: {"extra_weeks": float, "p_disrupt": float,
                           "delay_weeks": float, "lead_time": [lo, mode, hi]}}
    Returns a plain-Python dict (JSON-safe).
    """
    xp, backend = get_xp()
    rng = xp.random.default_rng(seed)
    parts = bom["parts"]
    target = bom["target_weeks"] if target_weeks is None else float(target_weeks)
    overrides = overrides or {}
    order = topo_order(parts)

    finish, argmax_child = {}, {}
    for k in order:
        p = parts[k]
        o = overrides.get(k, {})
        lo, mode, hi = o.get("lead_time", p.lead_time)
        dur = _triangular(xp, rng, lo, mode, hi, samples)
        pd = o.get("p_disrupt", p.p_disrupt)
        if pd > 0:
            hit = rng.random(samples, dtype=xp.float32) < pd
            dur = dur + hit * o.get("delay_weeks", p.delay_weeks)
        dur = dur + o.get("extra_weeks", 0.0)
        if p.needs:
            stacked = xp.stack([finish[n] for n in p.needs])
            argmax_child[k] = xp.argmax(stacked, axis=0)
            start = xp.max(stacked, axis=0)
        else:
            start = xp.zeros(samples, dtype=xp.float32)
        finish[k] = start + dur

    # Mark which parts sit on the critical path in each trial.
    root = bom["root"]
    crit = {root: xp.ones(samples, dtype=bool)}
    for k in reversed(order):
        if k not in crit:
            crit[k] = xp.zeros(samples, dtype=bool)
        for i, n in enumerate(parts[k].needs):
            on = crit[k] & (argmax_child[k] == i)
            crit[n] = crit.get(n, xp.zeros(samples, dtype=bool)) | on

    launch = finish[root]
    to_host = (lambda a: a.get()) if backend == "cupy" else (lambda a: a)
    launch_h = to_host(launch)

    critical = sorted(
        (
            {"part": k, "name": parts[k].name, "tier": parts[k].tier,
             "critical_share": float(to_host(crit[k].mean()))}
            for k in parts if parts[k].tier > 0
        ),
        key=lambda r: -r["critical_share"],
    )
    pct = np.percentile(launch_h, [10, 50, 80, 90])
    hist, edges = np.histogram(launch_h, bins=30)
    return {
        "backend": backend,
        "samples": samples,
        "target_weeks": target,
        "p_on_time": float((launch_h <= target).mean()),
        "launch_weeks": {"p10": float(pct[0]), "p50": float(pct[1]),
                         "p80": float(pct[2]), "p90": float(pct[3]),
                         "mean": float(launch_h.mean())},
        "critical_path": critical,
        "histogram": {"counts": hist.tolist(), "edges": [float(e) for e in edges]},
    }
