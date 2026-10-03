"""PicoFlow product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the one-piece 315 mm PVC housing with its nozzle
entries (no window and no split, PCF-DDR-003 accepted 2026-10-02), a filleted HDPE lid, an aluminium bearing housing with
cap screws and a grease nipple, stainless posts, a filleted generator plate, a 160 mm PVC pipe coupling
guard over a two-hub jaw coupling with its elastomer spider, a finned low-speed BLDC generator
with a label band and cable gland, the 125 x 90 mm tee, 90 mm branches with socket couplers,
two printed nozzles with swappable metal inserts, a gate valve with a handwheel, a steel angle frame
(galvanized or painted after welding) on foot plates, and a vented rectifier box with a lit status light. Context is a
short section of 125 mm penstock on a pipe saddle, the concrete edges of the tailrace channel
under the frame and the tailwater surface.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, _derived() and build_parts() in model.py.
Axes as model.py: Z up, normal tailwater at Z = 0, turbine axis vertical at X = Y = 0, penstock
from -X, front is -Y. The rectifier box (BOM 13) is not in model.py; it is shown as a loose
accessory beside the unit (RECT_AT), not at its installed place on the equipment post.
See docs/REVIEW.md, session 2026-09-26, for the appearance choices that differ from model.py.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Torus, extrude, fillet)
from model import PARAMS, _derived as derived, build_parts, _tube, _cone, _unite

TITLE = "PicoFlow: pico hydro Turgo turbine with a generator on the lid"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); generator on the lid, "
             "one-piece housing, penstock and gate valve arriving from the back left "
             "over the tailrace channel"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): generator, plate and posts, "
             "jaw coupling and guard, bearing housing, shaft, lid, one-piece housing, "
             "runner, nozzles with inserts, manifold, gate valve, frame and rectifier box"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 12, "az": -78,
     "note": "Detail view from the front, slightly right and above (about 12 deg elevation): the one-piece "
             "housing, the nozzle entering at left, the frame and the pad over the tailrace"},
]

# Colours (restrained product palette; kit accent for the runner)
C_ACCENT = "#0F766E"
C_PVC = "#D9DCDF"          # grey PVC housing
C_PVC2 = "#C4C9CE"         # branch pipe and fittings
C_PENSTOCK = "#A9AFB5"
C_HDPE = "#2B2F36"         # lid
C_ALU = "#B8BEC6"
C_STEEL = "#9AA1A8"
C_GALV = "#A7AEB3"
C_DARK = "#1F2329"
C_GEN = "#30353C"
C_RUBBER = "#1C1F24"
C_SPIDER = "#C2410C"
C_NOZZLE = "#3A3F47"
C_VALVE = "#8E2424"
C_WINDOW = "#DCEBF5"
C_LABEL = "#F4F4F2"
C_LED = "#22C55E"
C_CONCRETE = "#CFCCC6"
C_WATER = "#9EC3CF"

# Appearance-only layout and detail sizes (mm)
CH_IN = 165.0              # tailrace channel inner half width (X), under the frame legs
CH_WALL = 110.0
CH_Y = 280.0               # channel half length along Y
CH_FLOOR = -150.0
WATER_Z = -20.0            # tailwater drawn just below the channel edge (appearance only)
RECT_AT = (-620.0, -380.0)  # rectifier box position for the exploded view (layout only)


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _top_edges(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom_edges(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _cyl_between(a, b, r):
    return _tube(a, b, r)


def _hex_bolt(x, y, z, af=13.0, h=6.0, washer=True, up=True):
    """Hex bolt head (or nut) sitting on a surface at z, with an optional washer."""
    s = 1 if up else -1
    head = Pos(x, y, z + s * (1.5 + h / 2)) * extrude(RegularPolygon(af / math.sqrt(3), 6), amount=h / 2, both=True)
    head = _fillet_try(head, (_top_edges(head) if up else _bottom_edges(head)), [0.8, 0.4])
    if washer:
        head += Pos(x, y, z + s * 0.75) * Cylinder(af * 0.8, 1.5)
    return head


def _housing(p):
    """One-piece 315 mm PVC housing with nozzle entries and collars (no window, no split; PCF-DDR-003, accepted 2026-10-02)."""
    Ro = p["housing_od"] / 2
    t = p["housing_wall"]
    z0, h = p["housing_z0"], p["housing_h"]
    zc = z0 + h / 2
    pipe = Pos(0, 0, zc) * (Cylinder(Ro, h) - Cylinder(Ro - t, h + 2))
    # nozzle entry holes: the two nozzles pass through the wall at about X = +-138, Y = +-75
    a = math.radians(p["jet_angle"])
    ypc = p["runner_pcd"] / 2
    for sx in (1, -1):
        ax = (sx * p["nozzle_exit_x"], sx * ypc, p["jet_z"])
        bx = (sx * (p["nozzle_exit_x"] + 260 * math.cos(a)), sx * ypc, p["jet_z"] + 260 * math.sin(a))
        pipe -= _cyl_between(ax, bx, p["branch_od"] / 2 + 2)
    # shallow raised collars top and bottom (rolled pipe ends)
    band = lambda zb: Pos(0, 0, zb) * (Cylinder(Ro + 1.5, 14) - Cylinder(Ro - 1, 16))
    pipe += band(z0 + 7) + band(z0 + h - 7)
    # maker label plate, +X side
    lab_a = math.radians(55)
    label = Pos((Ro + 0.6) * math.sin(lab_a), (Ro + 0.6) * math.cos(lab_a), z0 + 70) * Rot(0, 0, -55) * Box(90, 1.2, 36)
    label = _fillet_try(label, label.edges().filter_by(Axis.Y), [3.0, 1.5])
    return pipe, label


def _nozzles(p):
    """Printed nozzle bodies with a collar, and metal inserts at the exit, both jets."""
    a = math.radians(p["jet_angle"])
    ypc = p["runner_pcd"] / 2
    rb = p["branch_od"] / 2
    rex = p["jet_d"] / 2 + 6
    bodies, inserts = [], []
    for sx in (1, -1):
        ex, ez = p["nozzle_entry_x"], p["nozzle_entry_z"]
        entry = (sx * ex, sx * ypc, ez)
        exit_ = (sx * p["nozzle_exit_x"], sx * ypc, p["jet_z"])
        body = _cone(entry, exit_, rb + 1, rex)
        d = [(exit_[i] - entry[i]) / p["nozzle_len"] for i in range(3)]
        c0 = tuple(entry[i] + d[i] * 18 for i in range(3))
        body += _tube(entry, c0, rb + 6)
        body -= _cone(entry, exit_, rb - 4, p["jet_d"] / 2 + 3)
        ins_a = tuple(exit_[i] - d[i] * 16 for i in range(3))
        ins_b = tuple(exit_[i] + d[i] * 6 for i in range(3))
        ins = _tube(ins_a, ins_b, rex + 1) - _tube(ins_a, tuple(ins_b[i] + d[i] for i in range(3)), p["jet_d"] / 2)
        body -= _tube(ins_a, exit_, rex + 1.2)
        bodies.append(body)
        inserts.append(ins)
    return bodies, inserts


def _pipework(p):
    """Tee, 90 mm branches, elbows and socket couplers, rebuilt from the model.py route."""
    mz = p["manifold_z"]; rb = p["branch_od"] / 2; ypc = p["runner_pcd"] / 2
    ex, ez = p["nozzle_entry_x"], p["nozzle_entry_z"]
    tx, by, bx = p["tee_x"], p["branch_y"], p["branch_x"]
    runs = [((tx, 0, mz), (tx, -ypc, mz)), ((tx, -ypc, mz), (-ex, -ypc, ez)),
            ((tx, 0, mz), (tx, by, mz)), ((tx, by, mz), (bx, by, mz)),
            ((bx, by, mz), (bx, ypc, mz)), ((bx, ypc, mz), (ex, ypc, ez))]
    pipes = _unite([_tube(a, b, rb) for a, b in runs])
    corners = [(tx, -ypc, mz), (tx, by, mz), (bx, by, mz), (bx, ypc, mz)]
    elbows = []
    for c in corners:
        e = Pos(*c) * Cylinder(rb + 5, 2 * rb + 10)
        elbows.append(_fillet_try(e, e.edges(), [4.0, 2.0]))
    fittings = _unite(elbows)
    tee = Pos(tx, 0, mz) * Rot(90, 0, 0) * Cylinder(rb + 8, 2 * ypc + 30)
    tee += Pos(tx - 45, 0, mz) * Rot(0, 90, 0) * Cylinder(p["penstock_od"] / 2 + 7, 70)
    tee = _fillet_try(tee, tee.edges(), [3.0, 1.5])
    # socket couplers mid-run on the long branches
    sockets = None
    for a, b in [runs[3], runs[2]]:
        m = tuple((a[i] + b[i]) / 2 for i in range(3))
        dv = [b[i] - a[i] for i in range(3)]
        L = math.sqrt(sum(v * v for v in dv))
        u = [v / L for v in dv]
        s = _tube(tuple(m[i] - u[i] * 30 for i in range(3)), tuple(m[i] + u[i] * 30 for i in range(3)), rb + 5)
        sockets = s if sockets is None else sockets + s
    return pipes, fittings + sockets, tee


def product_parts(P=PARAMS):
    p = derived(dict(P))
    m = build_parts()
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    R = p["runner_od"] / 2
    Ro = p["housing_od"] / 2
    z_lid = p["lid_z"]; bh0 = p["bh_z0"]

    # explode stack (upward) above the housing
    E_LID, E_BH, E_GUARD, E_CPL, E_PLATE, E_GEN, E_SHAFT = 260, 330, 420, 480, 560, 700, 250

    # ---- 1 runner (printed, kit accent) and hub nut
    add("Turgo runner (printed PETG)", m["runner"], C_ACCENT, "plastic", 1, "internal", (0, 0, -300))
    nut = Pos(0, 0, p["runner_bottom"] - 4) * (extrude(RegularPolygon(17, 6), amount=4, both=True)
                                               - Cylinder(p["shaft_d"] / 2 - 2, 10))
    nut = _fillet_try(nut, _bottom_edges(nut), [1.0, 0.5])
    add("Runner clamp nut", nut, C_STEEL, "metal", 2, "internal", (0, 0, -340))

    # ---- 2 shaft
    add("Stainless shaft", m["shaft"], C_STEEL, "metal", 2, "internal", (0, 0, E_SHAFT))

    # ---- 6 housing, lid
    housing, label = _housing(p)
    E_HOUS = (0, 0, -130)
    add("Housing (315 mm PVC, one piece)", housing, C_PVC, "plastic", 6, "shell", E_HOUS)
    add("Housing label plate", label, C_LABEL, "plastic", 6, "shell", E_HOUS)

    lid = Pos(0, 0, z_lid + p["lid_t"] / 2) * Box(p["lid"], p["lid"], p["lid_t"])
    lid = _fillet_try(lid, lid.edges().filter_by(Axis.Z), [18.0, 10.0])
    lid = _fillet_try(lid, _top_edges(lid), [3.0, 1.5])
    lid -= Pos(0, 0, z_lid + p["lid_t"] / 2) * Cylinder(p["shaft_d"] / 2 + 4, p["lid_t"] + 2)
    # shallow locating groove where the pipe sits, seen as a line on the lid edge
    lid -= Pos(0, 0, z_lid + p["lid_t"] - 0.6) * (Cylinder(Ro + 6, 2) - Cylinder(Ro + 4, 2.2))
    add("Lid (HDPE)", lid, C_HDPE, "plastic", 6, "shell", (0, 0, E_LID))
    lid_bolts = _unite([_hex_bolt(sx * 170, sy * 170, z_lid + p["lid_t"]) for sx in (-1, 1) for sy in (-1, 1)])
    add("Lid bolts", lid_bolts, C_STEEL, "metal", 6, "shell", (0, 0, E_LID))

    # ---- 3 bearing housing, flange screws, grease nipple, posts, plate, guard
    bh = Pos(0, 0, bh0 + p["brg_housing_h"] / 2) * Cylinder(p["brg_housing_d"] / 2, p["brg_housing_h"])
    bh = _fillet_try(bh, _top_edges(bh), [4.0, 2.0])
    bh -= Pos(0, 0, bh0 + p["brg_housing_h"] / 2) * Cylinder(p["shaft_d"] / 2 + 1, p["brg_housing_h"] + 2)
    # two cast rings marking the bearing seats
    for zr in (bh0 + 22, bh0 + p["brg_housing_h"] - 18):
        bh += Pos(0, 0, zr) * (Cylinder(p["brg_housing_d"] / 2 + 2, 6) - Cylinder(p["brg_housing_d"] / 2 - 2, 7))
    fl = Pos(0, 0, bh0 + 5) * Box(120, 120, 10)
    fl = _fillet_try(fl, fl.edges().filter_by(Axis.Z), [12.0, 6.0])
    fl = _fillet_try(fl, _top_edges(fl), [1.5, 0.8])
    fl -= Pos(0, 0, bh0 + 5) * Cylinder(p["shaft_d"] / 2 + 1, 12)
    bh += fl
    bh += Pos(p["brg_housing_d"] / 2 + 4, 0, bh0 + 50) * Rot(0, 90, 0) * Cylinder(4, 10)
    add("Bearing housing (aluminium)", bh, C_ALU, "metal", 3, "shell", (0, 0, E_BH))
    fl_screws = _unite([_hex_bolt(sx * 45, sy * 45, bh0 + 10, af=10, h=5) for sx in (-1, 1) for sy in (-1, 1)])
    fl_screws += Pos(p["brg_housing_d"] / 2 + 12, 0, bh0 + 50) * Rot(0, 90, 0) * extrude(RegularPolygon(5, 6), amount=4, both=True)
    add("Flange screws and grease nipple", fl_screws, C_STEEL, "metal", 3, "shell", (0, 0, E_BH))

    posts = None
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * p["post_offset"], sy * p["post_offset"]
            po = Pos(x, y, bh0 + p["post_h"] / 2) * Cylinder(p["post_d"] / 2, p["post_h"])
            po += Pos(x, y, bh0 + 5) * extrude(RegularPolygon(17 / math.sqrt(3), 6), amount=5, both=True)
            posts = po if posts is None else posts + po
    add("Generator posts (stainless)", posts, C_STEEL, "metal", 3, "shell", (0, 0, E_PLATE))
    plate = Pos(0, 0, p["plate_z0"] + p["plate_t"] / 2) * Box(p["plate"], p["plate"], p["plate_t"])
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Z), [16.0, 8.0])
    plate = _fillet_try(plate, _top_edges(plate), [2.0, 1.0])
    plate -= Pos(0, 0, p["plate_z0"] + p["plate_t"] / 2) * Cylinder(30, p["plate_t"] + 2)
    add("Generator plate (aluminium)", plate, C_ALU, "metal", 3, "shell", (0, 0, E_PLATE))
    pbolts = _unite([_hex_bolt(sx * p["post_offset"], sy * p["post_offset"], p["plate_z0"] + p["plate_t"], af=17, h=7)
                     for sx in (-1, 1) for sy in (-1, 1)])
    add("Plate nuts", pbolts, C_STEEL, "metal", 3, "shell", (0, 0, E_PLATE + 30))

    g0 = bh0 + p["brg_housing_h"]
    gh = p["plate_z0"] - g0
    guard = Pos(0, 0, g0 + gh / 2) * (Cylinder(p["guard_d"] / 2, gh) - Cylinder(p["guard_d"] / 2 - 2, gh + 2))
    add("Coupling guard (160 mm PVC pipe)", guard, C_PVC, "plastic", 3, "shell", (0, 0, E_GUARD))
    grings = (Pos(0, 0, g0 + 4) * (Cylinder(p["guard_d"] / 2 + 2, 8) - Cylinder(p["guard_d"] / 2 - 2, 9))
              + Pos(0, 0, g0 + gh - 4) * (Cylinder(p["guard_d"] / 2 + 2, 8) - Cylinder(p["guard_d"] / 2 - 2, 9)))
    add("Coupling guard rings", grings, C_ALU, "plastic", 3, "shell", (0, 0, E_GUARD))

    # ---- 4 jaw coupling: two hubs and an elastomer spider
    c0, cl, cr = p["coupling_z0"], p["coupling_len"], p["coupling_d"] / 2
    hubs = (Pos(0, 0, c0 + 7) * Cylinder(cr, 14) + Pos(0, 0, c0 + cl - 7) * Cylinder(cr, 14))
    hubs = _fillet_try(hubs, hubs.edges(), [1.5, 0.8])
    hubs -= Pos(0, 0, c0 + cl / 2) * Cylinder(p["shaft_d"] / 2, cl + 2)
    add("Jaw coupling hubs", hubs, C_ALU, "metal", 4, "internal", (0, 0, E_CPL))
    spider = Pos(0, 0, c0 + cl / 2) * (Cylinder(cr - 2, cl - 28) - Cylinder(p["shaft_d"] / 2 + 2, cl))
    add("Coupling spider (elastomer)", spider, C_SPIDER, "rubber", 4, "internal", (0, 0, E_CPL + 25))

    # ---- 5 generator: finned body, end caps, label band, cable gland
    gz0, gd, ghh = p["gen_z0"], p["gen_d"] / 2, p["gen_h"]
    body = Pos(0, 0, gz0 + ghh / 2) * Cylinder(gd - 4, ghh - 16)
    for k in range(36):
        a = k * 10.0
        if 55 <= a <= 85:
            continue                                # leave a flat band for the label
        body += Rot(0, 0, a) * Pos(gd - 3, 0, gz0 + ghh / 2) * Box(6, 3.0, ghh - 26)
    add("Generator body (low-speed BLDC)", body, C_GEN, "metal", 5, "shell", (0, 0, E_GEN))
    caps = Pos(0, 0, gz0 + 4) * Cylinder(gd, 8) + Pos(0, 0, gz0 + ghh - 4) * Cylinder(gd, 8)
    caps = _fillet_try(caps, caps.edges(), [3.0, 1.5])
    caps += Pos(0, 0, gz0 + ghh + 8) * Cylinder(40, 16)
    caps = _fillet_try(caps, _top_edges(caps), [4.0, 2.0])
    caps += Pos(0, 0, (p["coupling_z0"] + p["coupling_len"] + gz0) / 2) * Cylinder(
        p["shaft_d"] / 2, gz0 - p["coupling_z0"] - p["coupling_len"] + 2)
    for k in range(6):
        a = math.radians(k * 60 + 30)
        caps += Pos(0.8 * gd * math.cos(a), 0.8 * gd * math.sin(a), gz0 + ghh + 1) * Cylinder(4.5, 2)
    add("Generator end caps", caps, C_DARK, "metal", 5, "shell", (0, 0, E_GEN))
    la = math.radians(70)
    glabel = Pos((gd - 3.4) * math.cos(la), (gd - 3.4) * math.sin(la), gz0 + ghh / 2) * Rot(0, 0, 70) * Box(1.2, 60, 34)
    add("Generator rating label", glabel, C_LABEL, "plastic", 5, "shell", (0, 0, E_GEN))
    gland = Pos(gd + 10, 0, gz0 + ghh / 2) * Rot(0, 90, 0) * (Cylinder(9, 20) + Pos(0, 0, 12) * extrude(RegularPolygon(11, 6), amount=4, both=True))
    gland += _tube((gd + 20, 0, gz0 + ghh / 2), (gd + 70, 0, gz0 + ghh / 2 - 20), 5.5)
    add("Generator cable gland and lead", gland, C_RUBBER, "rubber", 16, "shell", (0, 0, E_GEN))

    # ---- 7 manifold, nozzles and inserts
    pipes, fittings, tee = _pipework(p)
    add("Branch pipes (90 mm PVC)", pipes, C_PVC2, "plastic", 7, "shell", (0, 0, 0))
    add("Elbows and socket couplers", fittings, C_PVC, "plastic", 7, "shell", (0, 0, 0))
    add("Reducing tee (125 x 90 mm)", tee, C_PVC, "plastic", 7, "shell", (0, 0, 0))
    bodies, inserts = _nozzles(p)
    for body, ins, side, sx in zip(bodies, inserts, ("jet 1", "jet 2"), (1, -1)):
        add(f"Nozzle, printed ({side})", body, C_NOZZLE, "plastic", 7, "shell", (0, 0, 150))
        add(f"Nozzle insert, 33 mm ({side})", ins, C_ALU, "metal", 7, "shell", (-sx * 70, 0, 150))

    # ---- 8 gate valve with handwheel
    mz, pr, vx = p["manifold_z"], p["penstock_od"] / 2, p["valve_x"]
    vb = Pos(vx, 0, mz) * Rot(0, 90, 0) * Cylinder(pr + 22, 90)
    vb = _fillet_try(vb, vb.edges(), [6.0, 3.0])
    vb += Pos(vx, 0, mz + pr + 10) * Box(80, 70, 40)
    vb = _fillet_try(vb, _top_edges(vb), [6.0, 3.0])
    for sx in (-1, 1):
        vb += Pos(vx + sx * 52, 0, mz) * Rot(0, 90, 0) * Cylinder(pr + 12, 14)
    add("Gate valve body", vb, C_PVC2, "plastic", 8, "shell", (0, 0, 0))
    stem = Pos(vx, 0, mz + 130) * Cylinder(14, 110) + Pos(vx, 0, mz + 190) * Cylinder(8, 30)
    add("Valve bonnet and stem", stem, C_STEEL, "metal", 8, "shell", (0, 0, 80))
    wheel = Pos(vx, 0, mz + 200) * Torus(72, 7)
    wheel += Pos(vx, 0, mz + 200) * Cylinder(16, 14)
    for k in range(4):
        wheel += Pos(vx, 0, mz + 200) * Rot(0, 0, 45 + k * 90) * Pos(36, 0, 0) * Box(72, 8, 6)
    add("Valve handwheel", wheel, C_VALVE, "painted", 8, "shell", (0, 0, 140))

    # ---- 11 frame: galvanized angle ring and legs on foot plates
    fs, fL, hz0 = p["frame"], p["frame_leg"], p["housing_z0"]
    t4 = 4.0
    outer = Pos(0, 0, hz0 - 15) * (Box(fs, fs, 30) - Box(fs - 2 * fL, fs - 2 * fL, 32))
    ring = outer - Pos(0, 0, hz0 - 15 - t4 / 2) * (Box(fs - 2 * t4, fs - 2 * t4, 30 - t4 + 0.01)
                                                   - Box(fs - 2 * fL - 2, fs - 2 * fL - 2, 40))
    legs = None
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * (fs - fL) / 2, sy * (fs - fL) / 2
            lg = Pos(cx, cy, hz0 / 2) * Box(fL, fL, hz0)
            lg -= Pos(cx - sx * t4 / 2, cy - sy * t4 / 2, hz0 / 2 - 2) * Box(fL - t4, fL - t4, hz0)
            lg += Pos(cx, cy, 3) * Box(fL + 30, fL + 30, 6)
            legs = lg if legs is None else legs + lg
    frame = ring + legs
    add("Frame (galvanized angle)", frame, C_GALV, "metal", 11, "shell", (0, 0, -440))
    anchors = _unite([_hex_bolt(sx * ((fs - fL) / 2 + 24), sy * ((fs - fL) / 2 - 6), 6, af=13, h=5, washer=True)
                      for sx in (-1, 1) for sy in (-1, 1)])
    add("Frame anchor bolts", anchors, C_STEEL, "metal", 11, "shell", (0, 0, -440))

    # ---- 13 rectifier box (accessory, beside the unit for the exploded view)
    rx, ry = RECT_AT
    rb = Pos(rx, ry, 55) * Box(130, 100, 110)
    rb = _fillet_try(rb, rb.edges().filter_by(Axis.Z), [8.0, 4.0])
    rb = _fillet_try(rb, _top_edges(rb), [4.0, 2.0])
    for k in range(6):
        rb -= Pos(rx - 30 + k * 12, ry - 50, 72) * Box(5, 6, 34)
    add("Rectifier box (vented)", rb, C_HDPE, "plastic", 13, "accessory", (0, 0, 60))
    fins = None
    for k in range(9):
        f = Pos(rx + 65 + 12, ry - 40 + k * 10, 55) * Box(24, 2.4, 90)
        fins = f if fins is None else fins + f
    fins += Pos(rx + 66.5, ry, 55) * Box(3, 90, 96)
    add("Rectifier heat sink", fins, C_ALU, "metal", 13, "accessory", (0, 0, 60))
    led = Pos(rx + 42, ry - 50.6, 92) * Rot(90, 0, 0) * Cylinder(3.0, 1.4)
    add("Rectifier status light (lit)", led, C_LED, "emissive", 13, "accessory", (0, 0, 60))
    rgl = _unite([Pos(rx + dx, ry, 110 + 6) * Cylinder(7, 12) for dx in (-35, 35)])
    add("Rectifier cable glands", rgl, C_RUBBER, "rubber", 16, "accessory", (0, 0, 60))
    rlab = Pos(rx - 12, ry - 50.6, 30) * Box(70, 1.2, 22)
    add("Rectifier label", rlab, C_ACCENT, "plastic", 13, "accessory", (0, 0, 60))

    # ---- context: penstock stub with a saddle, tailrace channel edges, tailwater
    pen = m["penstock_stub"] - Pos(p["valve_x"], 0, mz) * Rot(0, 90, 0) * Cylinder(pr + 1, 90)
    pen += Pos(-850, 0, mz) * Rot(0, 90, 0) * (Cylinder(pr + 6, 60) - Cylinder(pr - 2, 62))
    add("Penstock section (125 mm PVC)", pen, C_PENSTOCK, "plastic", 9, "context", (0, 0, 0))
    saddle = Pos(-700, 0, (mz - pr) / 2) * Box(50, 50, mz - pr)
    saddle += Pos(-700, 0, mz - pr + 8) * (Box(60, 150, 40) - Pos(0, 0, pr + 8 - 8) * Rot(0, 90, 0) * Cylinder(pr, 80))
    saddle += Pos(-700, 0, 4) * Box(140, 140, 8)
    add("Pipe saddle", saddle, C_GALV, "metal", None, "context", (0, 0, 0))

    x0 = -760.0
    left = Pos((x0 - CH_IN) / 2, 0, CH_FLOOR / 2) * Box(-CH_IN - x0, 2 * CH_Y, -CH_FLOOR)
    right = Pos(CH_IN + CH_WALL / 2, 0, CH_FLOOR / 2) * Box(CH_WALL, 2 * CH_Y, -CH_FLOOR)
    floor = Pos(0, 0, CH_FLOOR - 20) * Box(2 * CH_IN + 2, 2 * CH_Y, 40)
    chan = left + right + floor
    chan = _fillet_try(chan, chan.edges().filter_by(Axis.Y), [6.0, 3.0])
    add("Tailrace channel edge (concrete)", chan, C_CONCRETE, "clay", None, "context", (0, 0, 0))
    water = Pos(0, 0, (WATER_Z + CH_FLOOR) / 2) * Box(2 * CH_IN, 2 * CH_Y - 4, WATER_Z - CH_FLOOR)
    add("Tailwater", water, C_WATER, "clear", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for q in product_parts():
        s = q["shape"]
        print(f"{q['name']:42s} {q['group']:9s} {q['material']:8s} valid={s.is_valid} vol={s.volume / 1000:8.1f} cm3")
