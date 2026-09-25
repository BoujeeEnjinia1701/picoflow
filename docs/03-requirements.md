---
doc_id: PCF-REQ-001
title: PicoFlow requirements
project: PicoFlow
doc_type: Requirements
version: "0.2"
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
---

# PicoFlow requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users or at a site, and will be checked by calculation at TRL 3. The status column compares each target with the first-order estimates in PCF-PRC-001; every status is an estimate.

The **design point** used throughout is 2.0 m of gross head (forebay water surface to nozzle centerline) and 10 L/s through two nozzles, with a 20 m run of 110 mm PVC penstock.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (estimate) |
| --- | --- | --- | --- | --- |
| R1 | Operating head range | Generates from 1.0 to 3.0 m gross head with the same runner, changing only nozzle inserts | Performance calculation across the range | Met by design |
| R2 | Flow range | 5 to 15 L/s through interchangeable nozzle inserts, one or two jets | Nozzle sizing calculation | Met by design |
| R3 | Output at the design point | 80 W or more DC into the battery at 2.0 m and 10 L/s | Efficiency chain calculation; later bench test | Met, about 90 W, thin margin |
| R4 | Output at the lowest head | 30 W or more DC into the battery at 1.0 m and 7 L/s | Efficiency chain calculation | **At risk**, about 30 W |
| R5 | Water-to-wire efficiency | 40 % or more at the design point, from gross hydraulic power to DC into the battery | Calculation; later test | Met, about 46 % |
| R6 | Daily energy | 1.8 kWh or more per day at the design point, running 24 h | Calculation | Met, about 2.2 kWh |
| R7 | Battery charging and load control | Charges a 12 V nominal battery; holds the runner within 10 % of its best speed while charging; diverts 100 % of output to the dump load within 1 s when the battery is full or disconnected | Controller design review; later bench test | Unverified |
| R8 | Runaway and touch voltage | Every part survives indefinite runaway at 3.0 m head with no damage; no exposed conductor above 60 V DC in any state, including runaway | Speed and voltage calculation; design review | **Not met**, runaway open-circuit voltage about 83 V |
| R9 | Printable parts | Runner and nozzles print on a 220 x 220 x 250 mm build volume in PETG or nylon; runner prints in 24 h or less | Model check; slicer estimate | Met by geometry (200 mm runner) |
| R10 | Debris tolerance | Intake screen aperture 6 mm or less; smallest nozzle 20 mm or more; screen self-cleans by overflow | Design review | Met by design |
| R11 | Serviceability | Runner or nozzle inserts replaced with hand tools in 30 min or less; bearings in 60 min or less; bearings and generator above the spray zone | Design review; later timed trial | Met by layout, unverified |
| R12 | Service life | Bearing L10 life 20,000 h or more; runner 1 year (8,760 h) or more before replacement | Bearing life calculation; material review | **At risk**, printed runner creep and erosion unverified |
| R13 | Setting height | Nozzle centerline 0.3 m or less above normal tailwater, so little head is lost below the jet | Model check | **Not met**, about 0.44 m in the massing model |
| R14 | Portability | Heaviest single item 15 kg or less; turbine unit 25 kg or less, carried to site by two people | Mass estimate | Met, about 20 kg (estimate) |
| R15 | Cost | Turbine kit (all items except penstock and battery) $350 or less in parts | Priced BOM (`bom/bom.csv`) | **Not met**, about $424 with a new generator; about $354 with a salvaged one |
| R16 | Stream protection | Takes no more than half of the dry-season stream flow and returns all water to the same stream; intake passes fish-safe overflow | Site survey; design review | Site-dependent |

## Requirements not met or at risk

- **R8 (touch voltage) not met.** At 3.0 m head a runner with no load runs at about 830 rpm, which drives an estimated 83 V open circuit from a generator sized for 12 V charging. Options are a voltage clamp on the dump load, an enclosed DC side rated for 100 V, or both.
- **R13 (setting height) not met.** The frame in the massing model puts the nozzles about 0.44 m above the ground, which wastes about 18 % of a 2.44 m site drop. The frame must be lowered or the housing sunk into the tailrace, while keeping the runner above flood tailwater.
- **R15 (cost) not met.** About $424 with a new low-speed BLDC generator, about 21 % over. A salvaged direct-drive washing machine motor brings the kit to about $354, about at budget within the accuracy of these estimates.
- **R4 (1 m output) and R12 (runner life) at risk.**

## Assumptions

- Penstock friction loss about 10 % of gross head (110 mm PVC, 20 m, 10 L/s). Shorter or larger pipes lose less.
- Nozzle velocity coefficient 0.97.
- Runner jet-to-shaft efficiency 75 % for a first printed design, below the 87 to 91 % reached in laboratory work on an optimized low-head Turgo ([Williamson et al., 2013](https://research-information.bris.ac.uk/en/publications/performance-of-a-low-head-pico-hydro-turgo-turbine)).
- Generator efficiency 80 % at partial load and low speed; rectifier and MPPT converter 90 %.
- Generator constant about 10 rpm per volt of rectified DC (typical of low-speed direct-drive BLDC motors; to be confirmed for the chosen unit).
