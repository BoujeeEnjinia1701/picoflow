"""PicoFlow concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. Z up, ground and tailrace at Z = 0. The turbine axis is vertical at X = Y = 0.
Water arrives from a forebay on a 2.2 m weir or rock step at -X, drops through the penstock,
splits into two nozzles, strikes the Turgo runner from above and falls out of the open-bottomed
housing into the tailrace. The generator sits on the lid, clear of the spray.
Site parts (weir) are grey and carry no BOM number.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Cone, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, _render

# ---------------- key dimensions (concept values, proposed) ----------------
HOUSING_R = 157.5        # 315 mm PVC sewer pipe section
HOUSING_WALL = 6.0
HOUSING_Z0 = 250.0       # bottom of housing, on the frame
HOUSING_H = 300.0
LID_T = 12.0
RUNNER_OD = 200.0        # pitch diameter about 150 mm
RUNNER_Z = 385.0         # runner mid-plane
JET_Z = 440.0            # nozzle exit height (head is measured to here)
SHAFT_R = 10.0           # 20 mm stainless shaft
GEN_R, GEN_H = 100.0, 90.0

PIPE_R = 55.0            # 110 mm PVC penstock
BRANCH_R = 31.5          # 63 mm PVC branches to the nozzles
WEIR_X0, WEIR_X1, WEIR_TOP = -1550.0, -1100.0, 2200.0

HOUSING = "#D1D5DB"
KIT = "#0F766E"
PVC = "#E5E7EB"


def tube3(a, b, r):
    """Round bar or pipe between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def cone3(a, b, r1, r2):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cone(r1, r2, d.length, Plane(origin=a, z_dir=d.normalized()))


def unite(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


# ---------------- site (grey, not in kit) ----------------
weir = Pos((WEIR_X0 + WEIR_X1) / 2, 0, WEIR_TOP / 2) * Box(WEIR_X1 - WEIR_X0, 1000, WEIR_TOP)

# ---------------- 1 Turgo runner (printed) ----------------
hub = Pos(0, 0, RUNNER_Z) * Cylinder(40, 50)
rim = Pos(0, 0, RUNNER_Z - 18) * (Cylinder(RUNNER_OD / 2, 12) - Cylinder(RUNNER_OD / 2 - 8, 14))
web = Pos(0, 0, RUNNER_Z - 18) * (Cylinder(RUNNER_OD / 2 - 8, 6) - Cylinder(39, 8))
buckets = []
for k in range(20):
    th = k * 18.0
    r = 70.0
    buckets.append(Pos(r * math.cos(math.radians(th)), r * math.sin(math.radians(th)), RUNNER_Z + 2)
                   * Rot(0, 0, th) * Rot(35, 0, 0) * Box(56, 9, 34))
runner = hub + rim + web + unite(buckets)

# ---------------- 2 Shaft ----------------
shaft = Pos(0, 0, RUNNER_Z + (700 - RUNNER_Z) / 2) * Cylinder(SHAFT_R, 700 - RUNNER_Z)

# ---------------- 6 Housing and lid ----------------
lid_z = HOUSING_Z0 + HOUSING_H
housing = (Pos(0, 0, HOUSING_Z0 + HOUSING_H / 2) * (Cylinder(HOUSING_R, HOUSING_H) - Cylinder(HOUSING_R - HOUSING_WALL, HOUSING_H + 2))
           + Pos(0, 0, lid_z + LID_T / 2) * (Box(400, 400, LID_T) - Cylinder(SHAFT_R + 4, LID_T + 2)))

# ---------------- 3 Bearing housing (two sealed bearings) and motor mount ----------------
bh_z0 = lid_z + LID_T
bearing = Pos(0, 0, bh_z0 + 45) * (Cylinder(36, 90) - Cylinder(SHAFT_R, 92))
posts = unite([Pos(sx * 120, sy * 120, bh_z0 + 72.5) * Cylinder(10, 145) for sx in (-1, 1) for sy in (-1, 1)])
mount_plate = Pos(0, 0, bh_z0 + 150) * (Box(280, 280, 10) - Cylinder(30, 12))
bearing_mount = bearing + posts + mount_plate

# ---------------- 4 Coupling ----------------
coupling = Pos(0, 0, bh_z0 + 115) * Cylinder(24, 40)

# ---------------- 5 Generator (low-speed BLDC) ----------------
gen_z0 = bh_z0 + 155
generator = (Pos(0, 0, gen_z0 + GEN_H / 2) * Cylinder(GEN_R, GEN_H)
             + Pos(0, 0, gen_z0 + GEN_H + 8) * Cylinder(40, 16))

# ---------------- 7 Nozzle manifold and two nozzles ----------------
TEE_X = -340.0
branches = []
nozzles = []
for s in (-1, 1):
    a = (TEE_X, 0, JET_Z + 40)
    b = (TEE_X, s * 190, JET_Z + 40)
    c = (-215, s * 190, JET_Z + 40)
    branches += [tube3(a, b, BRANCH_R), tube3(b, c, BRANCH_R)]
    # nozzle aimed down 20 degrees at the runner pitch circle, entering the housing wall
    tip = (-100, s * 105, JET_Z - 5)
    nozzles.append(cone3(c, tip, BRANCH_R + 4, 18))
manifold = unite(branches) + unite(nozzles) + Pos(TEE_X, 0, JET_Z + 40) * Cylinder(BRANCH_R + 8, 90, rotation=(90, 0, 0))

# ---------------- 8 Inlet valve ----------------
VALVE_X = -500.0
valve = (Pos(VALVE_X, 0, JET_Z + 40) * Rot(0, 90, 0) * Cylinder(PIPE_R + 22, 70)
         + Pos(VALVE_X, 0, JET_Z + 40 + 110) * Cylinder(10, 120)
         + Pos(VALVE_X, 0, JET_Z + 40 + 175) * Box(160, 24, 14))

# ---------------- 9 Penstock (shortened for the figure) with support ----------------
elbow = (-640.0, 0.0, JET_Z + 40)
top = (WEIR_X1 + 20, 0.0, WEIR_TOP + 110)
penstock = (tube3(elbow, top, PIPE_R) + tube3((TEE_X - 20, 0, JET_Z + 40), elbow, PIPE_R)
            + Pos(*elbow) * Cylinder(PIPE_R + 6, 2 * PIPE_R + 12))
mid = tuple((e + t) / 2 for e, t in zip(elbow, top))
penstock = (penstock + tube3((mid[0], 0, 0), (mid[0], 0, mid[2] - PIPE_R), 20)
            + Pos(mid[0], 0, mid[2]) * Rot(0, 90 - math.degrees(math.atan2(top[2] - elbow[2], top[0] - elbow[0])), 0)
            * (Cylinder(PIPE_R + 10, 40) - Cylinder(PIPE_R, 42)))

# ---------------- 10 Forebay and intake screen ----------------
fb = Pos(WEIR_X1 - 230, 0, WEIR_TOP + 200) * (Box(460, 560, 400) - Pos(0, 0, 10) * Box(430, 530, 400))
screen = Pos(WEIR_X1 - 230, 0, WEIR_TOP + 395) * Box(440, 540, 10)
forebay = fb + screen

# ---------------- 11 Frame and equipment post ----------------
legs = unite([Pos(sx * 190, sy * 190, HOUSING_Z0 / 2) * Box(40, 40, HOUSING_Z0) for sx in (-1, 1) for sy in (-1, 1)])
ring = (Pos(0, 0, HOUSING_Z0 - 15) * (Box(420, 420, 30) - Box(340, 340, 32)))
POST = (620.0, -300.0)
post = Pos(POST[0], POST[1], 700) * Box(60, 60, 1400) + Pos(POST[0], POST[1], 20) * Box(300, 300, 40)
frame = legs + ring

# ---------------- 12 Rectifier, 13 controller, 14 dump load ----------------
rectifier = Pos(POST[0], POST[1] - 30 - 50, 900) * Box(130, 100, 110)
controller = Pos(POST[0], POST[1] - 30 - 55, 1130) * Box(260, 110, 200)
dump = (Pos(POST[0] + 30 + 45, POST[1], 620) * Rot(90, 0, 0) * Cylinder(40, 320)
        + unite([Pos(POST[0] + 30 + 45, POST[1] + dy, 620) * Rot(90, 0, 0) * Cylinder(62, 5) for dy in (-120, -60, 0, 60, 120)]))

# ---------------- 15 Wiring, 16 battery ----------------
wiring = (tube3((GEN_R - 10, -30, gen_z0 + 40), (POST[0] - 60, -30, gen_z0 + 40), 7)
          + tube3((POST[0] - 60, -30, gen_z0 + 40), (POST[0] - 60, POST[1] - 80, 860), 7)
          + tube3((POST[0] + 80, POST[1] - 80, 1050), (POST[0] + 180, POST[1] - 80, 300), 7)
          + tube3((POST[0] + 180, POST[1] - 80, 300), (POST[0] + 180, 180, 240), 7))
battery = Pos(POST[0] + 150, 280, 120) * Box(340, 190, 240)

# Numbering matches bom/bom.csv
parts = [
    Part("Weir or rock step (site, not in kit)", weir, "#A8A29E", None),
    Part("Turgo runner, printed", runner, KIT, 1),
    Part("Shaft and hub", shaft, "#475569", 2),
    Part("Sealed bearings, housing, motor mount", bearing_mount, "#94A3B8", 3),
    Part("Jaw coupling", coupling, "#D4A017", 4),
    Part("Generator, low-speed BLDC", generator, "#1F2937", 5),
    Part("Housing and lid", housing, HOUSING, 6),
    Part("Nozzle manifold, two nozzles", manifold, "#2563EB", 7),
    Part("Inlet valve", valve, "#DC2626", 8),
    Part("Penstock, 110 mm PVC (site-dependent)", penstock, PVC, 9),
    Part("Forebay and intake screen", forebay, "#0EA5E9", 10),
    Part("Turbine frame", frame, "#A16207", 11),
    Part("Equipment post", post, "#92400E", 12),
    Part("Three-phase rectifier", rectifier, "#7C3AED", 13),
    Part("MPPT and dump-load controller", controller, "#16A34A", 14),
    Part("Dump-load resistor, 300 W", dump, "#C2410C", 15),
    Part("Wiring, fuse and isolator", wiring, "#111827", 16),
    Part("Battery, 12 V (not in kit cost)", battery, "#65A30D", 17),
]

render_all(
    parts, project="PicoFlow", title="Low-head Turgo pico hydro concept", dwg_no="PCF-DWG-010",
    date="2026-09-25",
    key_figures=["Design point: 2 m gross head, 10 L/s (estimate)",
                 "Printed Turgo runner, 200 mm OD, two 33 mm jets",
                 "About 340 rpm; about 90 W into the battery (estimate)",
                 "About 2.2 kWh/day, 24 h running (estimate)",
                 "1 to 3 m head: about 30 to 165 W (estimate)",
                 "Kit about $424 new (battery, penstock excluded)"],
    cut_exclude=("Weir or rock step (site, not in kit)", "Forebay and intake screen",
                 "Penstock, 110 mm PVC (site-dependent)", "Equipment post",
                 "Three-phase rectifier", "MPPT and dump-load controller", "Dump-load resistor, 300 W",
                 "Wiring, fuse and isolator", "Battery, 12 V (not in kit cost)", "Inlet valve"),
    flow={"title": "power flow at the design point, 2 m gross head and 10 L/s, W (estimates)", "unit": "W",
          "stages": [("Water, 2 m x 10 L/s", 196), ("At the nozzles", 177), ("Jet", 166),
                     ("Runner shaft", 125), ("Generator AC", 100), ("Into battery", 90)],
          "losses": [(0, "Penstock friction (10 %)", 20), (1, "Nozzle (6 %)", 11),
                     (2, "Runner (25 %)", 41), (3, "Generator (20 %)", 25),
                     (4, "Rectifier, MPPT (10 %)", 10)]},
)

# ---------------- exploded view (turbine and electrics; penstock shown as a short stub) ----------------
# The full scene is dominated by the weir, so the exploded view leaves the site out and shows
# the penstock as a 700 mm stub with the forebay beside it.
stub_dir = Vector(top[0] - elbow[0], 0, top[2] - elbow[2]).normalized()
stub_top = (elbow[0] + stub_dir.X * 700, 0, elbow[2] + stub_dir.Z * 700)
stub = (tube3(elbow, stub_top, PIPE_R) + tube3((TEE_X - 20, 0, JET_Z + 40), elbow, PIPE_R)
        + Pos(*elbow) * Cylinder(PIPE_R + 6, 2 * PIPE_R + 12))
fb_ex = Pos(stub_top[0] - 300 - (WEIR_X1 - 230), 0, stub_top[2] + 250 - (WEIR_TOP + 200)) * forebay

by_bom = {p.bom: p for p in parts if p.bom}
EXPLODE = {1: (0, 0, 40), 2: (280, 0, 640), 3: (0, 0, 600), 4: (0, 0, 800), 5: (0, 0, 980),
           6: (0, 0, 300), 7: (-120, 0, 520), 8: (-200, 0, -780), 11: (0, 0, -380),
           12: (250, 0, 0), 13: (380, -520, -200), 14: (380, -520, 150), 15: (600, 0, 0),
           16: (450, -600, -450), 17: (650, 350, 0)}
ex_parts = []
for n in range(1, 18):
    p = by_bom[n]
    shape = {9: stub, 10: fb_ex}.get(n, p.shape)
    off = {9: (-250, 0, -1350), 10: (900, 0, -2050)}.get(n, EXPLODE.get(n, (0, 0, 0)))
    ex_parts.append(Part(p.name, shape, p.color, n, off))
_render(ex_parts, Path.cwd() / "media" / "exploded.png", offsets=True, labels=True,
        title="PicoFlow: exploded view",
        note="Penstock (9) shown as a short stub; site weir omitted. Numbers match bom/bom.csv.")
