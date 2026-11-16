# NPI Phase-Gate Plan

Four builds, each ending in a go/no-go review. The TPM runs the review. The launch lead and the board engineering lead hold the decision, and either one can block it.

Week numbers are from program start and assume the baseline plan. When the simulation's P80 date moves, the gates below PVT move with it.

| Phase | Purpose | Build size | Target week | Exit gate criteria |
|---|---|---|---|---|
| EVT (engineering validation) | Does the design work? | 10–20 boards, early packaged parts | 18 | Board powers on and trains a reference model. Power, thermal and signal integrity are inside spec margins. Every open bug has an owner. No open design blocker |
| DVT (design validation) | Does it meet every spec, and can it pass certification? | 50–100 boards, production-intent parts | 23 | Full spec compliance. Regulatory (EMC, safety) testing started. Thermal validated at worst-case ambient. Second-source parts qualified, or the single-source risk accepted in writing |
| PVT (production validation) | Can the factory build it at yield? | Several hundred boards on the production line | 27 | Line yield at or above the target. Test coverage and burn-in time signed off. Packaging and HBM allocation confirmed for the first production quarter |
| MP (mass production) | Ship | Production volume | 30 (launch ready) | PVT yield holds across two consecutive lots. Field-return and RMA process in place. Launch quantity in finished goods |

## What each gate asks of supply

The phase gates are about engineering, but most NPI slips start in supply, so each review also checks the supply plan.

| Gate | Supply question asked at the review |
|---|---|
| EVT | Are wafer starts for DVT and PVT placed? Is HBM allocation requested for PVT and MP volumes? |
| DVT | Is packaging capacity booked for PVT and the first MP quarter? What does the latest simulation say about P(on-time)? |
| PVT | Is every tier-3 supplier in the risk register green or amber? Any red item needs an approved mitigation before MP |
| MP | Is the next quarter's allocation confirmed? |

## Gate rules

- A gate passes, fails, or passes with conditions. A conditional pass names the condition, the owner and the date, and the condition gets its own row in the risk register.
- Nobody moves a gate date in a status update. A date only moves at a gate review, with the reason written down.
- The simulation is rerun before every gate with the latest supplier commitments. The P(on-time) and P80 figures go in the gate summary.
