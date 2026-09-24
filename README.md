# PicoFlow

**Area:** CleanTech · **Status:** Concept · **Prototype budget:** about $350 USD · **Difficulty:** 3 of 5

3D-printed Turgo runner in a printed or PVC nozzle housing, driving an off-the-shelf BLDC motor used as a generator, with an MPPT dump-load controller.

## Problem

Remote homes near streams with 1 to 3 m of head have no simple turbine option.

## Concept

3D-printed Turgo runner in a printed or PVC nozzle housing, driving an off-the-shelf BLDC motor used as a generator, with an MPPT dump-load controller.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- PETG or nylon Turgo runner
- 500 W BLDC motor as generator
- Sealed bearings
- PVC penstock and nozzle
- 3-phase rectifier
- Dump-load resistor
- Charge controller board

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
