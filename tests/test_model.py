import os

os.environ.setdefault("SIM_BACKEND", "numpy")

import pytest
from fastapi.testclient import TestClient

from sim.api import app
from sim.model import load_bom, simulate, topo_order

BOM = load_bom()


def test_bom_loads_and_orders_parents_after_children():
    order = topo_order(BOM["parts"])
    for k, part in BOM["parts"].items():
        for n in part.needs:
            assert order.index(n) < order.index(k)
    assert order[-1] == BOM["root"]


def test_launch_never_beats_the_fastest_possible_path():
    r = simulate(BOM, samples=20_000)
    # Shortest chain: die 14 + packaging 4 + test 1 + assembly 1 + board test 1.
    assert r["launch_weeks"]["p10"] >= 21
    assert 0 <= r["p_on_time"] <= 1


def test_packaging_slip_moves_the_date_by_about_the_slip():
    base = simulate(BOM, samples=50_000)
    slip = simulate(BOM, samples=50_000, overrides={"advanced_packaging": {"extra_weeks": 6}})
    assert slip["launch_weeks"]["p50"] - base["launch_weeks"]["p50"] == pytest.approx(6, abs=0.3)
    assert slip["p_on_time"] < base["p_on_time"]


def test_serial_parts_are_always_critical_and_inputs_split_the_rest():
    r = simulate(BOM, samples=20_000)
    share = {c["part"]: c["critical_share"] for c in r["critical_path"]}
    assert share["advanced_packaging"] == pytest.approx(1.0)
    inputs = share["gpu_die"] + share["hbm_stacks"] + share["interposer_substrate"]
    assert inputs == pytest.approx(1.0, abs=1e-6)


def test_same_seed_gives_same_answer():
    assert simulate(BOM, samples=5_000)["p_on_time"] == simulate(BOM, samples=5_000)["p_on_time"]


def test_api_runs_a_scenario():
    c = TestClient(app)
    r = c.get("/api/simulate", params={"scenario": "slip", "samples": 5000})
    assert r.status_code == 200
    assert r.json()["scenario"] == "slip"
    assert c.get("/").status_code == 200
