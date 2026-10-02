---
doc_id: PCF-DEC-001
title: PicoFlow design decisions register
project: PicoFlow
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from the review notes, PCF-DDR-001 to 003 and the build plan work
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Open decision 2 (inlet valve bore, N6) decided by Amish as recommended and moved to Decisions made; open items renumbered; clamp resistor added as a proposed item; value engineering updated for the full-bore valve
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: Amish accepted the recommendation of open item 8 (clamp resistor, option b, 6.8 Ω, 350 W); moved to Decisions made; value engineering updated (line 15 re-priced)
---

# PicoFlow design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes (frame, tie rods, flange bearing units, runner hub, nozzle saddles, manifold layout, pipe stands, fixings; the valve fittings of P11 are superseded by the full-bore valve decided on 2026-10-01) | Accept; accept with changes | Accept | The whole build plan | PCF-DDR-003, A1 |
| 2 | Frame made by welding or bolting | (a) welded by a local fabricator; (b) bolted with corner gussets | (a) | Frame (section 3.1) | PCF-DDR-003, A3 |
| 3 | First site type, region and co-design partner, including confirming that target sites carry about 5 to 15 L/s | Region and partner to be chosen | None yet | Site work: forebay, penstock length, pad, equipment post position | PCF-DDR-001 and 002, O1 |
| 4 | Split housing for runner inspection (shown in the product renders) | (a) one-piece pipe, as modelled; (b) split into bolted halves | (a) | Housing | REVIEW 2026-09-26, item 1 |
| 5 | Clear inspection window in the housing (shown in the product renders) | (a) none, as modelled; (b) optional bolted polycarbonate window | (b) as an option | Housing | REVIEW 2026-09-26, item 2 |
| 6 | Guard material (the renders show a clear guard) | (a) 160 mm PVC pipe, as modelled; (b) clear polycarbonate tube of the same size | (b) if a clear tube is found at that size, so the spider can be checked without removing it | Guard (section 3.9) | REVIEW 2026-09-26, item 3; PCF-DDR-003, P9 |
| 7 | Render layout choices: rectifier box shown loose beside the unit; tailwater drawn 20 mm below the channel edge | Accept as render choices; change the renders | Accept | Renders only | REVIEW 2026-09-26, items 5 and 6 |

Item 4 of the 2026-09-26 render review (nozzle holes in the housing) is now part of the design (PCF-DDR-003, P5) and needs no separate decision.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Generator: rpm per volt, losses and resistance at 200 to 400 rpm, overspeed rating at about 800 rpm, face screw circle and spigot, and a shaft at least 50 mm long | The calculation assumes 10 rpm/V; the plate holes and coupling position follow the face and shaft | PCF-CAL-001; PCF-DDR-003, P7 |
| 2 | Flange bearing units: 86 mm square, 64 mm bolt pitch, about 33 mm tall, 12.8 kN load rating | They set the lid holes, sleeve length and coupling height | PCF-DDR-003, P3 |
| 3 | Socket depths and centre-to-mouth sizes of the tee, reducer and elbows | The five pipe cut lengths assume 45 mm sockets and 70 mm elbow centre to mouth | PCF-DDR-003, P10 |
| 4 | The 90 mm flexible couplings fit the 90 mm printed spigot snugly | The spigot is printed; its outside may need sanding or a wrap of tape | PCF-DDR-003, P5 |
| 5 | Drainage pipe joints are good for 50 kPa | The surge check (R17) assumes it | PCF-CAL-001, section 9 |
| 6 | Full-bore 125 mm gate valve: socket depth (70 mm assumed), length over the sockets (330 mm), bore about 117 mm, mass (about 5.5 kg), price (USD 115 assumed), and that it takes about ten turns to close | Sets the pipe piece length, the valve loss and the pipework mass, and enforces the 10 s closure (R17) | PCF-CAL-001 v0.4; PCF-DDR-001, D8; decision of 2026-10-01 |
| 7 | Forebay tub size and wall stiffness for a 125 mm tank connector | The outlet hole and screen frame follow the tub | PCF-DDR-003, P13 |

## Value engineering

Value-engineering target: USD 450 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 618 for the turbine kit with a new generator (USD 168 over the target); USD 548 with a salvaged washing machine motor (USD 98 over the target). The penstock (about USD 140 for 20 m) and the battery (about USD 160) are outside the kit, as decided with the budget. Main cost drivers and savings worth trying:

- The largest lines are the full-bore inlet valve (USD 120, an estimate), the generator (USD 110), the nozzle manifold (USD 50), the controller (USD 43), the bearing units, plate, posts and guard (USD 43) and the housing and lid (USD 35). The 6.8 Ω, 350 W clamp resistor (decided 2026-10-01) raised line 15 from USD 28 to USD 32, an indicative price to be quoted.
- Making the design constructable added USD 86: fixings (USD 28), pipe stands (USD 15), flexible couplings and the reducer (USD 12), flange bearing units and plate (USD 10), valve fittings (USD 8, since replaced by the full-bore valve), the forebay tank connector and screen frame (USD 8), and smaller items (USD 5).
- Savings worth trying: a salvaged washing machine motor (about USD 70 less, already the documented variant); a 6 mm steel generator plate instead of 8 mm aluminium (a few dollars, about 0.6 kg heavier); timber pipe stands; buying fixings as one bulk pack. The full-bore valve (decided 2026-10-01) raised line 8 from USD 40 to USD 120 to recover 3.9 W at the design point, about USD 21 per watt; no published price was found for a 125 mm PVC-U gate valve, so getting real quotes is the first saving to try, and a cheaper full-bore valve of the same kind would bring most of the USD 80 back.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D10: budget USD 450 with the salvaged-motor variant documented, new low-speed BLDC generator, open-design controller (off-the-shelf only for first bench tests), 12 V battery, PETG then glass-filled nylon runner, vertical shaft, two jets, drainage pipe with a slow-closing valve, problem wording, Turgo | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | PCF-DDR-001 |
| 2026-09-25 | TRL 3 items N1 to N5: 125 mm design-point penstock, R4 relaxed to 20 W, R2 stated per head, R14 turbine-unit definition, USD 2 cost margin accepted | Amish: "i accept all your recommendations, go with them across all repos." | PCF-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | PCF-DDR-003 (changes open for review, open decision 1) |
| 2026-09-30 | Outstanding decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
| 2026-10-01 | Inlet valve bore (N6, open decision 2 in register v0.1): option (a), a full-bore valve matched to the 125 mm penstock, re-priced. A 125 mm PVC-U gate valve with solvent-weld sockets replaces the 90 mm valve, reducer and expander: 85.6 W at exactly 10 L/s, 5.6 W over R3; line 8 USD 120 | Amish: "picoflow - i agree with the recommendation" | PCF-DDR-003, A2; PCF-CAL-001 v0.4 |
| 2026-10-01 | The budget is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register, Value engineering |
| 2026-10-01 | Clamp resistor (R8, open item 8 in register v0.2): option (b), a 6.8 Ω aluminium-clad clamp resistor rated 350 W or more replaces the 8.2 Ω, 300 W one. In the worst case (3.0 m, 15 L/s) the clamp now settles the bus at 36.7 V, 3.3 V below its 40 V release, so it cycles as intended (the 8.2 Ω resistor settled at 40.1 V); 339 W at the 48 V switch-on point, inside the 350 W rating. BOM line 15 USD 32 (+USD 4) | Amish: "I approve of your recommendations for PicoFlow and GravitySort" | PCF-CAL-001 v0.5, section 6 |
