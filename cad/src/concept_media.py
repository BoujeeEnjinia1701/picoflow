"""PicoFlow concept media from the TRL 3 parametric model.

Run from the repo root:  python cad/src/concept_media.py
The turbine unit comes from cad/src/model.py; the site (weir, forebay, penstock run) and the
electrics are drawn here. Flow values and key figures are read from docs/04-calcs/results.json,
written by docs/04-calcs/sizing.py (PCF-CAL-001). Not for fabrication.

Coordinates in mm. Z up, normal tailwater at Z = 0. The turbine axis is vertical at X = Y = 0.
The weir is set so the forebay water surface is 2.0 m above the nozzle centerline (the design point).
Site parts (weir) are grey and carry no BOM number.
"""
import json
import math
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Cylinder, Pos, Rot, Vector
from concept import Part, render_all, _render
import model

P = model.build_parts()
p = P["_p"]
C = json.loads((ROOT / "docs" / "04-calcs" / "results.json").read_text())
tube3, unite = model._tube, model._unite

KIT = "#0F766E"
PIPE_R = p["penstock_od"] / 2
MZ = p["manifold_z"]
FB_WATER = 350.0                                   # forebay water surface above the weir top
WEIR_TOP = p["jet_z"] + 2000.0 - FB_WATER          # 2.0 m gross head to the nozzle centerline
WEIR_X0, WEIR_X1 = -1750.0, -1300.0

# ---------------- site (grey, not in kit) ----------------
weir = Pos((WEIR_X0 + WEIR_X1) / 2, p["pen_y"], WEIR_TOP / 2) * Box(WEIR_X1 - WEIR_X0, 1000, WEIR_TOP)

# ---------------- 9 Penstock (shortened for the figure) with a support ----------------
PY = p["pen_y"]
elbow = (p["stub_x"], PY, MZ)
top = (WEIR_X1 + 20, PY, WEIR_TOP + 110)
penstock = (tube3(elbow, top, PIPE_R) + P["penstock_stub"] + Pos(*elbow) * Cylinder(PIPE_R + 6, 2 * PIPE_R + 12))
mid = tuple((e + t) / 2 for e, t in zip(elbow, top))
ang = 90 - math.degrees(math.atan2(top[2] - elbow[2], top[0] - elbow[0]))
penstock = (penstock + tube3((mid[0], PY, 0), (mid[0], PY, mid[2] - PIPE_R), 20)
            + Pos(mid[0], PY, mid[2]) * Rot(0, ang, 0) * (Cylinder(PIPE_R + 10, 40) - Cylinder(PIPE_R, 42)))

# ---------------- 10 Forebay and intake screen ----------------
fb = Pos(WEIR_X1 - 230, PY, WEIR_TOP + 200) * (Box(460, 560, 400) - Pos(0, 0, 10) * Box(430, 530, 400))
screen = Pos(WEIR_X1 - 230, PY, WEIR_TOP + 395) * Box(440, 540, 10)
forebay = fb + screen

# ---------------- 12 Equipment post, 13 rectifier, 14 controller, 15 dump load and clamp ----------------
POST = (700.0, -450.0)
post = Pos(POST[0], POST[1], 700) * Box(60, 60, 1400) + Pos(POST[0], POST[1], 20) * Box(300, 300, 40)
rectifier = Pos(POST[0], POST[1] - 30 - 50, 900) * Box(130, 100, 110)
controller = Pos(POST[0], POST[1] - 30 - 55, 1130) * Box(260, 110, 200)
dump = (Pos(POST[0] + 30 + 45, POST[1], 620) * Rot(90, 0, 0) * Cylinder(40, 320)
        + unite([Pos(POST[0] + 30 + 45, POST[1] + dy, 620) * Rot(90, 0, 0) * Cylinder(62, 5) for dy in (-120, -60, 0, 60, 120)])
        + Pos(POST[0] + 30 + 45, POST[1], 400) * Box(60, 160, 40))

# ---------------- 16 Wiring, 17 battery ----------------
gz = p["gen_z0"] + 40
wiring = (tube3((p["gen_d"] / 2 - 10, -30, gz), (POST[0] - 60, -30, gz), 7)
          + tube3((POST[0] - 60, -30, gz), (POST[0] - 60, POST[1] - 80, 860), 7)
          + tube3((POST[0] + 80, POST[1] - 80, 1050), (POST[0] + 180, POST[1] - 80, 300), 7)
          + tube3((POST[0] + 180, POST[1] - 80, 300), (POST[0] + 180, -60, 240), 7))
battery = Pos(POST[0] + 180, 60, 120) * Box(340, 190, 240)

# Numbering matches bom/bom.csv
parts = [
    Part("Weir or rock step (site, not in kit)", weir, "#A8A29E", None),
    Part("Turgo runner, printed", P["runner"], KIT, 1),
    Part("Shaft and hub", P["shaft"], "#475569", 2),
    Part("Sealed bearings, housing, mount, guard", P["bearing_mount"], "#94A3B8", 3),
    Part("Jaw coupling", P["coupling"], "#D4A017", 4),
    Part("Generator, low-speed BLDC", P["generator"], "#1F2937", 5),
    Part("Housing and lid", P["housing"], "#D1D5DB", 6),
    Part("Nozzle manifold, two nozzles", P["manifold"], "#2563EB", 7),
    Part("Inlet gate valve", P["valve"], "#DC2626", 8),
    Part("Penstock, 125 mm PVC (site-dependent)", penstock, "#E5E7EB", 9),
    Part("Forebay and intake screen", forebay, "#0EA5E9", 10),
    Part("Turbine frame", P["frame"], "#A16207", 11),
    Part("Equipment post", post, "#92400E", 12),
    Part("Three-phase rectifier", rectifier, "#7C3AED", 13),
    Part("MPPT, dump-load and clamp controller", controller, "#16A34A", 14),
    Part("Dump-load and clamp resistors", dump, "#C2410C", 15),
    Part("Wiring, fuse and isolator", wiring, "#111827", 16),
    Part("Battery, 12 V (not in kit cost)", battery, "#65A30D", 17),
    Part("Pipe stands", P["stands"], "#92400E", 18),
    Part("Fixings (tie rods, post rods, bolts)", P["fixings"], "#374151", 19),
]

r = lambda v: int(round(v))
import os
if not os.environ.get("EXPLODED_ONLY"):
  render_all(
      parts, project="PicoFlow", title="Low-head Turgo pico hydro concept", dwg_no="PCF-DWG-010",
      date="2026-09-25",
      key_figures=[f"Design point: 2 m gross head, 10 L/s, 20 m of 125 mm pipe",
                   f"Runner 200 mm OD, two {C['d_insert']} mm jets, about {r(C['rpm'])} rpm",
                   f"About {r(C['p_batt'])} W into the battery, {C['kwh_day']:.2f} kWh/day",
                   f"Pipe losses {r(C['loss_pct'])} % of head (PCF-CAL-001)",
                   f"1 to 3 m head: about {r(C['range']['1.0']['p_batt'])} to {r(C['range']['3.0']['p_batt'])} W",
                   f"Kit about ${r(C['kit'])}; value-engineering target $450"],
      cut_exclude=("Weir or rock step (site, not in kit)", "Forebay and intake screen",
                   "Penstock, 125 mm PVC (site-dependent)", "Equipment post", "Pipe stands",
                   "Three-phase rectifier", "MPPT, dump-load and clamp controller", "Dump-load and clamp resistors",
                   "Wiring, fuse and isolator", "Battery, 12 V (not in kit cost)", "Inlet gate valve"),
      flow={"title": "power flow at the design point, 2 m gross head and 10 L/s, W (estimates, PCF-CAL-001)", "unit": "W",
            "stages": [("Water, 2 m x 10 L/s", r(C["p_hyd"])), ("At the nozzles", r(C["p_noz"])), ("Jet", r(C["p_jet"])),
                       ("Runner shaft", r(C["p_shaft"])), ("Rectified DC", r(C["p_dc"])), ("Into battery", r(C["p_batt"]))],
            "losses": [(0, f"Pipe and branches ({r(C['loss_pct'])} %)", r(C["p_hyd"] - C["p_noz"])),
                       (1, "Nozzle (6 %)", r(C["p_noz"] - C["p_jet"])),
                       (2, "Runner (25 %)", r(C["p_jet"] - C["p_shaft"])),
                       (3, "Generator, rectifier", r(C["p_shaft"] - C["p_dc"])),
                       (4, "Buck converter (6 %)", r(C["p_dc"] - C["p_batt"]))]},
  )

# ---------------- exploded view (turbine and electrics; penstock shown as a short stub) ----------------
stub_dir = Vector(top[0] - elbow[0], 0, top[2] - elbow[2]).normalized()
stub_top = (elbow[0] + stub_dir.X * 600, PY, elbow[2] + stub_dir.Z * 600)
stub = tube3(elbow, stub_top, PIPE_R) + P["penstock_stub"] + Pos(*elbow) * Cylinder(PIPE_R + 6, 2 * PIPE_R + 12)
fb_ex = Pos(stub_top[0] - 300 - (WEIR_X1 - 230), 0, stub_top[2] + 250 - (WEIR_TOP + 200)) * forebay

by_bom = {q.bom: q for q in parts if q.bom}
EXPLODE = {1: (0, 0, -40), 2: (320, 0, 760), 3: (0, 0, 560), 4: (-320, 0, 820), 5: (0, 0, 1000),
           6: (0, 0, 220), 7: (0, 0, -420), 8: (-200, 0, -650), 11: (0, 0, -760),
           12: (300, 0, 0), 13: (650, -1050, -300), 14: (420, -520, 150), 15: (650, 0, 0),
           16: (500, -600, -450), 17: (700, 400, 0), 18: (0, 0, -560), 19: (0, 0, 380)}
ex_parts = []
for n in range(1, 20):
    q = by_bom[n]
    shape = {9: stub, 10: fb_ex}.get(n, q.shape)
    off = {9: (-250, 0, -900), 10: (-150, 0, -2250)}.get(n, EXPLODE.get(n, (0, 0, 0)))
    ex_parts.append(Part(q.name, shape, q.color, n, off))
_render(ex_parts, ROOT / "media" / "exploded.png", offsets=True, labels=True,
        title="PicoFlow: exploded view",
        note="Penstock (9) shown as a short stub; site weir omitted. Numbers match bom/bom.csv.")

import shutil
for d in ("_views", "_views_fig"):
    shutil.rmtree(ROOT / "media" / d, ignore_errors=True)
print("Wrote media/")
