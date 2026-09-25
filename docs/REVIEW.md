# Review note: PicoFlow

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch run)

### What was done

- `docs/01-problem.md` (PCF-PRB-001 v0.2): problem, users, site context, constraints, out of scope, prior work with inline sources (World Bank SDG 7 report 2025, DFID R8150 Vietnam report, PowerSpout TRG, LH and DIY rotor pages, Williamson et al. 2013, Benzon et al. 2016, University of Bristol), open questions. There was no co-design checklist to keep.
- `docs/03-requirements.md` (PCF-REQ-001 v0.2): 16 measurable requirements (R1 to R16) with targets, verification and an estimated status column, plus a list of requirements not met.
- `docs/02-concept.md` (PCF-PRC-001 v0.2): how it works, 17 numbered components, design point and head-range numbers, runaway voltage, loads, mass, setting height, cost, design choices, safety section, open questions.
- `cad/src/concept_media.py`: massing model of the turbine unit (runner, shaft, bearing housing, coupling, generator, housing, two-nozzle manifold, valve, frame), the site (2.2 m weir, forebay, penstock) and the electrics (post, rectifier, controller, dump load, wiring, battery), each with a BOM number. A custom exploded view leaves the weir out and draws the penstock as a stub so the parts read clearly.
- `media/`: `hero.png` (1.75 m figure), `concept-blueprint.png`, `.pdf` and `.svg`, `cutaway.png`, `exploded.png` (callouts 1 to 17), `flow.png` (power flow at the design point, estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 17 lines with indicative USD costs, numbered to match the exploded view; `bom/bom-notes.md` gives the kit totals and exclusions.
- `README.md`: hero image and links line before "## Problem"; problem, concept, key components and a safety note brought in line with the concept.
- `project.yaml`: `problem` reworded (see decision 9). Budget, TRL, name, slug, area, licenses and pitch unchanged.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Design point | 2.0 m gross head, 10 L/s, 196 W hydraulic | |
| Jets | two, about 33 mm, at about 5.8 m/s | |
| Runner | 200 mm OD, 150 mm pitch, about 340 rpm, about 3.5 N·m | R9 met |
| Into the 12 V battery | about 90 W (about 46 % water to wire) | R3, R5 met, thin margin |
| Daily energy | about 2.2 kWh | R6 met |
| Output at 1.0 m / 3.0 m | about 30 W / about 165 W | R4 at risk |
| Runaway at 3.0 m | about 750 to 830 rpm, about 75 to 83 V DC open circuit | **R8 not met** |
| Nozzle height above tailrace | about 0.44 m (target 0.3 m) | **R13 not met** |
| Turbine unit mass | about 20 kg | R14 met |
| Kit cost, new generator | about $424 (penstock and battery excluded) | **R15 not met, about 21 % over** |
| Kit cost, salvaged washing machine motor | about $354 | About at budget |

Requirements not met or at risk: **R8** (touch voltage at runaway), **R13** (setting height), **R15** (cost), **R4** (30 W at 1 m, at risk), **R12** (printed runner life, at risk). R7 (controller behavior) and R16 (stream protection) are unverified or site-dependent.

### Proposed, awaiting Amish

1. **Budget.** The kit is about $424 with a new generator against `budget_usd: 350`. Options: (a) keep $350 and make the salvaged washing machine motor the baseline (about $354); (b) raise `budget_usd` to $450; (c) keep $350 and cut elsewhere (printed housing, cheaper valve), which is unlikely to close $74 alone. Recommendation: (b) for the prototype, so the reference build uses a repeatable generator, with (a) documented as the low-cost variant. `project.yaml` is unchanged.
2. **Generator.** A: new low-speed BLDC with a shaft (recommended for the prototype). B: salvaged direct-drive washing machine motor. C: e-bike hub motor with the runner on the disc flange.
3. **Controller.** A: open-design MPPT and dump-load board. B: off-the-shelf diversion controller. Recommendation: B for first bench tests, A as the TRL 3 design.
4. **Battery voltage.** 12 V (recommended; charges across 1 to 3 m with a buck converter) or 24 V (needs buck-boost at 1 m).
5. **Runner material.** PETG for the prototype, glass-filled nylon for field units (recommended), or nylon from the start.
6. **Layout.** Vertical shaft with the generator on the lid (recommended) or horizontal shaft.
7. **Two jets** (recommended) or one.
8. **Penstock pipe class.** Allow non-pressure drainage pipe with a slow-closing valve and a surge check (recommended), or require pressure pipe.
9. **Problem wording in `project.yaml`.** "No simple turbine option" is contradicted by the 100,000 or more cheap low-head units sold in Vietnam (DFID R8150). Changed to "few durable, repairable turbine options", which keeps the meaning. Revert if preferred.
10. **Turgo versus propeller.** The pitch's Turgo is kept. At sites with much more than 15 L/s a propeller may be better; confirm the target site type.
11. **First site type, region and partner** for co-design and a site survey.

### Safety concerns

- Drowning and flood risk at weirs and streams during survey, installation and service.
- Runaway voltage above 60 V DC if the load and dump load both fail (R8); needs a hardware clamp and a DC side rated and enclosed for 100 V.
- Exposed coupling between lid and generator; needs a guard.
- Dump-load resistor surface temperatures above 200 °C; fire risk near timber or grass.
- Battery short-circuit current (LiFePO4) or hydrogen venting (lead-acid); fuse at the terminal, BMS, ventilation.
- Water hammer from fast valve closure on a long penstock.
- Stream diversion effects on fish and downstream users; permits.

### Problems and notes

- The hero and blueprint show a short, steep penstock at a weir so the figure stays compact; typical sites need 10 to 30 m of pipe at a gentler slope. The caption says so.
- The massing model's frame height (0.44 m to the nozzles) is the reason R13 fails; it was left as drawn so the gap is visible.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- The portfolio's SwapCell 48 V pack is not used; a 12 V household battery fits this design better.
- Suggestion, not added to the repo: a co-design checklist (site survey, users, flow records through a dry season) in PCF-PRB-001, like the one in SunSpoke.

### Recommended next step

Review this note and the media, then decide items 1 to 4. If approved, run `/advance-trl3` to size the runner and nozzles by calculation, confirm the generator constant, design the runaway clamp, lower the frame, and produce the parametric model and drawing sheet.
