"""PicoFlow prototype build plan pictures (PCF-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png          every component pulled apart, numbered in build order
    cad/drawings/PCF-DWG-101 to 114          making sketches for the made and drilled components
    docs/05-build-plan/lid-holes.png         lid hole and groove layout
    docs/05-build-plan/nozzle-hole-template  full-size template for the nozzle hole (PNG and PDF)
    docs/05-build-plan/joint-NN.png          close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png           one picture per assembly step
    docs/05-build-plan/wiring.png            block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model  # noqa: E402
from model import PARAMS, build_components, nozzle_frame, pad_context, _derived  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
P = _derived(PARAMS)
C = build_components()
REPO = "github.com/BoujeeEnjinia1701/picoflow"

COL = {"frame": "#78716C", "rods": "#374151", "housing": "#C4B5FD", "nozzle": "#2563EB", "gasket": "#111827",
       "insert": "#F59E0B", "lid": "#FDE68A", "brg": "#475569", "vring": "#B91C1C", "shaft": "#64748B",
       "runner": "#0F766E", "hub": "#A16207", "guard": "#6EE7B7", "posts": "#0E7490", "plate": "#94A3B8",
       "coupling": "#D4A017", "gen": "#1F2937", "stands": "#92400E", "pipes": "#E5E7EB", "fittings": "#60A5FA",
       "cpl": "#111827", "valve": "#DC2626", "pen": "#D1D5DB", "forebay": "#0EA5E9", "screen": "#64748B",
       "post": "#92400E", "rect": "#7C3AED", "ctrl": "#16A34A", "dump": "#C2410C", "bolt": "#111827", "pad": "#A8A29E"}


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


S = lambda *ks: _fuse([C[k].shape for k in ks])  # noqa: E731


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def pad(c=None):
    return part("Pad over the tailrace (site)", pad_context(), COL["pad"])


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "frame": part("Turbine frame", S("frame"), COL["frame"]),
        "tie_rods": part("Tie rods (4)", S("tie_rods", "lid_nuts"), COL["rods"]),
        "housing": part("Housing", S("housing"), COL["housing"]),
        "nozzle_1": part("Nozzle, jet 1, with gasket and insert", S("nozzle_1"), COL["nozzle"]),
        "nozzle_2": part("Nozzle, jet 2, with gasket and insert", S("nozzle_2"), COL["nozzle"]),
        "lid": part("Lid", S("lid"), COL["lid"]),
        "bearings": part("Flange bearing units, sleeves, bolts", S("brg_low", "brg_up", "brg_sleeves", "brg_bolts"), COL["brg"]),
        "vring": part("V-ring seal", S("vring"), COL["vring"]),
        "shaft": part("Shaft", S("shaft"), COL["shaft"]),
        "hub": part("Clamping hub", S("hub", "hub_screws"), COL["hub"]),
        "runner": part("Turgo runner", S("runner"), COL["runner"]),
        "guard": part("Guard", S("guard"), COL["guard"]),
        "posts": part("Posts and post rods (4)", S("posts", "post_rods", "plate_nuts"), COL["posts"]),
        "plate": part("Generator plate", S("plate"), COL["plate"]),
        "coupling": part("Jaw coupling", S("coupling"), COL["coupling"]),
        "generator": part("Generator", S("generator", "gen_screws"), COL["gen"]),
        "stands": part("Pipe stands (3)", S("stands"), COL["stands"]),
        "pipework": part("Tee, reducer, elbows, pipes, couplings", S("fittings", "pipes", "couplings"), COL["fittings"]),
        "valve": part("Inlet valve, full bore, and pipe piece", S("valve", "valve_fittings"), COL["valve"]),
        "penstock": part("Penstock stub (site)", S("penstock_stub"), COL["pen"]),
        "forebay": part("Forebay tub, outlet and screen", S("forebay", "forebay_outlet", "screen"), COL["forebay"]),
        "eqpost": part("Equipment post and anchor", S("eq_post", "post_base"), COL["post"]),
        "electrics": part("Rectifier, controller, resistor guard", S("rectifier", "controller", "dump"), COL["ctrl"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    m1, m2 = nozzle_frame(P)["back"], None
    off = {"frame": (0, 0, -640), "tie_rods": (0, 0, -470), "housing": (0, 0, -330),
           "nozzle_1": (260, 0, -330), "nozzle_2": (-260, 0, -330), "lid": (0, 0, 0),
           "bearings": (0, 0, 150), "vring": (0, 0, -60), "shaft": (480, -330, 470), "hub": (480, -330, 380),
           "runner": (480, -330, 290), "guard": (0, 0, 380), "posts": (0, 0, 380), "plate": (0, 0, 560),
           "coupling": (480, -330, 570), "generator": (0, 0, 730), "stands": (0, 0, -560), "pipework": (0, 0, -260),
           "valve": (0, 0, -60), "penstock": (-300, 0, -260), "forebay": (250, 0, -1250),
           "eqpost": (550, -100, -650), "electrics": (750, -300, -650)}
    order = ["frame", "tie_rods", "housing", "nozzle_1", "nozzle_2", "lid", "bearings", "vring", "shaft", "hub", "runner",
             "guard", "posts", "plate", "coupling", "generator", "stands", "pipework", "valve", "penstock", "forebay",
             "eqpost", "electrics"]
    parts = [mv(M[k], off[k]) for k in order]
    return bv.overview(parts, OUT / "overview.png", "PicoFlow prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; the penstock is a short stub",
                       elev=22, azim=-62, size=(12, 8.5), dpi=150, key=True)


def pipe_lengths():
    """Cut lengths of the five 90 mm pipes, from the model's fitting positions (mm)."""
    tx, py, by, bxx, yj = P["tee_x"], P["pen_y"], P["branch_y"], P["branch_x"], P["runner_pcd"] / 2
    fc, sk, sp = P["fit_c"], P["sock"], P["spigot_end_x"]
    return {"P1": (by - fc + sk) - (py + 80 - sk), "P2": (bxx - fc + sk) - (tx + fc - sk),
            "P3": (by - fc + sk) - (yj + fc - sk), "P4": (bxx - fc + sk) - sp, "P5": (tx + 160 - sk) * -1 - sp}


# ----------------------------------------------------------------- making sketches
def _sheet(*a, **k):
    """component_sheet, limited to the drawing numbers in $SHEETS when that is set."""
    import os
    only = os.environ.get("SHEETS")
    if only and k["dwg_no"] not in only.split(","):
        return None
    return bv.component_sheet(*a, **k)


def sheets():
    import build123d as b
    M = made()
    base = dict(project="PicoFlow", date=DATE)
    out = []
    F = nozzle_frame(P)
    hf = P["frame"] / 2

    # 101 frame
    out.append(_sheet(
        Part("Turbine frame", S("frame"), COL["frame"]), [M["housing"], M["tie_rods"]],
        dwg_no="PCF-DWG-101", title="PicoFlow turbine frame: making sketch",
        material="Bare steel angle 40 x 40 x 4 mm; flat 80 x 80 x 5 and 30 x 20 x 5 mm; galvanized or painted after welding",
        inset_view=(28, -55),
        notes=["Square: four 380 mm lengths of 40 x 40 x 4 angle, mitred 45 deg at each",
               "  end, horizontal legs pointing inward, top faces flat and level.",
               "  Weld the corners; check the diagonals agree within 2 mm.",
               "Legs: four 70 mm lengths of the same angle, fitted inside each corner,",
               "  tight under the horizontal legs and against the vertical legs; weld.",
               "Feet: four 80 x 80 x 5 mm plates welded under the legs, reaching",
               "  outward; one 13 mm anchor hole in each, 208 mm from the centre lines.",
               "Pipe stops: four 30 x 20 x 5 mm flat bars welded upright on the",
               "  horizontal legs at the middle of each side, inner face 158.5 mm",
               "  from the centre (1 mm outside the housing).",
               "Tie rod holes: 11 mm in each corner, 170 mm from both centre lines.",
               "Clean the welds, then galvanize or paint the whole frame. Never weld after galvanizing.",
               "Check: top flat within 1 mm; the housing drops in between the stops."],
        **base))

    # 102 housing, drilled
    out.append(_sheet(
        Part("Housing", S("housing"), COL["housing"]), [M["frame"], M["nozzle_1"], M["nozzle_2"], M["lid"]],
        dwg_no="PCF-DWG-102", title="PicoFlow housing: making sketch", material="315 mm PVC sewer pipe, SN4 (7.7 mm wall)",
        inset_view=(22, -40),
        notes=["Cut 303 mm of 315 mm pipe. Wrap a strip of card round the pipe as a",
               "  guide, saw square with a fine-tooth saw, and file both ends flat.",
               "Two nozzle holes, on opposite sides, each with four bolt holes. Tape the",
               "  full-size template (nozzle hole template) to the pipe: its centre line",
               "  is 208.6 mm up from the bottom end; the second hole is the same,",
               "  turned half a turn round the pipe.",
               "Chain drill inside the hole outline with 6 mm, cut out with a jigsaw,",
               "  file to the line. Drill the eight bolt holes 6.6 mm square to the wall.",
               "The holes are larger than the nozzle tip by 2.5 mm all round; the",
               "  nozzle saddle and its gasket cover them.",
               "The 3 mm at the top sits in the groove under the lid.",
               "Check: each nozzle passes through its hole without touching the edge."],
        **base))

    # 103 nozzle (shown laid with its spigot along X)
    nz = S("nozzle_1")
    out.append(_sheet(
        Part("Nozzle", nz, COL["nozzle"]), [M["housing"], M["pipework"], M["runner"]],
        dwg_no="PCF-DWG-103", title="PicoFlow nozzle (make 2, both the same): making sketch",
        material="PETG, 3D printed, 4 mm walls, 40 % infill", inset_view=(35, -30),
        notes=["Print two from the model file (cad/step/picoflow-nozzle.step). They are",
               "  the same part: jet 2's nozzle is jet 1's turned half a turn.",
               "Print standing on the spigot end, with supports under the saddle;",
               "  the part fits a 167 x 130 x 244 mm space, about 300 g and 12 h each.",
               "Spigot: 90 mm outside, 60 mm long, horizontal. A gentle 20 deg bend",
               "  turns the nozzle down to the runner. Cone 170 mm long, from 90 mm",
               "  to 64 mm outside. Saddle: a patch 144 mm across shaped to the",
               "  housing, 6 mm thick, four 6.6 mm bolt holes.",
               "Tip: a 50 mm seat 25 mm deep for the insert, and two 5.6 mm holes",
               "  for M4 heat-set inserts, 28.5 mm each side of the centre.",
               "Fit: the tip goes through the housing hole; the saddle sits on a 2 mm",
               "  EPDM gasket, four M6 bolts, nuts inside. The spigot joins the pipe",
               "  in a 90 mm flexible coupling.",
               "Check: spigot 90 mm (fits the coupling); saddle sits on the pipe."],
        **base))

    # 104 insert
    ins = S("inserts") & model.bx(0, 400, 0, 400, 0, 600)
    out.append(_sheet(
        Part("Nozzle insert", ins, COL["insert"]), [M["nozzle_1"]],
        dwg_no="PCF-DWG-104", title="PicoFlow nozzle insert (make 2 per size): making sketch",
        material="PETG, 3D printed, 100 % infill", inset_view=(10, -165),
        view_shape=b.Plane(origin=F["X"], x_dir=(0, 1, 0), z_dir=F["back"]).to_local_coords(ins),
        notes=["Print a pair for each size used: 34 mm bore for the design point.",
               "  A set from 20 to 45 mm covers the head and flow range.",
               "Body: 50 mm outside, 25 mm long, fits the seat in the nozzle tip.",
               "Flange: 64 mm across, 3 mm thick, with two 4.4 mm holes 57 mm apart.",
               "Bore: converges smoothly from 46 mm at the back to the jet size at",
               "  the front face; the last few millimetres must be round and sharp.",
               "Print with the front face down on the bed so the jet edge is clean.",
               "Ream or sand the bore to size; check it with a caliper.",
               "Fit: slide into the nozzle tip from inside the housing, two M4",
               "  screws into the heat-set inserts.",
               "Check: the bore is within 0.2 mm of size and round."],
        **base))

    # 105 lid
    out.append(_sheet(
        Part("Lid", S("lid"), COL["lid"]), [M["housing"], M["bearings"], M["guard"], M["posts"], M["tie_rods"]],
        dwg_no="PCF-DWG-105", title="PicoFlow lid: making sketch", material="HDPE sheet 12 mm (or marine plywood, sealed)",
        inset_view=(30, -50),
        notes=["Cut 400 x 400 mm; round the corners to about 5 mm.",
               "Holes from the centre (the lid hole layout figure gives all of them):",
               "  shaft 28 mm in the centre; bearing bolts 11 mm at 32 each way;",
               "  post rods 11 mm at 125 each way; tie rods 11 mm at 170 each way.",
               "Underneath: a ring groove 3 mm deep, 148.8 to 158.5 mm radius, that",
               "  the top of the housing sits in. Rout with a trammel jig.",
               "On top: a ring groove 2 mm deep, 75.5 to 80.5 mm radius, for the guard.",
               "Mark the two grooves from the same centre as the shaft hole.",
               "Fit: housing in the lower groove; lower bearing unit, posts and guard",
               "  on top; four tie rods through the corners with washers and nuts.",
               "Check: the lid drops onto the housing and the groove takes the",
               "  whole rim without forcing."],
        **base))

    # 106 shaft (laid along X)
    sh = S("shaft")
    out.append(_sheet(
        Part("Shaft", sh, COL["shaft"]), [M["bearings"], M["runner"], M["coupling"], M["lid"]],
        dwg_no="PCF-DWG-106", title="PicoFlow shaft: making sketch", material="316 stainless steel bar, 20 mm, h9 or ground",
        view_shape=b.Rot(0, 90, 0) * b.Pos(0, 0, -(P["runner_bottom"] + P["shaft_len"] / 2)) * sh, inset_view=(20, -40),
        notes=[f"Cut {P['shaft_len']:.0f} mm of 20 mm ground stainless bar; face both ends",
               "  square and chamfer them 1 mm so the bearings slide on.",
               "Check the bar slides through a bearing unit by hand; polish any",
               "  burr with fine emery.",
               "No keyways: the runner hub and coupling clamp the shaft, and the",
               "  bearing inserts lock with their own set screws.",
               "At assembly, spot each set screw into the shaft with a 5 mm drill",
               "  0.5 mm deep through the screw hole, then tighten.",
               "Fit: bottom end flush with the underside of the runner hub; top end",
               "  half way into the jaw coupling, 30 mm above the upper bearing.",
               "Check: straight within 0.1 mm over its length (roll it on glass)."],
        **base))

    # 107 runner
    out.append(_sheet(
        Part("Turgo runner", S("runner"), COL["runner"]), [M["shaft"], M["hub"], M["bearings"], M["lid"]],
        dwg_no="PCF-DWG-107", title="PicoFlow Turgo runner: making sketch", material="PETG (prototype), glass-filled nylon (field)",
        inset_view=(-25, -40),
        notes=["Print from the model file (cad/step/picoflow-runner.step), hub down,",
               "  with supports under the buckets. 200 mm across, 50 mm tall,",
               "  about 525 g and 21 h at 0.4 mm; four perimeters.",
               "20 buckets on a 150 mm pitch circle; the jets strike the top of the",
               "  bucket band, which is 17 mm above the runner's mid-height.",
               "Hub: 80 mm across, 50 mm tall, 20 mm bore. Ream the bore to slide",
               "  on the shaft. Press four M5 heat-set inserts into the hub top on",
               "  a 44 mm circle with a soldering iron.",
               "Balance: hang the runner on a rod through the bore; if one side",
               "  always drops, sand the bucket backs on that side lightly.",
               "Fit: the clamping hub bolts to the hub top with four M5 screws.",
               "Check: the runner spins on a rod and stops in random places."],
        **base))

    # 108 guard
    out.append(_sheet(
        Part("Guard", S("guard"), COL["guard"]), [M["lid"], M["bearings"], M["plate"], M["coupling"]],
        dwg_no="PCF-DWG-108", title="PicoFlow bearing and coupling guard: making sketch", material="160 mm PVC pipe, 4 mm wall",
        inset_view=(25, -50),
        notes=["Cut 146 mm of 160 mm pipe; saw square, file both ends flat and",
               "  deburr inside.",
               "Drill two 6 mm holes at the bottom edge, on opposite sides, so any",
               "  water that gets in drains out.",
               "Fit: the bottom end stands in the 2 mm groove on top of the lid; the",
               "  top end stops 1 mm under the generator plate, which holds it in place.",
               "It covers both bearing units and the jaw coupling; nothing that turns",
               "  can be reached while the plate is on.",
               "Check: it stands in the groove and the plate clears it."],
        **base))

    # 109 post
    po = P["post_offset"]
    post1 = model.ztube(po, po, P["bh_z0"], P["plate_z0"], 10, 8)
    out.append(_sheet(
        Part("Post", post1, COL["posts"]), [M["lid"], M["plate"], M["guard"]],
        dwg_no="PCF-DWG-109", title="PicoFlow post and spacer sleeve (make 4 of each): making sketch",
        material="Steel tube 20 x 2 mm; M10 threaded rod", view_shape=b.Pos(-po, -po, -P["bh_z0"]) * post1, inset_view=(25, -50),
        notes=["Posts: cut four 145.0 mm lengths of 20 x 2 mm steel tube. Face the",
               "  ends square on a disc sander; all four the same within 0.2 mm,",
               "  so the plate sits level.",
               "Post rods: cut four 195 mm lengths of M10 rod; clean the thread ends.",
               "Bearing spacer sleeves: cut four 24.0 mm lengths of 20 mm tube with",
               "  a 10.5 mm or larger bore, the same within 0.1 mm.",
               "Tie rods: cut four 345 mm lengths of M10 rod.",
               "Paint or galvanize the cut ends.",
               "Fit: each post stands on the lid at 125 mm each way from the centre;",
               "  the rod goes up from under the lid, through the post and the plate,",
               "  with a 30 mm washer and nut under the lid and a washer and nut on",
               "  the plate.",
               "Check: the four posts stand the same height on a flat surface."],
        **base))

    # 110 generator plate
    out.append(_sheet(
        Part("Generator plate", S("plate"), COL["plate"]), [M["posts"], M["generator"], M["guard"]],
        dwg_no="PCF-DWG-110", title="PicoFlow generator plate: making sketch", material="Aluminium plate 8 mm, 5083 or 6082",
        inset_view=(30, -50),
        notes=["Cut 280 x 280 mm; file the edges and round the corners.",
               "Centre hole 62 mm for the generator shaft and spigot (check the",
               "  generator: the hole must clear its spigot by 1 mm).",
               "Post holes 11 mm at 125 mm each way from the centre.",
               "Generator screw holes 6.6 mm on a 176 mm circle at 45 deg (the model's",
               "  figure; copy the circle and angle from the generator bought).",
               "Mark the centre from the diagonals so the shaft lines up with the",
               "  bearings below.",
               "Fit: sits on the four posts, nuts on top; generator on top, four M6",
               "  screws from below; the guard stops 1 mm under it.",
               "Check: the plate sits on all four posts without rocking."],
        **base))

    # 111 pipe stand
    x, y, _ = P["stands"][1]
    st = S("stands") & model.bx(x - 80, x + 80, y - 80, y + 80, -1, 400)
    out.append(_sheet(
        Part("Pipe stand", st, COL["stands"]), [M["pipework"]],
        dwg_no="PCF-DWG-111", title="PicoFlow pipe stand (make 3): making sketch",
        material="Bare steel angle 40 x 40 x 4 mm, flat 100 x 100 x 6 and 60 x 60 x 5 mm; galvanized or painted after welding",
        view_shape=b.Pos(-x, -y, 0) * st, inset_view=(25, -60),
        notes=["Upright: 259 mm of 40 x 40 x 4 angle, ends square.",
               "Foot: 100 x 100 x 6 mm plate, one 11 mm anchor hole 35 mm in from",
               "  two edges; weld the upright to it in the middle, square.",
               "Top: 60 x 60 x 5 mm plate with a 9 mm hole in the middle, welded",
               "  square on top of the upright.",
               "Clip: a 90 mm pipe clip with an M8 boss, screwed onto an",
               "  M8 bolt up through the top plate. The clip's band holds the pipe.",
               "Height: pad to the bottom of the pipe 290 mm; adjust on the M8",
               "  thread if the pad is uneven.",
               "Fit: one under the tee branch, one under the long run, one under",
               "  the short drop to jet 1 (overview); M10 anchors in the pad.",
               "Check: the pipe sits in the clip without being pushed up or down."],
        **base))

    # 112 manifold pipework (cut list)
    L_ = pipe_lengths()
    pw = S("fittings", "pipes", "couplings")
    out.append(_sheet(
        Part("Pipework", pw, COL["fittings"]), [M["housing"], M["nozzle_1"], M["nozzle_2"], M["stands"], M["valve"]],
        dwg_no="PCF-DWG-112", title="PicoFlow nozzle manifold pipework: cutting and fitting sketch",
        material="90 mm PVC pipe and fittings; 125 x 90 mm reducing tee and reducer",
        view_shape=pw, inset_view=(35, -60),
        notes=["Cut five lengths of 90 mm pipe (for sockets 45 mm deep; adjust",
               "  each by the difference if your fittings differ):",
               f"  P1 tee branch to first elbow, {L_['P1']:.0f} mm; P2 long run, {L_['P2']:.0f} mm;",
               f"  P3 short drop, {L_['P3']:.0f} mm; P4 last elbow to jet 1 coupling, {L_['P4']:.0f} mm;",
               f"  P5 reducer to jet 2 coupling, {L_['P5']:.0f} mm.",
               "The valve's pipe piece enters the 125 mm run of the tee; the other end takes",
               "  a 125 x 90 reducer and P5 to jet 2. The 90 mm side branch takes",
               "  P1, then elbows and P2, P3, P4 round the housing to jet 1.",
               "Dry fit everything on the stands first. Then solvent weld the PVC",
               "  joints, one at a time, keeping the elbows square.",
               "Flexible couplings join P4 and P5 to the nozzle spigots; band clamps",
               "  snug, not crushed. Do not glue the nozzles.",
               "Check: centre line 338 mm above the pad all round."],
        **base))

    # 113 forebay
    fb = S("forebay", "forebay_outlet", "screen")
    out.append(_sheet(
        Part("Forebay", fb, COL["forebay"]), [],
        dwg_no="PCF-DWG-113", title="PicoFlow forebay tub and intake screen: making sketch",
        material="Polyethylene tub; 6 mm stainless mesh; aluminium angle 20 x 20 x 3 mm",
        view_shape=b.Pos(1700, 75, -1930) * fb, inset_view=(30, -60),
        notes=["Tub: about 560 x 460 x 400 mm outside, stiff polyethylene.",
               "Outlet: 128 mm hole centred 110 mm up in the downstream end, for a",
               "  125 mm tank connector (gasket inside, nut outside).",
               "Overflow: cut a notch 200 mm wide and 40 mm deep in the upstream",
               "  rim, so surplus water and leaves run off away from the outlet.",
               "Screen frame: 20 x 20 x 3 mm aluminium angle, 600 x 500 mm",
               "  outside, mitred and riveted; it rests on the rim and overlaps it",
               "  by 10 mm all round.",
               "Screen: 6 mm stainless mesh cut to 580 x 480 mm, riveted to the frame.",
               "The stream is led onto the screen; water drops through, surplus runs",
               "  over and carries leaves away.",
               "Check: no gap larger than 6 mm anywhere round the screen."],
        **base))

    # 114 equipment post
    ep = S("eq_post")
    ex, ey = P["eq_post"]
    out.append(_sheet(
        Part("Equipment post", ep, COL["post"]), [M["electrics"], part("Anchor", S("post_base"), "#9CA3AF")],
        dwg_no="PCF-DWG-114", title="PicoFlow equipment post: making sketch", material="Treated timber 70 x 70 mm; bolt-down post anchor",
        view_shape=b.Pos(-ex, -ey, 0) * ep, inset_view=(25, -50),
        notes=["Cut 1,400 mm of 70 x 70 mm treated timber; seal the cut ends.",
               "Bolt-down post anchor: drop the post in, drill through the anchor's",
               "  side holes and bolt with two M10 coach bolts.",
               "Mark the boxes on the front face (the face toward the turbine):",
               "  rectifier box 840 to 960 mm up; controller box 1,030 to 1,230 mm.",
               "Resistor guard on the side face, 540 to 700 mm up, with 50 mm air",
               "  space all round and nothing that burns within 300 mm above it.",
               "Fix each box with four stainless screws through its own mounting",
               "  holes; cable glands face down.",
               "Site: on ground above flood level, at least 1 m from the stream bank.",
               "Check: the post stands upright and does not rock in its anchor."],
        **base))
    return out


# ----------------------------------------------------------------- layouts (matplotlib)
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Rectangle, Circle, Wedge
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    res = []
    OUT.mkdir(parents=True, exist_ok=True)

    # ---- lid, seen from above
    fig = plt.figure(figsize=(10, 8.6), dpi=150)
    ax = fig.add_axes([0.04, 0.07, 0.6, 0.84]); ax.set_aspect("equal"); ax.set_axis_off()
    L = P["lid"] / 2
    ax.add_patch(Rectangle((-L, -L), 2 * L, 2 * L, fc="#F5F5F4", ec=INK, lw=1.2))
    ro, ri = P["housing_od"] / 2, P["housing_od"] / 2 - P["housing_wall"]
    ax.add_patch(Wedge((0, 0), ro + 1, 0, 360, width=ro + 1 - (ri - 0.5), fc="#DBEAFE", ec=MUT, lw=0.6, ls="--"))
    gr = P["guard_d"] / 2
    ax.add_patch(Wedge((0, 0), gr + 0.5, 0, 360, width=P["guard_wall"] + 1, fc="#FDE68A", ec=MUT, lw=0.6))
    J = P["brg_unit"][1] / 2
    for r, xy, lab in ((14, [(0, 0)], None),
                       (5.5, [(sx * J, sy * J) for sx in (-1, 1) for sy in (-1, 1)], None),
                       (5.5, [(sx * 125, sy * 125) for sx in (-1, 1) for sy in (-1, 1)], None),
                       (5.5, [(sx * 170, sy * 170) for sx in (-1, 1) for sy in (-1, 1)], None)):
        for x, y in xy:
            ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1))
            ax.plot([x - r - 3, x + r + 3], [y, y], color=MUT, lw=0.4); ax.plot([x, x], [y - r - 3, y + r + 3], color=MUT, lw=0.4)
    for v in (32, 125, 170):
        ax.plot([v, v], [-L, -L - 14], color=AC, lw=0.4, ls=":")
        ax.text(v, -L - 16, f"{v}", ha="center", va="top", fontsize=8, color=AC)
        ax.plot([L, L + 12], [v, v], color=AC, lw=0.4, ls=":")
        ax.text(L + 14, v, f"{v}", ha="left", va="center", fontsize=8, color=AC)
    ax.text(0, -L - 34, "from the centre, mm (same each way)", ha="center", fontsize=8, color=MUT)
    ax.plot([-L - 6, L + 6], [0, 0], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3))); ax.plot([0, 0], [-L - 6, L + 6], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    ax.set_xlim(-L - 10, L + 50); ax.set_ylim(-L - 44, L + 10)
    fig.text(0.04, 0.975, "Lid: holes and grooves", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.945, "Seen from above. Full size figures in mm, taken from the model. The lid is square, so it can go on any way round.",
             fontsize=8.5, color=MUT, va="top")
    key = ["Shaft hole 28, in the centre", "Bearing bolt holes 11, at 32", "Post rod holes 11, at 125", "Tie rod holes 11, at 170", "",
           "Blue ring, underneath: groove 3 deep,", "  radius 148.8 to 158.5, for the", "  top of the housing", "",
           "Yellow ring, on top: groove 2 deep,", "  radius 75.5 to 80.5, for the guard", "",
           "Lid 400 x 400 x 12, HDPE"]
    fig.text(0.68, 0.86, "What each opening is (mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(key):
        fig.text(0.68, 0.83 - i * 0.024, t, fontsize=8, color=INK, va="top")
    fig.text(0.04, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.96, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "lid-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "lid-holes.png")

    # ---- nozzle hole template: the housing outside surface unrolled, full size
    F = nozzle_frame(P)
    back = np.array(F["back"]); T = np.array(F["T"]); N = np.array(F["N"])
    fwd = -back
    a0 = T + 12 * fwd
    r0, r1 = P["nozzle_rex"] + 2.5, P["branch_od"] / 2 + 2.5
    Lc = np.linalg.norm(N - a0)
    W = F["W"]
    th0 = math.atan2(W[1], W[0])
    th = np.linspace(th0 - 0.6, th0 + 0.6, 1800)
    zz = np.linspace(W[2] - 90, W[2] + 90, 1400)
    TH, ZZ = np.meshgrid(th, zz)
    pts = np.stack([ro * np.cos(TH), ro * np.sin(TH), ZZ], -1)
    rel = pts - a0
    s = rel @ ((N - a0) / Lc)
    rad = np.linalg.norm(rel - s[..., None] * ((N - a0) / Lc), axis=-1)
    inside = (s >= 0) & (s <= Lc) & (rad <= r0 + (r1 - r0) * s / Lc)
    U = (TH - th0) * ro             # arc length from the saddle centre, mm
    zc = W[2] - P["housing_z0"]     # hole centre height above the housing bottom
    V = ZZ - W[2]                   # up from the hole centre
    fig = plt.figure(figsize=(210 / 25.4, 297 / 25.4), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-105, 105); ax.set_ylim(-150, 147); ax.set_axis_off()
    oy = -10.0                      # page position of the hole centre
    ax.contour(U, V + oy, inside.astype(float), levels=[0.5], colors=[INK], linewidths=1.2)
    for st in (-1, 1):
        for sz in (-1, 1):
            u, z = st * 48.0, sz * 48.0 + oy
            ax.add_patch(Circle((u, z), 3.3, fc="none", ec=INK, lw=1.0))
            ax.plot([u - 6, u + 6], [z, z], color=MUT, lw=0.4); ax.plot([u, u], [z - 6, z + 6], color=MUT, lw=0.4)
    t = np.linspace(0, 2 * math.pi, 200)
    ax.plot(P["saddle_r"] * np.cos(t), oy + P["saddle_r"] * np.sin(t), color=MUT, lw=0.6, ls="--")
    ax.plot([0, 0], [oy - 95, oy + 95], color=MUT, lw=0.4, ls=(0, (8, 3, 2, 3)))
    ax.plot([-100, 100], [oy, oy], color=AC, lw=0.8)
    ax.annotate("", xy=(0, oy + 104), xytext=(0, oy + 88), arrowprops=dict(arrowstyle="-|>", color=AC, lw=1.2))
    ax.text(3, oy + 100, "UP", fontsize=8, color=AC, fontweight="bold", va="center")
    ax.text(100, oy + 2, f"{zc:.1f} mm up", fontsize=6.5, color=AC, va="bottom", ha="right")
    ax.text(-100, oy - 82, "<- the nozzle's spigot runs off this way (left and up)", fontsize=7, color=INK)
    ax.text(-100, 141, "PicoFlow nozzle hole template (one per nozzle)", fontsize=10, fontweight="bold", color=INK, va="top")
    ax.text(-100, 134, "Print the PDF at 100 % (actual size) on A4 and check the 50 mm bar. Mark a line round the housing\n"
            f"{zc:.1f} mm up from its bottom end. Seen from outside, wrap the sheet on the pipe with UP upward and the\n"
            "green line on your mark. Solid line: the hole to cut. Small circles: 6.6 mm bolt holes. Dashed circle: the\n"
            "saddle outline. The second hole is the same, half way round the pipe. Distances are round the pipe surface.",
            fontsize=6.5, color=MUT, va="top", linespacing=1.4)
    ax.plot([-100, -50], [-125, -125], color=INK, lw=2); ax.text(-75, -123, "50 mm", ha="center", fontsize=7, color=INK)
    ax.text(-100, -141, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=6, color="#B45309")
    ax.text(100, -141, REPO, fontsize=6, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "nozzle-hole-template.pdf", facecolor="white")
    fig.savefig(OUT / "nozzle-hole-template.png", facecolor="white")
    plt.close(fig); res += [OUT / "nozzle-hole-template.png", OUT / "nozzle-hole-template.pdf"]
    return res


# ----------------------------------------------------------------- joints
def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & model.bx(x0, x1, y0, y1, z0, z1)


def joints():
    import os

    # limit drawing to the joint numbers in $JOINTS when that is set
    only = os.environ.get("JOINTS")
    _joint = bv.joint

    class _BV:
        def __getattr__(self, k):
            if k != "joint" or not only:
                return getattr(bv, k)
            return lambda parts, out, *a, **kw: (_joint(parts, out, *a, **kw)
                                                 if str(int(Path(out).stem.split("-")[1])) in only.split(",") else None)
    bvj = _BV()
    out = []
    hf = P["frame"] / 2
    z0h = P["housing_z0"]
    # 01 frame corner, cut along the corner's diagonal
    import build123d as b
    half = b.Rot(0, 0, 45) * b.Pos(0, -500, 0) * b.Box(3000, 1000, 2000)      # keeps y <= x
    bx_ = (110, 240, 110, 240, -30, 120)
    cut1 = lambda sh: win(sh, *bx_) & half  # noqa: E731
    out.append(bvj.joint([
        part("Frame square (angle, horizontal leg inward)", cut1(S("frame")) & model.bx(100, 240, 100, 240, 40, 130), COL["frame"]),
        part("Leg (angle) and foot plate, welded", cut1(S("frame")) & model.bx(100, 240, 100, 240, -1, 40), "#A8A29E"),
        part("Tie rod, nuts above and below the angle", cut1(S("tie_rods")), COL["rods"]),
        part("M12 anchor into the pad", cut1(S("anchors")), COL["bolt"])],
        OUT / "joint-01.png", "Joint 1: frame corner, leg, foot and tie rod (cut along the corner's diagonal)",
        subtitle="The leg is welded into the corner under the angle; the tie rod is locked to the angle by two nuts; the anchor is outside the corner",
        elev=12, azim=135, size=(8, 6)))
    # 02 housing on the frame at a pipe stop (cut through the middle of the +X side)
    bx_ = (120, 200, -25, 0, 60, 130)
    out.append(bvj.joint([
        part("Frame angle", win(S("frame"), *bx_) - model.bx(150, 200, -25, 0, z0h + 0.5, 130), COL["frame"]),
        part("Pipe stop, welded to the angle", win(S("frame"), *bx_) & model.bx(150, 200, -25, 0, z0h + 0.5, 130), "#B45309"),
        part("Housing wall, 7.7 mm", win(S("housing"), *bx_), COL["housing"])],
        OUT / "joint-02.png", "Joint 2: housing on the frame, at a pipe stop (cut open)",
        subtitle="The housing wall stands on the horizontal leg of the angle; the stop is 1 mm outside it",
        elev=15, azim=70, size=(8, 6)))
    # 03 nozzle saddle on the housing, from outside
    W = P["wall_pt"]
    bx_ = (60, 400, -20, 200, 200, 400)
    out.append(bvj.joint([
        part("Housing", win(S("housing"), 60, 260, -20, 200, 200, 380), COL["housing"]),
        part("Gasket, 2 mm EPDM", win(S("gaskets"), *bx_), COL["gasket"]),
        part("Nozzle saddle", win(S("nozzle_1"), *bx_), COL["nozzle"]),
        part("M6 bolts, nuts inside", win(S("saddle_bolts"), *bx_), "#6B7280")],
        OUT / "joint-03.png", "Joint 3: nozzle saddle on the housing (jet 1, outside)",
        subtitle="The printed saddle is shaped to the pipe and sits on a gasket; four M6 bolts go through the wall",
        elev=20, azim=35, size=(8, 6)))
    # 04 nozzle tip and insert, cut through the jet's centre line
    yj = P["runner_pcd"] / 2
    bx_ = (60, 230, yj, yj + 60, 220, 360)
    out.append(bvj.joint([
        part("Housing wall (cut)", win(S("housing"), *bx_), COL["housing"]),
        part("Nozzle (cut)", win(S("nozzle_1"), *bx_), COL["nozzle"]),
        part("Insert, 34 mm bore (cut)", win(S("inserts"), *bx_), COL["insert"]),
        part("Gasket", win(S("gaskets"), *bx_), COL["gasket"]),
        part("Runner", win(S("runner"), 0, 230, yj, yj + 60, 150, 360), COL["runner"])],
        OUT / "joint-04.png", "Joint 4: nozzle tip and insert, cut through the jet's centre line",
        subtitle="The insert sits in the tip from inside the housing, held by two M4 screws; the jet leaves just inside the wall",
        elev=4, azim=-90, size=(8, 6)))
    # 05 lid on the housing, cut through the +X side
    bx_ = (110, 205, -20, 0, 340, 400)
    out.append(bvj.joint([
        part("Lid (cut)", win(S("lid"), *bx_), COL["lid"]),
        part("Housing (cut)", win(S("housing"), *bx_), "#64748B")],
        OUT / "joint-05.png", "Joint 5: lid on the housing (cut open)",
        subtitle="The top of the housing sits 3 mm up in a groove under the lid; the tie rods clamp the lid down",
        elev=8, azim=80, size=(8, 6)))
    # 06 bearing stack, cut in half
    zl = P["lid_z"]
    bx_ = (-60, 60, -60, 0, zl - 15, P["brg_top"] + 8)
    out.append(bvj.joint([
        part("Lid (cut)", win(S("lid"), *bx_), COL["lid"]),
        part("Lower flange bearing unit (cut)", win(S("brg_low"), *bx_), COL["brg"]),
        part("Spacer sleeves", win(S("brg_sleeves"), *bx_), COL["posts"]),
        part("Upper flange bearing unit (cut)", win(S("brg_up"), *bx_), "#334155"),
        part("M10 bolts, heads under the lid", win(S("brg_bolts"), *bx_), COL["bolt"]),
        part("V-ring seal", win(S("vring"), *bx_), COL["vring"]),
        part("Shaft", win(S("shaft"), *bx_), COL["shaft"])],
        OUT / "joint-06.png", "Joint 6: the two bearings on the lid (cut in half)",
        subtitle="Four bolts clamp the lid, lower unit, sleeves and upper unit together; the V-ring keeps spray off the lower seal",
        elev=12, azim=90, size=(8, 6)))
    # 07 runner hub on the shaft, cut
    rz = P["runner_z"]
    bx_ = (-50, 50, -50, 0, rz - 30, rz + 60)
    out.append(bvj.joint([
        part("Runner hub (cut)", win(S("runner"), *bx_), COL["runner"]),
        part("Clamping hub (cut)", win(S("hub"), *bx_), COL["hub"]),
        part("M5 screws into heat-set inserts", win(S("hub_screws"), *bx_), COL["bolt"]),
        part("Shaft", win(S("shaft"), *bx_), COL["shaft"])],
        OUT / "joint-07.png", "Joint 7: runner on the shaft (cut in half)",
        subtitle="The clamping hub grips the shaft; four screws hold the runner to the hub. The shaft ends flush with the runner",
        elev=12, azim=90, size=(8, 6)))
    # 08 coupling, guard and generator, cut
    bx_ = (-100, 100, -100, 0, P["brg_up_z0"] + 5, P["gen_z0"] + 40)
    out.append(bvj.joint([
        part("Upper bearing unit", win(S("brg_up"), *bx_), COL["brg"]),
        part("Jaw coupling (cut)", win(S("coupling"), *bx_), COL["coupling"]),
        part("Shaft and generator shaft", win(S("shaft") + S("generator"), *bx_) & model.bx(-15, 15, -15, 15, 0, 2000), COL["shaft"]),
        part("Guard (cut)", win(S("guard"), *bx_), COL["guard"]),
        part("Generator plate (cut)", win(S("plate"), *bx_), COL["plate"]),
        part("Generator (cut)", win(S("generator"), *bx_) - model.bx(-15, 15, -15, 15, 0, P["gen_z0"]), COL["gen"]),
        part("M6 generator screws", win(S("gen_screws"), *bx_), COL["bolt"])],
        OUT / "joint-08.png", "Joint 8: coupling, guard and generator (cut in half)",
        subtitle="The guard stands in a groove on the lid and stops 1 mm under the plate; the generator screws come up from below",
        elev=10, azim=90, size=(8, 6)))
    # 09 jets and runner, from above
    F = nozzle_frame(P)
    jet = model._tube(F["X"], (0.0, yj, P["strike_z"]), P["jet_d"] / 2)
    jets = jet + model._rotz180(jet)
    zc = 300
    out.append(bvj.joint([
        part("Runner", S("runner"), COL["runner"]),
        part("Nozzles and inserts", win(S("nozzle_1", "nozzle_2", "inserts"), -400, 400, -400, 400, 0, zc), COL["nozzle"]),
        part("Jets (water)", jets, "#38BDF8"),
        part("Housing (cut above the jets)", win(S("housing"), -400, 400, -400, 400, 0, zc), COL["housing"]),
        part("Clamping hub", S("hub"), COL["hub"])],
        OUT / "joint-09.png", "Joint 9: the two jets at the runner, seen from above",
        subtitle="Each jet meets the 150 mm pitch circle at the top of the buckets; the nozzle tips stay 19 mm outside the runner's lift path",
        elev=88, azim=-90, size=(8, 6.5)))
    # 10 nozzle spigot in the flexible coupling
    sp = P["spigot_end_x"]
    mz = P["manifold_z"]
    bx_ = (sp - 90, sp + 140, yj - 0.3, yj + 60, mz - 70, mz + 70)
    out.append(bvj.joint([
        part("Nozzle spigot (printed)", win(model._tube((sp - P["spigot_len"], yj, mz), (sp, yj, mz), 45.0)
                                            - model._tube((sp - P["spigot_len"] - 1, yj, mz), (sp + 1, yj, mz), 41.0), *bx_), COL["nozzle"]),
        part("Flexible coupling and band clamps", win(S("couplings"), *bx_), COL["cpl"]),
        part("Pipe P4", win(S("pipes"), *bx_), COL["pipes"]),
        part("Elbow", win(S("fittings"), *bx_), COL["fittings"])],
        OUT / "joint-10.png", "Joint 10: nozzle inlet joined to the pipe (jet 1, cut in half)",
        subtitle="A 90 mm flexible coupling joins the printed spigot to the PVC pipe end to end; the nozzle is never glued",
        elev=20, azim=-70, size=(8, 6)))
    # 11 pipe stand
    x, y, _ = P["stands"][1]
    bx_ = (x - 90, x + 90, y - 70, y + 70, -1, mz + 60)
    out.append(bvj.joint([
        part("Pipe stand", win(S("stands"), *bx_), COL["stands"]),
        part("Pipe P2", win(S("pipes"), *bx_), COL["pipes"]),
        part("Pad (site)", win(pad_context(), *bx_), COL["pad"])],
        OUT / "joint-11.png", "Joint 11: pipe stand under the long run",
        subtitle="The clip's M8 boss screws onto a bolt through the top plate, which sets the height",
        elev=18, azim=-50, size=(7, 6)))
    # 12 post between lid and plate
    po = P["post_offset"]
    bx_ = (po - 30, po + 30, po - 30, po, P["lid_z"] - 20, P["plate_z0"] + 30)
    out.append(bvj.joint([
        part("Lid (cut)", win(S("lid"), *bx_), COL["lid"]),
        part("Post (cut)", win(S("posts"), *bx_), COL["posts"]),
        part("M10 post rod, washers and nuts", win(S("post_rods"), *bx_), COL["rods"]),
        part("Generator plate (cut)", win(S("plate"), *bx_), COL["plate"])],
        OUT / "joint-12.png", "Joint 12: post between the lid and the generator plate (cut in half)",
        subtitle="The rod clamps the post between the lid and the plate; a 30 mm washer spreads the load under the lid",
        elev=10, azim=90, size=(7, 6)))
    # 13 inlet valve between the tee and the penstock, cut in half along the pipe
    tx, py, vx = P["tee_x"], P["pen_y"], P["valve_x"]
    vl, vs = P["valve_len"] / 2, P["valve_sock"]
    piece = (tx - 90 + P["sock"]) - (vx + vl - vs)
    bx_ = (vx - vl - 120, tx - 20, py - 160, py, mz - 90, mz + 310)
    out.append(bvj.joint([
        part("Penstock, 125 mm (cut)", win(S("penstock_stub"), *bx_), COL["pen"]),
        part("Full-bore gate valve (cut)", win(S("valve"), *bx_), COL["valve"]),
        part(f"Pipe piece, 125 mm, {piece:.0f} mm long (cut)", win(S("valve_fittings"), *bx_), "#9CA3AF"),
        part("Reducing tee, 125 mm run (cut)", win(S("fittings"), *bx_), COL["fittings"])],
        OUT / "joint-13.png", "Joint 13: inlet valve between the penstock and the tee (cut in half)",
        subtitle="Both pipes go fully into the valve's solvent-weld sockets; the bore is the same as the penstock's all the way through",
        elev=12, azim=90, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    M = made()
    out = []
    F = nozzle_frame(P)
    back = F["back"]

    def st(n, done, new, title, sub, **kw):
        import os
        only = os.environ.get("STEPS")
        if only and str(n) not in only.split(","):
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    padp = pad()
    pads = part("Pad over the tailrace (site)", pad_context() & model.bx(-330, 330, -330, 330, -130, 1), COL["pad"])
    st(1, [], [mv(M["frame"], (0, 0, 220)), mv(part("M12 anchors (4)", S("anchors"), COL["bolt"]), (0, 0, 380))],
       "frame onto the pad", "Frame level over the tailrace opening; four M12 anchors through the foot plates into the pad",
       context=[pads], elev=28, azim=-55)
    rods = part("Tie rods (4)", S("tie_rods"), COL["rods"])
    M["tie_rods"] = rods
    st(2, [M["frame"]], [mv(rods, (0, 0, 260))], "tie rods into the frame",
       "Each rod through its corner hole, 12 mm below the angle; lock it with a nut above and below",
       context=[pads], elev=28, azim=-55, label_done=False)
    st(3, [M["housing"]], [mv(part("Nozzle, jet 1", S("nozzle_1"), COL["nozzle"]), tuple(160 * c for c in back)),
                           mv(part("Nozzle, jet 2", S("nozzle_2"), COL["nozzle"]), tuple(-160 * c if i < 2 else 160 * c for i, c in enumerate(back))),
                           mv(part("Gaskets", S("gaskets"), COL["gasket"]), (0, 0, 0)),
                           mv(part("M6 saddle bolts", S("saddle_bolts"), "#6B7280"), (0, 0, 0))],
       "nozzles onto the housing (on the bench)",
       "Tip through the hole, saddle on its gasket; four M6 bolts each from outside, nuts inside, snug",
       elev=25, azim=-30, label_done=False)
    st(4, [M["housing"], M["nozzle_1"], M["nozzle_2"]], [mv(part("Inserts, 34 mm", S("inserts"), COL["insert"]), (0, 0, 220)),
                                                        mv(part("M4 insert screws", S("insert_screws"), COL["bolt"]), (0, 0, 220))],
       "inserts into the nozzle tips", "From inside the housing: slide each insert into its tip, two M4 screws into the heat-set inserts",
       elev=55, azim=-60, label_done=False)
    unit_h = [M["housing"], M["nozzle_1"], M["nozzle_2"], part("Inserts", S("inserts", "gaskets", "saddle_bolts"), "#9CA3AF")]
    st(5, [M["frame"], M["tie_rods"]], [mv(part("Housing with nozzles", S("housing", "nozzle_1", "nozzle_2", "inserts", "gaskets", "saddle_bolts"), COL["housing"]), (0, 0, 320))],
       "housing onto the frame", "Lower it between the four stops, nozzles to the sides where the pipework will run",
       context=[pads], elev=25, azim=-55, label_done=False)
    st(6, [M["lid"]], [mv(part("Lower flange bearing unit", S("brg_low"), COL["brg"]), (0, 0, 120)),
                       mv(part("Spacer sleeves (4)", S("brg_sleeves"), COL["posts"]), (0, 0, 190)),
                       mv(part("Upper flange bearing unit", S("brg_up"), "#334155"), (0, 0, 260)),
                       mv(part("M10 bolts from below", S("brg_bolts"), COL["bolt"]), (0, 0, -150)),
                       mv(part("V-ring seal", S("vring"), COL["vring"]), (0, 0, -90))],
       "bearings onto the lid (on the bench)",
       "Units grease nipples outward; four M10 bolts up through lid, unit, sleeves and unit; nuts snug, not yet tight",
       elev=22, azim=-55, label_done=True)
    lidasm = [M["lid"], M["bearings"], M["vring"]]
    st(7, [M["runner"]], [mv(M["hub"], (0, 0, 120))], "clamping hub onto the runner (on the bench)",
       "Flange down on the runner hub; four M5 screws into the heat-set inserts, even and firm",
       elev=30, azim=-55, label_done=True)
    st(8, lidasm, [mv(M["shaft"], (0, 0, 330))], "shaft through the bearings",
       "Slide it down through both units, the lid and the V-ring; bearing set screws still loose",
       elev=18, azim=-55, label_done=False)
    st(9, lidasm + [M["shaft"]], [mv(part("Runner with its hub", S("runner", "hub", "hub_screws"), COL["runner"]), (0, 0, -170))],
       "runner onto the shaft", "Push the hub up the shaft until the shaft end is flush with the runner underside; tighten the hub clamp",
       elev=12, azim=-55, label_done=False)
    rotor = part("Lid with bearings, shaft and runner", S("lid", "brg_low", "brg_up", "brg_sleeves", "brg_bolts", "vring", "shaft", "runner", "hub", "hub_screws"), COL["lid"])
    st(10, [M["frame"], M["tie_rods"]] + unit_h, [mv(rotor, (0, 0, 380)), mv(part("Washers and nuts (4)", S("lid_nuts"), COL["rods"]), (0, 0, 560))],
       "lid assembly onto the housing",
       "Lower it over the tie rods, runner first, until the housing sits in the groove; washers and nuts, tightened evenly",
       context=[pads], elev=22, azim=-55, label_done=False)
    base10 = [M["frame"], M["tie_rods"], part("Lid nuts", S("lid_nuts"), "#9CA3AF")] + unit_h + [rotor]
    M["posts"] = part("Posts and post rods (4)", S("posts", "post_rods"), COL["posts"])
    st(11, base10, [mv(M["guard"], (0, 0, 200)), mv(M["posts"], (0, 0, 280))], "guard and posts onto the lid",
       "Guard into its groove; each post on its rod, washer and nut under the lid",
       context=[pads], elev=22, azim=-55, label_done=False)
    st(12, [M["plate"]], [mv(M["generator"], (0, 0, 160))], "generator onto the plate (on the bench)",
       "Spigot in the centre hole; four M6 screws from below into the generator face",
       elev=-25, azim=-55, label_done=True)
    st(13, base10 + [M["guard"], M["posts"]], [mv(M["coupling"], (0, 0, 220))], "coupling onto the shaft",
       "Lower hub on the shaft 10 mm above the upper bearing; fit the upper hub on the generator shaft at the same time",
       elev=22, azim=-55, label_done=False)
    st(14, base10 + [M["guard"], M["posts"], M["coupling"]],
       [mv(part("Generator on its plate", S("plate", "generator", "gen_screws"), COL["gen"]), (0, 0, 260)),
        mv(part("Washers and nuts (4)", S("plate_nuts"), COL["rods"]), (0, 0, 420))],
       "generator and plate onto the posts",
       "Engage the coupling jaws, plate down onto the posts over the guard; washers and nuts on top",
       elev=22, azim=-55, label_done=False)
    unit = base10 + [M["guard"], M["posts"], M["coupling"], M["plate"], M["generator"], part("Plate nuts", S("plate_nuts"), "#9CA3AF")]
    st(15, unit, [mv(M["stands"], (0, 0, 260))], "pipe stands", "Three stands on the pad under the line of the pipework; anchors loose for now",
       context=[padp], elev=26, azim=-50, label_done=False)
    st(16, unit + [M["stands"]], [mv(M["pipework"], (0, 0, 260))], "pipework onto the stands and nozzles",
       "Tee to the penstock side, pipes in the clips; flexible couplings over the nozzle spigots; band clamps snug",
       context=[padp], elev=26, azim=-50, label_done=False)
    st(17, unit + [M["stands"], M["pipework"]], [mv(M["valve"], (0, 0, 260)), mv(M["penstock"], (-300, 0, 0))],
       "inlet valve and penstock",
       "Pipe piece into the tee, full-bore valve onto it, penstock into the valve; stem up so the handwheel is easy to reach",
       context=[padp], elev=26, azim=-50, label_done=False)
    st(18, [part("Forebay tub", S("forebay"), COL["forebay"])],
       [mv(part("Outlet tank connector", S("forebay_outlet"), "#1F2937"), (220, 0, 0)), mv(part("Intake screen", S("screen"), COL["screen"]), (0, 0, 260))],
       "forebay (at the top of the drop)", "Outlet connector through the downstream end; screen frame on the rim; penstock into the outlet",
       elev=28, azim=-60, label_done=True)
    st(19, [part("Post anchor", S("post_base"), "#9CA3AF")],
       [mv(part("Equipment post", S("eq_post"), COL["post"]), (0, 0, 300)),
        mv(part("Rectifier box", S("rectifier"), COL["rect"]), (0, -200, 0)),
        mv(part("Controller box", S("controller"), COL["ctrl"]), (0, -260, 0)),
        mv(part("Resistor guard", S("dump"), COL["dump"]), (220, 0, 0))],
       "equipment post and electrical boxes", "Post into its anchor; boxes on the face toward the turbine; resistor guard on the side",
       elev=20, azim=-40, label_done=True)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "PicoFlow prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules wired at block level; no circuit board is laid out. Stranded copper; ferrules or crimped lugs on every terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, REPO, fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((27, 12.6), 68, 47.4, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(28.5, 58.8, "On the equipment post (enclosed, rated 100 V DC)", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, ORA = "#B91C1C", "#1D4ED8", "#6B7280", "#C2410C"
    blk(3, 42, 14, 14, "Generator", "low-speed BLDC,\n3 phase, on the\nturbine lid", "#1F2937")
    blk(30, 42, 14, 12, "Rectifier", "3 phase bridge,\n35 A 1,000 V,\non a heat sink", "#7C3AED")
    blk(52, 42, 16, 12, "MPPT buck charger", "15 to 60 V in,\n12 V LiFePO4 out", "#16A34A")
    blk(30, 22, 14, 12, "Voltage clamp", "comparator, on at\n48 V, off at 40 V,\nown supply", ORA)
    blk(52, 22, 16, 12, "Dump-load switch", "MOSFET, on when\nthe battery is full", "#16A34A")
    blk(77, 42, 15, 12, "DC isolator", "rated 100 V DC,\n2 pole", "#374151")
    blk(101, 42, 16, 14, "Battery", "12 V LiFePO4 with\nBMS (household),\n20 A fuse at +", "#65A30D")
    blk(77, 14, 15, 16, "Resistor guard", "300 W dump load\n(12 V side);\n6.8 ohm 350 W\nclamp (DC bus)", ORA)
    for yy in (51, 49, 47):
        wire([(17, yy), (30, yy)], "#111827", 1.4)
    lab(18, 44.3, "3 x 4 mm²,\nabout 10 m", INK)
    wire([(44, 48), (52, 48)], RED); lab(48, 51.4, "DC bus,\n4 mm²", RED, "center")
    wire([(48, 48), (48, 39), (37, 39), (37, 34)], RED, 1.6); lab(38, 37.0, "bus sense, 1.5 mm²", RED)
    wire([(68, 48), (77, 48)], RED); lab(72.5, 50.2, "12 V, 4 mm²", RED, "center")
    wire([(92, 48), (101, 48)], RED); lab(96.5, 51.2, "4 mm², fuse\nwithin 300 mm", RED, "center")
    wire([(72.5, 48), (72.5, 30), (68, 30)], RED); lab(73.2, 38, "12 V to the\nswitch, 4 mm²", RED)
    wire([(68, 25), (77, 25)], ORA); lab(72.5, 23.2, "4 mm²", ORA, "center")
    wire([(60, 42), (60, 34)], GRY, 1.2); lab(60.7, 38, "battery full,\n0.5 mm²", GRY)
    wire([(37, 22), (37, 16), (77, 16)], ORA); lab(40, 17.6, "to the 6.8 ohm clamp resistor, 1.5 mm²", ORA)
    ax.text(26, 8.8, "Safety: the clamp works on its own, whatever the charger is doing. Never run the turbine with the clamp or the dump load disconnected.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(26, 5.9, "Red: power. Orange: resistor circuits (run hot). Grey: control. The DC bus can reach 48 V in normal clamping and about 80 V on a double fault;"
            , fontsize=7.2, color=MUT)
    ax.text(26, 3.7, "every part on the DC bus side is rated and enclosed for 100 V DC.", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
