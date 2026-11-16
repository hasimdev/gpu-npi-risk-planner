# Supplier Risk Register

All probabilities and delays match the illustrative assumptions in [`sim/bom.yaml`](../sim/bom.yaml). Change them together, or the register and the model will disagree.

Status: **Red** means it threatens the launch date now, **Amber** means it's being watched with a trigger set, **Green** means it's under control.

Critical-path share comes from the baseline run (100,000 trials, seed 7). It is the fraction of trials in which this part sets the launch date.

| ID | Part / supplier tier | Risk | Likelihood (model) | Impact (model) | Critical-path share | Status | Owner | Trigger | Mitigation |
|---|---|---|---|---|---|---|---|---|---|
| SR-01 | Advanced packaging (tier 2) | Capacity is booked by bigger customers; allocation cut or delayed | 20% | +6 wk | 100% (serial) | Red | Packaging sourcing | Supplier confirms less than 80% of requested PVT slots | Book PVT and MP slots at EVT. Start qualifying a second packaging source now (see [scenario memo](05-scenario-packaging-slip.md)) |
| SR-02 | HBM stacks (tier 3) | Allocation shortfall from tight industry supply | 15% | +6 wk | 18% | Amber | Memory sourcing | Allocation letter not received 12 weeks before PVT | Request allocation at EVT. Pre-negotiate an expedite option. Qualify a second HBM vendor at DVT if the design allows |
| SR-03 | GPU die (tier 3) | Wafer start delay or a yield problem at the leading-edge node | 5% | +4 wk | 81% | Amber | Silicon ops | Die yield below plan on the first lot | Place DVT/PVT wafer starts early. Hold die bank for PVT |
| SR-04 | Interposer and substrate (tier 3) | Substrate capacity constraint | 10% | +4 wk | 1% | Green | Packaging sourcing | Lead time quoted above 14 weeks | Order with packaging slots. Low share today, but watch it if the die gets faster |
| SR-05 | Power stages / VRM (tier 2) | Component allocation (common parts, broad demand) | 10% | +4 wk | 0% | Green | Board sourcing | Distributor lead time above 12 weeks | Second source on the approved vendor list |
| SR-06 | PCB (tier 2) | High-layer-count fab capacity | 5% | +2 wk | 0% | Green | Board sourcing | First-article failure | Two qualified fabs |
| SR-07 | Board test and burn-in (tier 1) | Test escapes or burn-in failures force rework | 5% | +2 wk | 100% (serial) | Amber | Manufacturing | PVT first-pass yield below target | Burn-in time and test coverage signed off at DVT. Spare tester capacity at the contract manufacturer |
| SR-08 | Thermal solution (tier 2) | Late design change after DVT thermal testing | Not modeled | — | 0% | Green | Board engineering | Thermal margin under 5 °C at worst-case ambient | Freeze thermal design at DVT exit |

## How to read this

The model says something that a single-point plan hides. Board-side parts (PCB, power, thermal) almost never set the date, because they finish weeks before packaged GPUs are ready. Program attention belongs on the packaging chain: the die, HBM and packaging itself. If PCB lead times slip by a few weeks, that is noise. If packaging slips by a few weeks, the launch date moves week for week.

## Change log

| Date | Change |
|---|---|
| 2026-11-15 | Register created from the baseline model |
