---
doc_id: PCF-CAL-001
title: PicoFlow sizing calculations
project: PicoFlow
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First-principles sizing for TRL 3 against PCF-REQ-001 v0.3
---

# PicoFlow sizing calculations

By calculation, the design meets 8 of the 17 requirements in PCF-REQ-001 v0.3. Four are not met, two are at risk and three cannot be verified at TRL 3. The main finding is that the TRL 2 estimate of pipe loss (10 % of gross head) was too optimistic: 20 m of 110 mm PVC plus the fittings and the two nozzle branches lose about 24 % of the head at 10 L/s. As a result the design point gives about 77 W into the battery instead of about 90 W. That misses R3 (80 W) and R5 (40 % water to wire) by small margins, and R4 (30 W at 1 m) by a wider one. A 125 mm penstock recovers R3 and R5 (about 84 W, 43 %); that change is proposed, awaiting Amish. The two safety-critical items now pass on paper. A hardware clamp holds the DC bus below 48 V (R8), and a gate valve closing over 10 s or more keeps the drainage-grade penstock at about 35 kPa peak (R17).

Every number in this note is printed by `docs/04-calcs/sizing.py` (run `python docs/04-calcs/sizing.py` from the repo root), which also writes `docs/04-calcs/results.json` for the concept media. The script reads geometry from `cad/src/model.py` and costs from `bom/bom.csv`.

> **Safety:** PicoFlow works beside moving water, has a spinning runner and coupling, a generator that can reach about 76 V DC open circuit if both the load and the clamp fail, resistors that run hot, and a lithium battery. The numbers here are paper estimates, not evidence that a built unit is safe.

## 1. Results against requirements

Table 1 lists every requirement, with the items that are not met first. Status is one of met, not met, at risk, or not verifiable at TRL 3.

Table 1. Requirement status at TRL 3.

| ID | Target | Value from this note | Status |
| --- | --- | --- | --- |
| R2 | 5 to 15 L/s through inserts, one or two jets | 1.9 to 15.0 L/s at 2.0 m and 2.3 to 18.4 L/s at 3.0 m; only 1.3 to 10.5 L/s at 1.0 m (15 L/s would need 71 mm jets) | Not met at 1.0 m; met at 2.0 m and above |
| R3 | 80 W or more into the battery at 2.0 m, 10 L/s | 77.2 W (84.3 W with a 125 mm penstock) | Not met, 3.5 % short |
| R4 | 30 W or more at 1.0 m, 7 L/s | 23.9 W (26.3 W with a 125 mm penstock) | Not met |
| R5 | 40 % or more water to wire | 39.5 % (43.0 % with a 125 mm penstock) | Not met, 0.5 points short |
| R12 | Bearing L10 20,000 h or more; runner 8,760 h or more | Bearing L10 about 1.1 x 10^7 h at the worst load; printed runner life unknown | At risk (runner) |
| R15 | Kit $450 or less | $448.00 with a new generator; $378.00 with a salvaged one | At risk, $2 margin |
| R7 | 12 V charging, speed within 10 %, 100 % diversion within 1 s | 300 W dump load is 1.9 times the largest output (157.6 W); control behavior needs a bench test | Not verifiable at TRL 3 |
| R11 | Runner or inserts in 30 min, bearings in 60 min; bearings above the spray | Bearings 392 mm above tailwater on the lid, outside the housing; times need a trial | Not verifiable at TRL 3 |
| R16 | Half the dry-season flow at most; all water returned | Depends on the site survey | Not verifiable at TRL 3 |
| R1 | Generates from 1.0 to 3.0 m with the same runner | DC bus 19.2 V at 1.0 m, above the 15 V the buck converter needs | Met |
| R6 | 1.8 kWh/day or more at the design point | 1.85 kWh/day | Met, thin margin |
| R8 | No exposed conductor above 60 V DC; survives runaway | Clamp holds the bus at 37.2 V (below 48 V) in the worst case; 76.4 V open circuit only if the clamp also fails, inside the enclosed 100 V DC side; rim stress 0.07 MPa | Met by calculation; generator overspeed rating to confirm |
| R9 | Prints in 220 x 220 x 250 mm, runner 24 h or less | Runner 200 x 200 x 50 mm, about 525 g, about 21 h | Met (estimate) |
| R10 | Screen 6 mm or less, nozzles 20 mm or more | 6 mm screen; inserts 20 to 45 mm; design insert 34 mm | Met by design |
| R13 | Nozzle centerline 0.3 m or less above tailwater | 280 mm in the model | Met |
| R14 | Heaviest item 15 kg or less; turbine unit 25 kg or less | Generator 7.0 kg; turbine unit (items 1 to 6, 11) 22.2 kg; manifold and valve 5.2 kg carried separately | Met |
| R17 | Peak penstock pressure 50 kPa or less with the valve closed over 10 s or more | 34.7 kPa at 3.0 m | Met |

## 2. Assumptions

- Water at 15 °C: density 1,000 kg/m³, kinematic viscosity 1.14 x 10⁻⁶ m²/s; g = 9.81 m/s².
- Design point (PCF-REQ-001): 2.0 m gross head from the forebay surface to the nozzle centerline, 10 L/s, 20 m of 110 mm drainage PVC (SN4, 3.2 mm wall, 103.6 mm bore), roughness 0.0015 mm.
- Penstock fittings, as loss coefficients on the pipe velocity head: rounded entrance 0.20, intake screen 0.10, two bends 0.30 in total, open gate valve 0.15. Friction factor from the Swamee-Jain equation.
- Branches: 90 mm PVC, 84.0 mm bore. Jet 1 runs around the housing (1.40 m, tee branch 1.0 plus four elbows at 0.3); jet 2 is direct (0.30 m, tee branch 1.0 plus one elbow). Lengths come from the model layout.
- Nozzle velocity coefficient 0.97, so the nozzle loses 6 % of the head it receives.
- Runner: bucket speed 0.46 of jet speed at best efficiency, pitch diameter 150 mm, jet-to-shaft efficiency 75 % for a first printed runner (laboratory runners reach 87 to 91 %, per Williamson, Stark and Booker, 2013, cited in PCF-PRB-001), runaway at 2.0 times best speed (upper end of 1.8 to 2.0).
- Generator: 10 rpm per volt of rectified open-circuit DC; iron and friction loss 12 W at 340 rpm, proportional to speed; winding and cable resistance 0.8 Ω (DC equivalent); rectifier drop 1.6 V. These are typical of a low-speed permanent magnet machine and must be measured on the chosen unit.
- Buck converter 94 %; battery 13.6 V while charging; the converter needs a bus of about 15 V to reach 14.4 V absorption.
- Bearings: 6204-2RS with a dynamic load rating of 13.5 kN (catalog class).
- Printed runner: PETG at 1,270 kg/m³, printed mass 0.6 times the solid massing volume (thin buckets, partial infill), 25 g/h on a 0.4 mm nozzle.
- Surge: PVC modulus 3.0 GPa, water bulk modulus 2.2 GPa; the drainage pipe and joints are assumed good for 50 kPa (0.5 bar, the common joint tightness test level for non-pressure pipe). This rating must be confirmed with the pipe supplier.
- Costs are indicative prices from `bom/bom.csv`; the penstock (item 9) and battery (item 17) are excluded, as decided with the budget.

## 3. Hydraulics and nozzle size

At the design point the nozzles need a 34.1 mm jet for exactly 10 L/s; the 34 mm insert gives 9.94 L/s (Table 2). The penstock carries water at 1.18 m/s and loses 0.296 m. The branches lose 0.102 m (jet 1, around the housing) and 0.057 m (jet 2), so the two jets carry 4.94 and 5.01 L/s, within 1.5 % of each other. The mean net head at the nozzles is 1.53 m, a loss of 23.6 % of the gross head. With the 63 mm branches of the TRL 2 concept the loss would be 33.2 %, so the branches were enlarged to 90 mm in the model and the BOM.

Table 2. Design point hydraulics (2.0 m, two 34 mm jets).

| Quantity | Value |
| --- | --- |
| Flow | 9.94 L/s |
| Penstock loss | 0.296 m |
| Branch loss, jet 1 / jet 2 | 0.102 m / 0.057 m |
| Net head at the nozzles | 1.53 m |
| Pipe and branch loss | 23.6 % of gross head |
| Jet velocity | 5.31 m/s |
| Jet to pitch diameter ratio | 0.23 |

The jet to pitch diameter ratio of 0.23 is below the 0.28 of the PowerSpout DIY rotor cited in PCF-PRC-001, so 34 mm jets suit the 150 mm pitch circle.

## 4. Power chain at the design point

Table 3. Power at each stage, 2.0 m and 10 L/s.

| Stage | Power | Loss |
| --- | --- | --- |
| Gross hydraulic power | 195.1 W | |
| At the nozzles | 149.1 W | Pipe and branches, 46 W |
| Jet | 140.3 W | Nozzle, 9 W |
| Runner shaft | 105.3 W at 311 rpm, 3.23 N·m | Runner, 35 W |
| Rectified DC | 82.1 W at 27.1 V, 3.03 A | Generator and rectifier, 23 W (efficiency 78.0 %) |
| Into the battery | 77.2 W, 5.67 A at 13.6 V | Buck converter, 5 W |

Water to wire is 39.5 % and the daily energy, running 24 h, is 1.85 kWh. The generator runs at 31.1 V open circuit at best speed, so the bus is well above the battery.

## 5. Head range

With the 34 mm inserts left in place, flow and output rise with head (Table 4). The bus stays above 15 V down to 1.0 m, so a 12 V battery charges across the whole range with a buck converter (R1). At 1.0 m and 7 L/s (R4) the right insert is again 34 mm, and output is 23.9 W at 219 rpm.

Table 4. Head range with the design-point inserts.

| Gross head | Flow | Loss | Best speed | Open-circuit DC | Bus under load | Into battery | Water to wire | Runaway | Runaway DC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 m | 7.00 L/s | 24.3 % | 219 rpm | 21.9 V | 19.2 V | 23.9 W | 34.8 % | 438 rpm | 43.8 V |
| 1.5 m | 8.60 L/s | 23.9 % | 269 rpm | 26.9 V | 23.6 V | 48.2 W | 38.1 % | 538 rpm | 53.8 V |
| 2.0 m | 9.94 L/s | 23.6 % | 311 rpm | 31.1 V | 27.1 V | 77.2 W | 39.5 % | 622 rpm | 62.2 V |
| 2.5 m | 11.13 L/s | 23.3 % | 348 rpm | 34.8 V | 30.1 V | 110.1 W | 40.3 % | 697 rpm | 69.7 V |
| 3.0 m | 12.21 L/s | 23.2 % | 382 rpm | 38.2 V | 32.8 V | 146.4 W | 40.7 % | 764 rpm | 76.4 V |

### Flow range (R2)

From one 20 mm jet to two 45 mm jets, the inserts pass 1.3 to 10.5 L/s at 1.0 m, 1.9 to 15.0 L/s at 2.0 m and 2.3 to 18.4 L/s at 3.0 m. Two jets carrying 15 L/s need 70.9 mm bores at 1.0 m, 45.1 mm at 2.0 m and 38.7 mm at 3.0 m. A 71 mm jet on a 150 mm pitch circle is far outside Turgo practice, so R2 is not met at 1.0 m. At 1.0 m the practical ceiling is about 10.5 L/s.

### Sensitivity

Pipe loss dominates the shortfall. Table 5 resizes the inserts for 10 L/s in each case.

Table 5. Sensitivity at 2.0 m and 10 L/s.

| Case | Loss | Into battery | Water to wire | Daily energy | At 1.0 m, 7 L/s |
| --- | --- | --- | --- | --- | --- |
| 110 mm penstock, runner 75 % (baseline) | 23.7 % | 77.4 W | 39.4 % | 1.86 kWh | 23.9 W |
| 125 mm penstock (117.6 mm bore), runner 75 % | 17.5 % | 84.3 W | 43.0 % | 2.02 kWh | 26.3 W |
| 160 mm penstock (150.6 mm bore), runner 75 % | 12.2 % | 90.1 W | 45.9 % | 2.16 kWh | 28.4 W |
| 110 mm penstock, runner 80 % | 23.7 % | 82.6 W | 42.1 % | 1.98 kWh | 25.8 W |
| 125 mm penstock, runner 80 % | 17.5 % | 89.9 W | 45.8 % | 2.16 kWh | 28.4 W |

(The baseline row differs from Table 3 by 0.2 W because its inserts are sized for exactly 10 L/s rather than rounded to 34 mm.)

A 125 mm penstock on a 20 m run meets R3 and R5. No case in Table 5 reaches 30 W at 1.0 m, so R4 needs either a relaxed target or a better runner than assumed. Both are proposed, awaiting Amish (see `docs/REVIEW.md`).

## 6. Runaway and the voltage clamp (R8)

If the battery is lost and the dump-load switch fails, the runner speeds up toward runaway. With the design inserts at 3.0 m that is 764 rpm and 76.4 V DC open circuit. The largest shaft power in the operating envelope is 214.2 W, at 3.0 m and 15 L/s (38.7 mm inserts); there the bus under MPPT load is 30.1 V and runaway is 723 rpm and 72.3 V.

The clamp is a comparator on the DC bus, independent of the microcontroller, that switches an 8.2 Ω resistor across the bus at 48 V and releases it at 40 V. The turbine torque is taken to fall linearly from stall to zero at runaway. With the resistor connected in the worst case, the runner settles at 424 rpm with the bus at 37.2 V and 169 W in the resistor. That is below the 40 V release point, so the clamp cycles between 40 and 48 V and the bus never exceeds 48 V. 8.2 Ω is the largest E12 value that holds the equilibrium below 40 V. At 48 V it dissipates 281 W, so it needs a 300 W aluminium-clad resistor on a heat sink. In normal running the bus never reaches the clamp: its highest open-circuit value at best speed is 38.2 V.

Only a double fault (load and clamp) lets the generator reach about 76 V, which is why the whole DC side stays enclosed and rated for 100 V. Mechanically, runaway is benign for the runner: the rim runs at 7.6 m/s and the hoop stress is about 0.07 MPa, a small fraction of PETG strength. The generator's overspeed rating at about 760 rpm must be confirmed with its supplier.

## 7. Bearings (R12)

The worst bearing load is at 3.0 m and 15 L/s with one jet closed, so the remaining jet's force is not balanced by the other. The radial load is 41.8 N (jet force at the pitch radius). The axial load, taken conservatively as the full jet momentum plus runner weight, is 97.7 N. With X = 0.56 and Y = 2.0, the equivalent load is 218.8 N and the basic L10 life at 382 rpm is about 1.1 x 10⁷ h, so bearing fatigue is not a concern. Life will be set by seal wear and water ingress, which a paper calculation cannot verify. The printed runner's life under continuous flow with sand is also unknown, so R12 remains at risk.

## 8. Geometry, printing and mass (R9, R13, R14)

- **Runner.** The model's envelope is 200 x 200 x 50 mm, which fits a 220 x 220 x 250 mm bed. Printed mass is about 525 g and print time about 21 h at 25 g/h, inside the 24 h target but only just. A 0.6 mm nozzle would shorten it.
- **Setting height.** The model puts the nozzle centerline 280 mm above normal tailwater (TRL 2: 440 mm) by shortening the frame legs to 80 mm. The runner underside is 210 mm above tailwater, which is how far the tailwater can rise before it touches the runner. At the design point the setting height is 12.3 % of the total site drop (TRL 2: about 18 %).
- **Mass.** Table 6 gives the mass of the turbine unit.

Table 6. Mass estimate.

| Item | Mass |
| --- | --- |
| Generator, 500 W low-speed BLDC (catalog class, assumed) | 7.00 kg |
| Housing, 315 mm PVC | 3.12 kg |
| Lid, 12 mm HDPE | 1.82 kg |
| Frame, about 2.0 m of 40 x 40 x 4 mm angle | 4.84 kg |
| Bearing housing, posts, plate and guard (aluminium, model volume) | 3.81 kg |
| Shaft, 316 stainless | 0.75 kg |
| Runner, PETG | 0.53 kg |
| Coupling | 0.30 kg |
| **Turbine unit, items 1 to 6 and 11** | **22.2 kg** |
| Manifold and nozzles (about 2.0 m of 90 mm PVC and fittings) | 3.20 kg |
| Gate valve | 2.00 kg |
| **All of the above** | **27.4 kg** |

R14 is met with the turbine unit taken as items 1 to 6 and 11, the same basis as the TRL 2 estimate of about 20 kg. The manifold and valve are pipework that is carried and fitted separately. If Amish wants them counted in the turbine unit, R14 is not met at 27.4 kg.

## 9. Penstock surge (R17)

The pressure wave travels at 298 m/s in 110 mm SN4 PVC, so any closure faster than 0.13 s acts as instantaneous. An instantaneous stop at 3.0 m head (1.45 m/s in the pipe) would add 44.0 m of head, far beyond drainage pipe. Closing the gate valve over 10 s adds only 0.59 m, so the peak at the valve is 34.7 kPa (static 28.9 kPa), within the assumed 50 kPa. A multi-turn gate valve needs about ten turns to close, which enforces the 10 s. A single nozzle blocking at once would add about 22.0 m. The 6 mm screen keeps out anything that could plug a 20 mm or larger insert in one piece, but a mat of leaves could not be ruled out, so the forebay screen must be kept clear.

## 10. Dump load (R7)

The largest output on the 12 V side is 157.6 W (3.0 m, 15 L/s), so the 300 W dump load has a margin of 1.9 times. The control behavior in R7 (speed within 10 %, full diversion within 1 s) depends on the controller firmware and needs a bench test at TRL 4.

## 11. Cost (R15)

From `bom/bom.csv`, the kit (every item except the penstock and battery) costs $448.00 with a new generator, $2.00 under the $450 budget. With a salvaged washing machine motor at about $40 it costs $378.00. The penstock ($100.00 for 20 m of 110 mm pipe) and the battery ($160.00) are excluded. The TRL 3 changes added about $24 to the TRL 2 total of $424: the 90 mm branches, the gate valve, the clamp and its resistor, and a coupling guard, partly offset by the shorter frame. With indicative prices, a $2 margin is within the estimate's error, so R15 is at risk.

## 12. Numbers corrected from TRL 2

| Quantity | TRL 2 estimate | TRL 3 calculation |
| --- | --- | --- |
| Pipe loss | 10 % | 23.6 % |
| Jet diameter | about 33 mm | 34 mm |
| Best speed | about 340 rpm | 311 rpm |
| Into the battery at 2.0 m | about 90 W | 77.2 W |
| Water to wire | about 46 % | 39.5 % |
| Daily energy | about 2.2 kWh | 1.85 kWh |
| Output at 1.0 m / 3.0 m | about 30 W / 165 W | 23.9 W / 146.4 W |
| Runaway open circuit at 3.0 m | 75 to 83 V | 76.4 V (bus clamped at 48 V) |
| Nozzle height above tailwater | 0.44 m | 0.28 m |
| Turbine unit mass | about 20 kg | 22.2 kg |
| Kit cost, new generator | about $424 | $448.00 |
