---
doc_id: PCF-CAL-001
title: PicoFlow sizing calculations
project: PicoFlow
doc_type: Calculation note
version: "0.5"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First-principles sizing for TRL 3 against PCF-REQ-001 v0.3
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); 125 mm penstock, 33 mm inserts, results against PCF-REQ-001 v0.4
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: Rerun on the constructable design (PCF-DDR-003); valve reducer and expander, new manifold layout, flange bearing units, component masses; budget treated as a value-engineering target
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Full-bore 125 mm inlet valve (open decision N6, option a, decided by Amish 2026-10-01); design insert read from the model (34 mm); every number rerun; cost and pipework mass updated; clamp resistor equilibrium reported for the BOM resistor
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Clamp resistor changed from 8.2 Ω, 300 W to 6.8 Ω, 350 W (decided by Amish 2026-10-01); clamp voltage, dissipation and rating rechecked; cost rerun (BOM line 15 re-priced)
---

# PicoFlow sizing calculations

By calculation, the constructable design (PCF-DDR-003) with the full-bore inlet valve meets 12 of the 17 requirements in PCF-REQ-001 v0.7. None is not met, one is at risk (R12, printed runner life), three cannot be verified at TRL 3, and the cost requirement R15 is reported against its value-engineering target: USD 618, USD 168 over the USD 450 target. Version 0.4 replaces the 90 mm inlet valve, with its reducer and expander, by a full-bore 125 mm gate valve matched to the penstock (open decision N6, option a, decided by Amish on 2026-10-01). The valve now costs 0.007 m of head instead of 0.081 m. The design point gives 85.6 W into the battery at exactly 10 L/s, a margin of 5.6 W over R3 (it was 81.7 W and 1.7 W), and 87.8 W with the 34 mm design inserts, which pass 10.36 L/s. Water to wire is 43.6 % at 10 L/s. The two safety-critical items still pass on paper: a hardware clamp holds the DC bus below 48 V (R8), and a gate valve closing over 10 s or more keeps the drainage-grade penstock at about 34 kPa peak (R17). Version 0.5 changes the clamp resistor from 8.2 Ω to 6.8 Ω, 350 W (decided by Amish on 2026-10-01): in the worst case the clamp now settles the bus at 36.7 V, 3.3 V below its 40 V release point, where the 8.2 Ω resistor settled at 40.1 V (section 6).

Every number in this note is printed by `docs/04-calcs/sizing.py` (run `python docs/04-calcs/sizing.py` from the repo root), which also writes `docs/04-calcs/results.json` for the concept media and the drawing. The script reads geometry, the design insert, branch lengths and part volumes from `cad/src/model.py` and costs from `bom/bom.csv`.

> **Safety:** PicoFlow works beside moving water, has a spinning runner and coupling, a generator that can reach about 80 V DC open circuit if both the load and the clamp fail, resistors that run hot, and a lithium battery. The numbers here are paper estimates, not evidence that a built unit is safe.

## 1. Results against requirements

Table 1 lists every requirement, with the items at risk first. Status is one of met, not met, at risk, or not verifiable at TRL 3.

Table 1. Requirement status at TRL 3.

| ID | Target | Value from this note | Status |
| --- | --- | --- | --- |
| R12 | Bearing L10 20,000 h or more; runner 8,760 h or more | Bearing L10 about 7.1 x 10^6 h at the worst load; printed runner life unknown | At risk (runner) |
| R7 | 12 V charging, speed within 10 %, 100 % diversion within 1 s | 300 W dump load is 1.64 times the largest output (183.1 W); control behavior needs a bench test | Not verifiable at TRL 3 |
| R11 | Runner or inserts in 30 min, bearings in 60 min; bearings above the spray | Bearing units on the lid, 392 mm above tailwater, outside the housing; lid, shaft and runner lift out together; times need a trial | Not verifiable at TRL 3 |
| R16 | Half the dry-season flow at most; all water returned | Depends on the site survey | Not verifiable at TRL 3 |
| R1 | Generates from 1.0 to 3.0 m with the same runner | DC bus 20.1 V at 1.0 m, above the 15 V the buck converter needs | Met |
| R2 | 5 to 10 L/s at 1.0 m; 5 to 15 L/s from 2.0 m | 1.3 to 11.5 L/s at 1.0 m, 1.9 to 16.4 L/s at 2.0 m, 2.3 to 20.2 L/s at 3.0 m | Met |
| R3 | 80 W or more into the battery at 2.0 m, 10 L/s | 85.6 W with inserts sized for exactly 10 L/s; 87.8 W with the 34 mm inserts (10.36 L/s) | Met, 5.6 W margin at 10 L/s |
| R4 | 20 W or more at 1.0 m, 7 L/s | 26.8 W | Met |
| R5 | 40 % or more water to wire | 43.6 % at 10 L/s (43.2 % with the 34 mm inserts) | Met |
| R6 | 1.8 kWh/day or more at the design point | 2.05 kWh/day at 10 L/s (2.11 kWh/day with the 34 mm inserts) | Met |
| R8 | No exposed conductor above 60 V DC; survives runaway | Clamp (6.8 Ω) holds the bus at 36.7 V in the worst case, below 48 V and 3.3 V below the 40 V release; 79.5 V open circuit only if the clamp also fails, inside the enclosed 100 V DC side; rim stress 0.08 MPa | Met by calculation; generator overspeed rating to confirm |
| R9 | Prints in 220 x 220 x 250 mm, runner 24 h or less | Runner 200 x 200 x 50 mm, about 524 g, about 21 h; each nozzle fits 167 x 130 x 244 mm, about 308 g, about 12 h | Met (estimate) |
| R10 | Screen 6 mm or less, nozzles 20 mm or more | 6 mm screen; inserts 20 to 45 mm; design insert 34 mm | Met by design |
| R13 | Nozzle centerline 0.3 m or less above tailwater | 280 mm in the model | Met |
| R14 | Heaviest item 15 kg or less; turbine unit (items 1 to 6 and 11) 25 kg or less | Generator 7.0 kg; turbine unit 24.5 kg with its fixings; manifold, nozzles and valve 9.8 kg carried separately (the valve alone about 5.5 kg) | Met (definition confirmed, PCF-DDR-002) |
| R15 | Kit cost against the USD 450 value-engineering target | USD 618 with a new generator; USD 548 with a salvaged one | Over the value-engineering target by USD 168 (USD 98 with a salvaged motor) |
| R17 | Peak penstock pressure 50 kPa or less with the valve closed over 10 s or more | 33.5 kPa at 3.0 m | Met |

## 2. Assumptions

- Water at 15 °C: density 1,000 kg/m³, kinematic viscosity 1.14 x 10⁻⁶ m²/s; g = 9.81 m/s².
- Design point (PCF-REQ-001): 2.0 m gross head from the forebay surface to the nozzle centerline, 10 L/s, 20 m of 125 mm drainage PVC (SN8, 3.7 mm wall, 117.6 mm bore), roughness 0.0015 mm. The 110 mm pipe of v0.1 (SN4, 3.2 mm wall, 103.6 mm bore) is kept in Table 5 for comparison.
- Penstock fittings, as loss coefficients on the pipe velocity head: rounded entrance 0.20, intake screen 0.10, two bends 0.30 in total. Friction factor from the Swamee-Jain equation.
- Inlet valve (N6, option a, decided 2026-10-01): a full-bore 125 mm PVC-U gate valve with solvent-weld sockets, bore taken as the penstock bore, open loss coefficient 0.15 on the penstock velocity head. A 175 mm piece of the penstock pipe joins it to the tee. The 90 mm valve of v0.3, with a 125 x 90 mm reducer (0.10), the open 90 mm valve (0.15) and a sudden expansion (0.24) on its own velocity head, 1.88 in all on the penstock velocity head, is kept only as a comparison.
- Branches (PCF-DDR-003, P10): 90 mm PVC, 84.0 mm bore, from a 125 x 90 mm reducing tee with the penstock in its run. Jet 1 leaves the tee's side branch (1.0) and turns three elbows (0.3 each), 1.67 m of pipe; jet 2 runs straight through the tee (0.3) and a 125 x 90 reducer (0.1), 0.23 m. Lengths come from the model.
- Design insert: 34 mm, read from the model. With the full-bore valve, exactly 10 L/s needs 33.3 mm, so the 34 mm pair passes a little more than the design flow; R3 to R6 are judged at exactly 10 L/s.
- Nozzle velocity coefficient 0.97, so the nozzle loses 6 % of the head it receives.
- Runner: bucket speed 0.46 of jet speed at best efficiency, pitch diameter 150 mm, jet-to-shaft efficiency 75 % for a first printed runner (laboratory runners reach 87 to 91 %, per Williamson, Stark and Booker, 2013, cited in PCF-PRB-001), runaway at 2.0 times best speed (upper end of 1.8 to 2.0).
- Generator: 10 rpm per volt of rectified open-circuit DC; iron and friction loss 12 W at 340 rpm, proportional to speed; winding and cable resistance 0.8 Ω (DC equivalent); rectifier drop 1.6 V. These are typical of a low-speed permanent magnet machine and must be measured on the chosen unit.
- Buck converter 94 %; battery 13.6 V while charging; the converter needs a bus of about 15 V to reach 14.4 V absorption.
- Bearings: UC204 insert bearings in UCF204-class flange units, dynamic load rating 12.8 kN (catalog class).
- Printed parts: PETG at 1,270 kg/m³, printed mass 0.6 times the solid model volume, 25 g/h on a 0.4 mm nozzle.
- Surge: PVC modulus 3.0 GPa, water bulk modulus 2.2 GPa; the drainage pipe and joints are assumed good for 50 kPa (0.5 bar, the common joint tightness test level for non-pressure pipe). This rating must be confirmed with the pipe supplier.
- Costs are indicative prices from `bom/bom.csv`; the penstock (item 9) and battery (item 17) are excluded, as decided with the budget. `budget_usd` is a value-engineering target, not a limit (Amish, 2026-10-01).

## 3. Hydraulics and nozzle size

At the design point the nozzles need a 33.3 mm jet for exactly 10 L/s; the 34 mm design insert gives 10.36 L/s (Table 2). The penstock carries water at 0.95 m/s and loses 0.177 m, of which 0.007 m is at the full-bore valve (the 90 mm valve with its reducer and expander lost 0.081 m). The branches lose 0.100 m (jet 1, round the housing) and 0.021 m (jet 2, straight through the tee), so the two jets carry 5.12 and 5.24 L/s, within 2.3 % of each other. The mean net head at the nozzles is 1.66 m, a loss of 17.0 % of the gross head (20.3 % in v0.3). With the 63 mm branches of the TRL 2 concept the loss would be 25.0 %, so the 90 mm branches stay.

Table 2. Design point hydraulics (2.0 m, 125 mm penstock, full-bore valve, two 34 mm jets).

| Quantity | Value |
| --- | --- |
| Flow | 10.36 L/s |
| Penstock loss (with the valve) | 0.177 m |
| Full-bore valve | 0.007 m |
| Branch loss, jet 1 / jet 2 | 0.100 m / 0.021 m |
| Net head at the nozzles | 1.66 m |
| Pipe and branch loss | 17.0 % of gross head |
| Jet velocity | 5.53 m/s |
| Jet to pitch diameter ratio | 0.23 |

The jet to pitch diameter ratio of 0.23 is below the 0.28 of the PowerSpout DIY rotor cited in PCF-PRC-001, so 34 mm jets suit the 150 mm pitch circle. At exactly 10 L/s (33.3 mm inserts) the loss is 16.3 % and the output 85.6 W.

## 4. Power chain at the design point

Table 3. Power at each stage, 2.0 m with the 34 mm inserts (10.36 L/s).

| Stage | Power | Loss |
| --- | --- | --- |
| Gross hydraulic power | 203.2 W | |
| At the nozzles | 168.6 W | Pipe, valve and branches, 35 W |
| Jet | 158.7 W | Nozzle, 10 W |
| Runner shaft | 119.0 W at 324 rpm, 3.51 N·m | Runner, 40 W |
| Rectified DC | 93.4 W at 28.2 V, 3.32 A | Generator and rectifier, 26 W (efficiency 78.5 %) |
| Into the battery | 87.8 W, 6.46 A at 13.6 V | Buck converter, 6 W |

Water to wire is 43.2 % and the daily energy, running 24 h, is 2.11 kWh. At exactly 10 L/s the output is 85.6 W, 43.6 % and 2.05 kWh. The generator runs at 32.4 V open circuit at best speed, so the bus is well above the battery.

## 5. Head range

With the 34 mm inserts left in place, flow and output rise with head (Table 4). The bus stays above 15 V down to 1.0 m, so a 12 V battery charges across the whole range with a buck converter (R1). At 1.0 m and 7 L/s (R4) the right insert is 33.2 mm, and output is 26.8 W at 230 rpm with the bus at 20.3 V, above the 20 W target.

Table 4. Head range with the design-point inserts.

| Gross head | Flow | Loss | Best speed | Open-circuit DC | Bus under load | Into battery | Water to wire | Runaway | Runaway DC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 m | 7.30 L/s | 17.5 % | 229 rpm | 22.9 V | 20.1 V | 27.8 W | 38.8 % | 457 rpm | 45.7 V |
| 1.5 m | 8.96 L/s | 17.2 % | 280 rpm | 28.0 V | 24.5 V | 55.2 W | 41.9 % | 561 rpm | 56.1 V |
| 2.0 m | 10.36 L/s | 17.0 % | 324 rpm | 32.4 V | 28.2 V | 87.8 W | 43.2 % | 648 rpm | 64.8 V |
| 2.5 m | 11.59 L/s | 16.9 % | 363 rpm | 36.3 V | 31.3 V | 124.8 W | 43.9 % | 725 rpm | 72.5 V |
| 3.0 m | 12.71 L/s | 16.8 % | 398 rpm | 39.8 V | 34.0 V | 165.4 W | 44.2 % | 795 rpm | 79.5 V |

### Flow range (R2)

From one 20 mm jet to two 45 mm jets, the inserts pass 1.3 to 11.5 L/s at 1.0 m, 1.9 to 16.4 L/s at 2.0 m and 2.3 to 20.2 L/s at 3.0 m. Two jets carrying 15 L/s would need 55.2 mm bores at 1.0 m, 42.4 mm at 2.0 m and 37.4 mm at 3.0 m. A 55 mm jet on a 150 mm pitch circle is far outside Turgo practice, which is why R2 is stated as 5 to 10 L/s at 1.0 m and 5 to 15 L/s from 2.0 m (PCF-DDR-002). Both ranges are met.

### Sensitivity

Pipe loss dominates the result. Table 5 resizes the inserts for 10 L/s in each case; all rows include the full-bore valve.

Table 5. Sensitivity at 2.0 m and 10 L/s.

| Case | Loss | Into battery | Water to wire | Daily energy | At 1.0 m, 7 L/s |
| --- | --- | --- | --- | --- | --- |
| 110 mm penstock (103.6 mm bore), runner 75 % | 22.6 % | 78.7 W | 40.1 % | 1.89 kWh | 24.3 W |
| 125 mm penstock (117.6 mm bore), runner 75 % (design) | 16.3 % | 85.6 W | 43.6 % | 2.05 kWh | 26.8 W |
| 160 mm penstock (150.6 mm bore), runner 75 % | 11.0 % | 91.4 W | 46.6 % | 2.19 kWh | 28.8 W |
| 110 mm penstock, runner 80 % | 22.6 % | 84.0 W | 42.8 % | 2.01 kWh | 26.3 W |
| 125 mm penstock, runner 80 % | 16.3 % | 91.3 W | 46.5 % | 2.19 kWh | 28.9 W |

(The design row differs from Table 3 by 2.2 W because its inserts are sized for exactly 10 L/s rather than the 34 mm design inserts.)

R3 has a margin of 5.6 W (7.0 %) at exactly 10 L/s, up from 1.7 W with the 90 mm valve. Runner efficiency is still the number to measure first at TRL 4: a runner at about 70 % instead of the assumed 75 % would use up the margin.

## 6. Runaway and the voltage clamp (R8)

If the battery is lost and the dump-load switch fails, the runner speeds up toward runaway. With the design inserts at 3.0 m that is 795 rpm and 79.5 V DC open circuit. The largest shaft power in the operating envelope is 247.0 W, at 3.0 m and 15 L/s (37.4 mm inserts); there the bus under MPPT load is 32.4 V and runaway is 776 rpm and 77.6 V.

The clamp is a comparator on the DC bus, independent of the microcontroller, that switches the 6.8 Ω, 350 W resistor of the BOM across the bus at 48 V and releases it at 40 V. The turbine torque is taken to fall linearly from stall to zero at runaway. With the resistor connected in the worst case, the runner settles at 426 rpm with the bus at 36.7 V and 198 W in the resistor. That is 3.3 V below the 40 V release point, so the clamp cycles as intended: it switches in at 48 V, pulls the bus down, and releases once the bus falls below 40 V. With the 8.2 Ω resistor of v0.4 the worst case settled at 40.1 V, 0.1 V above the release point, because the full-bore valve delivers more power at the same site; Amish decided the change to 6.8 Ω on 2026-10-01 (PCF-DEC-001). At the 48 V switch-on point the 6.8 Ω resistor dissipates 339 W, inside its 350 W rating on a heat sink (3 % margin, and only for the moment before the bus falls); at equilibrium it carries 198 W. 6.8 Ω is also the largest E12 value that keeps the worst-case equilibrium below the release point. In normal running the bus never reaches the clamp: its highest open-circuit value at best speed is 39.8 V.

Only a double fault (load and clamp) lets the generator reach about 80 V, which is why the whole DC side stays enclosed and rated for 100 V. Mechanically, runaway is benign for the runner: the rim runs at 8.1 m/s and the hoop stress is about 0.08 MPa, a small fraction of PETG strength. The generator's overspeed rating at about 800 rpm must be confirmed with its supplier.

## 7. Bearings (R12)

The worst bearing load is at 3.0 m and 15 L/s with one jet closed, so the remaining jet's force is not balanced by the other. The radial load is 43.1 N (jet force at the pitch radius). The axial load, taken conservatively as the full jet momentum plus runner weight, is 104.5 N. With X = 0.56 and Y = 2.0, the equivalent load is 233.2 N and the basic L10 life of a UC204 insert (12.8 kN) at 388 rpm is about 7.1 x 10⁶ h, so bearing fatigue is not a concern. Life will be set by seal wear and water ingress, which a paper calculation cannot verify; the V-ring under the lid and the guard keep spray off the lower seal. The printed runner's life under continuous flow with sand is also unknown, so R12 remains at risk.

## 8. Geometry, printing and mass (R9, R13, R14)

- **Runner.** The model's envelope is 200 x 200 x 50 mm, which fits a 220 x 220 x 250 mm bed. Printed mass is about 524 g and print time about 21 h at 25 g/h, inside the 24 h target but only just. A 0.6 mm nozzle would shorten it.
- **Nozzles.** Each nozzle, with its saddle, fits a 167 x 130 x 244 mm space standing on its spigot: about 308 g and 12 h each.
- **Setting height.** The nozzle centerline is 280 mm above normal tailwater (R13). The runner underside is 199 mm above tailwater (210 mm in v0.2: the runner was lowered 11 mm with the nozzle tip, PCF-DDR-003 P6), which is how far the tailwater can rise before it touches the runner. At the design point the setting height is 12.3 % of the total site drop.
- **Mass.** Table 6 gives the mass of the turbine unit, component by component with its fixings, and of the pipework carried separately.

Table 6. Mass estimate.

| Item | Mass |
| --- | --- |
| Generator, 500 W low-speed BLDC (catalog class, assumed) | 7.00 kg |
| Frame, angle, foot plates and stops (steel, model volume) | 5.15 kg |
| Housing, 315 mm PVC | 3.04 kg |
| Tie rods, post rods, bearing bolts, nuts and washers (steel) | 1.94 kg |
| Lid, 12 mm HDPE | 1.77 kg |
| Generator plate, 8 mm aluminium | 1.62 kg |
| Bearing units, two UCF204 class (catalog) | 1.30 kg |
| Shaft, 316 stainless | 0.73 kg |
| Posts and spacer sleeves (steel tube) | 0.68 kg |
| Runner, PETG | 0.52 kg |
| Guard, 160 mm PVC | 0.40 kg |
| Coupling and clamping hub | 0.37 kg |
| **Turbine unit, items 1 to 6 and 11** | **24.5 kg** |
| Manifold (about 1.9 m of 90 mm PVC with tee, reducer, elbows and couplings) | 3.29 kg |
| Nozzles, printed, two | 0.62 kg |
| Gate valve, 125 mm PVC-U full bore (catalogue class, about 5.5 kg), with the 175 mm pipe piece | 5.88 kg |
| **All of the above** | **34.3 kg** |

R14 is met with the turbine unit taken as items 1 to 6 and 11 (Amish confirmed this definition on 2026-09-25, PCF-DDR-002), counted with its fixings, foot plates and tie rods. The margin is 0.5 kg. The full-bore valve does not change the turbine unit: it is part of the pipework, which now weighs 9.8 kg (6.3 kg in v0.3), and the valve alone, at about 5.5 kg, is well under the 15 kg limit for the heaviest item. The valve's mass is a catalogue-class figure to confirm on the unit bought.

## 9. Penstock surge (R17)

The pressure wave travels at 301 m/s in 125 mm SN8 PVC, so any closure faster than 0.13 s acts as instantaneous. An instantaneous stop at 3.0 m head (1.17 m/s in the pipe) would add 35.9 m of head, far beyond drainage pipe. Closing the gate valve over 10 s adds only 0.48 m, so the peak at the valve is 33.5 kPa (static 28.9 kPa), within the assumed 50 kPa. A multi-turn gate valve needs about ten turns to close, which enforces the 10 s; the full-bore valve must be multi-turn as well, never quarter-turn. A single nozzle blocking at once would add about 17.9 m. The 6 mm screen keeps out anything that could plug a 20 mm or larger insert in one piece, but a mat of leaves could not be ruled out, so the forebay screen must be kept clear.

## 10. Dump load (R7)

The largest output on the 12 V side is 183.1 W (3.0 m, 15 L/s), so the 300 W dump load has a margin of 1.64 times. The control behavior in R7 (speed within 10 %, full diversion within 1 s) depends on the controller and needs a bench test at TRL 4.

## 11. Cost (R15)

From `bom/bom.csv`, the kit (every item except the penstock and battery) costs USD 618.00 with a new generator. Value-engineering target: USD 450. Estimated cost of the constructable design: USD 618 (USD 168 over the target). With a salvaged washing machine motor at about USD 40 it costs USD 548.00 (USD 98 over). In v0.5 the 6.8 Ω, 350 W clamp resistor adds USD 4 to line 15 (an indicative price, to be quoted). The increase from USD 534.00 in v0.3 to USD 614.00 in v0.4 was the full-bore valve: line 8 rises from USD 40 to USD 120, an estimate, since no published price was found for a 125 mm PVC-U gate valve (see `bom/bom-notes.md`). It buys back 3.9 W at the design point, about USD 21 per watt. The penstock (USD 140.00 for 20 m) and the battery (USD 160.00) are excluded. Cost drivers and savings worth trying are listed in the design decisions register (PCF-DEC-001, Value engineering).

## 12. Numbers corrected from TRL 2 and earlier versions

| Quantity | TRL 2 estimate | v0.1 (110 mm penstock) | v0.2 (125 mm penstock) | v0.3 (constructable design) | v0.4 (full-bore valve) |
| --- | --- | --- | --- | --- | --- |
| Pipe loss | 10 % | 23.6 % | 17.0 % | 20.3 % (valve fittings added) | 17.0 % |
| Jet diameter | about 33 mm | 34 mm | 33 mm | 34 mm | 34 mm (33.3 mm for exactly 10 L/s) |
| Best speed | about 340 rpm | 311 rpm | 324 rpm | 318 rpm | 324 rpm |
| Into the battery at 2.0 m | about 90 W | 77.2 W | 82.8 W | 82.5 W (81.7 W at exactly 10 L/s) | 87.8 W (85.6 W at exactly 10 L/s) |
| Water to wire | about 46 % | 39.5 % | 43.2 % | 41.4 % | 43.2 % (43.6 % at 10 L/s) |
| Daily energy | about 2.2 kWh | 1.85 kWh | 1.99 kWh | 1.98 kWh | 2.11 kWh (2.05 kWh at 10 L/s) |
| Output at 1.0 m / 3.0 m | about 30 W / 165 W | 23.9 W / 146.4 W | 26.0 W / 156.4 W | 25.9 W / 155.7 W | 27.8 W / 165.4 W |
| Runaway open circuit at 3.0 m | 75 to 83 V | 76.4 V | 79.5 V (bus clamped at 48 V) | 78.0 V (bus clamped at 48 V) | 79.5 V (bus clamped at 48 V) |
| Nozzle height above tailwater | 0.44 m | 0.28 m | 0.28 m | 0.28 m | 0.28 m |
| Turbine unit mass | about 20 kg | 22.2 kg | 22.2 kg | 24.5 kg (with fixings) | 24.5 kg; pipework 9.8 kg |
| Kit cost, new generator | about $424 | $448.00 | $448.00 | USD 534 (value-engineering target USD 450) | USD 614 (value-engineering target USD 450) |

Version 0.5 (6.8 Ω clamp resistor) changes only the clamp figures of section 6 (worst-case equilibrium 36.7 V at 426 rpm, was 40.1 V at 456 rpm) and the kit cost (USD 618 with a new generator, USD 548 with a salvaged motor); every other number above is unchanged from v0.4.
