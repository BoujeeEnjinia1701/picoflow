---
doc_id: PCF-DDR-003
title: PicoFlow design for construction
project: PicoFlow
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction and open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: A2 accepted by Amish as recommended (full-bore inlet valve); A1 and A3 stay open
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. A2 in Table 3 is accepted: Amish, 2026-10-01: "picoflow - i agree with the recommendation", so option (a), a full-bore valve matched to the 125 mm penstock, re-priced, is decided and recorded in the design decisions register (PCF-DEC-001). A1 and A3 are still Proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of PCF-DDR-002 showed what PicoFlow does and was sized by calculation (PCF-CAL-001 v0.2), but it was a massing model. Checking it with build123d found parts that float, overlap or have no fixing:

- the 315 mm housing sat inside the 340 mm opening of the frame ring, 12.5 mm clear of it, so nothing carried it;
- each nozzle cut about 25 cm³ into the housing wall, and nothing held a nozzle in place;
- with the lid lifted for service, the runner could not pass the nozzle tips;
- the generator floated 5 mm above its plate;
- the inlet valve was drawn as a solid block on the 125 mm line, although the bill of materials lists a 90 mm valve;
- the reducing tee, elbows and nozzle inlets were placed closer together than real fittings allow.

The changes below keep what PicoFlow does: the same runner, jets, setting height (nozzle centerline 280 mm above tailwater), generator, housing pipe, penstock, valve type, electrics and safety measures. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now builds each component as a separate part and runs 69 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must stay apart are apart by at least the stated clearance, and a scan of every pair of components finds no unintended overlap. All 69 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | Frame drawn as solid square bars, 420 mm square with a 340 mm opening; the 315 mm housing did not rest on it. No feet or fixing to the pad. | A 380 mm square of 40 x 40 x 4 mm angle, horizontal legs inward, welded at mitred corners; the housing wall stands on the horizontal legs. Four 70 mm angle legs welded inside the corners, 80 x 80 x 5 mm foot plates with one M12 anchor each, and four flat bar pipe stops 1 mm outside the housing. | The inner edge of the angle lines up with the housing bore, so the wall bears on its full 7.7 mm and the water falls clear. Nozzles stay 280 mm above tailwater (R13). |
| P2 | Housing, lid and frame were not joined. | Four M10 tie rods, locked to the frame corners by two nuts each, pass up beside the housing and through the lid corners; washers and nuts on the lid clamp the lid onto the housing and the housing onto the frame. A 3 mm groove under the lid locates the housing top (housing cut to 303 mm). | One set of rods holds the whole stack; undoing four nuts frees the lid for service. |
| P3 | Bearing housing drawn as a plain cylinder bored only for the shaft, with an integral 120 mm square flange: no bearing seats, no retention, and it needs a lathe and a large block. | Two bought 4-bolt flange bearing units, 20 mm bore (UCF204 class, sealed 6204-class inserts), stacked on four 24 mm spacer sleeves and clamped to the lid by four M10 bolts with heads under the lid. A rubber V-ring on the shaft under the lid keeps spray off the lower seal. | Flange units come with seats, seals and set-screw locking, need no machining and are replaced in minutes (R11). Load rating 12.8 kN: bearing L10 8.0 x 10^6 h at the worst load (was 8.7 x 10^6 h); R12 bearing part still met. |
| P4 | Runner fixed by a "keyed hub and clamp nut" with no keyway or thread in the model. | A bought clamping shaft hub (20 mm bore, 56 mm flange) grips the shaft; four M5 screws hold the runner to it through heat-set inserts in the runner hub. The shaft ends flush with the runner underside. | No keyway or thread to machine; height is set by sliding the hub on the shaft. |
| P5 | Nozzles were cones that overlapped the housing wall, had no fixing, and met the horizontal 90 mm branches at 20 degrees with no fitting. | Each printed nozzle has a 60 mm horizontal 90 mm spigot, a gentle 20 degree bend and its cone, plus a 6 mm saddle shaped to the housing that sits on a 2 mm EPDM gasket and is held by four M6 bolts through the wall. The wall hole, cut from a full-size template, clears the nozzle by 2.5 mm. A 90 mm flexible coupling joins the spigot to the pipe. Both nozzles are the same part. | The saddle fixes the jet's aim to the housing and seals the hole; the coupling lets the printed nozzle come off without cutting pipe. The nozzle prints standing on its spigot in a 167 x 130 x 244 mm space (R9). |
| P6 | With the lid lifted for service, the runner hit the nozzle tips. | Nozzle exit moved from 85 to 115 mm before the strike point, so the tip sits at the inside of the wall, 19 mm outside the runner's lift path. The runner is lowered 11 mm (mid-plane 224 mm, underside 199 mm above tailwater) so the jet still meets the top of the buckets at the pitch circle. | Runner and inserts are reached by lifting the lid assembly, as R11 intends; the nozzle centerline stays 280 mm above tailwater (R13). The free jet is about 120 mm long, under four jet diameters. |
| P7 | Generator drawn 5 mm above its plate. | Generator sits on the plate, four M6 screws up through the plate into its face (screw circle to match the unit bought). | It needs a fixing; screws from below leave the top clear. |
| P8 | Posts were solid bars with no fixing; at 120 mm offset the washers under the lid would hit the housing. | Each post is a 20 x 2 mm steel tube on an M10 rod, with a 30 mm washer and nut under the lid and a washer and nut on the plate; posts moved to 125 mm each way. | The rod clamps lid, post and plate together; the washers now clear the housing by 4.3 mm. |
| P9 | The 110 mm coupling guard had no fixing and could not pass the bearing bolts. | A 146 mm length of 160 mm PVC pipe stands in a 2 mm groove on top of the lid and stops 1 mm under the generator plate, covering both bearing units and the coupling. | Fixed by the plate, nothing to screw; nothing that turns can be reached while the plate is on. |
| P10 | The penstock entered the side branch of a 125 x 90 tee, which standard tees do not offer; jet 2's elbow sat inside the tee and its reducer; there was no room between the last elbows and the nozzles. | Penstock moved to the jet 2 line (75 mm off the turbine axis) and into the run of a 125 x 90 reducing tee. Jet 2 goes straight through the tee and a 125 x 90 reducer; jet 1 leaves the 90 mm branch and runs round the housing through three elbows, the far corner moved from 330 to 460 mm. Five pipe lengths are given by the model (275, 970, 135, 100 and 110 mm). | Every fitting is a standard one with its socket depth allowed for. Branch lengths from the model: jet 1 1.67 m, jet 2 0.23 m. |
| P11 | The 90 mm valve of BOM line 8 was drawn as a solid block on the 125 mm line, and the calculation took it as full bore. | A 125 x 90 reducer, two short nipples and a 90 x 125 expander join the 90 mm valve into the 125 mm line. Their loss, 0.084 m at the design point, is now in PCF-CAL-001. Superseded on 2026-10-01 by A2 (a): a full-bore 125 mm PVC-U gate valve with solvent-weld sockets, joined to the tee by a 175 mm piece of penstock pipe (see Consequences). | The valve as bought can only be joined this way. The valve bore itself was open decision N6; see Table 3. |
| P12 | The branch pipework (about 6 kg with fittings, more with water) had no support. | Three pipe stands of 40 x 40 x 4 mm angle with foot plates and 90 mm pipe clips on M8 bosses (new BOM line 18). | Holds the pipework at the nozzle height without loading the printed nozzles. |
| P13 | The forebay had no outlet fitting or screen frame. | A 125 mm tank connector in the downstream end and a 6 mm stainless mesh riveted to an aluminium angle frame resting on the rim. | Lets the penstock join the tub and the screen lift off for cleaning. |
| P14 | Fixings were not listed. | New BOM line 19 for rods, bolts, nuts, washers, heat-set inserts and anchors. | Every joint above needs them. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Hydraulics | Valve reducer and expander add 0.084 m of loss; jet 2's straight path through the tee cuts its branch loss from 0.055 to 0.020 m; jet 1 has three elbows, not four. Pipe and branch loss is 20.3 % of head with the design inserts (was 17.0 %). Design-point insert 34 mm (33.7 mm for exactly 10 L/s, rounded; was 33 mm). Into the battery 82.5 W at 10.16 L/s, 81.7 W at exactly 10 L/s; water to wire 41.4 %; 1.98 kWh a day. R3, R5 and R6 still met; the margin on R3 is now 1.7 W at exactly 10 L/s. | Follows the model (P10, P11). |
| Other requirements | R1, R2, R4, R8, R17 recalculated and still met: 25.5 W at 1.0 m and 7 L/s; 1.3 to 11.0 L/s at 1.0 m and 1.9 to 15.6 L/s at 2.0 m; clamped bus 38.7 V at most; surge peak 33.4 kPa. | Small changes in flow split and losses. |
| Mass | Turbine unit (items 1 to 6 and 11, with their fixings) 24.5 kg, under R14's 25 kg. To keep it there the generator plate is 8 mm (was 10 mm), the foot plates 5 mm and the post tube 20 x 2 mm. | Tie rods, foot plates, bearing units and fixings add about 2 kg over the TRL 3 estimate of 22.2 kg, which left fixings out. |
| Cost | BOM lines 2, 3, 7, 8, 10 and 12 repriced and lines 18 and 19 added: turbine kit USD 534 with a new generator, USD 84 over the USD 450 value-engineering target; USD 464 with a salvaged motor. | Parts added for construction; `budget_usd` is unchanged. |
| Drawing | PCF-DWG-001 Rev P3; making sketches PCF-DWG-101 to 114 added. | Follows the model. |
| Documents | PCF-CAL-001 v0.3, PCF-REQ-001 v0.5 and PCF-PRC-001 v0.5: numbers updated. No performance or safety requirement changed status; R15 is now reported against its value-engineering target (USD 84 over) rather than as met. | Follows the model and Amish's 2026-10-01 instruction on budgets. |

*Table 3. Items for Amish: A2 accepted as recommended on 2026-10-01; A1 and A3 proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Accept the design-for-construction changes P1 to P14. | (a) accept; (b) accept with changes. | (a). |
| A2 | Inlet valve bore (N6, now quantified). The 90 mm valve with its reducer and expander costs 0.084 m of head; at exactly 10 L/s output is 81.7 W, 1.7 W over R3. A full-bore valve on the 125 mm line gives 85.6 W and 43.6 % water to wire. | (a) full-bore valve matched to the penstock, re-priced in the kit; (b) keep the 90 mm valve and its fittings. | (a), because R3 now rests on a 1.7 W margin and the runner efficiency is still unmeasured. Accepted by Amish, 2026-10-01. |
| A3 | Frame made by welding. | (a) welded by a local fabricator, as modelled; (b) a bolted frame with corner gussets, more parts but no welding. | (a): simplest and stiffest; one fabricator visit. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan PCF-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open items are in the design decisions register PCF-DEC-001.
- Requirement status (PCF-CAL-001 v0.3): none not met, 1 at risk (R12, printed runner life), 3 not verifiable at TRL 3, 12 met, and R15 over its value-engineering target by USD 84.
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept frame, bearing housing, guard and pipework; they need updating on Amish's Mac, where Blender is.
- With A2 accepted (2026-10-01), the 90 mm valve, reducer, expander and nipples are replaced in the model, BOM line 8 and the build plan (section 3.14, step 17, joint 13) by a full-bore 125 mm PVC-U gate valve with solvent-weld sockets, about 330 mm long and 5.5 kg (catalogue class, to confirm), joined to the tee by a 175 mm piece of penstock pipe. The model now runs 74 constructability checks, all passing. PCF-CAL-001 v0.4: 85.6 W into the battery at exactly 10 L/s, 5.6 W over R3 (was 81.7 W and 1.7 W); 87.8 W with the 34 mm inserts; water to wire 43.6 % at 10 L/s. The kit is USD 614, USD 164 over the USD 450 value-engineering target (line 8 from USD 40 to USD 120, an estimate to be quoted). The turbine unit stays 24.5 kg; the pipework carried separately is 9.8 kg (was 6.3 kg). PCF-DWG-001 is Rev P4.
- Bought parts are chosen at TRL 4; their sizes (flange units, generator face, fitting socket depths, valve bore) must be checked then and the model moved to suit.
