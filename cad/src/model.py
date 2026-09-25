"""PicoFlow parametric model (build123d), TRL 3 massing-plus level.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl.

Axes: Z up. Z = 0 is the normal tailwater surface under the turbine (the setting
height in R13 is measured from here). The turbine axis is vertical at X = Y = 0.
The penstock arrives horizontally from -X. Jet 1 strikes the runner pitch circle at
+Y travelling -X; jet 2 strikes it at -Y travelling +X, so the runner turns
counterclockwise seen from above and the two jet forces cancel radially.

Detail level: correct interfaces (runner hub on the shaft, two 6204 bearings in a
housing on the lid, jaw coupling, generator plate on four posts, nozzle inserts,
tee and valve on the penstock) and main dimensions. Not fabrication detail.
PRELIMINARY, NOT FOR FABRICATION.
"""
import math
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
    "runner_z": 235.0,         # runner mid-plane above tailwater
    # Jets (PCF-CAL-001 section 2)
    "jet_z": 280.0,            # nozzle exit centerline above tailwater (R13: 300 or less)
    "jet_angle": 20.0,         # jet angle below the runner plane, degrees
    "jet_d": 32.0,             # design-point insert bore (CAL-001 rounds to a stocked size)
    "nozzle_len": 170.0,       # converging nozzle length along the jet axis
    "nozzle_exit_x": 85.0,     # nozzle exit distance before the strike point, along X
    # Shaft, bearings, coupling
    "shaft_d": 20.0,           # 316 stainless
    "brg_od": 47.0,            # 6204-2RS: 20 x 47 x 14 mm
    "brg_w": 14.0,
    "brg_housing_d": 72.0,
    "brg_housing_h": 90.0,
    "coupling_d": 48.0,        # L-075 class jaw coupling envelope
    "coupling_len": 40.0,
    "post_d": 20.0,
    "post_h": 145.0,
    "post_offset": 120.0,
    "plate": 280.0,            # generator plate, square
    "plate_t": 10.0,
    "guard_d": 110.0,          # coupling guard
    # Generator (low-speed BLDC, new unit, decided 2026-09-25)
    "gen_d": 200.0,
    "gen_h": 90.0,
    # Housing, lid and frame
    "housing_od": 315.0,       # 315 mm PVC sewer pipe (SN4 class)
    "housing_wall": 7.7,
    "housing_z0": 80.0,        # housing bottom above tailwater
    "housing_h": 300.0,
    "lid": 400.0,
    "lid_t": 12.0,
    "frame": 420.0,            # frame outside size, square
    "frame_leg": 40.0,         # 40 mm galvanized angle (massing as square)
    # Pipework
    "penstock_od": 110.0,      # PVC drainage pipe
    "branch_od": 90.0,         # branches to the nozzles (CAL-001 section 1)
    "manifold_z": 338.0,       # manifold and branch centerline
    "tee_x": -400.0,
    "valve_x": -600.0,
    "stub_x": -900.0,          # end of the penstock stub in the model
    "branch_y": 260.0,         # far branch runs around the housing at this Y
    "branch_x": 330.0,
}


def _derived(p):
    d = dict(p)
    d["runner_bottom"] = p["runner_z"] - p["hub_h"] / 2
    d["lid_z"] = p["housing_z0"] + p["housing_h"]
    d["bh_z0"] = d["lid_z"] + p["lid_t"]
    d["plate_z0"] = d["bh_z0"] + p["post_h"]
    d["gen_z0"] = d["plate_z0"] + p["plate_t"] + 5.0
    d["coupling_z0"] = d["bh_z0"] + p["brg_housing_h"] + 8.0
    d["shaft_top"] = d["coupling_z0"] + p["coupling_len"] / 2
    d["shaft_len"] = d["shaft_top"] - d["runner_bottom"]
    a = math.radians(p["jet_angle"])
    d["nozzle_entry_x"] = p["nozzle_exit_x"] + p["nozzle_len"] * math.cos(a)
    d["nozzle_entry_z"] = p["jet_z"] + p["nozzle_len"] * math.sin(a)
    return d


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
        out = s if out is None else out + s
    return out


def build_parts(params=None):
    """Return {name: shape} for the turbine unit, plus '_p' with the derived parameters."""
    from build123d import Box, Cylinder, Pos, Rot
    p = _derived({**PARAMS, **(params or {})})
    R = p["runner_od"] / 2
    rz = p["runner_z"]

    # 1 Turgo runner: hub, web disc, outer rim and a band of inclined buckets
    hub = Pos(0, 0, rz) * (Cylinder(p["hub_d"] / 2, p["hub_h"]) - Cylinder(p["shaft_d"] / 2, p["hub_h"] + 2))
    web = Pos(0, 0, rz - 15) * (Cylinder(R - 8, 6) - Cylinder(p["hub_d"] / 2 - 1, 8))
    rim = Pos(0, 0, rz - 12) * (Cylinder(R, 12) - Cylinder(R - 8, 14))
    rb = p["runner_pcd"] / 2 - 5
    buckets = [Pos(rb * math.cos(math.radians(k * 360 / p["n_buckets"])),
                   rb * math.sin(math.radians(k * 360 / p["n_buckets"])), rz + 2)
               * Rot(0, 0, k * 360 / p["n_buckets"]) * Rot(35, 0, 0)
               * Box(p["bucket_len"], p["bucket_w"], p["bucket_h"]) for k in range(p["n_buckets"])]
    runner = hub + web + rim + _unite(buckets)

    # 2 Shaft
    shaft = Pos(0, 0, p["runner_bottom"] + p["shaft_len"] / 2) * Cylinder(p["shaft_d"] / 2, p["shaft_len"])

    # 3 Bearing housing (two 6204-2RS), posts, generator plate, coupling guard
    bh = Pos(0, 0, p["bh_z0"] + p["brg_housing_h"] / 2) * (
        Cylinder(p["brg_housing_d"] / 2, p["brg_housing_h"]) - Cylinder(p["shaft_d"] / 2 + 1, p["brg_housing_h"] + 2))
    flange = Pos(0, 0, p["bh_z0"] + 5) * (Box(120, 120, 10) - Cylinder(p["shaft_d"] / 2 + 1, 12))
    posts = _unite([Pos(sx * p["post_offset"], sy * p["post_offset"], p["bh_z0"] + p["post_h"] / 2)
                    * Cylinder(p["post_d"] / 2, p["post_h"]) for sx in (-1, 1) for sy in (-1, 1)])
    plate = Pos(0, 0, p["plate_z0"] + p["plate_t"] / 2) * (Box(p["plate"], p["plate"], p["plate_t"]) - Cylinder(30, p["plate_t"] + 2))
    g0 = p["bh_z0"] + p["brg_housing_h"]
    gh = p["plate_z0"] - g0
    guard = Pos(0, 0, g0 + gh / 2) * (Cylinder(p["guard_d"] / 2, gh) - Cylinder(p["guard_d"] / 2 - 2, gh + 2))
    bearing_mount = bh + flange + posts + plate + guard

    # 4 Jaw coupling
    coupling = Pos(0, 0, p["coupling_z0"] + p["coupling_len"] / 2) * Cylinder(p["coupling_d"] / 2, p["coupling_len"])

    # 5 Generator with its shaft down through the plate to the coupling
    generator = (Pos(0, 0, p["gen_z0"] + p["gen_h"] / 2) * Cylinder(p["gen_d"] / 2, p["gen_h"])
                 + Pos(0, 0, p["gen_z0"] + p["gen_h"] + 8) * Cylinder(40, 16)
                 + Pos(0, 0, (p["coupling_z0"] + p["coupling_len"] + p["gen_z0"]) / 2)
                 * Cylinder(p["shaft_d"] / 2, p["gen_z0"] - p["coupling_z0"] - p["coupling_len"] + 2))

    # 6 Housing (open bottom) and lid
    Ro = p["housing_od"] / 2
    shell = Pos(0, 0, p["housing_z0"] + p["housing_h"] / 2) * (
        Cylinder(Ro, p["housing_h"]) - Cylinder(Ro - p["housing_wall"], p["housing_h"] + 2))
    lid = Pos(0, 0, p["lid_z"] + p["lid_t"] / 2) * (Box(p["lid"], p["lid"], p["lid_t"]) - Cylinder(p["shaft_d"] / 2 + 4, p["lid_t"] + 2))
    housing = shell + lid

    # 7 Manifold, branches and two nozzles with inserts
    mz = p["manifold_z"]; rb_ = p["branch_od"] / 2; ypc = p["runner_pcd"] / 2
    ex, ez = p["nozzle_entry_x"], p["nozzle_entry_z"]
    tee = Pos(p["tee_x"], 0, mz) * Rot(90, 0, 0) * Cylinder(rb_ + 8, 2 * ypc + 30)
    # jet 2 at -Y, travelling +X
    b2 = [_tube((p["tee_x"], 0, mz), (p["tee_x"], -ypc, mz), rb_),
          _tube((p["tee_x"], -ypc, mz), (-ex, -ypc, ez), rb_)]
    n2 = _cone((-ex, -ypc, ez), (-p["nozzle_exit_x"], -ypc, p["jet_z"]), rb_, p["jet_d"] / 2 + 6)
    # jet 1 at +Y, travelling -X: the branch runs around the housing
    by, bx = p["branch_y"], p["branch_x"]
    b1 = [_tube((p["tee_x"], 0, mz), (p["tee_x"], by, mz), rb_),
          _tube((p["tee_x"], by, mz), (bx, by, mz), rb_),
          _tube((bx, by, mz), (bx, ypc, mz), rb_),
          _tube((bx, ypc, mz), (ex, ypc, ez), rb_)]
    n1 = _cone((ex, ypc, ez), (p["nozzle_exit_x"], ypc, p["jet_z"]), rb_, p["jet_d"] / 2 + 6)
    elbows = _unite([Pos(*c) * Cylinder(rb_ + 5, 2 * rb_ + 10) for c in
                     [(p["tee_x"], -ypc, mz), (p["tee_x"], by, mz), (bx, by, mz), (bx, ypc, mz)]])
    manifold = tee + _unite(b1 + b2) + n1 + n2 + elbows

    # 8 Inlet valve (slow-closing gate valve) with handwheel
    pr = p["penstock_od"] / 2; vx = p["valve_x"]
    valve = (Pos(vx, 0, mz) * Rot(0, 90, 0) * Cylinder(pr + 22, 90)
             + Pos(vx, 0, mz + 120) * Cylinder(28, 150)
             + Pos(vx, 0, mz + 200) * Cylinder(80, 12))

    # 9 Penstock stub (the site run is drawn in the concept media)
    penstock = _tube((p["stub_x"], 0, mz), (p["tee_x"], 0, mz), pr)

    # 11 Frame: four short legs and a top ring under the housing
    fs, fl = p["frame"], p["frame_leg"]
    legs = _unite([Pos(sx * (fs - fl) / 2, sy * (fs - fl) / 2, p["housing_z0"] / 2) * Box(fl, fl, p["housing_z0"])
                   for sx in (-1, 1) for sy in (-1, 1)])
    ring = Pos(0, 0, p["housing_z0"] - 15) * (Box(fs, fs, 30) - Box(fs - 2 * fl, fs - 2 * fl, 32))
    frame = legs + ring

    return {"runner": runner, "shaft": shaft, "bearing_mount": bearing_mount, "coupling": coupling,
            "generator": generator, "housing": housing, "manifold": manifold, "valve": valve,
            "penstock_stub": penstock, "frame": frame, "_p": p}


ORDER = ("runner", "shaft", "bearing_mount", "coupling", "generator", "housing", "manifold", "valve",
         "penstock_stub", "frame")


def build(params=None):
    """Turbine unit assembly as one compound."""
    from build123d import Compound
    parts = build_parts(params)
    return Compound(children=[parts[k] for k in ORDER])


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
    return parts


if __name__ == "__main__":
    parts = export()
    p = parts["_p"]
    bb = build().bounding_box()
    print(f"Turbine unit envelope {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print(f"Nozzle centerline {p['jet_z']:.0f} mm above tailwater; runner underside {p['runner_bottom']:.0f} mm")
    rb = parts["runner"].bounding_box()
    print(f"Runner envelope {rb.size.X:.0f} x {rb.size.Y:.0f} x {rb.size.Z:.0f} mm, volume {parts['runner'].volume / 1e3:.0f} cm3")
    print("Wrote cad/step/*.step and cad/stl/*.stl")
