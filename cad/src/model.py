"""PicoFlow parametric model (build123d), constructable design (PCF-DDR-003).

Run from the repo root:  python cad/src/model.py            exports STEP and STL
                         python cad/src/model.py --check    constructability checks only

Axes: Z up. Z = 0 is the normal tailwater surface under the turbine and the top of the pad the
frame stands on (the setting height in R13 is measured from here). The turbine axis is vertical
at X = Y = 0. The penstock arrives horizontally from -X along Y = -75 mm. Jet 1 strikes the
runner pitch circle at +Y travelling -X; jet 2 strikes it at -Y travelling +X, so the runner turns
counterclockwise seen from above and the two jet forces cancel radially. Jet 2's nozzle is jet 1's
turned 180 degrees about the axis, so the two nozzles are the same part.

Every component is a single made or bought piece (or a matched set of fixings) with the faces it
touches modelled as touching: build_components() returns them, checks() tests every joint with
build123d (overlap volume and distance). Bought parts are drawn to catalogue-class sizes, to be
checked against the datasheet of the part bought. PRELIMINARY, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Runner (PCF-CAL-001 section 3)
    "runner_od": 200.0,        # outside diameter, fits a 220 x 220 mm bed (R9)
    "runner_pcd": 150.0,       # pitch diameter where the jets strike
    "n_buckets": 20,
    "bucket_len": 50.0,        # radial length of the bucket band
    "bucket_w": 9.0,           # bucket thickness (massing)
    "bucket_h": 30.0,          # bucket axial depth
    "hub_d": 80.0,
    "hub_h": 50.0,
    "runner_z": 224.0,         # runner mid-plane above tailwater (DDR-003 P6: lowered 11 mm with the nozzle tip)
    # Jets (PCF-CAL-001 section 2)
    "jet_z": 280.0,            # nozzle exit centerline above tailwater (R13: 300 or less)
    "jet_angle": 20.0,         # jet angle below the runner plane, degrees
    "jet_d": 34.0,             # design-point insert bore (PCF-CAL-001 v0.3: 33.7 mm for 10 L/s, rounded)
    "nozzle_len": 170.0,       # converging nozzle length along the jet axis, exit to inlet bend
    "nozzle_exit_x": 115.0,    # nozzle exit before the strike point, along X (DDR-003 P6: was 85)
    "nozzle_rex": 32.0,        # nozzle outside radius at the tip (holds 20 to 45 mm inserts)
    "spigot_len": 60.0,        # horizontal 90 mm spigot at the nozzle inlet
    "insert_seat": 25.0,       # insert seat radius in the nozzle tip
    "insert_depth": 25.0,
    "saddle_r": 72.0,          # radius of the nozzle saddle patch on the housing
    "saddle_t": 6.0,
    "gasket_t": 2.0,
    # Shaft, bearings, coupling
    "shaft_d": 20.0,           # 316 stainless
    "brg_od": 47.0,            # 6204-class insert bearing in each flange unit
    "brg_w": 14.0,
    "brg_unit": (86.0, 64.0, 14.0, 32.0, 26.0, 33.0, 17.0),  # UCF204 class: square, bolt pitch, flange t, boss r, boss h, height, collar r
    "brg_sleeve": 24.0,        # spacer sleeves between the two flange units
    "brg_housing_d": 86.0,     # (legacy name) flange unit square
    "brg_housing_h": 71.0,     # (legacy name) height of the bearing stack on the lid
    "coupling_d": 48.0,        # L-075 class jaw coupling envelope
    "coupling_len": 40.0,
    "coupling_gap": 10.0,      # upper bearing collar to coupling
    "post_d": 20.0,            # post sleeve, 20 x 2 mm tube on an M10 rod
    "post_h": 145.0,
    "post_offset": 125.0,      # DDR-003 P8: was 120, so the washers under the lid clear the housing
    "plate": 280.0,            # generator plate, square
    "plate_t": 8.0,             # DDR-003: 8 mm (was 10) to keep R14
    "guard_d": 160.0,          # DDR-003 P9: 160 mm PVC pipe guard over the bearings and coupling (was 110)
    "guard_wall": 4.0,
    "gen_pcd": 176.0,          # generator face screws (to confirm on the unit bought)
    # Generator (low-speed BLDC, new unit, decided 2026-09-25)
    "gen_d": 200.0,
    "gen_h": 90.0,
    # Housing, lid and frame
    "housing_od": 315.0,       # 315 mm PVC sewer pipe (SN4 class)
    "housing_wall": 7.7,
    "housing_z0": 80.0,        # housing bottom above tailwater (sits on the frame)
    "housing_h": 303.0,        # 300 mm plus the 3 mm that sits in the lid groove
    "lid": 400.0,
    "lid_t": 12.0,
    "lid_groove": 3.0,         # groove under the lid that locates the housing top
    "frame": 380.0,            # DDR-003 P1: frame outside size, square (was 420)
    "frame_leg": 40.0,         # 40 x 40 x 4 mm galvanized angle
    "angle_t": 4.0,
    "foot": 80.0,              # foot plates, 80 x 80 x 5 mm
    "foot_t": 5.0,
    "tie_xy": 170.0,           # tie rods, frame to lid, at the corners
    "rod_d": 10.0,
    # Pipework
    "penstock_od": 125.0,      # PVC drainage pipe, SN8 (decided 2026-09-25, PCF-DDR-002 N1)
    "branch_od": 90.0,         # branches to the nozzles (CAL-001 section 1)
    "fit_od": 102.0,           # socket outside diameter of the 90 mm fittings
    "fit_c": 70.0,             # elbow centre to socket mouth
    "sock": 45.0,              # socket depth
    "manifold_z": 338.0,       # manifold and branch centerline (derived: the nozzle inlet height, 338.1)
    "pen_y": -75.0,            # penstock and tee on the jet 2 line (DDR-003 P10)
    "tee_x": -560.0,
    "valve_x": -875.0,         # full-bore 125 mm valve centre (N6 option a, decided 2026-10-01)
    "valve_len": 330.0,        # valve overall length over its two sockets (catalogue class, to confirm)
    "valve_sock": 70.0,        # valve socket depth for 125 mm pipe
    "stub_x": -1200.0,         # end of the penstock stub in the model
    "branch_y": 260.0,         # far branch runs around the housing at this Y
    "branch_x": 460.0,
    "stands": ((-560.0, 100.0, "y"), (-50.0, 260.0, "x"), (460.0, 168.0, "y")),
    # Equipment post (electrics), site-placed
    "eq_post": (700.0, -450.0),
}


def _derived(p):
    d = dict(p)
    d["runner_bottom"] = p["runner_z"] - p["hub_h"] / 2
    d["lid_z"] = p["housing_z0"] + p["housing_h"] - p["lid_groove"]          # lid underside
    d["bh_z0"] = d["lid_z"] + p["lid_t"]                                     # lid top
    d["plate_z0"] = d["bh_z0"] + p["post_h"]
    d["gen_z0"] = d["plate_z0"] + p["plate_t"]                               # DDR-003 P7: generator sits on the plate
    L, J, ft, br, bh, H, cr = p["brg_unit"]
    d["brg_up_z0"] = d["bh_z0"] + ft + p["brg_sleeve"]
    d["brg_top"] = d["brg_up_z0"] + H
    d["coupling_z0"] = d["brg_top"] + p["coupling_gap"]
    d["shaft_top"] = d["coupling_z0"] + p["coupling_len"] / 2
    d["shaft_len"] = d["shaft_top"] - d["runner_bottom"]
    a = math.radians(p["jet_angle"])
    d["nozzle_entry_x"] = p["nozzle_exit_x"] + p["nozzle_len"] * math.cos(a)
    d["nozzle_entry_z"] = p["jet_z"] + p["nozzle_len"] * math.sin(a)
    d["manifold_z"] = d["nozzle_entry_z"]                                     # pipework on the nozzle inlet line
    d["spigot_end_x"] = d["nozzle_entry_x"] + p["spigot_len"]
    d["strike_z"] = p["jet_z"] - p["nozzle_exit_x"] * math.tan(a)              # jet height over the pitch point
    d["bucket_top"] = p["runner_z"] + 2 + (p["bucket_h"] * math.cos(math.radians(35)) + p["bucket_w"] * math.sin(math.radians(35))) / 2
    ro = p["housing_od"] / 2
    yj = p["runner_pcd"] / 2
    xw = math.sqrt(ro ** 2 - yj ** 2)
    s = (xw - p["nozzle_exit_x"]) / math.cos(a)
    d["wall_pt"] = (xw, yj, p["jet_z"] + s * math.sin(a))                    # jet axis meets the housing outside
    # branch lengths along the centreline, tee centre to nozzle inlet (for PCF-CAL-001)
    tx, by, bx, py = p["tee_x"], p["branch_y"], p["branch_x"], p["pen_y"]
    d["branch_len_1"] = ((by - py) + (bx - tx) + (by - yj) + (bx - d["spigot_end_x"])) / 1000
    d["branch_len_2"] = (-d["spigot_end_x"] - tx) / 1000
    return d


derived = _derived


# ------------------------------------------------------------------ geometry helpers
def _b():
    import build123d as b
    return b


def _tube(a, b, r):
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); dv = b - a
    return Solid.make_cylinder(r, dv.length, Plane(origin=a, z_dir=dv.normalized()))


def _cone(a, b, r1, r2):
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); dv = b - a
    return Solid.make_cone(r1, r2, dv.length, Plane(origin=a, z_dir=dv.normalized()))


def _unite(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def bx(x0, x1, y0, y1, z0, z1):
    b = _b()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def zcyl(x, y, z0, z1, r):
    b = _b()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)


def ztube(x, y, z0, z1, ro, ri):
    return zcyl(x, y, z0, z1, ro) - zcyl(x, y, z0 - 1, z1 + 1, ri)


def hexnut(x, y, z0, h=8.0, af=17.0, axis=None):
    """Hex nut or bolt head, axis Z, from z0 to z0 + h (or along `axis`=(origin, direction))."""
    b = _b()
    n = b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), amount=h)
    if axis is None:
        return b.Pos(x, y, z0) * n
    o, dvec = axis
    return b.Plane(origin=o, z_dir=dvec) * n


def _add(v, w, k=1.0):
    return tuple(a + k * c for a, c in zip(v, w))


def _rotz180(shape):
    b = _b()
    return b.Rot(0, 0, 180) * shape


def _angle_bar(axis, a0, a1, c0, c1, inward, t, leg, zt):
    """A horizontal 40 x 40 x 4 angle with its top face at zt. axis 'x' or 'y' gives the run;
    c0..c1 is the across-run position of the vertical leg's outer face side; inward is +1 or -1
    (the horizontal leg points that way across the run)."""
    if axis == "x":
        horiz = bx(a0, a1, min(c0, c0 + inward * leg), max(c0, c0 + inward * leg), zt - t, zt)
        vert = bx(a0, a1, min(c0, c0 + inward * t), max(c0, c0 + inward * t), zt - leg, zt)
    else:
        horiz = bx(min(c0, c0 + inward * leg), max(c0, c0 + inward * leg), a0, a1, zt - t, zt)
        vert = bx(min(c0, c0 + inward * t), max(c0, c0 + inward * t), a0, a1, zt - leg, zt)
    return horiz + vert


@dataclass
class Comp:
    """One component: a single made or bought piece (or a matched set of fixings)."""
    name: str
    shape: object
    bom: int | None
    kind: str          # "made", "bought", "fixing", "site"
    group: str | None  # legacy build_parts key


# ------------------------------------------------------------------ the nozzle (jet 1; jet 2 is it turned 180 deg)
def nozzle_frame(p):
    d = _derived(p)
    a = math.radians(p["jet_angle"])
    back = (math.cos(a), 0.0, math.sin(a))                  # from the exit back toward the inlet
    yj = p["runner_pcd"] / 2
    X = (p["nozzle_exit_x"], yj, p["jet_z"])                # front face of the insert flange (jet exit)
    T = _add(X, back, 3.0)                                  # nozzle tip face
    N = _add(X, back, p["nozzle_len"])                      # inlet bend
    S = (d["spigot_end_x"], yj, N[2])                       # spigot end
    return dict(back=back, X=X, T=T, N=N, S=S, W=d["wall_pt"])


def _saddle_axes(p, W):
    n = (W[0], W[1], 0.0)
    ln = math.hypot(W[0], W[1])
    n = (n[0] / ln, n[1] / ln, 0.0)
    return n


def nozzle_parts(p):
    """(nozzle body with saddle, gasket, insert, saddle bolts and nuts, insert screws, hole cutter,
    bolt hole cutter) for jet 1."""
    b = _b()
    F = nozzle_frame(p)
    back, X, T, N, S, W = F["back"], F["X"], F["T"], F["N"], F["S"], F["W"]
    ro = p["housing_od"] / 2
    rex, rin = p["nozzle_rex"], p["branch_od"] / 2
    wall = 4.0
    # outside: cone tip to bend, sphere at the bend, horizontal spigot
    body = _cone(T, N, rex, rin) + b.Pos(*N) * b.Sphere(rin) + _tube(N, S, rin)
    # saddle patch on the housing outside, with a gasket under it
    n = _saddle_axes(p, W)
    zc = W[2]
    big = 2 * p["saddle_r"] + 20
    bound = _tube((0, 0, zc), (n[0] * (ro + 60), n[1] * (ro + 60), zc), p["saddle_r"])
    g0, g1 = ro, ro + p["gasket_t"]
    s1 = g1 + p["saddle_t"]
    shell_g = zcyl(0, 0, zc - big / 2, zc + big / 2, g1) - zcyl(0, 0, zc - big / 2 - 1, zc + big / 2 + 1, g0)
    shell_s = zcyl(0, 0, zc - big / 2, zc + big / 2, s1) - zcyl(0, 0, zc - big / 2 - 1, zc + big / 2 + 1, g1)
    # hole through the wall: the nozzle cone grown 2.5 mm
    fwd = tuple(-c for c in back)
    cutter = _cone(_add(T, fwd, 12.0), N, rex + 2.5, rin + 2.5)
    # solid round the nozzle body; cleared only round the tip so the insert flange goes in from inside
    saddle = (shell_s & bound) - _tube(_add(T, fwd, 12.0), _add(T, back, 2.0), rex + 2.5)
    gasket = (shell_g & bound) - cutter
    # four M6 bolts through saddle, gasket and wall, nuts inside
    tang = (-n[1], n[0], 0.0)
    bolts, bholes = [], []
    for st in (-1, 1):
        for sz in (-1, 1):
            ang = st * 48.0 / ro
            c, s_ = math.cos(ang), math.sin(ang)
            rdir = (n[0] * c - n[1] * s_, n[0] * s_ + n[1] * c, 0.0)
            z = zc + sz * 48.0
            ri = ro - p["housing_wall"]
            o_in = (rdir[0] * (ri - 5.4), rdir[1] * (ri - 5.4), z)
            bholes.append(_tube((rdir[0] * (ri - 8), rdir[1] * (ri - 8), z), (rdir[0] * (s1 + 8), rdir[1] * (s1 + 8), z), 3.3))
            shank = _tube(o_in, (rdir[0] * s1, rdir[1] * s1, z), 3.0)
            head = hexnut(0, 0, 0, 4.0, 10.0, axis=((rdir[0] * s1, rdir[1] * s1, z), rdir))
            nut = hexnut(0, 0, 0, 5.0, 10.0, axis=(o_in, rdir))
            bolts.append(shank + head + nut)
    saddle = saddle - _unite(bholes)
    gasket = gasket - _unite(bholes)
    part = body + saddle
    # bore: insert seat, converging bore, spigot bore, all opened at both ends
    seat_end = _add(T, back, p["insert_depth"])
    bore = (_tube(_add(T, fwd, 1.0), seat_end, p["insert_seat"])
            + _cone(seat_end, N, p["insert_seat"] - 2.0, rin - wall)
            + b.Pos(*N) * b.Sphere(rin - wall)
            + _tube(N, _add(S, (1, 0, 0), 1.0), rin - wall))
    part = part - bore
    part = part - _unite([_tube(_add(_add(T, (0, sy * 28.5, 0)), fwd, 1), _add(_add(T, (0, sy * 28.5, 0)), back, 10), 2.8) for sy in (-1, 1)])
    # insert: flange in front of the tip, body in the seat, converging bore to the jet size
    ins = _tube(X, T, rex) + _tube(T, seat_end, p["insert_seat"])
    ins = ins - _cone(_add(X, fwd, 1.0), _add(seat_end, back, 1.0), p["jet_d"] / 2 - 0.4, p["insert_seat"] - 2.0)
    # two M4 screws through the insert flange into heat-set inserts in the tip face
    scr = []
    for sy in (-1, 1):
        o = _add(X, (0, sy * 28.5, 0))
        scr.append(_tube(_add(o, fwd, 2.5), _add(o, back, 12.0), 2.0) + _tube(_add(o, fwd, 2.5), o, 3.5))
    ins = ins - _unite([_tube(_add(_add(X, (0, sy * 28.5, 0)), fwd, 1), _add(_add(X, (0, sy * 28.5, 0)), back, 4), 2.2) for sy in (-1, 1)])
    return dict(nozzle=part, gasket=gasket, insert=ins, bolts=_unite(bolts), screws=_unite(scr),
                cutter=cutter, bholes=_unite(bholes))


# ------------------------------------------------------------------ components
def build_components(p=None):
    """Every component as a Comp, keyed by a short name."""
    b = _b()
    p = _derived({**PARAMS, **(p or {})})
    C: dict[str, Comp] = {}

    def add(key, name, shape, bom, kind, group):
        C[key] = Comp(name, shape, bom, kind, group)

    t, leg = p["angle_t"], p["frame_leg"]
    hf = p["frame"] / 2
    z0h = p["housing_z0"]
    ro = p["housing_od"] / 2
    ri = ro - p["housing_wall"]
    rz = p["runner_z"]

    # ---- 11 frame: a welded square of 40 x 40 x 4 angle (horizontal legs inward, top at the
    #      housing bottom), four angle legs nested in the corners, foot plates, pipe stops
    ring = (_angle_bar("y", -hf, hf, hf, None, -1, t, leg, z0h) + _angle_bar("y", -hf, hf, -hf, None, 1, t, leg, z0h)
            + _angle_bar("x", -hf, hf, hf, None, -1, t, leg, z0h) + _angle_bar("x", -hf, hf, -hf, None, 1, t, leg, z0h))
    ft = p["foot_t"]
    legs, feet, holes = [], [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            xo, yo = sx * (hf - t), sy * (hf - t)                 # inside faces of the ring's vertical legs
            la = bx(min(xo, xo - sx * t), max(xo, xo - sx * t), min(yo, yo - sy * leg), max(yo, yo - sy * leg), ft, z0h - t)
            lb = bx(min(xo, xo - sx * leg), max(xo, xo - sx * leg), min(yo, yo - sy * t), max(yo, yo - sy * t), ft, z0h - t)
            legs.append(la + lb)
            fx0 = xo - sx * leg
            feet.append(bx(min(fx0, fx0 + sx * p["foot"]), max(fx0, fx0 + sx * p["foot"]),
                           min(yo - sy * leg, yo - sy * leg + sy * p["foot"]), max(yo - sy * leg, yo - sy * leg + sy * p["foot"]), 0, ft)
                        - zcyl(sx * (hf + 18), sy * (hf + 18), -1, ft + 1, 6.5))
            holes.append(zcyl(sx * p["tie_xy"], sy * p["tie_xy"], z0h - t - 1, z0h + 1, p["rod_d"] / 2 + 0.5))
    stops = _unite([b.Rot(0, 0, k * 90) * bx(ro + 1.0, ro + 6.0, -15, 15, z0h, z0h + 20) for k in range(4)])
    frame = ring + _unite(legs) + _unite(feet) + stops - _unite(holes)
    add("frame", "Turbine frame, welded", frame, 11, "made", "frame")
    anchors = _unite([zcyl(sx * (hf + 18), sy * (hf + 18), -40, ft + 6, 6.0) + hexnut(sx * (hf + 18), sy * (hf + 18), ft, 7.0, 19.0)
                      for sx in (-1, 1) for sy in (-1, 1)])
    add("anchors", "M12 anchors in the pad (4)", anchors, 19, "fixing", None)

    # ---- tie rods (frame to lid), two nuts on the frame, washer and nut on the lid
    lid_top = p["bh_z0"]
    rods, lnuts = [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * p["tie_xy"], sy * p["tie_xy"]
            rods.append(zcyl(x, y, z0h - t - 12, lid_top + 14, p["rod_d"] / 2)
                        + hexnut(x, y, z0h - t - 8, 8) + hexnut(x, y, z0h, 8))
            lnuts.append(ztube(x, y, lid_top, lid_top + 2.5, 15, 5.5) + (hexnut(x, y, lid_top + 2.5, 8) - zcyl(x, y, lid_top, lid_top + 12, 5.0)))
    add("tie_rods", "Tie rods, M10, with nuts on the frame (4)", _unite(rods), 19, "fixing", None)
    add("lid_nuts", "Tie rod washers and nuts on the lid (4)", _unite(lnuts), 19, "fixing", None)

    # ---- 7 nozzles (two, the same part), gaskets, inserts, saddle bolts
    NP = nozzle_parts(p)
    add("nozzle_1", "Nozzle, jet 1", NP["nozzle"], 7, "made", "manifold")
    add("nozzle_2", "Nozzle, jet 2", _rotz180(NP["nozzle"]), 7, "made", "manifold")
    add("gaskets", "Saddle gaskets (2)", NP["gasket"] + _rotz180(NP["gasket"]), 7, "made", "manifold")
    add("inserts", "Nozzle inserts, 34 mm (2)", NP["insert"] + _rotz180(NP["insert"]), 7, "made", "manifold")
    add("saddle_bolts", "M6 saddle bolts and nuts (8)", NP["bolts"] + _rotz180(NP["bolts"]), 19, "fixing", None)
    add("insert_screws", "M4 insert screws (4)", NP["screws"] + _rotz180(NP["screws"]), 19, "fixing", None)

    # ---- 6 housing: 315 mm PVC pipe cut to length, two nozzle holes and eight bolt holes
    shell = ztube(0, 0, z0h, z0h + p["housing_h"], ro, ri)
    cut = NP["cutter"] + NP["bholes"]
    shell = shell - cut - _rotz180(cut)
    add("housing", "Housing, 315 mm PVC pipe", shell, 6, "made", "housing")

    # ---- 6 lid: HDPE, groove for the housing underneath, groove for the guard on top, holes
    lz = p["lid_z"]
    lid = bx(-p["lid"] / 2, p["lid"] / 2, -p["lid"] / 2, p["lid"] / 2, lz, lz + p["lid_t"])
    lid -= ztube(0, 0, lz - 1, lz + p["lid_groove"], ro + 1.0, ri - 0.5)
    gr = p["guard_d"] / 2
    lid -= ztube(0, 0, lid_top - 2, lid_top + 1, gr + 0.5, gr - p["guard_wall"] - 0.5)
    lid -= zcyl(0, 0, lz - 1, lid_top + 1, p["shaft_d"] / 2 + 4)
    L, J, fth, br, bhh, H, cr = p["brg_unit"]
    for sx in (-1, 1):
        for sy in (-1, 1):
            for off, r in ((J / 2, 5.5), (p["post_offset"], 5.5), (p["tie_xy"], 5.5)):
                lid -= zcyl(sx * off, sy * off, lz - 1, lid_top + 1, r)
    add("lid", "Lid, 12 mm HDPE", lid, 6, "made", "housing")

    # ---- 3 bearings: two 4-bolt flange units (UCF204 class), spacer sleeves, M10 bolts, V-ring
    def flange_unit(z):
        f = b.Pos(0, 0, z) * b.extrude(b.RectangleRounded(L, L, 10), amount=fth)
        f += zcyl(0, 0, z, z + bhh, br) + zcyl(0, 0, z, z + H, cr)
        f -= zcyl(0, 0, z - 1, z + H + 1, p["shaft_d"] / 2)
        for sx in (-1, 1):
            for sy in (-1, 1):
                f -= zcyl(sx * J / 2, sy * J / 2, z - 1, z + fth + 1, 6.0)
        return f
    zl, zu = lid_top, p["brg_up_z0"]
    add("brg_low", "Lower flange bearing unit", flange_unit(zl), 3, "bought", "bearing_mount")
    add("brg_up", "Upper flange bearing unit", flange_unit(zu), 3, "bought", "bearing_mount")
    add("brg_sleeves", "Bearing spacer sleeves (4)",
        _unite([ztube(sx * J / 2, sy * J / 2, zl + fth, zu, 10.0, 5.5) for sx in (-1, 1) for sy in (-1, 1)]), 3, "made", "bearing_mount")
    bb = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * J / 2, sy * J / 2
            bb.append(zcyl(x, y, lz - 6.4, zu + fth + 10, 5.0) + hexnut(x, y, lz - 6.4, 6.4) + hexnut(x, y, zu + fth, 8))
    add("brg_bolts", "M10 bearing bolts and nuts (4)", _unite(bb), 19, "fixing", None)
    add("vring", "V-ring seal on the shaft under the lid", ztube(0, 0, lz - 9, lz, 19.0, p["shaft_d"] / 2), 3, "bought", "bearing_mount")

    # ---- 2 shaft and clamping hub
    add("shaft", "Shaft, 20 mm stainless", zcyl(0, 0, p["runner_bottom"], p["shaft_top"], p["shaft_d"] / 2), 2, "made", "shaft")
    htop = rz + p["hub_h"] / 2
    hub = ztube(0, 0, htop, htop + 8, 28.0, p["shaft_d"] / 2) + ztube(0, 0, htop + 8, htop + 28, 16.0, p["shaft_d"] / 2)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        hub -= zcyl(22 * math.cos(a), 22 * math.sin(a), htop - 1, htop + 9, 2.75)
    add("hub", "Clamping shaft hub, 20 mm bore", hub, 2, "bought", "shaft")
    hub_scr = _unite([zcyl(22 * math.cos(math.radians(45 + 90 * k)), 22 * math.sin(math.radians(45 + 90 * k)), htop - 10, htop + 8, 2.5)
                      + zcyl(22 * math.cos(math.radians(45 + 90 * k)), 22 * math.sin(math.radians(45 + 90 * k)), htop + 8, htop + 13, 4.3)
                      for k in range(4)])
    add("hub_screws", "M5 hub screws (4)", hub_scr, 19, "fixing", None)

    # ---- 1 Turgo runner: hub, web disc, outer rim and a band of inclined buckets (massing)
    R = p["runner_od"] / 2
    rhub = zcyl(0, 0, rz - p["hub_h"] / 2, rz + p["hub_h"] / 2, p["hub_d"] / 2) - zcyl(0, 0, rz - 30, rz + 30, p["shaft_d"] / 2)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        rhub -= zcyl(22 * math.cos(a), 22 * math.sin(a), htop - 12, htop + 1, 3.0)   # heat-set M5 inserts
    web = zcyl(0, 0, rz - 18, rz - 12, R - 8) - zcyl(0, 0, rz - 20, rz - 10, p["hub_d"] / 2 - 1)
    rim = ztube(0, 0, rz - 18, rz - 6, R, R - 8)
    rb = p["runner_pcd"] / 2 - 5
    buckets = [b.Pos(rb * math.cos(math.radians(k * 360 / p["n_buckets"])),
                     rb * math.sin(math.radians(k * 360 / p["n_buckets"])), rz + 2)
               * b.Rot(0, 0, k * 360 / p["n_buckets"]) * b.Rot(35, 0, 0)
               * b.Box(p["bucket_len"], p["bucket_w"], p["bucket_h"]) for k in range(p["n_buckets"])]
    runner = rhub + web + rim + _unite(buckets)
    add("runner", "Turgo runner, printed", runner, 1, "made", "runner")

    # ---- 3 guard, posts, generator plate
    add("guard", "Bearing and coupling guard, 160 mm PVC", ztube(0, 0, lid_top - 2, p["plate_z0"] - 1, gr, gr - p["guard_wall"]), 3, "made", "bearing_mount")
    po = p["post_offset"]
    posts, prods, pnuts = [], [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * po, sy * po
            posts.append(ztube(x, y, lid_top, p["plate_z0"], p["post_d"] / 2, p["post_d"] / 2 - 2))
            prods.append(zcyl(x, y, lz - 2.5 - 8 - 4, p["gen_z0"] + 2.5 + 8 + 3, p["rod_d"] / 2)
                         + ztube(x, y, lz - 2.5, lz, 15, 5.5) + hexnut(x, y, lz - 10.5, 8))
            pnuts.append(ztube(x, y, p["gen_z0"], p["gen_z0"] + 2.5, 12, 5.5)
                         + (hexnut(x, y, p["gen_z0"] + 2.5, 8) - zcyl(x, y, p["gen_z0"], p["gen_z0"] + 12, 5.0)))
    add("posts", "Posts, 20 mm tube (4)", _unite(posts), 3, "made", "bearing_mount")
    add("post_rods", "Post rods, M10, with nuts and washers under the lid (4)", _unite(prods), 19, "fixing", None)
    add("plate_nuts", "Post rod washers and nuts on the plate (4)", _unite(pnuts), 19, "fixing", None)
    pz = p["plate_z0"]
    plate = bx(-p["plate"] / 2, p["plate"] / 2, -p["plate"] / 2, p["plate"] / 2, pz, pz + p["plate_t"]) - zcyl(0, 0, pz - 1, pz + p["plate_t"] + 1, 31)
    gpr = p["gen_pcd"] / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            plate -= zcyl(sx * po, sy * po, pz - 1, pz + p["plate_t"] + 1, 5.5)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        plate -= zcyl(gpr * math.cos(a), gpr * math.sin(a), pz - 1, pz + p["plate_t"] + 1, 3.3)
    add("plate", "Generator plate, 8 mm aluminium", plate, 3, "made", "bearing_mount")
    gen_scr = _unite([zcyl(gpr * math.cos(math.radians(45 + 90 * k)), gpr * math.sin(math.radians(45 + 90 * k)), pz - 4, pz + p["plate_t"] + 10, 3.0)
                      + hexnut(gpr * math.cos(math.radians(45 + 90 * k)), gpr * math.sin(math.radians(45 + 90 * k)), pz - 4, 4, 10)
                      for k in range(4)])
    add("gen_screws", "M6 generator screws (4)", gen_scr, 19, "fixing", None)

    # ---- 4 coupling, 5 generator
    c0, cl = p["coupling_z0"], p["coupling_len"]
    add("coupling", "Jaw coupling", ztube(0, 0, c0, c0 + cl, p["coupling_d"] / 2, p["shaft_d"] / 2), 4, "bought", "coupling")
    gz = p["gen_z0"]
    gen = (zcyl(0, 0, gz, gz + p["gen_h"], p["gen_d"] / 2) + zcyl(0, 0, gz + p["gen_h"], gz + p["gen_h"] + 16, 40)
           + zcyl(0, 0, p["shaft_top"], gz, p["shaft_d"] / 2)
           + b.Pos(p["gen_d"] / 2 + 6, 0, gz + 45) * b.Rot(0, 90, 0) * b.Cylinder(9, 14))
    for k in range(4):
        an = math.radians(45 + 90 * k)
        gen -= zcyl(gpr * math.cos(an), gpr * math.sin(an), gz - 1, gz + 12, 3.0)
    add("generator", "Generator, low-speed BLDC", gen, 5, "bought", "generator")

    # ---- 7 manifold: reducing tee, reducer, pipes, elbows, flexible couplings
    mz, py, tx = p["manifold_z"], p["pen_y"], p["tee_x"]
    r9, rf, r12 = p["branch_od"] / 2, p["fit_od"] / 2, p["penstock_od"] / 2 + 7
    fc, sk = p["fit_c"], p["sock"]
    bxx, byy = p["branch_x"], p["branch_y"]
    yj = p["runner_pcd"] / 2
    sp = p["spigot_end_x"]
    tee = (_tube((tx - 90, py, mz), (tx + 90, py, mz), r12) + _tube((tx, py, mz), (tx, py + 80, mz), rf)
           + b.Pos(tx, py, mz) * b.Sphere(rf))
    reducer = _cone((tx + 90, py, mz), (tx + 160, py, mz), r12, rf)
    tee -= _tube((tx - 91, py, mz), (tx + 91, py, mz), p["penstock_od"] / 2) + _tube((tx, py, mz), (tx, py + 81, mz), r9)
    reducer -= _cone((tx + 89, py, mz), (tx + 161, py, mz), p["penstock_od"] / 2, r9)
    fittings = [tee, reducer]

    def elbow(c, u, v):
        e = b.Pos(*c) * b.Sphere(rf) + _tube(c, _add(c, u, fc), rf) + _tube(c, _add(c, v, fc), rf)
        return e - (b.Pos(*c) * b.Sphere(r9) + _tube(c, _add(c, u, fc + 1), r9) + _tube(c, _add(c, v, fc + 1), r9))
    E1, E2, E3 = (tx, byy, mz), (bxx, byy, mz), (bxx, yj, mz)
    fittings += [elbow(E1, (0, -1, 0), (1, 0, 0)), elbow(E2, (-1, 0, 0), (0, -1, 0)), elbow(E3, (0, 1, 0), (-1, 0, 0))]
    pipes = {
        "P1": ((tx, py + 80 - sk, mz), (tx, byy - fc + sk, mz)),
        "P2": ((tx + fc - sk, byy, mz), (bxx - fc + sk, byy, mz)),
        "P3": ((bxx, byy - fc + sk, mz), (bxx, yj + fc - sk, mz)),
        "P4": ((bxx - fc + sk, yj, mz), (sp, yj, mz)),
        "P5": ((tx + 160 - sk, py, mz), (-sp, py, mz)),
    }
    pipe_shapes = {k: _tube(a, c, r9) - _tube(a, c, r9 - 3.0) for k, (a, c) in pipes.items()}
    cpl = []
    for sx in (1, -1):
        c = (sx * sp, sx * yj, mz)
        cpl.append(_tube(_add(c, (-50, 0, 0)), _add(c, (50, 0, 0)), r9 + 7) - _tube(_add(c, (-51, 0, 0)), _add(c, (51, 0, 0)), r9)
                   + _unite([_tube(_add(c, (dx - 6, 0, 0)), _add(c, (dx + 6, 0, 0)), r9 + 9) - _tube(_add(c, (dx - 7, 0, 0)), _add(c, (dx + 7, 0, 0)), r9 + 7)
                             for dx in (-30, 30)]))
    add("fittings", "Tee, reducer and elbows", _unite(fittings), 7, "bought", "manifold")
    add("pipes", "Branch pipes, 90 mm PVC (5)", _unite(list(pipe_shapes.values())), 7, "made", "manifold")
    add("couplings", "Flexible couplings, 90 mm (2)", _unite(cpl), 7, "bought", "manifold")

    # ---- 8 inlet valve: full-bore 125 mm PVC-U gate valve with solvent-weld sockets (N6 option a,
    #      decided by Amish 2026-10-01), joined to the tee by a short piece of 125 mm pipe
    vx, vl, vs = p["valve_x"], p["valve_len"] / 2, p["valve_sock"]
    rp = p["penstock_od"] / 2
    rb = rp - 3.7                                                         # bore, as the SN8 pipe
    valve = (_tube((vx - vl, py, mz), (vx - vl + vs + 5, py, mz), rp + 8)  # upstream socket hub
             + _tube((vx + vl - vs - 5, py, mz), (vx + vl, py, mz), rp + 8)
             + _tube((vx - vl + vs + 5, py, mz), (vx + vl - vs - 5, py, mz), rp + 12)   # body
             + bx(vx - 40, vx + 40, py - 78, py + 78, mz, mz + 205)      # bonnet that takes the gate
             + bx(vx - 48, vx + 48, py - 86, py + 86, mz + 205, mz + 215)
             + zcyl(vx, py, mz + 215, mz + 300, 10)                       # stem
             + ztube(vx, py, mz + 290, mz + 302, 100, 86)                # 200 mm handwheel
             + bx(vx - 4, vx + 4, py - 92, py + 92, mz + 292, mz + 300) + bx(vx - 92, vx + 92, py - 4, py + 4, mz + 292, mz + 300))
    valve -= (_tube((vx - vl - 1, py, mz), (vx + vl + 1, py, mz), rb)
              + _tube((vx - vl - 1, py, mz), (vx - vl + vs, py, mz), rp) + _tube((vx + vl - vs, py, mz), (vx + vl + 1, py, mz), rp))
    nip = _tube((tx - 90 + sk, py, mz), (vx + vl - vs, py, mz), rp) - _tube((tx - 91 + sk, py, mz), (vx + vl - vs - 1, py, mz), rb)
    add("valve", "Inlet gate valve, 125 mm full bore, multi-turn", valve, 8, "bought", "valve")
    add("valve_fittings", "Pipe piece, 125 mm, tee to valve", nip, 8, "made", "valve")

    # ---- 9 penstock stub (site)
    add("penstock_stub", "Penstock, 125 mm PVC (stub)", _tube((p["stub_x"], py, mz), (vx - vl + vs, py, mz), p["penstock_od"] / 2), 9, "site", "penstock_stub")

    # ---- 18 pipe stands (three)
    st = []
    for x, y, ax in p["stands"]:
        zb = mz - r9 - 3
        s = bx(x - 50, x + 50, y - 50, y + 50, 0, 6)
        s += bx(x - 20, x + 20, y - 20, y - 16, 6, zb - 25) + bx(x - 20, x - 16, y - 20, y + 20, 6, zb - 25)
        s += bx(x - 30, x + 30, y - 30, y + 30, zb - 25, zb - 20)
        s += zcyl(x, y, zb - 20, zb, 8)
        ring = (_tube((x, y - 10, mz), (x, y + 10, mz), r9 + 3) - _tube((x, y - 11, mz), (x, y + 11, mz), r9)) if ax == "y" else \
               (_tube((x - 10, y, mz), (x + 10, y, mz), r9 + 3) - _tube((x - 11, y, mz), (x + 11, y, mz), r9))
        s -= zcyl(x + 35, y + 35, -1, 7, 5.5)
        st.append(s + ring)
    add("stands", "Pipe stands (3)", _unite(st), 18, "made", "stands")

    # ---- 10 forebay (site-placed at the top of the drop): tub, outlet connector, screen
    fx, fy, fz = -1700.0, -75.0, 1930.0
    tub = bx(fx - 280, fx + 280, fy - 230, fy + 230, fz, fz + 400) - bx(fx - 274, fx + 274, fy - 224, fy + 224, fz + 6, fz + 410)
    tub -= bx(fx - 280.5, fx - 274 + 0.5, fy - 100, fy + 100, fz + 360, fz + 401)       # overflow notch, upstream wall
    tub -= _tube((fx + 270, fy, fz + 110), (fx + 290, fy, fz + 110), 64)
    conn = (_tube((fx + 262, fy, fz + 110), (fx + 274, fy, fz + 110), 85) + _tube((fx + 280, fy, fz + 110), (fx + 300, fy, fz + 110), 85)
            + _tube((fx + 262, fy, fz + 110), (fx + 360, fy, fz + 110), 62.5)) - _tube((fx + 250, fy, fz + 110), (fx + 370, fy, fz + 110), 57)
    scr_frame = (bx(fx - 300, fx + 300, fy - 250, fy + 250, fz + 400, fz + 420) - bx(fx - 270, fx + 270, fy - 220, fy + 220, fz + 399, fz + 421))
    mesh = bx(fx - 290, fx + 290, fy - 240, fy + 240, fz + 403, fz + 405)
    add("forebay", "Forebay tub, drilled", tub, 10, "made", None)
    add("forebay_outlet", "Outlet tank connector, 125 mm", conn, 10, "bought", None)
    add("screen", "Intake screen, 6 mm mesh on a frame", scr_frame + mesh, 10, "made", None)

    # ---- 12 to 15 equipment post and electrics
    ex, ey = p["eq_post"]
    anchor = bx(ex - 75, ex + 75, ey - 75, ey + 75, 0, 5) + bx(ex - 40, ex - 35, ey - 35, ey + 35, 5, 155) + bx(ex + 35, ex + 40, ey - 35, ey + 35, 5, 155)
    add("post_base", "Bolt-down post anchor", anchor, 12, "bought", None)
    add("eq_post", "Equipment post, 70 mm timber", bx(ex - 35, ex + 35, ey - 35, ey + 35, 5, 1405), 12, "made", None)
    add("rectifier", "Rectifier box", bx(ex - 65, ex + 65, ey - 35 - 100, ey - 35, 845, 955), 13, "bought", None)
    add("controller", "Controller box", bx(ex - 130, ex + 130, ey - 35 - 110, ey - 35, 1030, 1230), 14, "bought", None)
    dump = bx(ex + 35, ex + 155, ey - 170, ey + 170, 540, 700) - bx(ex + 40, ex + 150, ey - 165, ey + 165, 545, 695)
    for k in range(-5, 6):
        dump -= bx(ex + 150, ex + 156, ey + 28 * k - 8, ey + 28 * k + 8, 560, 680)
    res = _tube((ex + 95, ey - 150, 585), (ex + 95, ey + 150, 585), 22) + bx(ex + 70, ex + 120, ey - 130, ey + 130, 640, 670)
    add("dump", "Dump-load and clamp resistors in a vented guard", dump + res, 15, "bought", None)
    return C


# ------------------------------------------------------------------ legacy groups (sizing, sheets, media)
ORDER = ("runner", "shaft", "bearing_mount", "coupling", "generator", "housing", "manifold", "valve",
         "penstock_stub", "frame")


def build_parts(params=None):
    """Return {group: shape} for the turbine unit, plus '_p' with the derived parameters and
    'fixings' and 'stands'."""
    C = build_components(params)
    out = {}
    for k, c in C.items():
        g = c.group or ("fixings" if c.kind == "fixing" else None)
        if g is None:
            continue
        out[g] = c.shape if g not in out else out[g] + c.shape
    out["_p"] = _derived({**PARAMS, **(params or {})})
    return out


def build(params=None):
    """Turbine unit assembly as one compound (frame, housing, rotor, bearings, generator, manifold, valve)."""
    from build123d import Compound
    parts = build_parts(params)
    return Compound(children=[parts[k] for k in ORDER + ("stands", "fixings")])


def pad_context(p=None):
    """The pad over the tailrace and the bank (site, grey); not in the BOM."""
    p = _derived({**PARAMS, **(p or {})})
    s = bx(-1250, 600, -350, 450, -120, 0)
    return s - bx(-160, 160, -160, 160, -130, 10)


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def _gap(a, b_):
    return a.distance_to(b_)


def checks(p=None):
    """Pairs that must touch, and pairs that must stay apart by a clearance (mm). Returns a list of
    (description, overlap volume mm3, gap mm, expectation, ok)."""
    b = _b()
    q = _derived({**PARAMS, **(p or {})})
    C = build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect, vtol=1e-3):
        v = _vol(a, b_)
        gp = _gap(a, b_)
        ok = v < vtol and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    def fits(desc, a, b_):
        """a sits inside a socket or bore of b_: they overlap only by design (contact)."""
        gp = _gap(a, b_)
        rows.append((desc, 0.0, gp, "touch", gp < 0.05))

    # frame and housing
    chk("Housing on the frame", S("housing"), S("frame"), "touch")
    chk("Housing clear of the pipe stops", S("housing") - bx(-500, 500, -500, 500, q["housing_z0"] + 25, 900), S("frame") - bx(-500, 500, -500, 500, -10, q["housing_z0"] + 0.5), 0.5)
    chk("Tie rods clear of the housing", S("tie_rods"), S("housing"), 20.0)
    chk("Tie rods through the frame (nuts on the angle)", S("tie_rods"), S("frame"), "touch")
    chk("Tie rods clear of the lid holes", S("tie_rods"), S("lid"), 0.4)
    chk("Tie rod washers on the lid", S("lid_nuts"), S("lid"), "touch")
    fits("Tie rod nuts on the rods", S("lid_nuts"), S("tie_rods"))
    chk("Anchors on the foot plates", S("anchors"), S("frame"), "touch", vtol=5e4)
    chk("Lid on the housing (in its groove)", S("lid"), S("housing"), "touch")
    # nozzles
    for k in ("nozzle_1", "nozzle_2"):
        chk(f"{C[k].name}: saddle on the gasket", S(k), S("gaskets"), "touch")
        chk(f"{C[k].name}: clear of the housing wall", S(k), S("housing"), 2.0)
        chk(f"{C[k].name}: clear of the runner", S(k), S("runner"), 15.0)
        chk(f"{C[k].name}: clear of the lid", S(k), S("lid"), 10.0)
        chk(f"{C[k].name}: clear of the frame and tie rods", S(k), S("frame") + S("tie_rods"), 20.0)
        chk(f"{C[k].name}: clear of the post rods", S(k), S("post_rods"), 5.0)
    chk("Gaskets on the housing", S("gaskets"), S("housing"), "touch")
    chk("Inserts in the nozzles", S("inserts"), S("nozzle_1") + S("nozzle_2"), "touch")
    lift = zcyl(0, 0, q["runner_bottom"], q["lid_z"], q["runner_od"] / 2)
    chk("Nozzles clear of the runner's lift path (lid lifted for service)", S("nozzle_1") + S("nozzle_2") + S("inserts") + S("saddle_bolts"), lift, 5.0)
    # jets: from the exit to the pitch point, clear of everything but the runner
    F = nozzle_frame(q)
    a = math.radians(q["jet_angle"])
    jet1 = _tube(F["X"], (0.0, q["runner_pcd"] / 2, q["strike_z"]), q["jet_d"] / 2)
    jets = jet1 + _rotz180(jet1)
    chk("Jets clear of the housing", jets, S("housing"), 5.0)
    chk("Jets clear of the clamping hub", jets, S("hub"), 5.0)
    rows.append(("Jet meets the pitch point at the top of the buckets", 0.0, q["bucket_top"] - q["strike_z"], 0.0,
                 0.0 <= q["bucket_top"] - q["strike_z"] <= 3.0))
    # rotor
    chk("Runner clear of the housing", S("runner"), S("housing"), 30.0)
    chk("Runner clear of the frame", S("runner"), S("frame"), 30.0)
    chk("Runner above normal tailwater", S("runner"), bx(-400, 400, -400, 400, -50, 0), 150.0)
    chk("Clamping hub on the runner", S("hub"), S("runner"), "touch")
    fits("Shaft through the clamping hub", S("shaft"), S("hub"))
    fits("Shaft through the runner hub", S("shaft"), S("runner"))
    chk("Clamping hub clear of the lid", S("hub"), S("lid"), 50.0)
    chk("Shaft clear of the lid hole", S("shaft"), S("lid"), 3.0)
    chk("V-ring on the lid underside", S("vring"), S("lid"), "touch")
    fits("V-ring on the shaft", S("vring"), S("shaft"))
    chk("Lower bearing unit on the lid", S("brg_low"), S("lid"), "touch")
    chk("Spacer sleeves on the lower unit", S("brg_sleeves"), S("brg_low"), "touch")
    chk("Upper unit on the spacer sleeves", S("brg_up"), S("brg_sleeves"), "touch")
    chk("Lower unit clear of the upper unit", S("brg_low"), S("brg_up"), 3.0)
    fits("Shaft in the bearing units", S("shaft"), S("brg_low") + S("brg_up"))
    chk("Bearing bolts clear of the shaft", S("brg_bolts"), S("shaft"), 10.0)
    chk("Bearing bolt heads under the lid", S("brg_bolts"), S("lid"), "touch")
    chk("Bearing bolt heads clear of the housing", S("brg_bolts"), S("housing"), 20.0)
    chk("Coupling clear of the upper unit", S("coupling"), S("brg_up"), 5.0)
    chk("Coupling clear of the guard", S("coupling"), S("guard"), 20.0)
    fits("Shaft in the coupling", S("shaft"), S("coupling"))
    chk("Guard in the lid groove", S("guard"), S("lid"), "touch")
    chk("Guard clear of the bearing units and bolts", S("guard"), S("brg_low") + S("brg_up") + S("brg_bolts"), 3.0)
    chk("Guard just under the plate", S("guard"), S("plate"), 0.5)
    chk("Posts on the lid", S("posts"), S("lid"), "touch")
    chk("Posts under the plate", S("posts"), S("plate"), "touch")
    chk("Post rod washers clear of the housing", S("post_rods"), S("housing"), 3.0)
    chk("Post rod washers on the plate", S("plate_nuts"), S("plate"), "touch")
    chk("Post rod nuts clear of the generator", S("plate_nuts"), S("generator"), 3.0)
    chk("Post rods clear of the nozzles' saddle bolts", S("post_rods"), S("saddle_bolts"), 3.0)
    chk("Generator on the plate", S("generator"), S("plate"), "touch")
    chk("Generator screw heads clear of the guard", S("gen_screws"), S("guard"), 2.0)
    chk("Generator clear of the post nuts", S("generator"), S("post_rods"), 3.0)
    fits("Generator shaft in the coupling", S("generator"), S("coupling"))
    # manifold
    pipes_all = S("fittings") + S("pipes") + S("couplings")
    chk("Pipework clear of the lid", pipes_all, S("lid"), 10.0)
    chk("Pipework clear of the frame, tie rods and housing", pipes_all, S("frame") + S("tie_rods") + S("housing"), 10.0)
    chk("Pipework clear of the post rods and plate", pipes_all, S("post_rods") + S("plate"), 10.0)
    fits("Nozzle spigots in the flexible couplings", S("couplings"), S("nozzle_1") + S("nozzle_2"))
    fits("Branch pipes in the flexible couplings", S("couplings"), S("pipes"))
    fits("Pipe stands under the branch pipes", S("stands"), S("pipes"))
    chk("Pipe stands clear of the frame", S("stands"), S("frame"), 30.0)
    chk("Valve handwheel clear of the pipework", S("valve"), S("pipes") + S("fittings"), 20.0)
    fits("Pipe piece in the tee's 125 mm run", S("valve_fittings"), S("fittings"))
    fits("Pipe piece in the valve's downstream socket", S("valve_fittings"), S("valve"))
    fits("Penstock in the valve's upstream socket", S("penstock_stub"), S("valve"))
    chk("Valve clear of the tee", S("valve"), S("fittings"), 20.0)
    chk("Valve clear of the pad", S("valve"), pad_context(), 20.0)
    return rows


def print_checks(p=None):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:66s} overlap {v:9.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


def export(out=None):
    from build123d import Compound, export_step, export_stl
    out = Path(out) if out else Path(__file__).resolve().parents[1]
    (out / "step").mkdir(parents=True, exist_ok=True)
    (out / "stl").mkdir(parents=True, exist_ok=True)
    asm = build()                 # separate build: a shape placed in a compound cannot be exported alone
    parts = build_parts()
    export_step(asm, str(out / "step" / "picoflow-turbine-assembly.step"))
    export_stl(asm, str(out / "stl" / "picoflow-turbine-assembly.stl"))
    for name in ("runner", "manifold", "housing", "bearing_mount"):
        export_step(parts[name], str(out / "step" / f"picoflow-{name}.step"))
        export_stl(parts[name], str(out / "stl" / f"picoflow-{name}.stl"))
    C = build_components()
    for key, name in (("nozzle_1", "nozzle"), ("inserts", "insert-pair-34mm"), ("gaskets", "saddle-gaskets")):
        export_step(C[key].shape, str(out / "step" / f"picoflow-{name}.step"))
        export_stl(C[key].shape, str(out / "stl" / f"picoflow-{name}.stl"))
    return parts


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    parts = export()
    p = parts["_p"]
    bb = build().bounding_box()
    print(f"Turbine unit envelope {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print(f"Nozzle centerline {p['jet_z']:.0f} mm above tailwater; runner underside {p['runner_bottom']:.0f} mm; "
          f"jet at the pitch point {p['strike_z']:.1f} mm, bucket top {p['bucket_top']:.1f} mm")
    rb = parts["runner"].bounding_box()
    print(f"Runner envelope {rb.size.X:.0f} x {rb.size.Y:.0f} x {rb.size.Z:.0f} mm, volume {parts['runner'].volume / 1e3:.0f} cm3")
    print(f"Branch lengths: jet 1 {p['branch_len_1']:.3f} m, jet 2 {p['branch_len_2']:.3f} m; shaft {p['shaft_len']:.0f} mm")
    print("Wrote cad/step/*.step and cad/stl/*.stl")
    print_checks()
