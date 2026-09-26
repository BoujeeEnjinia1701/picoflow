---
doc_id: PCF-REQ-001
title: PicoFlow requirements
project: PicoFlow
doc_type: Requirements
version: "0.4"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply Amish's 2026-09-25 decisions (PCF-DDR-001), R15 to $450, add R17 penstock surge, status from PCF-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# PicoFlow requirements

These requirements were set at TRL 2 and checked by calculation at TRL 3 in PCF-CAL-001 v0.2. The status column gives the TRL 3 result; "not verifiable at TRL 3" means a bench or site test is needed. Decisions of 2026-09-25 are recorded in PCF-DDR-001 (the budget in R15 is $450, and R17 was added for the drainage-grade penstock) and PCF-DDR-002 (125 mm design-point penstock, R2 stated per head, R4 relaxed to 20 W, R14 definition confirmed, R15 margin accepted). Targets are still not validated with users or at a site.

The **design point** used throughout is 2.0 m of gross head (forebay water surface to nozzle centerline) and 10 L/s through two nozzles, with a 20 m run of 125 mm PVC penstock (decided by Amish, 2026-09-25, PCF-DDR-002).

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (PCF-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Operating head range | Generates from 1.0 to 3.0 m gross head with the same runner, changing only nozzle inserts | Performance calculation across the range | Met; DC bus 20.2 V at 1.0 m |
| R2 | Flow range | 5 to 10 L/s at 1.0 m and 5 to 15 L/s from 2.0 m gross head, through interchangeable nozzle inserts, one or two jets | Nozzle sizing calculation | Met; 1.3 to 11.3 L/s at 1.0 m, 1.9 to 16.1 L/s at 2.0 m |
| R3 | Output at the design point | 80 W or more DC into the battery at 2.0 m and 10 L/s | Efficiency chain calculation; later bench test | Met, 82.8 W (2.8 W margin) |
| R4 | Output at the lowest head | 20 W or more DC into the battery at 1.0 m and 7 L/s | Efficiency chain calculation | Met, 26.3 W |
| R5 | Water-to-wire efficiency | 40 % or more at the design point, from gross hydraulic power to DC into the battery | Calculation; later test | Met, 43.2 % |
| R6 | Daily energy | 1.8 kWh or more per day at the design point, running 24 h | Calculation | Met, 1.99 kWh |
| R7 | Battery charging and load control | Charges a 12 V nominal battery; holds the runner within 10 % of its best speed while charging; diverts 100 % of output to the dump load within 1 s when the battery is full or disconnected | Controller design review; later bench test | Not verifiable at TRL 3; dump load 1.68 times the largest output |
| R8 | Runaway and touch voltage | Every part survives indefinite runaway at 3.0 m head with no damage; no exposed conductor above 60 V DC in any state, including runaway | Speed and voltage calculation; design review | Met by calculation: hardware clamp keeps the bus at 48 V or less; 79.5 V only on a double fault, inside the enclosed 100 V DC side; generator overspeed rating to confirm |
| R9 | Printable parts | Runner and nozzles print on a 220 x 220 x 250 mm build volume in PETG or nylon; runner prints in 24 h or less | Model check; slicer estimate | Met (estimate); 200 x 200 x 50 mm, about 21 h |
| R10 | Debris tolerance | Intake screen aperture 6 mm or less; smallest nozzle 20 mm or more; screen self-cleans by overflow | Design review | Met by design |
| R11 | Serviceability | Runner or nozzle inserts replaced with hand tools in 30 min or less; bearings in 60 min or less; bearings and generator above the spray zone | Design review; later timed trial | Not verifiable at TRL 3; bearings above the spray by layout |
| R12 | Service life | Bearing L10 life 20,000 h or more; runner 1 year (8,760 h) or more before replacement | Bearing life calculation; material review | **At risk**; bearings about 8.7 x 10^6 h, printed runner life unknown |
| R13 | Setting height | Nozzle centerline 0.3 m or less above normal tailwater, so little head is lost below the jet | Model check | Met, 280 mm in the model |
| R14 | Portability | Heaviest single item 15 kg or less; turbine unit (items 1 to 6 and 11) 25 kg or less, carried to site by two people | Mass estimate | Met, 22.2 kg; generator 7.0 kg (definition confirmed by Amish, PCF-DDR-002) |
| R15 | Cost | Turbine kit (all items except penstock and battery) $450 or less in parts; salvaged-motor variant documented | Priced BOM (`bom/bom.csv`) | Met, $448.00; $2 margin accepted by Amish (PCF-DDR-002), prices to be firmed with quotes before any build; $378.00 with a salvaged motor |
| R16 | Stream protection | Takes no more than half of the dry-season stream flow and returns all water to the same stream; intake passes fish-safe overflow | Site survey; design review | Not verifiable at TRL 3 (site-dependent) |
| R17 | Penstock surge | Peak pressure at the valve (static plus surge) 50 kPa or less at 3.0 m head, with a valve that cannot close in under 10 s | Surge calculation | Met, 33.3 kPa with a multi-turn gate valve |

## Requirements not met or at risk

No requirement is not met by calculation after the decisions of 2026-09-25 (PCF-DDR-002):

- **R2** is now stated per head (5 to 10 L/s at 1.0 m, 5 to 15 L/s from 2.0 m), because 15 L/s at 1.0 m would need 57 mm jets on a 150 mm pitch circle.
- **R3 and R5** are met with the 125 mm design-point penstock (82.8 W, 43.2 %). The margin on R3 is 2.8 W, so it depends on the runner reaching the assumed 75 % and on the inlet valve being full bore (see `docs/REVIEW.md`).
- **R4** was relaxed from 30 W to 20 W; the calculation gives 26.3 W.
- **R12 (runner life) remains at risk.** Only a TRL 4 test can close it.
- **R15** is met with the $2 margin accepted; indicative prices may move either way.

## Budget scope

The $450 budget covers the turbine kit: runner, shaft, bearings, coupling, generator, housing, manifold and nozzles, valve, forebay and screen, frame, equipment post, rectifier, controller, dump-load and clamp resistors, and wiring. The penstock and the household battery are site- and household-specific and are costed separately (decided by Amish, 2026-09-25, PCF-DDR-001 D1).

## Assumptions

The full list is in PCF-CAL-001 section 2. The main ones are:

- Penstock: 125 mm drainage PVC, SN8 (117.6 mm bore), 20 m, with a rounded entrance, screen, two bends and a gate valve; branches 90 mm.
- Nozzle velocity coefficient 0.97.
- Runner jet-to-shaft efficiency 75 % for a first printed design, below the 87 to 91 % reached in laboratory work on an optimized low-head Turgo ([Williamson et al., 2013](https://research-information.bris.ac.uk/en/publications/performance-of-a-low-head-pico-hydro-turgo-turbine)).
- Generator about 10 rpm per volt of rectified DC, 12 W fixed loss at 340 rpm, 0.8 Ω; rectifier 1.6 V drop; buck converter 94 %.
- Drainage pipe joints good for 50 kPa, to be confirmed with the supplier.

> **Safety:** R8 and R17 are safety requirements. They are met on paper only; neither the clamp nor the pipe rating has been tested.
