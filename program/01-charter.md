# Program Charter: GPU Board NPI Supply Risk

**Program TPM:** Abu Ansari
**Status:** Draft
**Last updated:** 2026-11-15

## Problem

A new datacenter GPU board has a committed launch-ready date of week 30 from program start. The date was set top-down, by adding up typical supplier lead times along one path. Nobody has asked how likely it is, which suppliers decide it, or what happens when one of them slips. On a board like this the slow parts are well known: leading-edge silicon, HBM memory, and advanced 2.5D packaging. Packaging is the step where all three meet.

This program gives the launch team a supply plan they can defend. It covers the probability of hitting the date, the parts that drive it, a phase-gate plan, a supplier risk register, and pre-worked options for the most likely bad news.

## A note on the data

This is a portfolio program. The BOM is simplified to about ten parts. Every lead time, disruption probability and delay in [`sim/bom.yaml`](../sim/bom.yaml) is an illustrative assumption, loosely shaped by public reporting on GPU supply chains. None of it is real supplier data. What carries over to a real program is the method, the structure and the decisions. The specific numbers don't.

## Scope

In scope:

- A multi-tier BOM model: silicon, HBM, interposer and substrate, advanced packaging, package test, PCB, power stages, thermal, board assembly and board test
- A Monte Carlo simulation of lead times and disruptions that reports P(on-time launch), P50/P80/P90 dates and the critical-path share for each part
- An EVT / DVT / PVT / MP phase-gate plan ([02-phase-gates.md](02-phase-gates.md))
- A supplier risk register with owners and mitigations ([03-supplier-risk-register.md](03-supplier-risk-register.md))
- A RACI ([04-raci.md](04-raci.md))
- A scenario memo on a 6-week packaging slip ([05-scenario-packaging-slip.md](05-scenario-packaging-slip.md))
- A small API and dashboard so the launch team can rerun scenarios themselves

Out of scope:

- Unit volume and allocation planning (how many boards ship at launch, and to whom)
- Cost modeling beyond rough relative premiums in the scenario memo
- Real supplier data, contracts or pricing

## Success criteria

1. The simulation reproduces known behavior. Tests confirm that a 6-week slip on a serial step moves the median launch date by about 6 weeks, and that the shares for packaging inputs always add up to 100%.
2. The launch team gets a P(on-time) figure and a P80 date for the current plan, not a single-point date.
3. Every tier-2 and tier-3 supplier in the BOM has an entry in the risk register with an owner and a trigger.
4. The scenario memo gives leadership three costed options with a recommendation, and every number in it can be reproduced with one command.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| Launch / product lead | A launch date they can commit to externally |
| Silicon operations | Wafer starts and die availability |
| Memory and packaging sourcing | HBM allocation and packaging capacity |
| Board engineering | PCB, power and thermal readiness for EVT/DVT |
| Manufacturing / contract manufacturer | Assembly and test capacity, yield |
| Finance | Expedite premiums and second-source qualification cost |
