---
doc_id: PCF-PRC-001
title: PicoFlow design precis
project: PicoFlow
doc_type: Design precis
version: "0.7"
status: Draft
date: '2026-10-01'
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; Amish's 2026-09-25 decisions (PCF-DDR-001), numbers from PCF-CAL-001, 90 mm branches, opposed jets, lowered frame, gate valve, voltage clamp
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Constructable design (PCF-DDR-003) and numbers from PCF-CAL-001 v0.3; budget treated as a value-engineering target
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Full-bore 125 mm inlet valve (N6, option a, decided by Amish 2026-10-01); numbers from PCF-CAL-001 v0.4
- version: "0.7"
  date: '2026-10-01'
  author: Amish Chadha
  change: Clamp resistor 6.8 Ω, 350 W (decided by Amish 2026-10-01; was 8.2 Ω, 300 W); clamp and cost figures from PCF-CAL-001 v0.5
---

# PicoFlow design precis

PicoFlow is a vertical-shaft pico hydro turbine for 1 to 3 m of head: water from a small forebay runs down a PVC penstock to two opposed printed nozzles, which drive a 200 mm 3D-printed Turgo runner inside an open-bottomed PVC housing. The runner turns a low-speed BLDC motor, used as a generator, that sits on the lid above the spray. An MPPT controller charges a 12 V battery and diverts surplus power to a dump load, and a hardware clamp keeps the DC side below 48 V if everything else fails. The TRL 3 calculation on the constructable design (PCF-CAL-001 v0.3, PCF-DDR-003) gives about 82 W into the battery at 2 m and 10 L/s (1.98 kWh a day), about 26 W at 1 m and about 156 W at 3 m, with a 125 mm penstock (decided by Amish on 2026-09-25, PCF-DDR-002); pipe, valve and branch losses take about 20 % of the head. Value-engineering target: USD 450. Estimated cost of the constructable design: USD 534 for the turbine kit with a new generator (USD 84 over the target), or USD 464 with a salvaged washing machine motor; the penstock and battery are excluded. How to build the prototype is in the build plan, PCF-BLD-001.

![Hero render](../media/hero.png)

*Figure 1. PicoFlow at a weir or rock step set for 2.0 m of gross head, with a 1.75 m person for scale. The penstock is drawn short; real sites typically need 10 to 30 m of pipe. Kit parts are colored; the site is grey.*

## How it works

1. **Intake.** A small forebay (a plastic tub or masonry box) at the top of the drop settles sand and passes water through a 6 mm screen. Surplus water spills over the forebay and carries leaves away, so the screen cleans itself.
2. **Penstock.** A 125 mm PVC pipe (decided 2026-09-25, PCF-DDR-002; 110 mm lost about 24 % of the head) carries about 10 L/s down 1 to 3 m of head. Drainage-grade pipe is allowed (decided 2026-09-25) because the static pressure is at most about 29 kPa (4.2 psi) and a multi-turn gate valve at the bottom cannot close in under about 10 s, which keeps the surge to about 34 kPa peak (PCF-CAL-001 section 9).
3. **Nozzles.** A 125 x 90 mm reducing tee splits the flow into two 90 mm branches. One runs straight on through a reducer to its nozzle; the other runs around the housing, so the two jets strike the runner on opposite sides and their radial forces cancel. Each printed nozzle is bolted to the housing wall through a gasketed saddle and joined to its pipe by a flexible coupling; a swappable insert (20 to 45 mm bore) sets the jet, 34 mm at the design point. The jets strike the runner from above at 20 degrees to the runner plane.
4. **Runner.** A printed Turgo runner, 200 mm outside diameter and 150 mm pitch diameter, with 20 buckets, turns at about 318 rpm at the design point. The water leaves the far side of the buckets and falls out of the open bottom of the housing into the tailrace, so nothing floods the runner.
5. **Shaft and bearings.** A 20 mm stainless shaft runs up through the lid into two sealed flange bearing units (UCF204 class) stacked on the lid, above the spray, and drives the generator through a jaw coupling inside a guard.
6. **Generator.** A new low-speed BLDC motor (about 500 W rated, about 10 rpm per volt; decided 2026-09-25) produces three-phase AC, about 28 V DC after the rectifier at the design point. Its mounting plate also accepts a salvaged direct-drive washing machine motor.
7. **Power electronics.** A three-phase bridge rectifies the output. The open-design controller (the TRL 3 design, decided 2026-09-25) runs a buck converter that holds the runner at its best speed (maximum power point tracking, MPPT) and charges the 12 V battery. When the battery is full or disconnected it switches the output into a 300 W dump load. Separately, a comparator on the DC bus switches a 6.8 Ω, 350 W clamp resistor across the bus at 48 V and releases it at 40 V, whatever the microcontroller is doing.

![Power flow](../media/flow.png)

*Figure 2. Power flow at the design point (2.0 m gross head, 10 L/s), from PCF-CAL-001. All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3), the general arrangement drawing PCF-DWG-001 and `bom/bom.csv`.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Turgo runner | 200 mm OD, 150 mm pitch diameter, 20 buckets; PETG for the prototype, glass-filled nylon for field units (decided 2026-09-25) | About 525 g, about 21 h to print (R9) |
| 2 | Shaft and hub | 20 mm 316 stainless shaft, 294 mm, clamping hub screwed to the runner | |
| 3 | Bearings, motor mount, guard | Two UCF204-class flange bearing units on the lid; four posts carry an 8 mm generator plate; 160 mm pipe guard over the bearings and coupling | Bearings above the spray (R11); L10 about 8.0 x 10^6 h |
| 4 | Coupling | Jaw coupling with elastomer spider | Inside the guard |
| 5 | Generator | New low-speed BLDC, about 500 W rated, about 10 rpm/V (decided); salvaged washing machine motor as the low-cost variant | About 7 kg |
| 6 | Housing and lid | 315 mm PVC sewer pipe, 303 mm long, open bottom at 80 mm above tailwater; 400 x 400 mm HDPE lid with a groove that locates the housing; four tie rods clamp lid, housing and frame | |
| 7 | Nozzle manifold and nozzles | 125 x 90 mm reducing tee and reducer, 90 mm branches, three elbows, flexible couplings, two printed nozzles with saddles and swappable inserts, opposed jets | Inserts 20 to 45 mm (R2, R10); 34 mm at the design point |
| 8 | Inlet valve | Full-bore 125 mm PVC-U multi-turn gate valve with solvent-weld sockets, joined to the tee by a short piece of penstock pipe | Slow closing (R17); full bore decided by Amish, 2026-10-01 (PCF-DEC-001) |
| 9 | Penstock | 125 mm PVC (SN8), about 20 m, drainage grade allowed, support every 2 to 3 m | Site-dependent; excluded from kit cost; 125 mm decided 2026-09-25 |
| 10 | Forebay and intake screen | Plastic tub or masonry box, 6 mm stainless mesh, overflow lip | Keep the screen clear (surge risk if a nozzle plugs) |
| 11 | Turbine frame | 40 mm galvanized steel angle, 380 mm welded square, short legs and foot plates, anchored to a pad over the tailrace | Nozzles 280 mm above tailwater (R13) |
| 12 | Equipment post | Treated timber post on a base plate | Keeps electronics out of spray and flood |
| 13 | Rectifier | Three-phase bridge, 35 A, 1,000 V, on a heat sink | |
| 14 | MPPT, dump-load and clamp controller | Microcontroller, synchronous buck converter, MOSFET dump-load switch, independent comparator clamp, IP65 box rated for 100 V DC | Open design (decided); off-the-shelf unit for first bench tests only |
| 15 | Dump-load and clamp resistors | 300 W, 12 V heating element or wire-wound resistor; 6.8 Ω, 350 W (or higher rated) aluminium-clad clamp resistor; vented guard | Both run hot |
| 16 | Wiring, fuse and isolator | 4 mm² cable, 20 A fuse at the battery, DC isolator rated 100 V, cable glands | |
| 17 | Battery | 12 V (decided), about 50 Ah LiFePO4 with BMS, or an existing lead-acid battery | Household item; excluded from kit cost |
| 18 | Pipe stands | Three steel angle stands with 90 mm pipe clips | Carry the branch pipework |
| 19 | Fixings | Tie rods, post rods, bolts, nuts, washers, heat-set inserts, anchors | |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM. The penstock is shown as a short stub and the site weir is omitted.*

![Cutaway](../media/cutaway.png)

*Figure 4. Cutaway of the turbine unit: opposed nozzles, runner inside the open-bottomed housing, shaft, bearing housing, guarded coupling and generator above the lid.*

## Key numbers

The numbers below are calculated in PCF-CAL-001 (script `docs/04-calcs/sizing.py`), which lists every assumption. They replace the TRL 2 first-order estimates. The general arrangement is drawing PCF-DWG-001 (`cad/drawings/PCF-DWG-001.pdf`), generated from `cad/src/model.py`.

### Design point: 2.0 m gross head, 10 L/s

| Quantity | Value | Basis |
| --- | --- | --- |
| Gross hydraulic power | 203.2 W | ρ g Q H, 10.36 L/s with 34 mm inserts |
| Pipe, valve and branch loss | 17.0 % of head | 20 m of 125 mm PVC, fittings, full-bore 125 mm valve, 90 mm branches |
| Net head at the nozzles | 1.66 m | |
| Jet velocity, jet size | 5.53 m/s, two 34 mm jets | Velocity coefficient 0.97 |
| Best runner speed, torque | 324 rpm, 3.51 N·m | Bucket speed 0.46 of jet speed; runner 75 % |
| Rectified DC | 93.4 W at 28.2 V | Generator and rectifier 78.5 % |
| **Into the battery** | **87.8 W, 6.46 A at 13.6 V** | Buck converter 94 % |
| Water-to-wire efficiency | 43.2 % | R5 (40 %) met |
| Daily energy | 2.11 kWh | R6 (1.8 kWh) met |

At exactly 10 L/s the output is 85.6 W, 5.6 W over R3, with 43.6 % water to wire and 2.05 kWh a day. The full-bore inlet valve, chosen by Amish on 2026-10-01 (PCF-DEC-001), loses 0.007 m of head; the 90 mm valve with its reducer and expander lost 0.081 m and left 81.7 W, 1.7 W over R3.

### Across the head range

With the design-point inserts, flow rises with head. The bus stays above the 15 V the buck converter needs, so the 12 V battery charges across the whole range.

| Gross head | Flow | Best speed | Bus under load | Into battery | Requirement |
| --- | --- | --- | --- | --- | --- |
| 1.0 m | 7.3 L/s | 229 rpm | 20.1 V | 27.8 W | R4 (20 W) met |
| 2.0 m | 10.4 L/s | 324 rpm | 28.2 V | 87.8 W | R3 (80 W) met |
| 3.0 m | 12.7 L/s | 398 rpm | 34.0 V | 165.4 W | |

At 1.0 m the inserts pass at most about 11.5 L/s, which meets R2 as restated on 2026-09-25 (5 to 10 L/s at 1.0 m, 5 to 15 L/s from 2.0 m).

### Runaway and the voltage clamp

With no load, the runner would reach about 795 rpm at 3.0 m, and the generator about 80 V DC open circuit, above the 60 V extra-low voltage limit. The hardware clamp prevents this: in the worst case (3.0 m, 15 L/s) the 6.8 Ω clamp resistor holds the runner at about 426 rpm and the bus at about 36.7 V, so the bus stays at or below 48 V. That equilibrium is 3.3 V below the clamp's 40 V release point, so the clamp cycles as intended; with the earlier 8.2 Ω resistor it settled at 40.1 V and stayed switched in, which is why Amish chose 6.8 Ω on 2026-10-01 (PCF-CAL-001 section 6). Only a double fault (load and clamp) lets the voltage rise to about 80 V, and the DC side is enclosed and rated for 100 V for that case. The runner rim reaches only about 8.1 m/s at runaway, so the printed runner does not burst; the generator's overspeed rating is still to be confirmed.

### Setting height, loads, mass and life

- **Setting height.** The housing stands on the frame 80 mm above the pad, so the nozzle centerline is 280 mm above normal tailwater (R13 met) and the runner underside is 199 mm above it. The setting height costs 12.3 % of the site drop at the design point, down from about 18 % at TRL 2.
- **Bearing loads** are small: with one jet closed at 3.0 m and 15 L/s, 43 N radial and 105 N axial, giving an L10 life of about 7.1 x 10^6 h. Seal wear and water ingress, not fatigue, will set bearing life. The printed runner's life under sandy water is unknown (R12 at risk).
- **Mass:** turbine unit (items 1 to 6 and 11, with their fixings) 24.5 kg, with the 7 kg generator the heaviest item; the manifold, nozzles and full-bore valve add 9.8 kg and are carried separately (the valve alone about 5.5 kg) (R14; definition confirmed by Amish, 2026-09-25).
- **Surge:** closing the gate valve over 10 s at 3.0 m adds 0.48 m of head; an instant stop would add about 36 m, which is why a quarter-turn ball valve is not allowed.

### Cost

Value-engineering target: USD 450 (a hypothetical control target, not a limit; Amish, 2026-10-01). Estimated cost of the constructable design: USD 618 (USD 168 over the target); the 6.8 Ω, 350 W clamp resistor added USD 4 and the full-bore valve added USD 80 of that, an estimate to be quoted. Cost drivers and savings worth trying are in the design decisions register (PCF-DEC-001).

| Group | Cost | Against the target |
| --- | --- | --- |
| Turbine kit with a new generator (items 1 to 8, 10 to 16, 18, 19) | USD 618.00 | USD 168 over |
| Turbine kit with a salvaged washing machine motor | USD 548.00 | USD 98 over; documented low-cost variant |
| Penstock, 20 m of 125 mm (item 9, excluded) | USD 140.00 | Site-dependent |
| Battery, 12 V 50 Ah LiFePO4 (item 17, excluded) | USD 160.00 | Often already owned |

For comparison, cheap low-head propeller units sold in Vietnam cost $20 to $90, but most last only 2 to 3 years ([DFID R8150](https://assets.publishing.service.gov.uk/media/57a08cf340f0b652dd001676/R8150-Vietnam.pdf)). PicoFlow's case rests on durability, repair and output per dollar over several years, not on first cost.

## Key design choices

Amish decided the TRL 2 review items on 2026-09-25 by accepting every recommendation (PCF-DDR-001), and later that day accepted the TRL 3 recommendations too (PCF-DDR-002).

- **Turgo rather than propeller at 1 to 3 m.** Decided 2026-09-25. A Turgo runs in air, tolerates debris, keeps its efficiency at part flow, and has reached 87 % at 1 m in the lab. Its limit is flow: it suits streams of about 5 to 15 L/s (about 10 L/s at 1 m) rather than the larger flows a propeller such as the PowerSpout LH uses (14 to 55 L/s ([PowerSpout](https://www.powerspout.com/pages/low-head-lh-info))). Confirming that the first target sites are in this range is part of open item O1.
- **Vertical shaft with the generator on the lid.** Decided 2026-09-25.
- **Two jets, opposed.** Decided 2026-09-25 (two jets). Two 34 mm jets keep the jet-to-pitch ratio at 0.23; placing them on opposite sides, a TRL 3 layout choice, cancels their radial forces, and one can be closed in the dry season.
- **Generator.** Decided 2026-09-25: a new low-speed BLDC for the prototype, with a mount that also takes a salvaged direct-drive washing machine motor.
- **Runner material.** Decided 2026-09-25: PETG for the first prototype, glass-filled nylon for field units.
- **Battery voltage.** Decided 2026-09-25: 12 V.
- **Controller.** Decided 2026-09-25: the open-design MPPT, dump-load and clamp board is the TRL 3 design; an off-the-shelf diversion controller is only for the first bench tests (TRL 4, on hold).
- **Drainage pipe for the penstock.** Decided 2026-09-25: allowed with a slow-closing valve and a surge check. The check is in PCF-CAL-001 and the multi-turn gate valve meets R17.
- **Budget.** Decided 2026-09-25: USD 450, with the salvaged-motor variant documented; since 2026-10-01 treated as a value-engineering target, not a limit.
- **90 mm branches.** A TRL 3 sizing result: with the 125 mm penstock, 63 mm branches would lose 27 % of the head instead of 17 %.
- **125 mm penstock.** Decided 2026-09-25 (PCF-DDR-002, N1): cuts pipe and branch loss from 24 % to 17 % of head. The penstock is outside the kit budget; 20 m costs about $140 instead of $100.

Decided by Amish, 2026-09-25 (PCF-DDR-002): the 125 mm design-point penstock (N1), R4 relaxed to 20 W (N2), R2 stated as 5 to 10 L/s at 1.0 m and 5 to 15 L/s from 2.0 m (N3), the R14 definition confirmed (N4) and the $2 cost margin accepted (N5). Still open: the first site type, region and partner (O1), the inlet valve bore against the 125 mm penstock (N6) and the design-for-construction changes of PCF-DDR-003; all are listed in the design decisions register (PCF-DEC-001).

## Safety

> **Safety:** PicoFlow combines moving water at a weir, a spinning runner, a generator that can exceed 60 V DC if both the load and the clamp fail, resistors that run hot, and a lithium battery. Treat each as a hazard at every stage, including site survey.

- **Water and the site.** Weirs, rock steps and streams in flood can drown people, especially children. Install and service only at low flow, never stand on a weir crest, keep the intake and tailrace fenced or covered where children play, and site the turbine above normal flood level. Close the intake before entering the stream. The runner is only 199 mm above normal tailwater, so check flood levels before siting.
- **Rotating parts.** The runner is enclosed in the housing, and the bearings and coupling are inside a guard under the generator plate. Always close the valve and wait for the runner to stop before opening the housing or removing the guard; a runner turning at 300 to 400 rpm can still cut fingers.
- **Runaway voltage.** The hardware clamp keeps the DC bus at 48 V or less, but a double fault can reach about 80 V DC at 3 m head. The DC side must stay enclosed and rated for at least 100 V.
- **Dump load and clamp heat.** The 300 W dump load and the 350 W clamp resistor can exceed 200 °C in still air. Mount them in a vented metal guard, away from timber, dry grass and roofs, or immerse the dump load in a water tank with a thermal cut-out.
- **Lithium battery.** A LiFePO4 battery is less prone to thermal runaway than other lithium chemistries but can still deliver hundreds of amperes into a short circuit. Use a battery with a BMS, a 20 A fuse within 300 mm of the battery terminal, charge-temperature limits from the BMS, and a dry, ventilated, non-combustible location. Lead-acid batteries vent hydrogen while charging and need ventilation.
- **Water hammer.** Use only the multi-turn gate valve and close it over at least 10 s. Never fit a quarter-turn ball valve: an instant stop on a 20 m penstock could add about 35 m of head and burst drainage pipe. Keep the screen clear, because a nozzle plugged all at once could add about 18 m.
- **Environment and permits.** Leave enough water in the stream for fish and downstream users (R16), screen the intake, and check local water-use rules before building.

## Open questions (TRL 4 is on hold)

- Measure the chosen generator's constant (rpm per volt), resistance, losses at 200 to 400 rpm and overspeed rating.
- Confirm the runner efficiency of a printable bucket shape against the Bristol low-head results.
- Confirm the drainage pipe joint rating with the supplier.
- Check PETG and nylon creep, water uptake and sand erosion under continuous duty (R12).
- Choose the first site type, region and partner (O1).

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
