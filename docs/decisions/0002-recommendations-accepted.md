---
doc_id: PCF-DDR-002
title: PicoFlow recommendations accepted
project: PicoFlow
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 acceptance of the TRL 3 recommendations (N1 to N5)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items N1 to N5); item O1 and the new item N6 remain proposed

## Context

The TRL 3 session (`docs/REVIEW.md`, session "TRL 3", and PCF-DDR-001) left five new items marked "Proposed, awaiting Amish", each with a recommendation, and one older item (O1) with no recommendation. On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is therefore decided as recommended. Items without one stay open. TRL 4 remains on hold by Amish's instruction, so any part of a decision that needs building, testing or purchasing is recorded but not carried out.

## Options considered

Table 1. Items with a recommendation.

| # | Item | Options | Recommendation |
| --- | --- | --- | --- |
| N1 | Design-point penstock | 110 mm; 125 mm | 125 mm for a 20 m run |
| N2 | R4, output at 1.0 m and 7 L/s | Keep 30 W and report not met; relax to 20 W | Relax to 20 W |
| N3 | R2, flow range | Keep 5 to 15 L/s at every head; state 5 to 10 L/s at 1.0 m and 5 to 15 L/s from 2.0 m | State the range per head |
| N4 | R14, turbine unit definition | Items 1 to 6 and 11; include the manifold and valve | Items 1 to 6 and 11 |
| N5 | R15, $2 cost margin | Accept; trim cost (for example a printed bearing housing) | Accept, and firm prices with quotes before any build |

## Decision

- **N1.** Decided by Amish, 2026-09-25: go with recommendation. The design-point penstock is 125 mm drainage PVC (SN8, 117.6 mm bore) on a 20 m run. Pipe and branch loss falls from 23.6 % to 17.0 % of head; output into the battery rises from 77.2 W to 82.8 W and water to wire from 39.5 % to 43.2 %. The design-point inserts change from 34 mm to 33 mm. The penstock stays outside the kit budget; 20 m costs about $140 instead of $100.
- **N2.** Decided by Amish, 2026-09-25: go with recommendation. R4 is now 20 W or more at 1.0 m and 7 L/s (was 30 W). The calculation gives 26.3 W (was 23.9 W with 110 mm), so R4 is met.
- **N3.** Decided by Amish, 2026-09-25: go with recommendation. R2 is now 5 to 10 L/s at 1.0 m and 5 to 15 L/s from 2.0 m. The inserts pass 1.3 to 11.3 L/s at 1.0 m and 1.9 to 16.1 L/s at 2.0 m, so R2 is met.
- **N4.** Decided by Amish, 2026-09-25: go with recommendation. The turbine unit in R14 is items 1 to 6 and 11 (22.2 kg); the manifold and valve (5.2 kg) are pipework carried separately. R14 is met.
- **N5.** Decided by Amish, 2026-09-25: go with recommendation. The $2 margin under the $450 budget is accepted and R15 is recorded as met. Firming prices with supplier quotes is purchasing work, which is TRL 4 and on hold; it is recorded as decided but not done. `budget_usd` stays $450.

Items that remain open (no recommendation, so they stay "Proposed, awaiting Amish"):

- **O1.** First site type, region and co-design partner, including confirmation that target sites carry about 5 to 15 L/s. Proposed, awaiting Amish.

New item raised while applying N1:

- **N6.** Inlet valve bore. `bom/bom.csv` lists a 90 mm (3 in) gate valve, while the calculation and the model treat the valve as full bore on the penstock. On a 125 mm line a 90 mm valve needs a reducer and an expander, which add loss and could erode the 2.8 W margin on R3. Options: (a) a full-bore gate valve matched to the penstock, re-priced in the kit; (b) keep the 90 mm valve and add the reducer losses to PCF-CAL-001. Recommendation: (b) first, to see whether R3 still holds, then (a) only if it does not. Proposed, awaiting Amish.

## Consequences

- PCF-REQ-001 v0.4: R2 and R4 restated; R3, R4, R5 and R2 now met; R14 definition confirmed; R15 met with the margin accepted.
- PCF-CAL-001 v0.2 and `docs/04-calcs/sizing.py`: design penstock 125 mm (SN8, 3.7 mm wall); all results rerun. 13 met, 1 at risk (R12), 3 not verifiable at TRL 3, none not met.
- PCF-PRC-001 v0.4 and PCF-PRB-001 v0.4: numbers updated from PCF-CAL-001 v0.2.
- `cad/src/model.py`: `penstock_od` 110 to 125 mm, `jet_d` 32 to 33 mm; STEP and STL re-exported. PCF-DWG-001 moved from Rev P1 to Rev P2. Concept media regenerated.
- `bom/bom.csv` and `bom/bom-notes.md`: item 7 now uses a 125 x 90 mm reducing tee; item 9 is 125 mm pipe at about $7.00 per meter ($140.00, excluded). Kit total unchanged at $448.00.
- `README.md`: concept numbers updated. `project.yaml`: no change needed (`budget_usd: 450`, `trl: 3`, `trl_target: 3`).
- PCF-DDR-001 v0.2: N1 to N5 marked as decided.
