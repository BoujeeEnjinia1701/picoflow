---
doc_id: PCF-DDR-001
title: PicoFlow TRL 2 review decisions
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
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review points
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items D1 to D10); item O1 and the new TRL 3 items N1 to N5 remain proposed

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25, /populate) listed 11 items marked "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided as recommended. The item without a recommendation stays open.

The portfolio-wide decisions on the SwapCell interface do not apply: PicoFlow charges a 12 V household battery and does not use a SwapCell pack.

## Options considered

Table 1. Items with a recommendation (numbers match the TRL 2 review note).

| # | Item | Options | Recommendation |
| --- | --- | --- | --- |
| D1 | Budget | (a) keep $350 with a salvaged motor as baseline; (b) raise `budget_usd` to $450; (c) keep $350 and cut elsewhere | (b), with (a) documented as the low-cost variant |
| D2 | Generator | A new low-speed BLDC; B salvaged washing machine motor; C e-bike hub motor | A for the prototype, with a mount that also accepts B |
| D3 | Controller | A open-design MPPT and dump-load board; B off-the-shelf diversion controller | B for the first bench tests, A as the TRL 3 design |
| D4 | Battery voltage | 12 V; 24 V | 12 V |
| D5 | Runner material | PETG; glass-filled nylon; nylon from the start | PETG for the prototype, glass-filled nylon for field units |
| D6 | Layout | Vertical shaft, generator on the lid; horizontal shaft | Vertical shaft |
| D7 | Jets | Two; one | Two, with the option to close one in the dry season |
| D8 | Penstock pipe class | Non-pressure drainage pipe with a slow-closing valve and a surge check; pressure pipe | Drainage pipe with a slow-closing valve and a surge check |
| D9 | Problem wording in `project.yaml` | "few durable, repairable turbine options"; revert to "no simple turbine option" | Keep the new wording |
| D10 | Turgo or propeller | Turgo, as in the pitch; propeller for sites well above 15 L/s | Turgo |

## Decision

- **D1.** Decided by Amish, 2026-09-25: go with recommendation. `budget_usd` is $450. The salvaged washing machine motor is the documented low-cost variant ($378.00 in PCF-CAL-001). The penstock and battery stay excluded from the kit budget. R15 now targets $450.
- **D2.** Decided by Amish, 2026-09-25: go with recommendation. The reference build uses a new low-speed BLDC with an output shaft; the generator plate on four posts is meant to take a salvaged direct-drive motor as well.
- **D3.** Decided by Amish, 2026-09-25: go with recommendation. The open-design MPPT, dump-load and clamp board is the TRL 3 design. An off-the-shelf diversion controller is for the first bench tests only, which are TRL 4 work and on hold.
- **D4.** Decided by Amish, 2026-09-25: go with recommendation. 12 V battery with a buck converter.
- **D5.** Decided by Amish, 2026-09-25: go with recommendation. PETG for the prototype runner and glass-filled nylon for field units.
- **D6.** Decided by Amish, 2026-09-25: go with recommendation. Vertical shaft with the bearings and generator on the lid.
- **D7.** Decided by Amish, 2026-09-25: go with recommendation. Two jets, one may be closed in the dry season. At TRL 3 the jets are placed opposite each other so their radial forces cancel.
- **D8.** Decided by Amish, 2026-09-25: go with recommendation. Drainage-grade pipe is allowed with a slow-closing (multi-turn gate) valve. The surge check is in PCF-CAL-001 section 9 and is now requirement R17.
- **D9.** Decided by Amish, 2026-09-25: go with recommendation. The problem line in `project.yaml` and `README.md` keeps "few durable, repairable turbine options".
- **D10.** Decided by Amish, 2026-09-25: go with recommendation. The design stays a Turgo, as in the pitch.

The pitch line was not proposed for change and is unchanged.

Items that remain open (no recommendation was made, so they stay "Proposed, awaiting Amish"):

- **O1.** First site type, region and co-design partner, including confirmation of the target site type (streams of about 5 to 15 L/s, which suit a Turgo, rather than larger flows, which suit a propeller). Portfolio guidance is that community designs pick co-design partners per area later. Proposed, awaiting Amish.

New items raised at TRL 3 (not part of the 2026-09-25 decision; details in `docs/REVIEW.md`):

- **N1.** Design-point penstock: 125 mm instead of 110 mm for a 20 m run, which meets R3 and R5. Recommendation: 125 mm. Proposed, awaiting Amish.
- **N2.** R4 (30 W at 1.0 m): relax to 20 W or keep 30 W as not met. Recommendation: relax to 20 W. Proposed, awaiting Amish.
- **N3.** R2 at 1.0 m: state the range as 5 to 10 L/s at 1.0 m. Recommendation: yes. Proposed, awaiting Amish.
- **N4.** R14: confirm that the "turbine unit" excludes the manifold and valve (22.2 kg; 27.4 kg with them). Recommendation: confirm. Proposed, awaiting Amish.
- **N5.** R15: accept the $2 margin or trim cost (for example a printed bearing housing). Recommendation: accept for now and firm up prices with quotes at TRL 4. Proposed, awaiting Amish.

## Consequences

- PCF-REQ-001 v0.3: R15 targets $450; R17 (penstock surge) added; R3, R4 and R5 now show not met by calculation.
- PCF-PRC-001 v0.3: design choices recorded as decided; numbers replaced by PCF-CAL-001; 90 mm branches, opposed jets, lowered frame, gate valve and hardware clamp added.
- PCF-PRB-001 v0.3: budget constraint and the battery voltage question updated.
- `project.yaml`: `budget_usd: 450`; TRL 3 evidence listed. TRL 4 stays on hold by Amish's instruction.
