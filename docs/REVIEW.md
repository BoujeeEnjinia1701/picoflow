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

Items 1 to 10 were later decided by Amish, 2026-09-25: go with recommendation (PCF-DDR-001, D1 to D10). Item 11 has no recommendation and stays proposed, awaiting Amish (O1).

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

## Session 2026-09-25: TRL 3

Amish approved all TRL 2 recommendations on 2026-09-25 ("proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them."). This session took PicoFlow to TRL 3 and stopped there.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (PCF-DDR-001 v0.1): decisions D1 to D10 recorded as "Decided by Amish, 2026-09-25: go with recommendation"; O1 left open; new TRL 3 items N1 to N5 proposed.
- `docs/04-calcs/01-sizing.md` (PCF-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: first-principles hydraulics (Darcy-Weisbach with fittings, per-branch flow split), power chain with a generator loss model, head and flow range, sensitivity, runaway and clamp sizing, bearing life, print time, mass, penstock surge, dump load and cost. The script prints every quoted number and writes `docs/04-calcs/results.json`.
- `cad/src/model.py`: parametric build123d model of the turbine unit (runner, shaft, bearing housing with posts, plate and coupling guard, coupling, generator, housing and lid, 90 mm manifold with opposed nozzles, gate valve, penstock stub, frame). Exports `cad/step/picoflow-turbine-assembly.step` and `.stl` plus the runner, manifold, housing and bearing mount separately.
- `cad/src/sheets.py` and `cad/drawings/PCF-DWG-001.svg`, `.pdf`, `.png`: turbine unit general arrangement, Rev P1, scale 1:10, with main dimensions and a parts list; marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet keeps PCF-DWG-010, so DWG-001 was the next free number.
- `bom/bom.csv` and `bom/bom-notes.md`: every line priced with a supplier or supplier type; kit $448.00 against $450.
- `cad/src/concept_media.py`: now builds the turbine from `model.py` and reads the flow values and key figures from `results.json`; the weir is set for exactly 2.0 m of gross head. All media in `media/` refreshed and checked by eye; no `_views` folders left.
- `docs/01-problem.md`, `docs/02-concept.md`, `docs/03-requirements.md` moved to v0.3; `project.yaml` (`trl: 3`, `trl_target: 3`, `budget_usd: 450`, evidence list) and `README.md` updated. PDFs rebuilt in `docs/pdf/`.

### Requirements at TRL 3 (PCF-CAL-001)

17 requirements: 8 met, 4 not met, 2 at risk, 3 not verifiable at TRL 3.

| Status | Requirements |
| --- | --- |
| **Not met** | **R2** flow range at 1.0 m (10.5 L/s maximum, not 15); **R3** 77.2 W against 80 W; **R4** 23.9 W against 30 W at 1.0 m; **R5** 39.5 % against 40 % |
| At risk | R12 printed runner life (bearings fine, about 1.1 x 10^7 h); R15 $448.00 against $450, $2 margin |
| Not verifiable at TRL 3 | R7 controller behavior; R11 service times; R16 stream protection |
| Met | R1, R6 (1.85 kWh, thin), R8 (clamp holds 48 V; generator overspeed to confirm), R9 (about 21 h print), R10, R13 (280 mm), R14 (22.2 kg), R17 (34.7 kPa) |

Key numbers: pipe and branch losses 23.6 % of head (TRL 2 assumed 10 %); two 34 mm jets; 311 rpm and 3.23 N·m; 82.1 W rectified at 27.1 V; 77.2 W into the battery; 146.4 W at 3.0 m; runaway 764 rpm and 76.4 V open circuit at 3.0 m, clamped to 37 to 48 V by an 8.2 Ω, 300 W resistor; surge 0.59 m with a 10 s closure versus 44 m for an instant stop.

The main design changes at TRL 3, all within sizing scope: branches 63 to 90 mm, jets moved to opposite sides, frame legs cut to 80 mm (nozzles 440 to 280 mm above tailwater), quarter-turn valve replaced by a multi-turn gate valve, independent voltage clamp added, coupling guard added.

### Decisions recorded (PCF-DDR-001)

D1 budget $450 with the salvaged-motor variant documented; D2 new low-speed BLDC; D3 open-design controller as the TRL 3 design, off-the-shelf unit for first bench tests only; D4 12 V; D5 PETG prototype, glass-filled nylon for field units; D6 vertical shaft; D7 two jets; D8 drainage pipe with a slow-closing valve and surge check; D9 problem wording kept; D10 Turgo. All: "Decided by Amish, 2026-09-25: go with recommendation."

### Still awaiting Amish

N1 to N5 below were decided later on 2026-09-25 (PCF-DDR-002); only O1 remains open.

- **O1.** First site type, region and co-design partner, including confirmation that target sites carry about 5 to 15 L/s (Turgo range). No recommendation; partners are picked per area later.
- **N1.** Design-point penstock 125 mm instead of 110 mm for a 20 m run: 84.3 W and 43.0 %, meeting R3 and R5; costs more but sits outside the kit budget. Recommendation: 125 mm. Decided by Amish, 2026-09-25: go with recommendation (PCF-DDR-002).
- **N2.** R4: relax to 20 W at 1.0 m and 7 L/s, or keep 30 W as not met. Recommendation: relax to 20 W. Decided by Amish, 2026-09-25: go with recommendation (PCF-DDR-002).
- **N3.** R2: state the flow range as 5 to 10 L/s at 1.0 m and 5 to 15 L/s from 2.0 m. Recommendation: yes. Decided by Amish, 2026-09-25: go with recommendation (PCF-DDR-002).
- **N4.** R14: confirm "turbine unit" means items 1 to 6 and 11 (22.2 kg). Counting the manifold and valve gives 27.4 kg, which fails 25 kg. Recommendation: confirm. Decided by Amish, 2026-09-25: go with recommendation (PCF-DDR-002).
- **N5.** R15: accept the $2 margin or trim cost. Recommendation: accept, and firm prices with quotes before any build. Decided by Amish, 2026-09-25: go with recommendation (PCF-DDR-002).

### Safety concerns

- Drowning and flood risk at weirs and streams; the runner sits only 210 mm above normal tailwater, so flood levels must be checked at siting.
- Double-fault runaway (load and clamp) reaches about 76 V DC at 3 m; keep the DC side enclosed and rated for 100 V; confirm the generator's overspeed rating.
- Water hammer: a quarter-turn valve or a suddenly plugged nozzle could add 22 to 44 m of head to drainage pipe rated (assumed) for 50 kPa. Only the multi-turn gate valve is allowed; keep the screen clear. The 50 kPa rating is an assumption to confirm with the supplier.
- Dump load and clamp resistor surfaces above 200 °C; fire risk.
- Coupling guard added; still close the valve and wait for the runner to stop before service.
- LiFePO4 battery short-circuit current; fuse at the terminal and a BMS.

### Other notes

- No TRL 4 material exists in the repo (`build-log/` holds only its README, and `electronics/` and `firmware/` are empty). The TRL change was not written to the build log because build-log entries are TRL 4 evidence and are on hold.
- Citations: the TRL 2 review did not flag any unchecked citations, and no new external sources were added at TRL 3. The pipe joint rating (50 kPa) and generator constants are stated as assumptions, not sourced facts.
- The exploded view labels sit over the small coupling (item 4), which is hard to see; acceptable for concept media.

### Recommended next step

TRL 4 is on hold by Amish's instruction. The next step is for Amish to decide N1 to N5 and O1; if N1 to N3 are accepted, a short document update (PCF-REQ-001 and PCF-PRC-001) closes R2, R3 and R5 on paper, still at TRL 3.

For reference only, TRL 4 would need: a chosen generator with measured constants and overspeed rating; a printed runner and nozzles; a lab rig with a head tank or pump giving 1 to 3 m and 5 to 15 L/s; controller and clamp hardware; a lab test report (TST, `environment: lab`) covering output, efficiency, clamp response and runaway; and build log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25, in chat: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation" and recorded in `docs/decisions/0002-recommendations-accepted.md` (PCF-DDR-002 v0.1). TRL stays at 3.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| N1 | 125 mm design-point penstock | 110 mm; loss 23.6 %; 77.2 W; 39.5 %; 1.85 kWh/day; 34 mm inserts | 125 mm SN8; loss 17.0 %; 82.8 W; 43.2 %; 1.99 kWh/day; 33 mm inserts |
| N2 | R4 relaxed | 30 W target; 23.9 W, not met | 20 W target; 26.3 W, met |
| N3 | R2 stated per head | 5 to 15 L/s at every head; not met at 1.0 m | 5 to 10 L/s at 1.0 m, 5 to 15 L/s from 2.0 m; met (1.3 to 11.3 and 1.9 to 16.1 L/s) |
| N4 | R14 definition confirmed | Met, definition to confirm | Met, items 1 to 6 and 11 (22.2 kg) |
| N5 | $2 cost margin accepted | R15 at risk | R15 met; quotes before any build (TRL 4, on hold) |

Side effects of N1, from PCF-CAL-001 v0.2: runaway at 3.0 m 764 to 795 rpm and 76.4 to 79.5 V open circuit; worst-case clamped bus 37.2 to 39.6 V (still under the 40 V release, margin now 0.4 V); dump-load margin 1.90 to 1.68 times; bearing L10 1.1 x 10^7 to 8.7 x 10^6 h; surge peak 34.7 to 33.3 kPa; penstock cost (excluded) $100 to $140. Kit cost unchanged at $448.00 against `budget_usd: 450` (no budget change).

Files changed: `docs/03-requirements.md` (PCF-REQ-001 v0.4), `docs/04-calcs/01-sizing.md` (PCF-CAL-001 v0.2) and `sizing.py`, `results.json`, `docs/02-concept.md` (PCF-PRC-001 v0.4), `docs/01-problem.md` (PCF-PRB-001 v0.4), `docs/decisions/0001-trl2-review-decisions.md` (PCF-DDR-001 v0.2), new PCF-DDR-002, `cad/src/model.py` (`penstock_od` 125, `jet_d` 33) with STEP and STL re-exported, `cad/src/sheets.py` (PCF-DWG-001 Rev P1 to P2), `cad/src/concept_media.py` labels, `bom/bom.csv`, `bom/bom-notes.md`, `README.md`, `project.yaml` (evidence list only). All media, drawings and PDFs regenerated with designmolecule.com in the footers.

README: the four write-up sections (Concept rationale, Burning platform, Where it could be used, What sparked the idea) were added before "## Problem". The inspiration point is Eric Crewdson's Turgo patent (applied 1919, granted 1920), cited to Hydropower & Dams International.

### Requirement status (PCF-CAL-001 v0.2)

17 requirements: 0 not met, 1 at risk, 3 not verifiable at TRL 3, 13 met.

| Status | Requirements |
| --- | --- |
| Not met | None |
| At risk | R12 printed runner life (bearings fine) |
| Not verifiable at TRL 3 | R7 controller behavior; R11 service times; R16 stream protection |
| Met | R1, R2, R3 (82.8 W, 2.8 W margin), R4 (26.3 W), R5 (43.2 %), R6, R8, R9, R10, R13, R14, R15 ($2 margin accepted), R17 |

### Still awaiting Amish

- **O1.** First site type, region and co-design partner (no recommendation).
- **N6 (new).** Inlet valve bore: the BOM's 90 mm gate valve on the 125 mm penstock needs a reducer and expander that the calculation does not yet include and that could erode the 2.8 W margin on R3. Recommendation: add the reducer losses to PCF-CAL-001 first; move to a full-bore valve only if R3 then fails.

### Cross-repo actions

None. No PicoFlow recommendation depends on another repo.

### Safety

No safety requirement changed status. The double-fault open-circuit voltage rises to about 80 V DC at 3.0 m, still inside the enclosed 100 V DC side. The clamp margin below its 40 V release is now 0.4 V in the worst case; a 6.8 Ω clamp resistor is noted in PCF-CAL-001 as the option if measured generator constants are less favorable.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Firming prices with quotes (N5), measuring runner efficiency and generator constants, and any build or test were not started.
