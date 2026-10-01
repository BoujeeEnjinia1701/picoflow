---
doc_id: PCF-DEC-001
title: PicoFlow design decisions register
project: PicoFlow
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from the review notes, PCF-DDR-001 to 003 and the build plan work
---

# PicoFlow design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes (frame, tie rods, flange bearing units, runner hub, nozzle saddles, manifold layout, valve fittings, pipe stands, fixings) | Accept; accept with changes | Accept | The whole build plan | PCF-DDR-003, A1 |
| 2 | Inlet valve bore (N6). The 90 mm valve with its reducer and expander costs 0.084 m of head: 81.7 W at exactly 10 L/s, 1.7 W over R3. A full-bore valve gives 85.6 W | (a) full-bore valve matched to the 125 mm penstock, re-priced; (b) keep the 90 mm valve and its fittings | (a) | Inlet valve and its fittings (build plan section 3.14, step 17) | PCF-DDR-002, N6; PCF-DDR-003, A2 |
| 3 | Frame made by welding or bolting | (a) welded by a local fabricator; (b) bolted with corner gussets | (a) | Frame (section 3.1) | PCF-DDR-003, A3 |
| 4 | First site type, region and co-design partner, including confirming that target sites carry about 5 to 15 L/s | Region and partner to be chosen | None yet | Site work: forebay, penstock length, pad, equipment post position | PCF-DDR-001 and 002, O1 |
| 5 | Split housing for runner inspection (shown in the product renders) | (a) one-piece pipe, as modelled; (b) split into bolted halves | (a) | Housing | REVIEW 2026-09-26, item 1 |
| 6 | Clear inspection window in the housing (shown in the product renders) | (a) none, as modelled; (b) optional bolted polycarbonate window | (b) as an option | Housing | REVIEW 2026-09-26, item 2 |
| 7 | Guard material (the renders show a clear guard) | (a) 160 mm PVC pipe, as modelled; (b) clear polycarbonate tube of the same size | (b) if a clear tube is found at that size, so the spider can be checked without removing it | Guard (section 3.9) | REVIEW 2026-09-26, item 3; PCF-DDR-003, P9 |
| 8 | Render layout choices: rectifier box shown loose beside the unit; tailwater drawn 20 mm below the channel edge | Accept as render choices; change the renders | Accept | Renders only | REVIEW 2026-09-26, items 5 and 6 |

Item 4 of the 2026-09-26 render review (nozzle holes in the housing) is now part of the design (PCF-DDR-003, P5) and needs no separate decision.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Generator: rpm per volt, losses and resistance at 200 to 400 rpm, overspeed rating at about 800 rpm, face screw circle and spigot, and a shaft at least 50 mm long | The calculation assumes 10 rpm/V; the plate holes and coupling position follow the face and shaft | PCF-CAL-001; PCF-DDR-003, P7 |
| 2 | Flange bearing units: 86 mm square, 64 mm bolt pitch, about 33 mm tall, 12.8 kN load rating | They set the lid holes, sleeve length and coupling height | PCF-DDR-003, P3 |
| 3 | Socket depths and centre-to-mouth sizes of the tee, reducer and elbows | The five pipe cut lengths assume 45 mm sockets and 70 mm elbow centre to mouth | PCF-DDR-003, P10 |
| 4 | The 90 mm flexible couplings fit the 90 mm printed spigot snugly | The spigot is printed; its outside may need sanding or a wrap of tape | PCF-DDR-003, P5 |
| 5 | Drainage pipe joints are good for 50 kPa | The surge check (R17) assumes it | PCF-CAL-001, section 9 |
| 6 | Gate valve bore and that it takes about ten turns to close | Sets the valve loss and enforces the 10 s closure (R17) | PCF-CAL-001; PCF-DDR-001, D8 |
| 7 | Forebay tub size and wall stiffness for a 125 mm tank connector | The outlet hole and screen frame follow the tub | PCF-DDR-003, P13 |

## Value engineering

Value-engineering target: USD 450 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 534 for the turbine kit with a new generator (USD 84 over the target); USD 464 with a salvaged washing machine motor (USD 14 over the target). The penstock (about USD 140 for 20 m) and the battery (about USD 160) are outside the kit, as decided with the budget. Main cost drivers and savings worth trying:

- The largest lines are the generator (USD 110), the nozzle manifold (USD 50), the controller (USD 43), the bearing units, plate, posts and guard (USD 43), the valve and its fittings (USD 40) and the housing and lid (USD 35).
- Making the design constructable added USD 86: fixings (USD 28), pipe stands (USD 15), flexible couplings and the reducer (USD 12), flange bearing units and plate (USD 10), valve fittings (USD 8), the forebay tank connector and screen frame (USD 8), and smaller items (USD 5).
- Savings worth trying: a salvaged washing machine motor (about USD 70 less, already the documented variant); a 6 mm steel generator plate instead of 8 mm aluminium (a few dollars, about 0.6 kg heavier); timber pipe stands; buying fixings as one bulk pack. If decision 2 goes to a full-bore valve, the valve line rises, so its price should be quoted against the output it recovers (about 4 W).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D10: budget USD 450 with the salvaged-motor variant documented, new low-speed BLDC generator, open-design controller (off-the-shelf only for first bench tests), 12 V battery, PETG then glass-filled nylon runner, vertical shaft, two jets, drainage pipe with a slow-closing valve, problem wording, Turgo | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | PCF-DDR-001 |
| 2026-09-25 | TRL 3 items N1 to N5: 125 mm design-point penstock, R4 relaxed to 20 W, R2 stated per head, R14 turbine-unit definition, USD 2 cost margin accepted | Amish: "i accept all your recommendations, go with them across all repos." | PCF-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | PCF-DDR-003 (changes open for review, open decision 1) |
| 2026-09-30 | Outstanding decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
| 2026-10-01 | The budget is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register, Value engineering |
