---
doc_id: PCF-CAL-001
title: PicoFlow sizing calculations
project: PicoFlow
doc_type: Calculation note
version: "0.3"
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
---

# PicoFlow sizing calculations

By calculation, the constructable design (PCF-DDR-003) meets 12 of the 17 requirements in PCF-REQ-001 v0.5. None is not met, one is at risk (R12, printed runner life), three cannot be verified at TRL 3, and the cost requirement R15 is reported against its value-engineering target: USD 534, USD 84 over the USD 450 target. Version 0.3 reruns every number on the buildable model. Two changes affect the hydraulics. The 90 mm inlet valve of the bill of materials needs a reducer and an expander to join the 125 mm penstock, which costs 0.084 m of head at the design point; and the re-routed manifold sends jet 2 straight through the tee, which cuts its branch loss. Net of both, the design point gives 82.5 W into the battery with the 34 mm design inserts (81.7 W at exactly 10 L/s) and 41.4 % water to wire, so R3 and R5 are still met, but the margin on R3 is now 1.7 W. A full-bore valve would give 85.6 W (open decision N6). The two safety-critical items still pass on paper: a hardware clamp holds the DC bus below 48 V (R8), and a gate valve closing over 10 s or more keeps the drainage-grade penstock at about 33 kPa peak (R17).

Every number in this note is printed by `docs/04-calcs/sizing.py` (run `python docs/04-calcs/sizing.py` from the repo root), which also writes `docs/04-calcs/results.json` for the concept media and the drawing. The script reads geometry, branch lengths and part volumes from `cad/src/model.py` and costs from `bom/bom.csv`.

> **Safety:** PicoFlow works beside moving water, has a spinning runner and coupling, a generator that can reach about 80 V DC open circuit if both the load and the clamp fail, resistors that run hot, and a lithium battery. The numbers here are paper estimates, not evidence that a built unit is safe.

## 1. Results against requirements

Table 1 lists every requirement, with the items at risk first. Status is one of met, not met, at risk, or not verifiable at TRL 3.

Table 1. Requirement status at TRL 3.

| ID | Target | Value from this note | Status |
| --- | --- | --- | --- |
| R12 | Bearing L10 20,000 h or more; runner 8,760 h or more | Bearing L10 about 8.0 x 10^6 h at the worst load; printed runner life unknown | At risk (runner) |
| R7 | 12 V charging, speed within 10 %, 100 % diversion within 1 s | 300 W dump load is 1.76 times the largest output (170.4 W); control behavior needs a bench test | Not verifiable at TRL 3 |
| R11 | Runner or inserts in 30 min, bearings in 60 min; bearings above the spray | Bearing units on the lid, 392 mm above tailwater, outside the housing; lid, shaft and runner lift out together; times need a trial | Not verifiable at TRL 3 |
| R16 | Half the dry-season flow at most; all water returned | Depends on the site survey | Not verifiable at TRL 3 |
| R1 | Generates from 1.0 to 3.0 m with the same runner | DC bus 19.7 V at 1.0 m, above the 15 V the buck converter needs | Met |
| R2 | 5 to 10 L/s at 1.0 m; 5 to 15 L/s from 2.0 m | 1.3 to 11.0 L/s at 1.0 m, 1.9 to 15.6 L/s at 2.0 m, 2.3 to 19.2 L/s at 3.0 m | Met |
| R3 | 80 W or more into the battery at 2.0 m, 10 L/s | 82.5 W with the 34 mm inserts (10.16 L/s); 81.7 W with inserts sized for exactly 10 L/s | Met, 1.7 W margin at 10 L/s |
| R4 | 20 W or more at 1.0 m, 7 L/s | 25.5 W | Met |
| R5 | 40 % or more water to wire | 41.4 % | Met |
| R6 | 1.8 kWh/day or more at the design point | 1.98 kWh/day | Met |
| R8 | No exposed conductor above 60 V DC; survives runaway | Clamp holds the bus at 38.7 V (below 48 V) in the worst case; 78.0 V open circuit only if the clamp also fails, inside the enclosed 100 V DC side; rim stress 0.08 MPa | Met by calculation; generator overspeed rating to confirm |
| R9 | Prints in 220 x 220 x 250 mm, runner 24 h or less | Runner 200 x 200 x 50 mm, about 524 g, about 21 h; each nozzle fits 167 x 130 x 244 mm, about 308 g, about 12 h | Met (estimate) |
| R10 | Screen 6 mm or less, nozzles 20 mm or more | 6 mm screen; inserts 20 to 45 mm; design insert 34 mm | Met by design |
| R13 | Nozzle centerline 0.3 m or less above tailwater | 280 mm in the model | Met |
| R14 | Heaviest item 15 kg or less; turbine unit (items 1 to 6 and 11) 25 kg or less | Generator 7.0 kg; turbine unit 24.5 kg with its fixings; manifold, nozzles and valve 6.3 kg carried separately | Met (definition confirmed, PCF-DDR-002) |
| R15 | Kit cost against the USD 450 value-engineering target | USD 534 with a new generator; USD 464 with a salvaged one | Over the value-engineering target by USD 84 (USD 14 with a salvaged motor) |
| R17 | Peak penstock pressure 50 kPa or less with the valve closed over 10 s or more | 33.4 kPa at 3.0 m | Met |

## 2. Assumptions

- Water at 15 °C: density 1,000 kg/m³, kinematic viscosity 1.14 x 10⁻⁶ m²/s; g = 9.81 m/s².
- Design point (PCF-REQ-001): 2.0 m gross head from the forebay surface to the nozzle centerline, 10 L/s, 20 m of 125 mm drainage PVC (SN8, 3.7 mm wall, 117.6 mm bore), roughness 0.0015 mm. The 110 mm pipe of v0.1 (SN4, 3.2 mm wall, 103.6 mm bore) is kept in Table 5 for comparison.
- Penstock fittings, as loss coefficients on the pipe velocity head: rounded entrance 0.20, intake screen 0.10, two bends 0.30 in total. Friction factor from the Swamee-Jain equation.
- Inlet valve (PCF-DDR-003, P11): a 90 mm gate valve, bore taken as 84 mm, between a 125 x 90 mm reducer and a 90 x 125 mm expander. On the valve's own velocity head: reducer 0.10, open gate valve 0.15, sudden expansion 0.24; 1.88 in all on the penstock velocity head. A full-bore valve on the penstock (0.15) is kept as the comparison for open decision N6.
- Branches (PCF-DDR-003, P10): 90 mm PVC, 84.0 mm bore, from a 125 x 90 mm reducing tee with the penstock in its run. Jet 1 leaves the tee's side branch (1.0) and turns three elbows (0.3 each), 1.67 m of pipe; jet 2 runs straight through the tee (0.3) and a 125 x 90 reducer (0.1), 0.23 m. Lengths come from the model.
- Nozzle velocity coefficient 0.97, so the nozzle loses 6 % of the head it receives.
- Runner: bucket speed 0.46 of jet speed at best efficiency, pitch diameter 150 mm, jet-to-shaft efficiency 75 % for a first printed runner (laboratory runners reach 87 to 91 %, per Williamson, Stark and Booker, 2013, cited in PCF-PRB-001), runaway at 2.0 times best speed (upper end of 1.8 to 2.0).
- Generator: 10 rpm per volt of rectified open-circuit DC; iron and friction loss 12 W at 340 rpm, proportional to speed; winding and cable resistance 0.8 Ω (DC equivalent); rectifier drop 1.6 V. These are typical of a low-speed permanent magnet machine and must be measured on the chosen unit.
- Buck converter 94 %; battery 13.6 V while charging; the converter needs a bus of about 15 V to reach 14.4 V absorption.
- Bearings: UC204 insert bearings in UCF204-class flange units, dynamic load rating 12.8 kN (catalog class).
- Printed parts: PETG at 1,270 kg/m³, printed mass 0.6 times the solid model volume, 25 g/h on a 0.4 mm nozzle.
- Surge: PVC modulus 3.0 GPa, water bulk modulus 2.2 GPa; the drainage pipe and joints are assumed good for 50 kPa (0.5 bar, the common joint tightness test level for non-pressure pipe). This rating must be confirmed with the pipe supplier.
- Costs are indicative prices from `bom/bom.csv`; the penstock (item 9) and battery (item 17) are excluded, as decided with the budget. `budget_usd` is a value-engineering target, not a limit (Amish, 2026-10-01).

## 3. Hydraulics and nozzle size

At the design point the nozzles need a 33.7 mm jet for exactly 10 L/s; the 34 mm insert gives 10.16 L/s (Table 2). The penstock carries water at 0.94 m/s and loses 0.248 m, of which 0.084 m is at the valve and its reducer and expander. The branches lose 0.096 m (jet 1, round the housing) and 0.020 m (jet 2, straight through the tee), so the two jets carry 5.02 and 5.13 L/s, within 2.2 % of each other. The mean net head at the nozzles is 1.59 m, a loss of 20.3 % of the gross head (17.0 % in v0.2, which took the valve as full bore). With the 63 mm branches of the TRL 2 concept the loss would be 27.6 %, so the 90 mm branches stay.

Table 2. Design point hydraulics (2.0 m, 125 mm penstock, 90 mm valve, two 34 mm jets).

| Quantity | Value |
| --- | --- |
| Flow | 10.16 L/s |
| Penstock loss (with valve fittings) | 0.248 m |
| Valve, reducer and expander | 0.084 m |
| Branch loss, jet 1 / jet 2 | 0.096 m / 0.020 m |
| Net head at the nozzles | 1.59 m |
| Pipe and branch loss | 20.3 % of gross head |
| Jet velocity | 5.43 m/s |
| Jet to pitch diameter ratio | 0.23 |

The jet to pitch diameter ratio of 0.23 is below the 0.28 of the PowerSpout DIY rotor cited in PCF-PRC-001, so 34 mm jets suit the 150 mm pitch circle. With a full-bore valve (N6, option a) the loss at exactly 10 L/s would be 16.3 %, the insert 33.3 mm and the output 85.6 W.

## 4. Power chain at the design point

Table 3. Power at each stage, 2.0 m with the 34 mm inserts (10.16 L/s).

| Stage | Power | Loss |
| --- | --- | --- |
| Gross hydraulic power | 199.3 W | |
| At the nozzles | 158.9 W | Pipe, valve and branches, 40 W |
| Jet | 149.5 W | Nozzle, 9 W |
| Runner shaft | 112.1 W at 318 rpm, 3.37 N·m | Runner, 37 W |
| Rectified DC | 87.8 W at 27.6 V, 3.18 A | Generator and rectifier, 24 W (efficiency 78.3 %) |
| Into the battery | 82.5 W, 6.07 A at 13.6 V | Buck converter, 5 W |

Water to wire is 41.4 % and the daily energy, running 24 h, is 1.98 kWh. The generator runs at 31.8 V open circuit at best speed, so the bus is well above the battery.

## 5. Head range

With the 34 mm inserts left in place, flow and output rise with head (Table 4). The bus stays above 15 V down to 1.0 m, so a 12 V battery charges across the whole range with a buck converter (R1). At 1.0 m and 7 L/s (R4) the right insert is 33.5 mm, and output is 25.5 W at 225 rpm with the bus at 19.8 V, above the 20 W target.

Table 4. Head range with the design-point inserts.

| Gross head | Flow | Loss | Best speed | Open-circuit DC | Bus under load | Into battery | Water to wire | Runaway | Runaway DC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 m | 7.16 L/s | 20.7 % | 224 rpm | 22.4 V | 19.7 V | 25.9 W | 36.9 % | 448 rpm | 44.8 V |
| 1.5 m | 8.79 L/s | 20.5 % | 275 rpm | 27.5 V | 24.1 V | 51.7 W | 40.0 % | 550 rpm | 55.0 V |
| 2.0 m | 10.16 L/s | 20.3 % | 318 rpm | 31.8 V | 27.6 V | 82.5 W | 41.4 % | 636 rpm | 63.6 V |
| 2.5 m | 11.36 L/s | 20.1 % | 356 rpm | 35.6 V | 30.7 V | 117.3 W | 42.1 % | 711 rpm | 71.1 V |
| 3.0 m | 12.46 L/s | 20.0 % | 390 rpm | 39.0 V | 33.4 V | 155.7 W | 42.5 % | 780 rpm | 78.0 V |

### Flow range (R2)

From one 20 mm jet to two 45 mm jets, the inserts pass 1.3 to 11.0 L/s at 1.0 m, 1.9 to 15.6 L/s at 2.0 m and 2.3 to 19.2 L/s at 3.0 m. Two jets carrying 15 L/s would need 60.6 mm bores at 1.0 m, 43.7 mm at 2.0 m and 38.0 mm at 3.0 m. A 61 mm jet on a 150 mm pitch circle is far outside Turgo practice, which is why R2 is stated as 5 to 10 L/s at 1.0 m and 5 to 15 L/s from 2.0 m (PCF-DDR-002). Both ranges are met.

### Sensitivity

Pipe loss dominates the result. Table 5 resizes the inserts for 10 L/s in each case; all rows include the 90 mm valve with its fittings.

Table 5. Sensitivity at 2.0 m and 10 L/s.

| Case | Loss | Into battery | Water to wire | Daily energy | At 1.0 m, 7 L/s |
| --- | --- | --- | --- | --- | --- |
| 110 mm penstock (103.6 mm bore), runner 75 % | 25.9 % | 75.0 W | 38.2 % | 1.80 kWh | 23.1 W |
| 125 mm penstock (117.6 mm bore), runner 75 % (design) | 19.9 % | 81.7 W | 41.6 % | 1.96 kWh | 25.5 W |
| 160 mm penstock (150.6 mm bore), runner 75 % | 14.7 % | 87.3 W | 44.5 % | 2.10 kWh | 27.5 W |
| 110 mm penstock, runner 80 % | 25.9 % | 80.1 W | 40.8 % | 1.92 kWh | 25.0 W |
| 125 mm penstock, runner 80 % | 19.9 % | 87.1 W | 44.4 % | 2.09 kWh | 27.5 W |

(The design row differs from Table 3 by 0.8 W because its inserts are sized for exactly 10 L/s rather than rounded to 34 mm.)

R3 has a margin of 1.7 W (2.1 %) at exactly 10 L/s. A runner below the assumed 75 % would erase it, so runner efficiency is the number to measure first at TRL 4; a full-bore valve would restore a 5.6 W margin.

## 6. Runaway and the voltage clamp (R8)

If the battery is lost and the dump-load switch fails, the runner speeds up toward runaway. With the design inserts at 3.0 m that is 780 rpm and 78.0 V DC open circuit. The largest shaft power in the operating envelope is 230.6 W, at 3.0 m and 15 L/s (38.0 mm inserts); there the bus under MPPT load is 31.3 V and runaway is 750 rpm and 75.0 V.

The clamp is a comparator on the DC bus, independent of the microcontroller, that switches an 8.2 Ω resistor across the bus at 48 V and releases it at 40 V. The turbine torque is taken to fall linearly from stall to zero at runaway. With the resistor connected in the worst case, the runner settles at 441 rpm with the bus at 38.7 V and 183 W in the resistor. That is below the 40 V release point, so the clamp cycles between 40 and 48 V and the bus never exceeds 48 V. 8.2 Ω is still the largest E12 value that holds the equilibrium below 40 V, now with a 1.3 V margin; a 6.8 Ω resistor would give more if the generator constants come out less favorable. At 48 V the 8.2 Ω resistor dissipates 281 W, so it needs a 300 W aluminium-clad resistor on a heat sink. In normal running the bus never reaches the clamp: its highest open-circuit value at best speed is 39.0 V.

Only a double fault (load and clamp) lets the generator reach about 78 V, which is why the whole DC side stays enclosed and rated for 100 V. Mechanically, runaway is benign for the runner: the rim runs at 7.9 m/s and the hoop stress is about 0.08 MPa, a small fraction of PETG strength. The generator's overspeed rating at about 800 rpm must be confirmed with its supplier.

## 7. Bearings (R12)

The worst bearing load is at 3.0 m and 15 L/s with one jet closed, so the remaining jet's force is not balanced by the other. The radial load is 42.8 N (jet force at the pitch radius). The axial load, taken conservatively as the full jet momentum plus runner weight, is 101.2 N. With X = 0.56 and Y = 2.0, the equivalent load is 226.3 N and the basic L10 life of a UC204 insert (12.8 kN) at 375 rpm is about 8.0 x 10⁶ h, so bearing fatigue is not a concern. Life will be set by seal wear and water ingress, which a paper calculation cannot verify; the V-ring under the lid and the guard keep spray off the lower seal. The printed runner's life under continuous flow with sand is also unknown, so R12 remains at risk.

## 8. Geometry, printing and mass (R9, R13, R14)

- **Runner.** The model's envelope is 200 x 200 x 50 mm, which fits a 220 x 220 x 250 mm bed. Printed mass is about 524 g and print time about 21 h at 25 g/h, inside the 24 h target but only just. A 0.6 mm nozzle would shorten it.
- **Nozzles.** Each nozzle, with its saddle, fits a 167 x 130 x 244 mm space standing on its spigot: about 308 g and 12 h each.
- **Setting height.** The nozzle centerline is 280 mm above normal tailwater (R13). The runner underside is 199 mm above tailwater (210 mm in v0.2: the runner was lowered 11 mm with the nozzle tip, PCF-DDR-003 P6), which is how far the tailwater can rise before it touches the runner. At the design point the setting height is 12.3 % of the total site drop.
- **Mass.** Table 6 gives the mass of the turbine unit, now component by component with its fixings.

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
| Gate valve with reducer and expander | 2.40 kg |
| **All of the above** | **30.8 kg** |

R14 is met with the turbine unit taken as items 1 to 6 and 11 (Amish confirmed this definition on 2026-09-25, PCF-DDR-002), now counted with its fixings, foot plates and tie rods, which the v0.2 estimate of 22.2 kg left out. The margin is 0.5 kg; the generator plate was thinned to 8 mm, the foot plates to 5 mm and the post tube to 20 x 2 mm to keep it.

## 9. Penstock surge (R17)

The pressure wave travels at 301 m/s in 125 mm SN8 PVC, so any closure faster than 0.13 s acts as instantaneous. An instantaneous stop at 3.0 m head (1.15 m/s in the pipe) would add 35.2 m of head, far beyond drainage pipe. Closing the gate valve over 10 s adds only 0.47 m, so the peak at the valve is 33.4 kPa (static 28.9 kPa), within the assumed 50 kPa. A multi-turn gate valve needs about ten turns to close, which enforces the 10 s. A single nozzle blocking at once would add about 17.6 m. The 6 mm screen keeps out anything that could plug a 20 mm or larger insert in one piece, but a mat of leaves could not be ruled out, so the forebay screen must be kept clear.

## 10. Dump load (R7)

The largest output on the 12 V side is 170.4 W (3.0 m, 15 L/s), so the 300 W dump load has a margin of 1.76 times. The control behavior in R7 (speed within 10 %, full diversion within 1 s) depends on the controller and needs a bench test at TRL 4.

## 11. Cost (R15)

From `bom/bom.csv`, the kit (every item except the penstock and battery) costs USD 534.00 with a new generator. Value-engineering target: USD 450. Estimated cost of the constructable design: USD 534 (USD 84 over the target). With a salvaged washing machine motor at about USD 40 it costs USD 464.00 (USD 14 over). The increase from USD 448.00 in v0.2 is the parts added to make the design buildable (PCF-DDR-003): fixings, pipe stands, flexible couplings, the valve reducer and expander, flange bearing units and the forebay connector. The penstock (USD 140.00 for 20 m) and the battery (USD 160.00) are excluded. Cost drivers and savings worth trying are listed in the design decisions register (PCF-DEC-001, Value engineering).

## 12. Numbers corrected from TRL 2 and earlier versions

| Quantity | TRL 2 estimate | v0.1 (110 mm penstock) | v0.2 (125 mm penstock) | v0.3 (constructable design) |
| --- | --- | --- | --- | --- |
| Pipe loss | 10 % | 23.6 % | 17.0 % | 20.3 % (valve fittings added) |
| Jet diameter | about 33 mm | 34 mm | 33 mm | 34 mm |
| Best speed | about 340 rpm | 311 rpm | 324 rpm | 318 rpm |
| Into the battery at 2.0 m | about 90 W | 77.2 W | 82.8 W | 82.5 W (81.7 W at exactly 10 L/s) |
| Water to wire | about 46 % | 39.5 % | 43.2 % | 41.4 % |
| Daily energy | about 2.2 kWh | 1.85 kWh | 1.99 kWh | 1.98 kWh |
| Output at 1.0 m / 3.0 m | about 30 W / 165 W | 23.9 W / 146.4 W | 26.0 W / 156.4 W | 25.9 W / 155.7 W |
| Runaway open circuit at 3.0 m | 75 to 83 V | 76.4 V | 79.5 V (bus clamped at 48 V) | 78.0 V (bus clamped at 48 V) |
| Nozzle height above tailwater | 0.44 m | 0.28 m | 0.28 m | 0.28 m |
| Turbine unit mass | about 20 kg | 22.2 kg | 22.2 kg | 24.5 kg (with fixings) |
| Kit cost, new generator | about $424 | $448.00 | $448.00 | USD 534 (value-engineering target USD 450) |
