"""PicoFlow drawing sheets.

Run from the repo root:  python cad/src/sheets.py
Builds PCF-DWG-001 (turbine unit general arrangement, Rev P5) in cad/drawings/ from
cad/src/model.py. PCF-DWG-010 is the concept sheet made by cad/src/concept_media.py.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad" / "src"))
from drawing import Sheet, project_views  # noqa: E402
import model  # noqa: E402

p = model.build_parts()["_p"]
C = json.loads((ROOT / "docs" / "04-calcs" / "results.json").read_text())
asm = model.build()
work = ROOT / "cad" / "drawings" / "_views"
views = project_views(asm, work)

s = Sheet(project="PicoFlow", title="Turbine unit general arrangement", dwg_no="PCF-DWG-001", rev="P5",
          author="Amish Chadha", date="2026-10-02", scale=None, concept=True,
          material="Runner and nozzles PETG; housing PVC SN4; lid HDPE; frame steel, galvanized or painted after welding. PRELIMINARY, NOT FOR FABRICATION",
          revisions=[("P1", "General arrangement for TRL 3 (PCF-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Penstock 125 mm, 33 mm inserts (PCF-DDR-002)", "2026-09-25", "AC"),
                     ("P3", "Design for construction (PCF-DDR-003)", "2026-10-01", "AC"),
                     ("P4", "Full-bore 125 mm inlet valve (PCF-DDR-003, A2)", "2026-10-01", "AC"),
                     ("P5", "Frame steel welded bare, then galvanized or painted (2026-10-02)", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 38, 140, 72, label="Isometric view", sublabel="Not to scale; penstock shown as a stub")
s.add_notes("Main dimensions (mm), Z from normal tailwater", [
    f"Nozzle centerline {p['jet_z']:.0f} above tailwater (R13: 300 max)",
    f"Runner {p['runner_od']:.0f} OD, {p['runner_pcd']:.0f} pitch dia., {p['n_buckets']} buckets, mid-plane {p['runner_z']:.0f}",
    f"Runner underside {p['runner_bottom']:.0f}; housing {p['housing_od']:.0f} OD x {p['housing_h']:.0f}, bottom at {p['housing_z0']:.0f}",
    f"Two jets, {C['d_insert']} mm inserts (20 to 45 range), {p['jet_angle']:.0f} deg below runner plane",
    f"Jets strike the pitch circle at +Y and -Y, opposed",
    f"Shaft {p['shaft_d']:.0f} dia. x {p['shaft_len']:.0f}; two UCF204 units on the lid at {p['bh_z0']:.0f}",
    f"Generator {p['gen_d']:.0f} dia. x {p['gen_h']:.0f} on plate at {p['plate_z0']:.0f}",
    f"Penstock {p['penstock_od']:.0f} OD at Y {p['pen_y']:.0f}; branches {p['branch_od']:.0f} OD at Z {p['manifold_z']:.0f}",
    f"Lid {p['lid']:.0f} sq. x {p['lid_t']:.0f}; frame {p['frame']:.0f} sq., 4 tie rods",
], x=276, y=126, width=140)
s.add_notes("Parts list (items match bom/bom.csv)", [
    "1 Turgo runner, printed",
    "2 Shaft and hub",
    "3 Bearing units, posts, plate, guard",
    "4 Jaw coupling",
    "5 Generator, low-speed BLDC",
    "6 Housing and lid",
], x=20, y=222, width=100)
s.add_notes("Parts list, continued", [
    "7 Manifold, two nozzles",
    "8 Inlet gate valve, 125 mm full bore",
    "9 Penstock (stub shown)",
    "11 Turbine frame",
    "18 Pipe stands; 19 Fixings",
    "Items 10, 12 to 17 not shown",
    "Guard the coupling; DC side 100 V",
], x=124, y=222, width=100)
s.save(ROOT / "cad" / "drawings" / "PCF-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("Wrote cad/drawings/PCF-DWG-001.svg, .pdf and .png")
