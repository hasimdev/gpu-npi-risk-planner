"""FastAPI service and dashboard.

    uvicorn sim.api:app --reload
    open http://127.0.0.1:8000
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse

from .cli import SCENARIOS
from .model import load_bom, simulate

app = FastAPI(title="GPU NPI Risk Planner")
BOM = load_bom()
STATIC = Path(__file__).with_name("static")


@app.get("/")
def dashboard():
    return FileResponse(STATIC / "index.html")


@app.get("/api/scenarios")
def scenarios():
    return {"scenarios": list(SCENARIOS), "target_weeks": BOM["target_weeks"]}


@app.get("/api/simulate")
def run(
    scenario: str = Query("baseline"),
    target_weeks: float | None = Query(None, ge=1, le=104),
    packaging_slip_weeks: float = Query(0, ge=0, le=26),
    samples: int = Query(100_000, ge=1_000, le=2_000_000),
):
    overrides = {k: dict(v) for k, v in SCENARIOS.get(scenario, {}).items()}
    if packaging_slip_weeks:
        o = overrides.setdefault("advanced_packaging", {})
        o["extra_weeks"] = o.get("extra_weeks", 0) + packaging_slip_weeks
    result = simulate(BOM, samples=samples, target_weeks=target_weeks, overrides=overrides)
    result["scenario"] = scenario
    return result
