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

## Session 2026-09-26: sources strengthened

Amish asked on 2026-09-26 to fix the weaker sources in the README. Changes (README only; no controlled document changed):

- What sparked the idea: the trade-press source (Hydropower & Dams International) was replaced by Gilkes' own history, "100 Years of the Turgo Impulse Turbine", which gives the 1919 application, the 1920 grant to Eric Crewdson, twice Pelton speed at the same head and the side-entry jet. Crewdson is now described as a trainee at Gilkes, as the source says, rather than naming the later company title. The Bristol paper (Williamson, Stark and Booker, Applied Energy 102, 2013) was rechecked and its test range (3.5 m down to 1 m, 87 % at 1 m) is now stated. INSPIRATIONS.md line updated to the new source.
- By country or region: "Andean South America (Peru, Bolivia)" had no source and was replaced by a Peru row citing the World Bank's 2019 results note on rural electrification (11,915 solar home systems in isolated areas; studies for 21 small hydropower projects).
- Burning platform: the Vietnam figure now follows the DFID R8150 wording ("doubtful whether there are more than 30,000" still running).
- Kept and rechecked: World Bank Tracking SDG 7 2025 (666 million, 85 %), DFID R8150, AEPC. The PowerSpout page (the maker's own) was kept but could not be refetched in this session.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose PicoFlow on 2026-09-26 for the first batch of product renders. This session added an appearance model for photoreal renders; no controlled document, the BOM or `cad/src/model.py` changed.

### What was added

- `cad/src/product_model.py`: `product_parts()` (47 parts: 33 shell, 5 internal, 5 accessory and 4 context, including the clear window, guard and tailwater), `TITLE` and three `RENDER_VIEWS` (hero, exploded, detail). All main dimensions and interfaces come from `PARAMS`, `_derived()` and `build_parts()` in `model.py`.
- Finished-product detail: filleted HDPE lid with corner bolts; aluminium bearing housing with bearing-seat rings, a filleted flange, cap screws and a grease nipple; stainless posts with nuts under a filleted generator plate; a two-hub jaw coupling with an orange elastomer spider; a finned BLDC generator with end caps, a rating label, a cable gland and lead; the tee, 90 mm branches, elbows and socket couplers; printed nozzles with separate 33 mm metal inserts; a gate valve with bonnet and handwheel; the frame drawn as galvanized angle on foot plates with anchor bolts.
- Context (group "context"): the model.py penstock stub on a pipe saddle, the concrete edges of the tailrace channel under the frame and the tailwater surface.
- README hero image now points to `media/render-hero.png`, with a link to `media/render-exploded.png`. The render files are produced separately.

### Differences from model.py (each Proposed, awaiting Amish)

1. **Housing split into two halves.** The model has one 315 mm pipe section. The appearance model splits it on the Y = 0 plane into front and back halves joined by bolted vertical seam flanges, so the exploded view can show the runner. Recommendation: keep the one-piece pipe for the kit (cheaper, no seam to seal); adopt the split only if runner inspection without lifting the lid is wanted.
2. **Clear inspection window.** A bolted polycarbonate window (about 180 x 200 mm) in the front of the housing shows the runner. It is not in the model or the BOM. Recommendation: adopt it as an optional part; it helps fault finding and teaching, adds a few dollars and needs a guard against impact from debris.
3. **Clear coupling guard.** The BOM gives a 110 mm coupling guard without a material; the renders show clear polycarbonate. Recommendation: accept, since a clear guard lets the owner check the spider without removing it.
4. **Nozzle entry holes in the housing.** The massing model lets the nozzles overlap the housing wall; the appearance model cuts clearance holes. Recommendation: accept; the holes are implied by the design.
5. **Rectifier box position.** The rectifier (BOM 13) is not in model.py and is installed on the equipment post; the exploded view shows it loose beside the unit. Recommendation: accept as a render layout only.
6. **Tailwater drawn 20 mm below the channel edge.** In model.py Z = 0 is both normal tailwater and the top of the pad under the frame. The render draws the water surface 20 mm lower so it reads as a surface. Recommendation: accept as an appearance choice; the setting height (R13) is unchanged.

### Status

This is an appearance model only: no tolerances, fabrication detail or TRL 4 work. `trl` stays 3 in `project.yaml`, and TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: kit 1.7.0, design for construction and the prototype build plan

Amish approved the build plan format on 2026-09-30 and asked for it across all repos, with outstanding decisions kept in a separate register. This session installed kit 1.7.0, made the PicoFlow design constructable and wrote the illustrated build plan. Nothing was built; TRL stays 3.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- `cad/src/model.py` rewritten as separate components (frame, tie rods, housing, nozzles, gaskets, inserts, lid, bearing units, sleeves, V-ring, shaft, hub, runner, guard, posts, plate, coupling, generator, pipework, valve and fittings, stands, forebay, equipment post, electrics and every fixing) with 69 constructability checks (`python cad/src/model.py --check`, all pass) and a clean all-pairs overlap scan. STEP and STL re-exported, including the nozzle, insert pair and saddle gaskets for printing and cutting.
- `docs/decisions/0003-design-for-construction.md` (PCF-DDR-003 v0.1, Draft): every change, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `docs/05-build-plan.md` (PCF-BLD-001 v0.1) and `cad/src/build_plan_media.py`: overview, 14 making sketches (PCF-DWG-101 to 114), 12 joint close-ups, 19 step pictures, a lid hole layout, a full-size nozzle hole template (PNG and PDF) and a block wiring diagram.
- `docs/06-design-decisions.md` (PCF-DEC-001 v0.1): open decisions, items to confirm when parts are bought, value engineering and decisions made.
- `docs/04-calcs/sizing.py` and PCF-CAL-001 v0.3, PCF-REQ-001 v0.5, PCF-PRC-001 v0.5, `bom/bom.csv` (lines 2, 3, 7, 8, 10, 11, 12 respecified; lines 18 and 19 added), `bom/bom-notes.md`, PCF-DWG-001 Rev P3, concept media regenerated, `project.yaml` (`design_state: constructable`, evidence), README (links line and "Building the prototype").

### Design changes made for construction (PCF-DDR-003)

| # | Change |
| --- | --- |
| P1 | Frame: a 380 mm welded square of 40 x 40 x 4 mm angle (was a 420 mm massing frame the housing did not rest on), with legs, foot plates, anchors and pipe stops |
| P2 | Four M10 tie rods clamp lid, housing and frame; a groove under the lid locates the housing (housing cut to 303 mm) |
| P3 | Two UCF204-class flange bearing units on spacer sleeves, bolted through the lid, and a V-ring seal, in place of an unmachinable bearing housing |
| P4 | Runner fixed by a bought clamping hub and four M5 screws into heat-set inserts |
| P5 | Printed nozzles with a horizontal spigot, a 20 degree bend and a gasketed saddle bolted to the housing; wall holes cut from a template; flexible couplings to the pipe |
| P6 | Nozzle exit moved from 85 to 115 mm before the strike point and the runner lowered 11 mm, so the runner lifts out past the nozzle tips; nozzle height unchanged at 280 mm |
| P7 | Generator sits on its plate, four M6 screws (was floating 5 mm above it) |
| P8 | Posts are 20 x 2 mm tubes on M10 rods, moved to 125 mm so the washers clear the housing |
| P9 | Guard is a 160 mm PVC pipe in a groove on the lid, covering both bearings and the coupling |
| P10 | Penstock on the jet 2 line into the run of a 125 x 90 reducing tee; standard fittings with socket depths allowed for; jet 1's far corner moved from 330 to 460 mm |
| P11 | Reducer, expander and nipples join the 90 mm valve into the 125 mm line; their loss is now in the calculation |
| P12 | Three pipe stands (new BOM line 18) |
| P13 | Forebay tank connector and screen frame |
| P14 | Fixings listed (new BOM line 19); generator plate 8 mm, foot plates 5 mm and post tube 20 x 2 mm to keep R14 |

### Key results (PCF-CAL-001 v0.3)

- Design point: 82.5 W into the battery with the 34 mm inserts (was 33 mm), 81.7 W at exactly 10 L/s, 41.4 % water to wire, 1.98 kWh a day. Pipe, valve and branch loss 20.3 % of head (17.0 % in v0.2, which took the valve as full bore). **The margin on R3 is now 1.7 W.**
- Clamped bus 38.7 V at most (R8); surge peak 33.4 kPa (R17); bearing L10 8.0 x 10^6 h; turbine unit 24.5 kg with fixings (R14, 0.5 kg margin).
- Requirements: none not met, R12 at risk, R7, R11, R16 not verifiable at TRL 3, 12 met, and R15 reported against its value-engineering target: USD 534, USD 84 over the USD 450 target (USD 464 with a salvaged motor).

### Proposed, awaiting Amish

All listed in `docs/06-design-decisions.md`: accept PCF-DDR-003 (recommended); inlet valve bore N6, now quantified (full bore gives 85.6 W; recommended); welded frame (recommended); O1 site and partner; and the four appearance items from the 2026-09-26 render session (split housing, inspection window, clear guard, render layout).

### Safety

No safety requirement changed status. The build plan carries safety stops S1 to S7 (stream work, lid and plate closure, wiring, first water, opening for service). The clamp margin below its 40 V release is now 1.3 V in the worst case.

### Stale outputs

The design changed visibly (frame, bearings, guard, nozzles, pipework). The photoreal renders `media/render-*.png`, `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept and need regenerating on Amish's Mac. The `render-*.png` files are not in this cloud copy, so the README hero and render links point at files made there.

### Recommended next step

Amish reviews PCF-DDR-003 and decides the open items in PCF-DEC-001, starting with the valve bore. Then refresh the product renders on the Mac. TRL 4 (building and testing to this plan) stays on hold.

## Session 2026-10-01: inlet valve bore decided (full bore)

Amish decided open decision 2 of the design decisions register (inlet valve bore, N6) on 2026-10-01. He was told the R3 output margin had dropped to 1.7 W and that the recommendation was a full-bore inlet valve, and replied: "picoflow - i agree with the recommendation". Option (a) is now the design: a full-bore valve matched to the 125 mm penstock, re-priced. Only this item is decided; acceptance of PCF-DDR-003 (A1), the welded frame and the other open items stay open. Nothing was built; TRL stays 3.

### What was done

- `cad/src/model.py`: the 90 mm gate valve, reducer, expander and nipples are replaced by a full-bore 125 mm PVC-U gate valve with solvent-weld sockets for 125 mm pipe (assumed type, catalogue class, to confirm: PN10, multi-turn handwheel with a non-rising stem, 330 mm over the sockets, 70 mm deep sockets, 200 mm handwheel about 300 mm above the pipe centre line, about 5.5 kg). It sits 60 mm clear of the tee, joined to it by a 175 mm piece of the penstock pipe; the penstock goes straight into its upstream socket. Five checks added (pipe piece in the tee and the valve, penstock in the valve, valve clear of the tee and of the pad): 74 of 74 pass. STEP and STL re-exported. The five 90 mm branch cut lengths are unchanged; the new cut length is the 175 mm pipe piece.
- `docs/04-calcs/sizing.py` and PCF-CAL-001 v0.4: valve loss coefficient 0.15 on the penstock velocity head (the v0.3 90 mm arrangement is kept as a printed comparison); the design insert is now read from the model (34 mm) rather than rounded from the exact bore, which with the full-bore valve is 33.3 mm; the clamp check now uses the 8.2 Ω resistor in the BOM and also reports the largest E12 value that keeps the clamp cycling. Every number rerun.
- `bom/bom.csv` line 8 and `bom/bom-notes.md`: re-priced with a stated basis (below).
- PCF-REQ-001 v0.6, PCF-PRC-001 v0.6 (`docs/02-concept.md`) and `README.md`: figures updated.
- PCF-BLD-001 v0.2 (`docs/05-build-plan.md`): change table row, section 3.14 rewritten as "Inlet valve and its pipe piece" with a new joint picture (Figure 28, `joint-13.png`; later figures renumbered), the bought-parts list, step 17, pipework dry fit wording, cost line and "Where the numbers come from".
- Pictures regenerated with `cad/src/build_plan_media.py`: `docs/05-build-plan/overview.png`, `step-17.png`, new `joint-13.png`, and `cad/drawings/PCF-DWG-112` (the pipework sketch shows the valve and its note now names the pipe piece). The script gained `STEPS` and `JOINTS` filters, like the existing `SHEETS`, so one picture can be redrawn. No other joint or step picture shows the valve.
- PCF-DWG-001 moved to Rev P4 (parts list item 8: "Inlet gate valve, 125 mm full bore"). Concept media regenerated (`media/hero.png`, `concept-blueprint`, `cutaway.png`, `exploded.png`, `flow.png`, `model.glb`).
- PCF-DEC-001 v0.2: item 2 moved to Decisions made (2026-10-01, Amish's words, record PCF-DDR-003 A2); open items renumbered 1 to 7; a new proposed item 8 (clamp resistor, below); item 6 to confirm now covers the full-bore valve; Value engineering updated. PCF-DDR-003 v0.2 records that Amish accepted A2 (a) on 2026-10-01; A1 and A3 stay open.

### Key results (PCF-CAL-001 v0.4)

- Valve loss 0.007 m at the design point (0.081 m with the 90 mm valve and its fittings).
- **R3: 85.6 W into the battery at exactly 10 L/s, a 5.6 W margin (was 81.7 W and 1.7 W).** With the 34 mm design inserts: 87.8 W at 10.36 L/s. Water to wire 43.6 % at 10 L/s (43.2 % with the inserts); 2.05 kWh a day at 10 L/s. Pipe, valve and branch loss 16.3 % at 10 L/s.
- R4 26.8 W; surge peak 33.5 kPa (R17); bearing L10 7.1 x 10^6 h; dump load margin 1.64 times (R7).
- Mass (R14): turbine unit unchanged at 24.5 kg. The pipework carried separately is now 9.8 kg (was 6.3 kg), of which the valve is about 5.5 kg, well under the 15 kg heaviest-item limit; all items together 34.3 kg.
- Cost (R15): Value-engineering target: USD 450. Estimated cost of the constructable design: USD 614 (USD 164 over the target). USD 544 with a salvaged motor (USD 94 over).
- Price basis for line 8 (USD 120, was USD 40): an estimate, not a quote. Full-bore PVC-U gate valves with socket ends are made up to DN300 (for example Petron Thermoplast, PN10, handwheel), but no published price was found for the 125 mm size; US-made 4 in PVC gate valves list at over USD 1,000 (Spears 2022-040, USD 1,700.91 at pvcfittingsonline.com, read 2026-10-01). USD 115 is assumed for an imported metric valve plus USD 5 for the pipe piece and cement. The line must be quoted; it is now the largest line in the kit.
- Requirements: none not met, R12 at risk, R7, R11 and R16 not verifiable at TRL 3, 12 met, R15 USD 164 over its value-engineering target.

### Proposed, awaiting Amish

- **New, register item 8: clamp resistor.** The full-bore valve delivers more power at the worst-case site (3.0 m, 15 L/s: 247 W at the shaft). With the 8.2 Ω clamp resistor the bus now settles at 40.1 V, 0.1 V above the clamp's 40 V release point, so in that case the clamp stays switched in instead of cycling. The bus still never exceeds 48 V, so R8 is met. Options: (a) keep 8.2 Ω, 300 W; (b) 6.8 Ω, which settles at 36.7 V but needs a 350 W or larger rating (339 W at 48 V). Recommendation (b). Not changed in the BOM or the wiring picture until Amish decides.
- Unchanged: accept PCF-DDR-003 (A1), welded frame, site and partner, and the appearance items.

### Safety

No safety requirement changed status. The valve is still multi-turn (never quarter-turn), so R17 holds at 33.5 kPa; the build plan's safety stops are unchanged. The clamp's margin below its release point is gone in the worst case (see item 8 above); the 48 V ceiling and the 100 V enclosure are unaffected.

### Found, not changed

- `bom/bom.csv` line 7 still says "a pair of printed 33 mm inserts", while the model, the calculation and the build plan use 34 mm. Worth correcting with the next BOM edit.

### Stale outputs

The valve is visible in all three photoreal renders: `media/render-hero.png` (penstock and gate valve from the back left), `media/render-exploded.png` (gate valve listed) and `media/render-detail.png` may show it at the left edge. They, `media/card.png` and `media/social-preview.png` still show the earlier valve and need regenerating on Amish's Mac; `cad/src/product_model.py` draws its own gate valve and still sizes it as before (it reads only the valve position from the model).

### Recommended next step

Amish decides register item 8 (clamp resistor) and the other open items, starting with acceptance of PCF-DDR-003. A real quote for the 125 mm gate valve would firm up the cost. Then refresh the product renders on the Mac. TRL 4 stays on hold.

## Session 2026-10-01: clamp resistor decided (6.8 Ω, 350 W)

Amish, 2026-10-01: "I approve of your recommendations for PicoFlow and GravitySort". For PicoFlow this answers open item 8 of the design decisions register (PCF-DEC-001 v0.2), the clamp resistor, whose recommendation was option (b). Only this item is decided; acceptance of PCF-DDR-003 (A1), the welded frame and the other open items stay open. Nothing was built; trl stays 3.

### Accepted, as recommended

| Register item (v0.2) | Decision |
| --- | --- |
| 8 | Clamp resistor: a 6.8 Ω aluminium-clad resistor rated 350 W or more replaces the 8.2 Ω, 300 W one, so the clamp keeps a margin below its 40 V release point in the worst case |

### What changed

- `docs/06-design-decisions.md` (PCF-DEC-001 v0.3): item 8 moved to Decisions made, dated 2026-10-01, with Amish's words and the record (PCF-CAL-001 v0.5, section 6); it was the last open item, so items 1 to 7 keep their numbers. Value engineering updated: USD 618 (USD 168 over the target), USD 548 with a salvaged motor (USD 98 over), and the line 15 change named.
- `docs/04-calcs/sizing.py`: clamp resistor 6.8 Ω (was 8.2 Ω) and its 350 W rating added, with the rating and the release margin printed; rerun, `docs/04-calcs/results.json` rewritten. PCF-CAL-001 v0.5 (`docs/04-calcs/01-sizing.md`): summary, R8 and R15 rows, section 6 (clamp) and section 11 (cost) rewritten; a note under the history table says what v0.5 changed.
- `bom/bom.csv` line 15: 6.8 ohm, 350 W (or higher rated) aluminium-clad clamp resistor; re-priced from USD 28 to USD 32 (+USD 4, indicative, to be quoted). `bom/bom-notes.md`: totals and a paragraph on the change.
- `docs/05-build-plan.md` (PCF-BLD-001 v0.3): the voltage clamp and resistor rows of section 3.16, wiring item 3 and the parts cost (USD 618); "Where the numbers come from" points at PCF-CAL-001 v0.5 and PCF-REQ-001 v0.7.
- `docs/05-build-plan/wiring.png` (Figure 31) regenerated with `cad/src/build_plan_media.py wiring`: the resistor guard now reads "6.8 ohm 350 W clamp (DC bus)" and the clamp wire "to the 6.8 ohm clamp resistor". Checked by eye: labels readable, nothing overlapping.
- `docs/02-concept.md` (PCF-PRC-001 v0.7): controller description, component table line 15, runaway paragraph, cost table and the heat safety note (350 W clamp resistor).
- `docs/03-requirements.md` (PCF-REQ-001 v0.7): R8 and R15 status and notes.
- `README.md`: parts list and kit cost.
- Concept media regenerated (`media/concept-blueprint.*` carries the kit cost; `hero.png`, `cutaway.png`, `exploded.png`, `flow.png`, `model.glb`); no geometry changed.
- PDFs regenerated with `python3 .kit/render.py`.

### Consistency fix

`bom/bom.csv` line 7 said "a pair of printed 33 mm inserts" and "two 33 mm inserts at the design point", while the model, PCF-CAL-001 and the build plan use 34 mm (flagged under "Found, not changed" in the previous session). Both now say 34 mm. No price change.

### Key results (PCF-CAL-001 v0.5)

| Quantity | 8.2 Ω, 300 W (v0.4) | 6.8 Ω, 350 W (v0.5) |
| --- | --- | --- |
| Worst-case clamped bus (3.0 m, 15 L/s) | 40.1 V, 0.1 V above the 40 V release | 36.7 V, 3.3 V below the release |
| Clamped runner speed | 456 rpm | 426 rpm |
| Dissipation at equilibrium | 196 W | 198 W |
| Dissipation at the 48 V switch-on point | 281 W (300 W rating) | 339 W (350 W rating, 3 % margin) |
| Kit cost, new generator | USD 614 (USD 164 over the USD 450 target) | USD 618 (USD 168 over) |
| Kit cost, salvaged motor | USD 544 (USD 94 over) | USD 548 (USD 98 over) |

6.8 Ω is the largest E12 value that keeps the worst-case equilibrium below the release point. R8 stays met by calculation; no requirement changed status: none not met, R12 at risk, R7, R11 and R16 not verifiable at TRL 3, 12 met, R15 reported against its value-engineering target.

### Still open (PCF-DEC-001)

1. Accept the design-for-construction changes (PCF-DDR-003, A1).
2. Frame welded or bolted (A3).
3. First site type, region and co-design partner.
4. Split housing for runner inspection.
5. Clear inspection window in the housing.
6. Guard material.
7. Render layout choices.

### Safety

The clamp now cycles as designed in the worst case instead of staying switched in. The resistor runs close to its rating for the moment after switch-on (339 W in a 350 W part), so it must sit on its heat sink inside the vented guard; a 500 W part would give more margin if 350 W aluminium-clad resistors are not stocked. The 48 V ceiling, the 100 V enclosure and the double-fault case (about 80 V) are unchanged.

### Found, not changed

`cad/src/product_model.py` still names the nozzle insert "33 mm" in its part list; it affects only the photoreal render labels and is left for the next render refresh on the Mac.

### Recommended next step

Amish decides the remaining open items, starting with acceptance of PCF-DDR-003 (A1). Quotes for the 125 mm gate valve and the 6.8 Ω, 350 W clamp resistor would firm up the cost. Then refresh the product renders on the Mac. TRL 4 stays on hold.
