---
doc_id: PCF-PRB-001
title: PicoFlow problem statement
project: PicoFlow
doc_type: Problem statement
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (users, site context, constraints, out of scope, prior work with sources)
---

# PicoFlow problem statement

Homes near small streams with only 1 to 3 m of usable drop have water running past them all day and night, yet the turbines they can buy for that head are either cheap closed units that wear out in two or three years or professional machines that cost several times a household's budget. PicoFlow aims to be an open, printable, repairable pico hydro turbine for 1 to 3 m of head that charges a household battery with roughly 30 to 165 W, around the clock.

## The problem

About 666 million people had no electricity in 2023, and 85 % of them live in sub-Saharan Africa ([World Bank, Tracking SDG 7: The Energy Progress Report 2025](https://www.worldbank.org/en/topic/energy/publication/tracking-sdg-7-the-energy-progress-report-2025)). Many live in hilly, well-watered areas where a stream passes close to the house. Pico hydro, meaning hydro generation under 5 kW ([Wikipedia, Pico hydro](https://en.wikipedia.org/wiki/Pico_hydro)), turns that stream into continuous power: unlike solar, it runs 24 hours a day, so 90 W of hydro delivers about as much daily energy as 500 to 650 W of solar panels (estimate, see PCF-PRC-001).

The difficulty is head. Most small streams offer a drop of only 1 to 5 m over a practical pipe length, and low-head sites are by far the most common kind ([DFID project R8150, Vietnam country report](https://assets.publishing.service.gov.uk/media/57a08cf340f0b652dd001676/R8150-Vietnam.pdf)). Turbines for that range fall into two groups:

1. **Cheap closed units.** In Vietnam alone, 100,000 to 120,000 low-head propeller units were sold over 10 to 15 years at $20 to $30 for 100 W, but only about 30,000 were still running, because most become unusable after 2 to 3 years. Lower bearings, generator windings and seals fail, and a year of repairs on a 100 W unit costs about as much as the unit ([DFID R8150](https://assets.publishing.service.gov.uk/media/57a08cf340f0b652dd001676/R8150-Vietnam.pdf)). The bearings and generator sit in or near the water, which is the root of the failures.
2. **Durable commercial units.** Well-engineered pico turbines exist for this range, for example the PowerSpout LH propeller turbine for 1 to 5 m of head and 14 to 55 L/s ([PowerSpout LH](https://www.powerspout.com/pages/low-head-lh-info)) and the PowerSpout TRG Turgo for 2 to 30 m and 8 to 16 L/s ([PowerSpout TRG](https://www.powerspout.com/pages/turgo-trg-info)). They are sound machines but are priced and shipped for well-off off-grid owners, and their parts come from one supplier.

The gap is a turbine for 1 to 3 m of head and 5 to 15 L/s that is cheap enough for a household, keeps its bearings and generator out of the water, and can be built and repaired from printed parts and generic components.

Research shows the technical route exists. A single-jet Turgo turbine, normally a medium- to high-head machine, reached 91 % jet-to-mechanical efficiency at 3.5 m of head and 87 % at 1.0 m in laboratory tests at the University of Bristol ([Williamson, Stark and Booker, "Performance of a low-head pico-hydro Turgo turbine," Applied Energy 102 (2013)](https://research-information.bris.ac.uk/en/publications/performance-of-a-low-head-pico-hydro-turgo-turbine)). The same group designs its low-head Turgo to be made "in rural workshops with a minimal amount of tooling" ([University of Bristol, Pico hydropower](https://www.bristol.ac.uk/research/groups/em/electromechanical-power-conversion/pico-hydropower/)). What is missing is an open reference design that a household or local workshop can build with a 3D printer, PVC pipe and an off-the-shelf motor.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Off-grid household near a stream | Lights, phone charging, radio, a small TV or fridge, all day and night | Stream within 50 m of the house; 1 to 3 m of drop available over 10 to 30 m of pipe |
| Local technician or workshop | Build, install and repair the turbine with local tools and parts, and earn from it | 3D printer or access to one; hand tools; PVC plumbing and electrical parts from town |
| Small institution (clinic, school, farm) | A second, continuous source beside solar, especially in the rainy season when solar is weakest | Existing battery bank, possibly 12 V or 24 V |
| Hobbyist or educator | An inspectable, measurable turbine for teaching fluid machinery and power electronics | Workshop or lab with a hose or a garden stream |

### Operating environment

- **Site:** a small stream, irrigation channel or spring outflow; a weir, rock step or pipe run providing 1 to 3 m of gross head; tailrace returning the water to the same stream.
- **Water:** 5 to 15 L/s available through the turbine, with seasonal variation of perhaps 3 to 1 between wet and dry seasons (estimate; site-dependent); leaves, sand and small stones in the flow; floods several times a year.
- **Climate:** 0 to 40 °C ambient, constant spray and humidity at the turbine, sun and UV on exposed parts.
- **Duty:** continuous, 24 hours a day, often unattended for weeks.
- **Load:** a household battery (commonly 12 V) feeding LED lights and small DC or inverter loads.

## Constraints

- Garage-buildable prototype, about $350 USD for the turbine kit. The penstock and the battery are site- and household-specific and are costed separately (see `bom/bom-notes.md`).
- Runner and nozzles 3D-printed on a common desktop printer (build volume about 220 x 220 x 250 mm).
- Generator is an off-the-shelf brushless DC (BLDC) motor used as a generator; no custom windings.
- Bearings and generator kept out of the water and the spray.
- Low voltage only (12 V battery system); no mains voltage in the kit.
- Water is diverted briefly and returned to the same stream; local water-use and environmental rules apply and are site-specific.

## Out of scope

- Heads above about 5 m (conventional Turgo and Pelton designs already serve these).
- Mini-grids and multi-turbine networks (a possible later step; the Bristol group has worked on networking identical units).
- Grid-tie inverters and AC mains output.
- Civil works beyond a simple forebay, screen and pipe support.
- The household battery and inverter, which are specified but not designed here.

## Prior work

- **Low-head Turgo research.** Williamson, Stark and Booker tested a single-jet Turgo at 1.0 to 3.5 m of head and reached 87 to 91 % jet-to-mechanical efficiency ([Applied Energy, 2013](https://research-information.bris.ac.uk/en/publications/performance-of-a-low-head-pico-hydro-turgo-turbine)). Benzon, Aggidis and Anagnostopoulos review how the Turgo carries more flow than a Pelton through the same nozzle and spear system ([Applied Energy 166 (2016)](https://ideas.repec.org/a/eee/appene/v166y2016icp1-18.html)).
- **Commercial pico Turgo.** PowerSpout sells a Turgo turbine for 2 to 30 m of head ([PowerSpout TRG](https://www.powerspout.com/pages/turgo-trg-info)) and a separate DIY Turgo rotor, 180 mm outside diameter with a 90 mm running diameter, jets up to 25 mm and a glass-filled nylon body ([PowerSpout DIY Turgo rotor](https://www.powerspout.com/products/diy-turgo-rotor)). That rotor is designed to fit Smart Drive permanent magnet generators, which are direct-drive washing machine motors; this shows a salvaged low-speed BLDC can serve as a hydro generator.
- **Low-head propeller units.** Cheap propeller units dominate the low-head market in Southeast Asia but have short lives ([DFID R8150](https://assets.publishing.service.gov.uk/media/57a08cf340f0b652dd001676/R8150-Vietnam.pdf)); durable propeller units such as the PowerSpout LH exist at higher cost ([PowerSpout LH](https://www.powerspout.com/pages/low-head-lh-info)).
- **Community pico hydro.** Pico hydro schemes of 1.1 and 2.2 kW in Kenya have powered whole villages ([Wikipedia, Pico hydro](https://en.wikipedia.org/wiki/Pico_hydro)), which shows the social value of continuous small hydro.

## Open questions

- Which first site type and region: a household stream in East Africa, a hill farm in Southeast Asia, or a teaching rig? Proposed, awaiting Amish.
- How common are 1 to 3 m sites with 5 to 15 L/s in the dry season, compared with the larger flows propeller turbines need? This sets whether a Turgo or a propeller is the better low-head choice for the target users.
- Are 12 V household batteries the norm, or should the kit charge 24 V? Proposed, awaiting Amish (see PCF-PRC-001).
- Which water-use and fisheries rules apply to small diversions in the first target country?
