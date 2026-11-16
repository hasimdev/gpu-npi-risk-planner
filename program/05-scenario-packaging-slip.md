# Scenario Memo: Advanced Packaging Capacity Slips 6 Weeks

**To:** Launch lead, sourcing, finance
**From:** Program TPM
**Date:** 2026-11-15
**Decision needed by:** next DVT review

## Summary

The packaging supplier has told us our PVT and first-production slots will run 6 weeks late. Packaging is a serial step for every board, so the delay passes straight through to launch. Under the current plan the chance of being launch-ready by week 30 drops from 46% to effectively zero.

The baseline was already weak. Before this news, the week-30 date was a coin flip (46%). Whatever option we choose, I recommend recommitting to a P80 date instead of a P50 date.

**Recommendation:** qualify a second packaging source (option B), and recommit externally to week 35. That holds the launch within about two weeks of plan at P80 and costs a qualification effort and a unit premium. If qualification can't start within two weeks, fall back to option A and recommit to week 40.

## The numbers

Every figure comes from `python -m sim.cli --scenario all` (100,000 trials, seed 7). The inputs are illustrative assumptions (see [`sim/bom.yaml`](../sim/bom.yaml) and the scenario definitions in [`sim/cli.py`](../sim/cli.py)).

| Scenario | P(launch by wk 30) | P50 | P80 | P90 |
|---|---|---|---|---|
| Baseline (before the news) | 46.4% | 30.3 | 33.9 | 35.8 |
| Slip, no action | 0.0% | 36.3 | 39.9 | 41.8 |
| Option B: second-source packaging | 27.7% | 31.7 | 34.4 | 35.9 |
| Option C: phased launch, expedite HBM | 2.3% | 34.0 | 37.4 | 39.4 |

## Options

### A. Accept the slip and recommit

Keep the single packaging source and move the launch-ready commitment to week 40, the P80 under the slip.

- Cost: no new spend.
- Schedule: P80 moves from about week 34 to week 40.
- Risk: we stay single-sourced on the step that just slipped. If it slips again, there is no fallback.

### B. Qualify a second packaging source (recommended)

Bring up a second advanced-packaging line. In the model, its process takes longer to run (5–9 weeks against 4–9 weeks) and has higher disruption odds (30% against 20%) because the line is newer to this product.

- Cost: qualification engineering time, plus a per-unit premium on second-source volume. Both need a quote from sourcing before the DVT review.
- Schedule: P80 of week 34.4, within a week of the original baseline P80. Week 30 itself only reaches 28%, so this does not rescue the original date.
- Risk: qualification has to finish before PVT. If it slips, we fall back to A, having lost about two weeks.
- Side benefit: it removes the single-source exposure on the riskiest step for every product after this one.

### C. Phased launch with an HBM expedite

Ask the packaging supplier for a small early allocation (about 2 weeks sooner for a limited first batch), and pay to expedite HBM so it isn't the next constraint.

- Cost: HBM expedite premium. The first batch is small, so launch volume is limited.
- Schedule: P80 of week 37.4. Better than A, worse than B.
- Risk: the early allocation depends on the supplier's goodwill, and the expedite does little because HBM was setting the pace in only 18% of trials. The die and packaging still dominate.

## What the model says that the slip report doesn't

- Board-side parts (PCB, power, thermal) never set the date in this plan. Spending on board-side expedites would not move launch at all.
- In option C, expediting HBM cuts its critical-path share from 18% to 8%. That is real, but the GPU die then sets the pace in about 91% of trials, so the overall gain is small.
- The original week-30 commitment was never better than even odds. The bigger lesson is to commit at P80 from the start.

## Next steps if B is approved

| Action | Owner | Due |
|---|---|---|
| Quote for qualification effort and unit premium | Packaging sourcing | Before DVT review |
| Qualification plan with exit criteria | Board eng + manufacturing | Within 2 weeks of approval |
| Update the model with the quoted lead times and rerun | TPM | Within 1 day of quotes |
| Communicate the recommitted P80 date | Launch lead | After the DVT review |
