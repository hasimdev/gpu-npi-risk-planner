# GPU Supply Chain and NPI Risk Planner

This program asks how likely a new GPU board is to hit its launch date, and what to do when a supplier slips. It is run the way a technical program manager would run the supply side of a hardware launch. There is a charter, an EVT/DVT/PVT phase-gate plan, a supplier risk register and a RACI, plus a scenario memo that gives leadership three options and a recommendation.

Behind the documents is a small Monte Carlo model of a multi-tier GPU board BOM: leading-edge die, HBM memory, interposer and substrate, advanced 2.5D packaging, then board parts, assembly and test. It reports the probability of an on-time launch, P50/P80/P90 dates, and how often each part sets the date.

**About the data:** every lead time, probability and delay in this repo is an illustrative assumption, loosely shaped by public reporting on GPU supply chains. None of it is real supplier data. The method and the program structure are the point.

## Program artifacts

Start here.

| Document | What it covers |
|---|---|
| [Charter](program/01-charter.md) | Problem, scope, success criteria, stakeholders |
| [Phase gates](program/02-phase-gates.md) | EVT / DVT / PVT / MP: purpose, build size, exit criteria, and the supply questions asked at each gate |
| [Supplier risk register](program/03-supplier-risk-register.md) | Eight supplier risks with likelihood, impact, critical-path share, owner, trigger and mitigation |
| [RACI](program/04-raci.md) | Who does what, and who has to agree before a date moves |
| [Scenario memo: packaging slips 6 weeks](program/05-scenario-packaging-slip.md) | Three costed options and a recommendation, with every number reproducible |

## What the model found

From the baseline run (100,000 trials):

| Scenario | P(launch by wk 30) | P50 | P80 |
|---|---|---|---|
| Baseline plan | 46.4% | 30.3 | 33.9 |
| Packaging slips 6 weeks, no action | 0.0% | 36.3 | 39.9 |
| Option B: second-source packaging | 27.7% | 31.7 | 34.4 |
| Option C: phased launch, expedite HBM | 2.3% | 34.0 | 37.4 |

Three findings drive the recommendations:

1. The week-30 commitment was a coin flip before anything went wrong. The program should commit at P80.
2. The packaging chain sets the date. The GPU die is the slowest input in 81% of trials, HBM in 18%. Board-side parts (PCB, power, thermal) never set it, so expediting them buys nothing.
3. A second packaging source recovers most of a 6-week slip at P80. Expediting HBM recovers much less, because HBM is rarely the constraint.

## Run it

```bash
pip install -r requirements.txt
```

```bash
python -m sim.cli --scenario all
```

```bash
uvicorn sim.api:app --reload
```

Then open http://127.0.0.1:8000 to change the scenario, target week or packaging slip and rerun.

Tests:

```bash
python -m pytest -q
```

The tests check that the BOM rolls up in dependency order, that a 6-week slip on a serial step moves the median date by about 6 weeks, that the packaging inputs' critical-path shares add up to 100%, and that the API serves both the dashboard and the simulation.

## CPU vs GPU

The simulation runs on CuPy when a CUDA GPU is available and falls back to NumPy otherwise (`SIM_BACKEND=numpy` forces the CPU). The same code runs on both.

```bash
python -m sim.cli --benchmark
```

| Backend | Hardware | 1,000,000 trials |
|---|---|---|
| NumPy | Windows laptop CPU | 0.52–0.59 s (3 runs) |
| CuPy | TBD, measured | TBD, measured |

At this BOM size, NumPy is already fast enough for interactive use. The GPU path matters once the model grows to a realistic BOM with hundreds of parts, per-lot yield and allocation constraints, or millions of trials for tail risk. The GPU number goes here once it has been measured.

## Layout

```
program/            charter, phase gates, risk register, RACI, scenario memo
sim/bom.yaml        the BOM: parts, dependencies, lead times, disruptions (illustrative)
sim/model.py        Monte Carlo engine (NumPy or CuPy)
sim/cli.py          scenarios and benchmark
sim/api.py          FastAPI service
sim/static/         dashboard
tests/              pytest suite
```

## Related

[GPU Cluster Bring-Up Program](https://github.com/hasimdev/gpu-cluster-bringup-program) is the infrastructure side of the same portfolio.
