"""PicoFlow sizing calculations (PCF-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes them to
docs/04-calcs/results.json, which cad/src/concept_media.py reads for the flow diagram
and key figures. Geometry (setting height, runner envelope, branch lengths, part volumes) is read
from cad/src/model.py (the constructable design, PCF-DDR-003) and costs from bom/bom.csv.

All values are first-principles estimates for a TRL 3 proof of concept on paper.
"""
import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))

# ---------------------------------------------------------------- assumptions
RHO, G = 1000.0, 9.81          # water density kg/m3, gravity m/s2
NU = 1.14e-6                   # kinematic viscosity at 15 C, m2/s
EPS = 1.5e-6                   # PVC absolute roughness, m

H_DESIGN, Q_DESIGN = 2.0, 0.010   # design point: gross head m, flow m3/s
L_PEN = 20.0                   # penstock length, m
D_PEN = 0.1176                 # 125 mm drainage PVC (SN8, 3.7 mm wall), bore m; decided 2026-09-25 (PCF-DDR-002 N1)
D_PEN_110 = 0.1036             # 110 mm drainage PVC (SN4, 3.2 mm wall), TRL 3 v0.1 baseline, for comparison
K_PEN = {"rounded entrance": 0.20, "intake screen": 0.10, "two bends": 0.30}
# Inlet valve (BOM 8): a full-bore 125 mm PVC-U gate valve with solvent-weld sockets on the penstock
# (N6 option a, decided by Amish 2026-10-01). Open gate valve 0.15 on the penstock velocity head.
K_VALVE_FULL = 0.15
# v0.3 comparison only: a 90 mm gate valve between a 125 x 90 reducer and a 90 x 125 expander
# (PCF-DDR-003 P11), coefficients on the valve's own velocity head, bore the 90 mm pipe bore.
D_VALVE = 0.0840
K_VALVE = {"reducer 125 to 90": 0.10, "gate valve 90 mm, open": 0.15,
           "expander 90 to 125 (sudden)": (1 - (D_VALVE / 0.1176) ** 2) ** 2}
D_BR = 0.0840                  # 90 mm PVC branch bore, m
D_BR_ALT = 0.0578              # 63 mm branch bore used at TRL 2, m (comparison)
# branch losses on branch velocity head (PCF-DDR-003 P10 layout): jet 1 leaves the side of a
# 125 x 90 reducing tee (1.0) and turns three 90 degree elbows (0.3 each); jet 2 runs straight
# through the tee (0.3) and a 125 x 90 reducer (0.1). Lengths are read from the model.
K_BR = {"jet 1 (around the housing)": 1.0 + 3 * 0.3, "jet 2 (direct)": 0.3 + 0.1}
L_BR = {"jet 1 (around the housing)": 1.40, "jet 2 (direct)": 0.30}   # m, replaced from the model in main()
CV = 0.97                      # nozzle velocity coefficient
PHI = 0.46                     # bucket speed / jet speed at best efficiency
D_PITCH = 0.150                # runner pitch diameter, m
ETA_RUNNER = 0.75              # jet to shaft, first printed runner (lab optimum 0.87 to 0.91)
RUNAWAY = 2.0                  # runaway speed / best speed, Turgo (1.8 to 2.0; upper value used)
KV = 10.0                      # generator rpm per volt of rectified open-circuit DC
P_FIX_REF, N_REF = 12.0, 340.0 # generator iron and friction loss W at N_REF rpm, scales with speed
R_GEN = 0.8                    # generator plus cable resistance, DC equivalent, ohm
V_RECT = 1.6                   # three-phase bridge, two diode drops, V
ETA_BUCK = 0.94                # MPPT buck converter
V_BATT = 13.6                  # 12 V LiFePO4 charging, V
V_BUCK_MIN = 15.0              # bus voltage the buck needs to charge at 14.4 V absorption
INSERTS = (20, 45)             # nozzle insert bore range, mm
CLAMP_ON, CLAMP_OFF = 48.0, 40.0   # hardware clamp thresholds on the DC bus, V
CLAMP_R = 6.8                  # clamp resistor in the BOM (line 15), ohm (8.2 before 2026-10-01)
CLAMP_W = 350.0                # its power rating in the BOM, W
TOUCH_LIMIT = 60.0             # R8 limit, V DC
BRG_C = 12.8e3                 # UC204 insert bearing in a UCF204-class flange unit, dynamic load rating, N (catalog class)
PETG_RHO = 1270.0              # kg/m3
PRINT_FILL = 0.6               # printed mass / solid massing volume (thin buckets, infill)
PRINT_RATE = 25.0              # g/h, PETG, 0.4 mm nozzle, 0.28 mm layers
E_PVC, K_WATER = 3.0e9, 2.2e9  # Pa, for water hammer wave speed
WALL_PEN = 0.0037              # m, 125 mm SN8
T_CLOSE = 10.0                 # gate valve closing time, s (about ten turns)
P_PIPE = 50.0                  # kPa, assumed rating of drainage pipe joints (to confirm)
BUDGET = 450.0                 # budget_usd: a value-engineering target, not a limit (Amish, 2026-10-01)
EXCLUDED = ("9 ", "17 ")       # penstock and battery lines, excluded from kit cost
SALVAGED_GEN = 40.0            # USD, salvaged direct-drive washing machine motor (30 to 50)

R = {}                         # results written to results.json


def f_swamee(re, d):
    return 0.25 / math.log10(EPS / (3.7 * d) + 5.74 / re ** 0.9) ** 2


def pipe_k(q, d, length, k_minor):
    """Head loss coefficient h = k q^2 for a pipe carrying q."""
    a = math.pi / 4 * d ** 2
    v = max(q / a, 1e-6)
    f = f_swamee(v * d / NU, d)
    return (f * length / d + k_minor) / (2 * G * a ** 2)


FULL_BORE = True               # N6 option (a), decided 2026-10-01; False gives the v0.3 90 mm valve for comparison


def k_pen_total(d_pen):
    """Penstock minor losses on the penstock velocity head, including the inlet valve."""
    if FULL_BORE:
        return sum(K_PEN.values()) + K_VALVE_FULL
    return sum(K_PEN.values()) + sum(K_VALVE.values()) * (d_pen / D_VALVE) ** 4


def hydraulics(h_gross, d_jet, jets=2, d_br=D_BR, d_pen=D_PEN):
    """Solve flow through the penstock, branches and nozzles for a gross head. d_jet in m."""
    aj = math.pi / 4 * d_jet ** 2
    k_jet = 1 / (2 * G * CV ** 2 * aj ** 2)      # nozzle head h = k_jet q^2
    names = list(K_BR)[:jets] if jets == 2 else [list(K_BR)[1]]
    def branch_flows(h_tee):
        q = {n: 0.004 for n in names}
        for _ in range(40):
            q = {n: math.sqrt(h_tee / (pipe_k(q[n], d_br, L_BR[n], K_BR[n]) + k_jet)) for n in names}
        return q

    lo, hi = 0.0, h_gross                        # bisection on the head at the tee
    for _ in range(60):
        h_tee = (lo + hi) / 2
        q = branch_flows(h_tee)
        qt = sum(q.values())
        need = h_tee + pipe_k(qt, d_pen, L_PEN, k_pen_total(d_pen)) * qt ** 2
        lo, hi = (h_tee, hi) if need < h_gross else (lo, h_tee)
    qt = sum(q.values())
    hp = pipe_k(qt, d_pen, L_PEN, k_pen_total(d_pen)) * qt ** 2
    hn = {n: k_jet * q[n] ** 2 * CV ** 2 for n in names}        # net head at each nozzle
    vj = {n: CV * math.sqrt(2 * G * hn[n]) for n in names}
    pj = sum(0.5 * RHO * q[n] * vj[n] ** 2 for n in names)
    hb = {n: pipe_k(q[n], d_br, L_BR[n], K_BR[n]) * q[n] ** 2 for n in names}
    vmean = sum(q[n] * vj[n] for n in names) / qt
    return dict(q=qt, q_each=q, h_pen=hp, h_br=hb, hn=hn, vj=vmean, p_hyd=RHO * G * qt * h_gross,
                p_jet=pj, v_pen=qt / (math.pi / 4 * d_pen ** 2))


def generator(p_shaft, rpm):
    """Return (bus voltage, current, DC out of rectifier, into battery, generator loss)."""
    e = rpm / KV
    p_fix = P_FIX_REF * rpm / N_REF
    pem = max(p_shaft - p_fix, 0.0)
    i = pem / e if e > 0 else 0.0
    v_bus = e - i * R_GEN - V_RECT
    p_dc = v_bus * i
    return dict(e=e, i=i, v_bus=v_bus, p_dc=p_dc, p_batt=ETA_BUCK * p_dc, p_fix=p_fix, p_cu=i * i * R_GEN,
                p_rect=V_RECT * i)


def chain(h_gross, d_jet, jets=2, d_pen=D_PEN, eta_runner=ETA_RUNNER):
    hy = hydraulics(h_gross, d_jet, jets, D_BR, d_pen)
    rpm = PHI * hy["vj"] / (math.pi * D_PITCH) * 60
    p_shaft = eta_runner * hy["p_jet"]
    ge = generator(p_shaft, rpm)
    return dict(**hy, rpm=rpm, p_shaft=p_shaft, torque=p_shaft / (rpm * 2 * math.pi / 60), **ge,
                eta_w2w=ge["p_batt"] / hy["p_hyd"], rpm_run=RUNAWAY * rpm, v_run=RUNAWAY * rpm / KV)


def solve_jet(h_gross, q_target, jets=2, d_pen=D_PEN):
    lo, hi = 0.005, 0.120
    for _ in range(60):
        mid = (lo + hi) / 2
        if hydraulics(h_gross, mid, jets, D_BR, d_pen)["q"] < q_target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def line(label, value, unit="", fmt="{:.1f}"):
    print(f"  {label:<58} {fmt.format(value)} {unit}")


def main():
    global FULL_BORE
    import model
    parts = model.build_parts()
    C = model.build_components()
    mp = parts["_p"]
    L_BR["jet 1 (around the housing)"] = mp["branch_len_1"]
    L_BR["jet 2 (direct)"] = mp["branch_len_2"]

    print("PicoFlow sizing (PCF-CAL-001). Estimates for TRL 3.\n")

    # ---------------------------------------------------------- 1 hydraulics and nozzle
    d_exact = solve_jet(H_DESIGN, Q_DESIGN)
    d_ins = round(mp["jet_d"])                          # design insert bore, from the model (34 mm)
    dp = chain(H_DESIGN, d_ins / 1000)
    alt = hydraulics(H_DESIGN, d_ins / 1000, 2, D_BR_ALT)
    print("1. Design point: 2.0 m gross head, 10 L/s, 20 m of 125 mm PVC, two jets")
    line("Jet diameter for exactly 10 L/s", d_exact * 1000, "mm")
    line("Design insert bore (model)", d_ins, "mm", "{:.0f}")
    line("Flow with the chosen inserts", dp["q"] * 1000, "L/s", "{:.2f}")
    line("Penstock velocity", dp["v_pen"], "m/s", "{:.2f}")
    line("Penstock loss (friction and fittings)", dp["h_pen"], "m", "{:.3f}")
    for n in dp["h_br"]:
        line(f"Branch loss, {n}", dp["h_br"][n], "m", "{:.3f}")
        line(f"Flow, {n}", dp["q_each"][n] * 1000, "L/s", "{:.2f}")
    loss_frac = 1 - sum(dp["hn"].values()) / len(dp["hn"]) / H_DESIGN
    line("Mean net head at the nozzles", sum(dp["hn"].values()) / len(dp["hn"]), "m", "{:.2f}")
    line("Pipe and branch loss as share of gross head", 100 * loss_frac, "%")
    alt_frac = 1 - sum(alt["hn"].values()) / 2 / H_DESIGN
    line("Same, with the TRL 2 63 mm branches", 100 * alt_frac, "%")
    line("Jet velocity (flow-weighted mean)", dp["vj"], "m/s", "{:.2f}")
    line("Jet to pitch diameter ratio", d_ins / (D_PITCH * 1000), "", "{:.2f}")
    line("Branch length, jet 1 (model)", L_BR["jet 1 (around the housing)"], "m", "{:.2f}")
    line("Branch length, jet 2 (model)", L_BR["jet 2 (direct)"], "m", "{:.2f}")
    kv = K_VALVE_FULL
    line("Full-bore valve, on the penstock velocity head", kv, "", "{:.2f}")
    line("Head lost at the valve", kv * dp["v_pen"] ** 2 / (2 * G), "m", "{:.3f}")
    ex10 = chain(H_DESIGN, d_exact)
    loss10 = 100 * (1 - sum(ex10["hn"].values()) / 2 / H_DESIGN)
    line("Into the battery at exactly 10 L/s (inserts sized for it)", ex10["p_batt"], "W")
    line("Margin over R3 (80 W) at exactly 10 L/s", ex10["p_batt"] - 80.0, "W")
    line("Water to wire at exactly 10 L/s", 100 * ex10["eta_w2w"], "%")
    line("Pipe and branch loss at exactly 10 L/s", loss10, "%")
    FULL_BORE = False                                   # v0.3 comparison: 90 mm valve with fittings
    kv90 = sum(K_VALVE.values()) * (D_PEN / D_VALVE) ** 4
    old_d = solve_jet(H_DESIGN, Q_DESIGN)
    old10 = chain(H_DESIGN, old_d)
    FULL_BORE = True
    line("v0.3 comparison: 90 mm valve, reducer and expander, coefficient", kv90, "", "{:.2f}")
    line("v0.3 comparison: head lost there", kv90 * ex10["v_pen"] ** 2 / (2 * G), "m", "{:.3f}")
    line("v0.3 comparison: into the battery at exactly 10 L/s", old10["p_batt"], "W")
    R.update(br_len=[L_BR["jet 1 (around the housing)"], L_BR["jet 2 (direct)"]], k_valve=kv,
             h_valve=kv * dp["v_pen"] ** 2 / (2 * G), p_batt_10=ex10["p_batt"], w2w_10=100 * ex10["eta_w2w"],
             loss_10=loss10, r3_margin=ex10["p_batt"] - 80.0,
             v03_k_valve=kv90, v03_h_valve=kv90 * ex10["v_pen"] ** 2 / (2 * G), v03_p_batt_10=old10["p_batt"], v03_d=old_d * 1000)
    R.update(d_jet_exact=d_exact * 1000, d_insert=d_ins, q_design=dp["q"] * 1000, h_pen=dp["h_pen"],
             loss_pct=100 * loss_frac, loss_pct_63=100 * alt_frac, hn=sum(dp["hn"].values()) / 2, vj=dp["vj"],
             jet_ratio=d_ins / (D_PITCH * 1000), v_pen=dp["v_pen"])

    # ---------------------------------------------------------- 2 power chain
    print("\n2. Power chain at the design point")
    p_noz = dp["p_hyd"] * (1 - loss_frac)
    stages = [("Gross hydraulic power", dp["p_hyd"]), ("Hydraulic power at the nozzles", p_noz),
              ("Jet power", dp["p_jet"]), ("Runner shaft power", dp["p_shaft"]),
              ("DC out of the rectifier", dp["p_dc"]), ("Into the battery", dp["p_batt"])]
    for s, v in stages:
        line(s, v, "W")
    line("Best runner speed", dp["rpm"], "rpm", "{:.0f}")
    line("Shaft torque", dp["torque"], "N m", "{:.2f}")
    line("Generator open-circuit DC at best speed", dp["e"], "V")
    line("DC bus voltage under load", dp["v_bus"], "V")
    line("Generator current (DC side)", dp["i"], "A", "{:.2f}")
    line("Generator losses: fixed, copper", dp["p_fix"] + dp["p_cu"], "W")
    line("Generator plus rectifier efficiency", 100 * dp["p_dc"] / dp["p_shaft"], "%")
    line("Battery charging current at 13.6 V", dp["p_batt"] / V_BATT, "A", "{:.2f}")
    line("Water-to-wire efficiency", 100 * dp["eta_w2w"], "%")
    line("Daily energy, 24 h", dp["p_batt"] * 24 / 1000, "kWh", "{:.2f}")
    R.update(p_hyd=dp["p_hyd"], p_noz=p_noz, p_jet=dp["p_jet"], p_shaft=dp["p_shaft"], p_dc=dp["p_dc"],
             p_batt=dp["p_batt"], rpm=dp["rpm"], torque=dp["torque"], e_oc=dp["e"], v_bus=dp["v_bus"],
             i_gen=dp["i"], eta_w2w=100 * dp["eta_w2w"], kwh_day=dp["p_batt"] * 24 / 1000)

    # ---------------------------------------------------------- 3 head range
    print("\n3. Head range with the design-point inserts")
    print(f"  {'Head m':>6} {'Q L/s':>6} {'Loss %':>6} {'rpm':>5} {'Voc V':>6} {'Vbus V':>6} {'Batt W':>6} {'W2W %':>6} {'Run rpm':>7} {'Run V':>6}")
    rng = {}
    for h in (1.0, 1.5, 2.0, 2.5, 3.0):
        c = chain(h, d_ins / 1000)
        lf = 100 * (1 - sum(c["hn"].values()) / 2 / h)
        print(f"  {h:>6.1f} {c['q']*1000:>6.2f} {lf:>6.1f} {c['rpm']:>5.0f} {c['e']:>6.1f} {c['v_bus']:>6.1f} "
              f"{c['p_batt']:>6.1f} {100*c['eta_w2w']:>6.1f} {c['rpm_run']:>7.0f} {c['v_run']:>6.1f}")
        rng[h] = c
    R["range"] = {str(h): dict(q=c["q"] * 1000, rpm=c["rpm"], e=c["e"], v_bus=c["v_bus"], p_batt=c["p_batt"],
                               rpm_run=c["rpm_run"], v_run=c["v_run"]) for h, c in rng.items()}
    # R4 case: 1.0 m and 7 L/s, inserts resized for that flow
    d4 = solve_jet(1.0, 0.007)
    c4 = chain(1.0, d4)
    print("\n  R4 case, 1.0 m and 7 L/s with inserts sized for it:")
    line("Insert bore", d4 * 1000, "mm")
    line("Into the battery", c4["p_batt"], "W")
    line("DC bus voltage (buck needs about 15 V)", c4["v_bus"], "V")
    line("Best speed", c4["rpm"], "rpm", "{:.0f}")
    R.update(r4_d=d4 * 1000, r4_p=c4["p_batt"], r4_vbus=c4["v_bus"])

    # ---------------------------------------------------------- 4 flow range (R2)
    print("\n4. Flow range with 20 to 45 mm inserts (R2)")
    fr = {}
    for h in (1.0, 2.0, 3.0):
        qmin = hydraulics(h, INSERTS[0] / 1000, 1)["q"] * 1000
        qmax = hydraulics(h, INSERTS[1] / 1000, 2)["q"] * 1000
        fr[h] = (qmin, qmax)
        line(f"{h:.1f} m: one 20 mm jet to two 45 mm jets", 0, f"{qmin:.1f} to {qmax:.1f} L/s", "")
    d15 = {h: solve_jet(h, 0.015) * 1000 for h in (1.0, 2.0, 3.0)}
    for h, d in d15.items():
        line(f"Two-jet insert for 15 L/s at {h:.1f} m", d, "mm")
    R["flow_range"] = {str(h): v for h, v in fr.items()}
    R["d15"] = {str(h): v for h, v in d15.items()}

    # sensitivity: penstock bore and runner efficiency at the design point
    print("\n   Sensitivity at 2.0 m and 10 L/s (inserts resized for 10 L/s each time)")
    sens = {}
    for label, dpen, eta in (("110 mm penstock (103.6 mm bore), runner 75 %", D_PEN_110, ETA_RUNNER),
                             ("125 mm penstock (117.6 mm bore), runner 75 %", D_PEN, ETA_RUNNER),
                             ("160 mm penstock (150.6 mm bore), runner 75 %", 0.1506, ETA_RUNNER),
                             ("110 mm penstock, runner 80 %", D_PEN_110, 0.80),
                             ("125 mm penstock, runner 80 %", D_PEN, 0.80)):
        cs = chain(H_DESIGN, solve_jet(H_DESIGN, Q_DESIGN, 2, dpen), 2, dpen, eta)
        cs1 = chain(1.0, solve_jet(1.0, 0.007, 2, dpen), 2, dpen, eta)
        lf = 100 * (1 - sum(cs["hn"].values()) / 2 / H_DESIGN)
        line(label, 0, f"loss {lf:.1f} %, {cs['p_batt']:.1f} W, {100*cs['eta_w2w']:.1f} %, "
             f"{cs['p_batt']*24/1000:.2f} kWh/day; 1 m: {cs1['p_batt']:.1f} W", "")
        sens[label] = dict(loss=lf, p=cs["p_batt"], w2w=100 * cs["eta_w2w"], kwh=cs["p_batt"] * 24 / 1000, p1=cs1["p_batt"])
    R["sensitivity"] = sens

    # ---------------------------------------------------------- 5 runaway and clamp (R8)
    print("\n5. Runaway and voltage clamp (R8)")
    d15_3 = d15[3.0] / 1000
    worst = chain(3.0, d15_3)
    line("Runaway at 3.0 m, design inserts", rng[3.0]["rpm_run"], "rpm", "{:.0f}")
    line("Open-circuit DC at that runaway", rng[3.0]["v_run"], "V")
    line("Worst case: 3.0 m and 15 L/s, shaft power at best speed", worst["p_shaft"], "W")
    line("Worst case DC bus under MPPT load", worst["v_bus"], "V")
    line("Worst case runaway speed", worst["rpm_run"], "rpm", "{:.0f}")
    line("Worst case open-circuit DC at runaway", worst["v_run"], "V")
    # Clamp: resistor across the DC bus switched by a hardware comparator. Turbine torque falls
    # linearly from stall to zero at runaway; find the speed where generator torque into R_c balances it.
    w_run = worst["rpm_run"] * 2 * math.pi / 60
    t_stall = 4 * worst["p_shaft"] / w_run

    def clamp_eq(rc):
        lo, hi = 1.0, w_run
        for _ in range(80):
            w = (lo + hi) / 2
            rpm = w * 60 / (2 * math.pi)
            e = rpm / KV
            i = max(e - V_RECT, 0) / (R_GEN + rc)
            t_gen = (e * i + P_FIX_REF * rpm / N_REF) / w
            t_tur = t_stall * (1 - w / w_run)
            if t_gen > t_tur:
                hi = w
            else:
                lo = w
        rpm = lo * 60 / (2 * math.pi)
        e = rpm / KV
        i = max(e - V_RECT, 0) / (R_GEN + rc)
        return rpm, i * rc, i * i * rc

    e12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
    cands = [m * k for k in (1, 10) for m in e12]
    rc_best = max(r for r in cands if clamp_eq(r)[1] < CLAMP_OFF)
    rc = CLAMP_R                                        # the resistor in the BOM (line 15)
    rpm_c, v_c, p_c = clamp_eq(rc)
    p_rating = CLAMP_ON ** 2 / rc
    line("Clamp resistor in the BOM", rc, "ohm")
    line("Largest E12 value holding the equilibrium below the 40 V release", rc_best, "ohm")
    line("That value's clamped bus voltage and rating needed at 48 V", clamp_eq(rc_best)[1], f"V, {CLAMP_ON ** 2 / rc_best:.0f} W")
    line("Clamped speed, worst case", rpm_c, "rpm", "{:.0f}")
    line("Clamped bus voltage, worst case", v_c, "V")
    line("Clamp dissipation at equilibrium", p_c, "W", "{:.0f}")
    line("Clamp resistor rating needed (at 48 V turn-on)", p_rating, "W", "{:.0f}")
    line("Clamp resistor rating in the BOM", CLAMP_W, "W", "{:.0f}")
    line("Release margin, 40 V release less clamped bus voltage", CLAMP_OFF - v_c, "V")
    rim_v = worst["rpm_run"] * 2 * math.pi / 60 * 0.1
    line("Runner rim speed at worst runaway", rim_v, "m/s")
    line("Rim hoop stress, rho v^2 (PETG)", PETG_RHO * rim_v ** 2 / 1e6, "MPa", "{:.2f}")
    R.update(run_rpm_3=rng[3.0]["rpm_run"], run_v_3=rng[3.0]["v_run"], worst_p_shaft=worst["p_shaft"],
             worst_run_rpm=worst["rpm_run"], worst_run_v=worst["v_run"], clamp_r=rc, clamp_r_best=rc_best, clamp_v_best=clamp_eq(rc_best)[1], clamp_rpm=rpm_c, clamp_v=v_c,
             clamp_p=p_c, clamp_rating=p_rating, clamp_w=CLAMP_W, rim_v=rim_v, rim_stress=PETG_RHO * rim_v ** 2 / 1e6)

    # ---------------------------------------------------------- 6 bearings (R12)
    print("\n6. Bearing life (R12)")
    # worst load: 3.0 m, 15 L/s, one jet closed so the other jet's force is not balanced
    one = chain(3.0, solve_jet(3.0, 0.0075, 1), 1)
    f_t = one["torque"] / (D_PITCH / 2)
    m_runner = model_mass = parts["runner"].volume * 1e-9 * PETG_RHO * PRINT_FILL
    fa = RHO * worst["q"] * worst["vj"] + m_runner * G
    fr_ = f_t
    p_eq = 0.56 * fr_ + 2.0 * fa
    n = worst["rpm"]
    l10 = (BRG_C / p_eq) ** 3 * 1e6 / (60 * n)
    line("Radial load, one jet at 3.0 m, 7.5 L/s", fr_, "N")
    line("Axial load, jet momentum at 15 L/s plus runner weight", fa, "N")
    line("Equivalent load (X 0.56, Y 2.0)", p_eq, "N")
    line("Basic L10 life at the worst-case best speed", l10, "h", "{:.2e}")
    R.update(brg_fr=fr_, brg_fa=fa, brg_p=p_eq, brg_l10=l10)

    # ---------------------------------------------------------- 7 geometry, print, mass (R9, R13, R14)
    print("\n7. Geometry, printing and mass (R9, R13, R14)")
    vol = lambda k: C[k].shape.volume * 1e-9  # noqa: E731  m3
    rb = parts["runner"].bounding_box()
    line("Runner envelope X", rb.size.X, "mm", "{:.0f}")
    line("Runner envelope Z", rb.size.Z, "mm", "{:.0f}")
    print_g = m_runner * 1000
    line("Runner printed mass (model volume x 0.6 x PETG density)", print_g, "g", "{:.0f}")
    line("Print time at 25 g/h", print_g / PRINT_RATE, "h")
    line("Nozzle printed mass, each (model volume x 0.6 x PETG density)", vol("nozzle_1") * PETG_RHO * PRINT_FILL * 1000, "g", "{:.0f}")
    line("Nozzle print time at 25 g/h, each", vol("nozzle_1") * PETG_RHO * PRINT_FILL * 1000 / PRINT_RATE, "h")
    setting = mp["jet_z"] / 1000
    line("Nozzle centerline above tailwater (model)", setting * 1000, "mm", "{:.0f}")
    line("Runner underside above tailwater (model)", mp["runner_bottom"], "mm", "{:.0f}")
    line("Setting height as share of site drop at the design point", 100 * setting / (H_DESIGN + setting), "%")
    masses = {
        "Generator, 500 W low-speed BLDC (catalog class, assumed)": 7.0,
        "Housing, 315 mm PVC (model volume x 1,400 kg/m3)": vol("housing") * 1400,
        "Lid, 12 mm HDPE (model volume x 950 kg/m3)": vol("lid") * 950,
        "Frame, 40 x 40 x 4 mm angle, foot plates, stops (model volume, steel)": vol("frame") * 7850,
        "Bearing units, two UCF204 class (catalog, about 0.65 kg each)": 1.30,
        "Generator plate, 8 mm aluminium (model volume)": vol("plate") * 2700,
        "Posts and spacer sleeves, steel tube (model volume)": (vol("posts") + vol("brg_sleeves")) * 7850,
        "Guard, 160 mm PVC (model volume)": vol("guard") * 1400,
        "Tie rods, post rods, bearing bolts and nuts (model volume, steel)": (vol("tie_rods") + vol("lid_nuts") + vol("post_rods") + vol("plate_nuts") + vol("brg_bolts")) * 7850,
        "Shaft, 316 stainless (model volume)": vol("shaft") * 7950,
        "Clamping hub (aluminium, model volume)": vol("hub") * 2700,
        "Runner, PETG": m_runner,
        "Coupling": 0.3,
        "Manifold: about 1.9 m of 90 mm PVC at 1.1 kg/m, tee, reducer, elbows, couplings": 1.9 * 1.1 + 1.2,
        "Nozzles, printed (two, model volume x 0.6 x PETG)": 2 * vol("nozzle_1") * PETG_RHO * PRINT_FILL,
        "Gate valve, 125 mm PVC-U full bore (catalogue class, about 5.5 kg), with the 125 mm pipe piece": 5.5 + 0.175 * 2.2,
    }
    for k, v in masses.items():
        line(k, v, "kg", "{:.2f}")
    total = sum(masses.values())
    pipework = (masses["Manifold: about 1.9 m of 90 mm PVC at 1.1 kg/m, tee, reducer, elbows, couplings"]
                + masses["Nozzles, printed (two, model volume x 0.6 x PETG)"]
                + masses["Gate valve, 125 mm PVC-U full bore (catalogue class, about 5.5 kg), with the 125 mm pipe piece"])
    unit = total - pipework
    line("Turbine unit, items 1 to 6 and 11 (R14 definition)", unit, "kg")
    line("Manifold and valve, carried separately as pipework", pipework, "kg")
    line("Everything above together", total, "kg")
    R.update(runner_env=[rb.size.X, rb.size.Y, rb.size.Z], print_g=print_g, print_h=print_g / PRINT_RATE,
             setting_mm=mp["jet_z"], runner_bottom=mp["runner_bottom"],
             setting_pct=100 * setting / (H_DESIGN + setting), mass_total=total, mass_unit=unit,
             mass_pipework=pipework, mass_gen=7.0, masses=masses,
             nozzle_g=vol("nozzle_1") * PETG_RHO * PRINT_FILL * 1000)

    # ---------------------------------------------------------- 8 penstock surge (R17)
    print("\n8. Penstock surge (R17)")
    a = math.sqrt(K_WATER / RHO / (1 + K_WATER * D_PEN / (E_PVC * WALL_PEN)))
    c3 = rng[3.0]
    h_static = 3.0 - (mp["manifold_z"] - mp["jet_z"]) / 1000
    dh_slow = 2 * L_PEN * c3["v_pen"] / (G * T_CLOSE)
    dh_fast = a * c3["v_pen"] / G
    dh_half = a * c3["v_pen"] / 2 / G
    peak = RHO * G * (h_static + dh_slow) / 1000
    line("Pressure wave speed in 125 mm SN8 PVC", a, "m/s", "{:.0f}")
    line("Critical closure time 2L/a", 2 * L_PEN / a, "s", "{:.2f}")
    line("Penstock velocity at 3.0 m", c3["v_pen"], "m/s", "{:.2f}")
    line("Static head at the valve, 3.0 m site", h_static, "m", "{:.2f}")
    line("Surge head, 10 s closure (Michaud)", dh_slow, "m", "{:.2f}")
    line("Peak pressure, static plus surge, 10 s closure", peak, "kPa")
    line("Surge head, instant closure (Joukowsky)", dh_fast, "m")
    line("Surge head if one nozzle blocks instantly", dh_half, "m")
    line("Static pressure at the valve, 3.0 m", RHO * G * h_static / 1000, "kPa")
    R.update(wave=a, t_crit=2 * L_PEN / a, surge_slow=dh_slow, surge_peak=peak, surge_fast=dh_fast,
             surge_half=dh_half, p_static3=RHO * G * h_static / 1000)

    # ---------------------------------------------------------- 9 dump load (R7)
    print("\n9. Dump load (R7)")
    line("Largest output into the 12 V side (3.0 m, 15 L/s)", worst["p_batt"], "W")
    line("300 W dump load margin over that", 300 / worst["p_batt"], "x", "{:.2f}")
    R.update(dump_worst=worst["p_batt"], dump_margin=300 / worst["p_batt"])

    # ---------------------------------------------------------- 10 cost (R15)
    print("\n10. Cost (R15)")
    rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
    kit = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if not r["item"].startswith(EXCLUDED))
    exc = {r["item"]: float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if r["item"].startswith(EXCLUDED)}
    gen_new = next(float(r["unit_cost_usd"]) for r in rows if r["item"].startswith("5 "))
    salv = kit - gen_new + SALVAGED_GEN
    line("Turbine kit, new generator", kit, "USD", "{:.2f}")
    line("Turbine kit, salvaged washing machine motor", salv, "USD", "{:.2f}")
    for k, v in exc.items():
        line(f"Excluded: {k}", v, "USD", "{:.2f}")
    line("Value-engineering target (project.yaml budget_usd)", BUDGET, "USD", "{:.0f}")
    line("Over (+) or under (-) the target, new generator", kit - BUDGET, "USD", "{:+.2f}")
    R.update(kit=kit, kit_salvaged=salv, budget=BUDGET, excluded=exc)

    out = ROOT / "docs" / "04-calcs" / "results.json"
    out.write_text(json.dumps(R, indent=1, default=float))
    print(f"\nWrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
