---
doc_id: PCF-BLD-001
title: PicoFlow prototype build plan
project: PicoFlow
doc_type: Build plan
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan; design made constructable (PCF-DDR-003)
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Full-bore 125 mm inlet valve fitted with a short pipe piece (section 3.14, step 17, joint 13); pictures regenerated
  - version: "0.3"
    date: '2026-10-01'
    author: Amish Chadha
    change: Clamp resistor 6.8 ohm, 350 W (was 8.2 ohm, 300 W) in section 3.16 and the wiring picture (Figure 31); parts cost USD 618
  - version: "0.4"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Decisions of 2026-10-02: frame and pipe stands welded from bare steel and galvanized or painted afterwards; guard PVC or polycarbonate, never acrylic; no housing window; safety stops S6 and S7 updated. Pictures unchanged"
  - version: "0.5"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Approved follow-ups: frame and pipe stand making sketches (PCF-DWG-101, 111) now say bare steel, galvanized or painted after welding"
---

# PicoFlow prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. The penstock is a short stub; the real run is 10 to 30 m of pipe from the forebay.*

The prototype is one PicoFlow turbine set on a concrete pad over a tailrace, with its pipework, inlet valve, forebay and an equipment post for the electrics. Water from the forebay runs down the penstock, through a slow-closing valve and a tee, to two printed nozzles that fire jets onto a printed Turgo runner inside an open-bottomed plastic pipe; the runner turns a generator on top through a shaft in two sealed bearings. Figure 1 shows the 23 components in the order you make or fit them. Fourteen are made in a small workshop: the welded steel frame, the housing cut from sewer pipe, two printed nozzles and their inserts, the plastic lid, the shaft, the printed runner, the guard, the posts and sleeves, the generator plate, three pipe stands, the cut pipework, the forebay and the equipment post. Everything else is bought and fitted: bearing units, hub, coupling, generator, pipe fittings, valve, rectifier, controller modules, resistors, wiring and fixings. The work is sawing and welding steel angle, cutting and drilling plastic pipe and sheet, 3D printing, solvent welding PVC, and wiring bought modules. The turbine kit costs about USD 618 in parts with a new generator, from the bill of materials; the penstock and battery are extra.

> **Safety:** Streams and weirs can drown people; work at the site only at low flow, never alone, and close the intake before entering the stream. The runner and coupling spin at 300 to 450 rpm: close the valve and wait for them to stop before opening anything. With no load and a failed clamp the generator can reach about 80 V DC, so the DC side is enclosed and rated for 100 V. The dump load and clamp resistor run above 200 °C. The 12 V battery can deliver hundreds of amperes into a short. Close the gate valve slowly, over at least ten turns. Welding, grinding and printing need eye protection and ventilation.

## 2. What changed to make it buildable

The concept showed what the turbine does; some of its parts could not be made, fixed or assembled as drawn. Each change below keeps what the turbine does, and all of them are recorded in decision record PCF-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Frame | Solid square bars, 420 mm square; the housing sat inside the opening with nothing under it | A welded square of 40 x 40 x 4 mm angle, 380 mm outside, with legs, foot plates and pipe stops (Figures 2 and 3) | The housing wall now stands on the angle |
| Frame, housing and lid | Not joined | Four tie rods from the frame corners through the lid; a groove under the lid locates the housing (Figures 3 and 13) | One set of nuts holds the stack and frees the lid for service |
| Bearings | A plain cylinder bored for the shaft, with no bearing seats | Two bought flange bearing units on spacer sleeves, bolted through the lid, and a V-ring seal (Figure 14) | No machining; seats, seals and locking come with the units |
| Runner fixing | A keyed hub and clamp nut, not drawn | A bought clamping hub screwed to the runner (Figure 17) | No keyway or thread to cut |
| Nozzles | Cones cutting into the housing wall, with no fixing and no joint to the pipe | Printed nozzles with a horizontal spigot, a bend and a saddle bolted to the housing on a gasket; a flexible coupling to the pipe (Figures 5 to 8) | The saddle fixes the aim and seals the hole |
| Nozzle tip and runner | The runner could not be lifted past the nozzle tips | Nozzle tips end at the housing wall, 115 mm before the strike point; runner 11 mm lower so the jets still meet the top of the buckets (Figure 18) | The lid, shaft and runner lift out together for service |
| Generator, posts, guard | Generator 5 mm above its plate; posts and guard with no fixing | Generator screwed to the plate; posts as tubes on threaded rods; a 160 mm pipe guard held between lid and plate (Figures 20 and 22) | Everything is clamped or screwed |
| Pipework | A tee and elbows placed closer together than real fittings allow; no supports | Penstock on the jet 2 line into a reducing tee, standard fittings with their sockets allowed for, three pipe stands (Figures 24 to 27) | Every fitting is a standard one |
| Inlet valve | A 90 mm valve drawn as a block on the 125 mm line | A full-bore 125 mm gate valve with solvent-weld sockets, joined to the tee by a 175 mm piece of penstock pipe (Figure 28) | It joins the 125 mm line directly, and its bore matches the penstock's, so it costs almost no head |
| Mass | Fixings and feet not counted | Generator plate 8 mm, foot plates 5 mm, post tube 20 x 2 mm | Keeps the turbine unit at 24.5 kg, under the 25 kg limit |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. Heights are measured up from the top of the pad, which is the normal tailwater level. "Jet 1" is the nozzle whose pipe runs round the housing; "jet 2" is the one fed straight from the tee. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Turbine frame

![Figure 2. Making sketch of the turbine frame](../cad/drawings/PCF-DWG-101.png)

*Figure 2. Turbine frame making sketch (PCF-DWG-101).*

**What it is and what it is made from.** The square steel frame the housing stands on, bolted to the pad over the tailrace. Bare (uncoated) steel angle 40 x 40 x 4 mm, about 1.8 m; flat bar 80 x 5 mm and 30 x 5 mm; hot-dip galvanized or painted after welding. A local fabricator welds it.

**How to make it.**

1. Cut four 380 mm lengths of angle with 45° mitres at both ends, so the horizontal legs point inward when the square is assembled.
2. Clamp the square on a flat bench, check that the diagonals agree within 2 mm, and weld the four corners. Grind the top faces flush.
3. Drill an 11 mm tie rod hole in each corner, through the overlapping horizontal legs, 170 mm from both centre lines.
4. Cut four 70 mm lengths of angle for the legs. Fit each inside a corner, tight under the horizontal legs and against the vertical legs, and weld.
5. Cut four 80 x 80 mm foot plates from 5 mm flat bar. Drill a 13 mm anchor hole in each, 18 mm in from two adjacent edges. Weld one under each leg so it reaches outward, with the hole outside the corner of the square (208 mm from both centre lines).
6. Cut four 30 mm lengths of 20 x 5 mm flat bar for the pipe stops. Weld one upright on each horizontal leg at the middle of each side, its inner face 158.5 mm from the centre of the frame.
7. Clean the welds, then have the whole frame hot-dip galvanized, or paint it. Never weld galvanized steel: the zinc gives off toxic fumes.

**How it fits the parts next to it.**

![Figure 3. Joint 1: frame corner, leg, foot and tie rod](05-build-plan/joint-01.png)

*Figure 3. A frame corner cut along its diagonal: the leg is welded inside the corner, the tie rod is locked to the angle by a nut above and below, and the anchor goes into the pad outside the corner.*

The housing wall stands on the horizontal legs; the inner edge of the angle lines up with the inside of the housing, so water falling from the runner passes clear. The four stops sit 1 mm outside the housing and stop it sliding (Figure 4). The tie rods pass up through the corner holes, beside the housing.

![Figure 4. Joint 2: housing on the frame at a pipe stop](05-build-plan/joint-02.png)

*Figure 4. The housing wall on the angle, with a pipe stop 1 mm outside it.*

**Check before moving on.** The top of the frame is flat within 1 mm; a 315 mm pipe offcut drops in between the stops without forcing.

### 3.2 Housing

![Figure 5. Making sketch of the housing](../cad/drawings/PCF-DWG-102.png)

*Figure 5. Housing making sketch (PCF-DWG-102).*

![Figure 6. Full-size template for the nozzle holes](05-build-plan/nozzle-hole-template.png)

*Figure 6. Nozzle hole template, unrolled onto the pipe surface. Print the PDF version (`docs/05-build-plan/nozzle-hole-template.pdf`) at 100 %.*

**What it is and what it is made from.** The open-ended pipe the runner turns inside; the jets come in through its wall and the water falls out of its bottom. 315 mm PVC sewer pipe, SN4 class, 7.7 mm wall.

**How to make it.**

1. Cut 303 mm of pipe. Wrap a strip of card round the pipe as a guide, saw square with a fine-tooth saw and file both ends flat.
2. Mark a line round the pipe 208.6 mm up from one end (the bottom end).
3. Print two copies of the template (Figure 6) at actual size and check the 50 mm bar. Tape one to the pipe with its green line on your mark and UP toward the top. Tape the second half way round the pipe, also on the mark and also with UP toward the top.
4. Drill the eight 6.6 mm bolt holes square to the wall through the small circles.
5. Chain drill 6 mm holes just inside each hole outline, cut out with a jigsaw and file to the line. The holes are 2.5 mm larger all round than the nozzle that passes through them.
6. Deburr every edge.

**How it fits the parts next to it.** The bottom end stands on the frame between the four stops (Figure 4). The top 3 mm sits in the groove under the lid (Figure 13). Each nozzle passes through its hole, and its saddle covers the hole (Figure 8).

**Check before moving on.** Hold a nozzle in each hole: the tip passes through without touching the edge, and the saddle's bolt holes line up with the wall's.

### 3.3 Nozzles (make 2, both the same)

![Figure 7. Making sketch of the nozzle](../cad/drawings/PCF-DWG-103.png)

*Figure 7. Nozzle making sketch (PCF-DWG-103).*

**What it is and what it is made from.** The printed part that turns the pipe flow into a jet aimed at the runner. Each has a horizontal spigot that joins the pipe, a gentle bend, a converging cone, a saddle shaped to the housing, and a seat in its tip for the insert. PETG, 4 mm walls, 40 % infill. Jet 2's nozzle is jet 1's turned half a turn, so both are the same print.

**How to make it.**

1. Print two from the model file, standing on the spigot end, with supports under the saddle. Each needs a 167 x 130 x 244 mm space, about 310 g of filament and 12 h at 0.4 mm.
2. Remove the supports and sand the saddle face smooth so it follows the pipe.
3. Check the spigot is 90 mm outside; sand it down or build it up with tape until it fits the flexible coupling snugly.
4. Press two M4 heat-set inserts into the holes in the tip face with a soldering iron.
5. Cut two gaskets from 2 mm EPDM sheet to the saddle outline, with the nozzle hole and four bolt holes (the template's dashed circle, solid line and small circles).

**How it fits the parts next to it.**

![Figure 8. Joint 3: nozzle saddle on the housing](05-build-plan/joint-03.png)

*Figure 8. The saddle sits on its gasket on the outside of the housing; four M6 bolts go through saddle, gasket and wall, nuts inside.*

The tip passes through the housing hole and ends just inside the wall, 115 mm before the point where the jet meets the runner. The saddle and gasket cover the hole, held by four M6 x 25 stainless bolts from outside with washers and nuts inside, tightened evenly until the gasket is just squeezed. The spigot joins its pipe in a 90 mm flexible coupling (Figure 27). The nozzle is never glued.

**Check before moving on.** The saddle sits on the pipe with no rocking; the spigot slides into a flexible coupling by hand.

### 3.4 Nozzle inserts (make 2 per size)

![Figure 9. Making sketch of the nozzle insert](../cad/drawings/PCF-DWG-104.png)

*Figure 9. Nozzle insert making sketch (PCF-DWG-104).*

**What it is and what it is made from.** The replaceable ring in each nozzle tip that sets the jet size. The design point uses 34 mm; a set from 20 to 45 mm covers the head and flow range. PETG, 100 % infill.

**How to make it.**

1. Print a pair of 34 mm inserts with the front face down on the bed, so the jet edge is clean.
2. Ream or sand the bore to size and check it with a caliper; it must be round and within 0.2 mm.
3. Check the body (50 mm) slides into the nozzle seat.

**How it fits the parts next to it.**

![Figure 10. Joint 4: nozzle tip and insert](05-build-plan/joint-04.png)

*Figure 10. The insert sits in the nozzle tip from inside the housing, its flange against the tip face, held by two M4 screws into the heat-set inserts.*

**Check before moving on.** Each insert seats fully and its screws pull it flat against the tip.

### 3.5 Lid

![Figure 11. Making sketch of the lid](../cad/drawings/PCF-DWG-105.png)

*Figure 11. Lid making sketch (PCF-DWG-105).*

![Figure 12. Lid hole and groove layout](05-build-plan/lid-holes.png)

*Figure 12. Every hole and groove in the lid, measured from its centre.*

**What it is and what it is made from.** The square plate on top of the housing that carries the bearings, posts, guard and generator. HDPE sheet 12 mm (marine plywood, sealed, also works).

**How to make it.**

1. Cut 400 x 400 mm and round the corners to about 5 mm. Mark the centre from the diagonals.
2. Drill the holes from Figure 12: shaft 28 mm in the centre; bearing bolts 11 mm at 32 each way; post rods 11 mm at 125 each way; tie rods 11 mm at 170 each way.
3. Underneath, rout a ring groove 3 mm deep from 148.8 to 158.5 mm radius with a trammel jig pivoting in the centre hole.
4. On top, rout a ring groove 2 mm deep from 75.5 to 80.5 mm radius for the guard.

**How it fits the parts next to it.**

![Figure 13. Joint 5: lid on the housing](05-build-plan/joint-05.png)

*Figure 13. The top of the housing sits in the groove under the lid.*

The lid sits on the housing with its top 3 mm in the groove; the four tie rods come up through the corners and washers and nuts clamp it down (step 10).

**Check before moving on.** The lid drops onto the housing and the groove takes the whole rim without forcing.

### 3.6 Bearing units, spacer sleeves and V-ring

**What they are and what they are made from.** Two bought 4-bolt flange bearing units with a 20 mm bore (UCF204 class, sealed insert bearings), stacked on four 24 mm steel spacer sleeves and clamped to the lid by four M10 x 80 bolts. A rubber V-ring for a 20 mm shaft keeps spray off the lower bearing. The sleeves are cut with the posts (section 3.10).

**How to make it.** Nothing to make on the units. Check each turns freely and has both set screws.

**How it fits the parts next to it.**

![Figure 14. Joint 6: the two bearings on the lid](05-build-plan/joint-06.png)

*Figure 14. The four bolts go up from under the lid through the lower unit, the sleeves and the upper unit; nuts on top. The V-ring sits on the shaft under the lid.*

The lower unit's flange sits on the lid top; the sleeves stand on its flange; the upper unit sits on the sleeves, 5 mm above the lower unit's insert. Both inserts face the same way. The V-ring is pushed up the shaft until its lip just touches the lid underside.

**Check before moving on.** With the bolts snug, a 20 mm bar slides through both units without binding.

### 3.7 Shaft

![Figure 15. Making sketch of the shaft](../cad/drawings/PCF-DWG-106.png)

*Figure 15. Shaft making sketch (PCF-DWG-106).*

**What it is and what it is made from.** The 20 mm stainless shaft from the runner up to the coupling. 316 stainless bar, ground or h9, 20 mm.

**How to make it.**

1. Cut 294 mm; face both ends square and chamfer them 1 mm.
2. Polish off any burr so it slides through the bearings by hand.
3. At assembly, spot each bearing set screw into the shaft with a 5 mm drill 0.5 mm deep through the screw hole, then tighten.

**How it fits the parts next to it.** The bottom end is flush with the underside of the runner hub (Figure 17); the top end is half way into the jaw coupling, 30 mm above the upper bearing (Figure 20).

**Check before moving on.** Straight within 0.1 mm over its length: roll it on a sheet of glass.

### 3.8 Turgo runner and clamping hub

![Figure 16. Making sketch of the runner](../cad/drawings/PCF-DWG-107.png)

*Figure 16. Runner making sketch (PCF-DWG-107).*

**What it is and what it is made from.** The 200 mm printed runner with 20 buckets on a 150 mm pitch circle, and the bought clamping hub that fixes it to the shaft. PETG for the prototype (glass-filled nylon for field units); clamping shaft hub, 20 mm bore, 56 mm flange with four 5.5 mm holes.

**How to make it.**

1. Print the runner hub down, with supports under the buckets: about 525 g and 21 h at 0.4 mm, four perimeters.
2. Ream the bore to slide on the shaft.
3. Press four M5 heat-set inserts into the hub top on a 44 mm circle.
4. Balance: hang the runner on a rod through the bore. If one side always drops, sand the backs of the buckets on that side lightly until it stops in random places.

**How it fits the parts next to it.**

![Figure 17. Joint 7: runner on the shaft](05-build-plan/joint-07.png)

*Figure 17. The clamping hub grips the shaft; four M5 screws hold the runner to the hub.*

![Figure 18. Joint 9: the two jets at the runner](05-build-plan/joint-09.png)

*Figure 18. Seen from above: each jet meets the 150 mm pitch circle at the top of the buckets, and the nozzle tips stay 19 mm outside the circle the runner sweeps when it is lifted out.*

The hub's flange sits on the runner hub with four M5 screws into the heat-set inserts. The runner hangs 20 mm or more clear of everything round it: 50 mm from the housing, 46 mm from each nozzle, and 199 mm above normal tailwater.

**Check before moving on.** On the shaft, the runner spins freely and runs true within 1 mm at the rim.

### 3.9 Guard

![Figure 19. Making sketch of the guard](../cad/drawings/PCF-DWG-108.png)

*Figure 19. Guard making sketch (PCF-DWG-108).*

**What it is and what it is made from.** A short tube that covers both bearing units and the jaw coupling. 160 mm PVC pipe, 4 mm wall. A clear polycarbonate tube of the same size may replace it; never acrylic, which is brittle and would crack under a coupling failure. With the PVC guard, check the coupling spider only with the turbine stopped and the generator plate off.

**How to make it.**

1. Cut 146 mm; saw square, file both ends flat and deburr inside.
2. Drill two 6 mm drain holes at the bottom edge, on opposite sides.

**How it fits the parts next to it.**

![Figure 20. Joint 8: coupling, guard and generator](05-build-plan/joint-08.png)

*Figure 20. The guard stands in the groove on the lid and stops 1 mm under the generator plate, which holds it in place.*

**Check before moving on.** It stands upright in the groove; the plate clears its top.

### 3.10 Posts, post rods, spacer sleeves and tie rods

![Figure 21. Making sketch of the post and spacer sleeve](../cad/drawings/PCF-DWG-109.png)

*Figure 21. Post and spacer sleeve making sketch (PCF-DWG-109).*

**What they are and what they are made from.** Four posts that hold the generator plate 145 mm above the lid, each a steel tube on a threaded rod; the four short sleeves of the bearing stack; and the four tie rods from frame to lid. Steel tube 20 x 2 mm, 20 mm tube with a 10.5 mm or larger bore, and M10 threaded rod, stainless or galvanized.

**How to make it.**

1. Cut four posts 145.0 mm long; face the ends square on a disc sander, all four the same within 0.2 mm.
2. Cut four spacer sleeves 24.0 mm long, the same within 0.1 mm.
3. Cut four post rods 195 mm long and four tie rods 345 mm long from M10 rod. Clean the threads at the cut ends with a nut.
4. Paint or galvanize the cut ends.

**How it fits the parts next to it.**

![Figure 22. Joint 12: post between lid and generator plate](05-build-plan/joint-12.png)

*Figure 22. The rod clamps the post between the lid and the plate; a 30 mm washer under the lid spreads the load.*

Each post stands on the lid 125 mm each way from the centre. Its rod goes up from under the lid, through the post and the plate, with a 30 mm washer and nut under the lid and a washer and nut on the plate. The washers under the lid clear the housing by 4 mm. Each tie rod stands 12 mm below the frame angle, locked by a nut above and below (Figure 3), and its top passes through the lid with a 30 mm washer and nut.

**Check before moving on.** The four posts stand the same height on a flat surface.

### 3.11 Generator plate

![Figure 23. Making sketch of the generator plate](../cad/drawings/PCF-DWG-110.png)

*Figure 23. Generator plate making sketch (PCF-DWG-110).*

**What it is and what it is made from.** The plate the generator stands on. Aluminium plate 8 mm, 5083 or 6082 class, 280 x 280 mm.

**How to make it.**

1. Cut 280 x 280 mm, file the edges and round the corners. Mark the centre from the diagonals.
2. Drill or cut a 62 mm centre hole for the generator's shaft and spigot (it must clear the spigot of the generator bought by 1 mm).
3. Drill four 11 mm post holes at 125 mm each way from the centre.
4. Drill four 6.6 mm generator screw holes on the screw circle of the generator bought (the model uses a 176 mm circle at 45°).

**How it fits the parts next to it.** The plate sits on the four posts, nuts on top; the generator stands on it, held by four M6 screws from below into its face; the guard stops 1 mm under it (Figure 20).

**Check before moving on.** The plate sits on all four posts without rocking, and its centre hole lines up over the shaft.

### 3.12 Pipe stands (make 3)

![Figure 24. Making sketch of the pipe stand](../cad/drawings/PCF-DWG-111.png)

*Figure 24. Pipe stand making sketch (PCF-DWG-111).*

**What it is and what it is made from.** A short steel stand with a pipe clip that carries the branch pipework at the nozzle height. Bare steel angle 40 x 40 x 4 mm, galvanized or painted after welding, flat bar 100 x 6 mm and 60 x 5 mm, a 90 mm pipe clip with an M8 boss.

**How to make it.**

1. Cut a 259 mm upright from angle and a 100 x 100 mm foot from 6 mm flat bar; drill an 11 mm anchor hole in the foot, 35 mm in from two edges.
2. Weld the upright square in the middle of the foot.
3. Cut a 60 x 60 mm top plate from 5 mm flat bar, drill 9 mm in the middle and weld it square on top of the upright.
4. Galvanize or paint the stand once it is welded, never before.
5. Put an M8 bolt up through the top plate and screw the clip's boss onto it.

**How it fits the parts next to it.**

![Figure 25. Joint 11: pipe stand under the long run](05-build-plan/joint-11.png)

*Figure 25. The clip's band holds the pipe; turning the clip on its M8 bolt sets the height.*

One stand goes under the tee branch, one under the long run behind the housing and one under the short drop to jet 1 (Figure 1). The bottom of the pipe is 290 mm above the pad.

**Check before moving on.** The pipe sits in each clip without being pushed up or pulled down.

### 3.13 Nozzle manifold pipework

![Figure 26. Cutting and fitting sketch of the pipework](../cad/drawings/PCF-DWG-112.png)

*Figure 26. Pipework cutting and fitting sketch (PCF-DWG-112).*

**What it is and what it is made from.** The fittings and pipes that split the flow from the penstock to the two nozzles. A 125 x 90 mm reducing tee, a 125 x 90 mm reducer, three 90° elbows, about 1.6 m of 90 mm PVC pipe and two 90 mm flexible rubber couplings with band clamps.

**How to make it.**

1. Cut five lengths of 90 mm pipe, square and deburred, for fittings with 45 mm sockets (adjust each by the difference if yours differ): P1, tee branch to the first elbow, 275 mm; P2, the long run behind the housing, 970 mm; P3, the short drop, 135 mm; P4, last elbow to the jet 1 coupling, 100 mm; P5, reducer to the jet 2 coupling, 110 mm.
2. Dry fit everything on the stands with the nozzles in place: the valve's pipe piece (section 3.14) enters one end of the tee's 125 mm run; the other end takes the reducer and P5 to jet 2; the 90 mm side branch takes P1, an elbow, P2, an elbow, P3, an elbow and P4 to jet 1.
3. Mark each joint across both parts so it goes back the same way, then solvent weld the PVC joints one at a time, keeping the elbows square. Never glue a nozzle.

**How it fits the parts next to it.**

![Figure 27. Joint 10: nozzle inlet joined to the pipe](05-build-plan/joint-10.png)

*Figure 27. A flexible coupling joins the printed spigot to the end of P4 (or P5), end to end; two band clamps hold it.*

The pipework centre line is 338 mm above the pad all round, the height of the nozzle spigots. It sits in the three stand clips and joins each nozzle through a flexible coupling, band clamps snug but not crushing the printed spigot.

**Check before moving on.** Dry fitted, the pipework reaches both spigots with no strain and the centre line is level within 3 mm.

### 3.14 Inlet valve and its pipe piece

**What they are and what they are made from.** A bought full-bore 125 mm PVC-U gate valve, multi-turn with a handwheel so it cannot close in under about 10 s, with a solvent-weld socket for 125 mm pipe at each end. The one drawn is about 330 mm long over its sockets, with 70 mm deep sockets, a 200 mm handwheel whose top is about 300 mm above the pipe centre line, and a mass of about 5.5 kg. A 175 mm piece of the 125 mm penstock pipe joins it to the tee.

**How to make it.**

1. Before cutting, measure the valve's socket depth and the depth of the tee's 125 mm socket. Cut the pipe piece from the penstock pipe, square and deburred, to 60 mm plus both socket depths: 175 mm for a 70 mm valve socket and a 45 mm tee socket. The 60 mm is the clear gap between the valve and the tee, which leaves room to turn the handwheel and to cut the line out later.
2. Chamfer both ends of the pipe piece and the end of the penstock lightly, so they slide into the sockets without pushing the cement off.
3. Count the turns from open to closed and write the number on the handwheel; it should be about ten. Look through the open valve: the gate must lift clear of the bore.

**How it fits the parts next to it.**

![Figure 28. Joint 13: inlet valve between the penstock and the tee](05-build-plan/joint-13.png)

*Figure 28. The pipe piece goes fully into the tee's free 125 mm socket and the valve's downstream socket; the penstock goes fully into the valve's upstream socket. The bore is 117 to 118 mm all the way through.*

The pipe piece is solvent welded into the free end of the tee's 125 mm run and into the valve's downstream socket; the penstock is solvent welded into the valve's upstream socket (step 17). No reducer or expander is needed. The valve stem stands straight up so the handwheel is easy to reach and clears the pipework by 60 mm. The valve is heavier than the pipe either side, so the penstock's own site support goes within 300 mm of the valve's upstream socket, and the stand under the tee branch carries the downstream side.

**Check before moving on.** The valve opens and closes fully, takes about ten turns, and the pipe piece and penstock each go fully home in their sockets when dry fitted.

### 3.15 Forebay tub and intake screen

![Figure 29. Making sketch of the forebay](../cad/drawings/PCF-DWG-113.png)

*Figure 29. Forebay making sketch (PCF-DWG-113).*

**What it is and what it is made from.** The tub at the top of the drop that settles sand and screens the water before it enters the penstock. A stiff polyethylene tub about 560 x 460 x 400 mm, a 125 mm tank connector, 6 mm stainless mesh and 20 x 20 x 3 mm aluminium angle.

**How to make it.**

1. Cut a 128 mm hole centred 110 mm up in the downstream end and fit the tank connector, gasket inside, nut outside.
2. Cut an overflow notch 200 mm wide and 40 mm deep in the upstream rim.
3. Make a 600 x 500 mm frame from mitred angle, riveted at the corners; rivet a 580 x 480 mm piece of mesh to it.

**How it fits the parts next to it.** The screen frame rests on the rim and overlaps it 10 mm all round. The stream is led onto the screen; water drops through, and surplus runs over and carries leaves away. The penstock joins the tank connector.

**Check before moving on.** No gap larger than 6 mm anywhere round the screen.

### 3.16 Equipment post and electrics

![Figure 30. Making sketch of the equipment post](../cad/drawings/PCF-DWG-114.png)

*Figure 30. Equipment post making sketch (PCF-DWG-114).*

**What it is and what it is made from.** A timber post beside the turbine that carries the rectifier box, the controller box and the guarded resistors, out of the spray and above flood level. Treated timber 70 x 70 mm, 1.4 m, in a bolt-down post anchor.

**How to make it.**

1. Cut the post, seal the cut ends and bolt it into its anchor with two M10 coach bolts.
2. Mark the boxes on the face toward the turbine: rectifier box 840 to 960 mm up, controller box 1,030 to 1,230 mm up.
3. Mark the resistor guard on the side face, 540 to 700 mm up, with 50 mm of air all round and nothing that burns within 300 mm above it.
4. Fit each box on four stainless screws through its own mounting holes, cable glands facing down.

#### 3.16.1 Wiring

![Figure 31. Block-level wiring](05-build-plan/wiring.png)

*Figure 31. Block-level wiring with wire sizes. No circuit board is laid out at this stage; bought modules stand in for the controller board.*

The controller in the bill of materials is an open-design board, laid out at TRL 4. For this prototype, buy modules that meet this specification:

*Table 2. Modules that stand in for the controller board.*

| Module | What to buy |
| --- | --- |
| Rectifier | Three-phase bridge, 35 A, 1,000 V, on an aluminium heat sink in a vented box |
| Charger | Synchronous buck charge controller with input-voltage (maximum power point) regulation, 15 to 60 V in, a 12 V LiFePO4 charge profile, and a battery-full output |
| Dump-load switch | MOSFET switch module rated 30 A at 12 V, driven by the charger's battery-full output |
| Voltage clamp | A comparator module with its own supply from the DC bus, on at 48 V and off at 40 V, driving a MOSFET or DC solid-state relay rated 100 V and 10 A that switches the 6.8 ohm clamp resistor across the bus, with no connection to the charger's control |
| Resistors | A 300 W, 12 V heating element or wire-wound dump load and a 6.8 ohm aluminium-clad clamp resistor rated 350 W or more, both on a heat sink inside a vented steel guard |
| Isolation | A 2-pole DC isolator rated 100 V, a 20 A fuse within 300 mm of the battery positive, cable glands |

Wire it like this, with stranded copper and a crimped lug or ferrule on every terminal:

1. Generator to rectifier, three phases: 4 mm², about 10 m, in a conduit along the pipework.
2. Rectifier to the charger input (the DC bus): 4 mm².
3. DC bus to the voltage clamp's sense input: 1.5 mm². Clamp switch to the 6.8 ohm resistor: 1.5 mm².
4. Charger output (12 V) to the DC isolator and on to the battery, with the 20 A fuse within 300 mm of the battery: 4 mm².
5. Charger output to the dump-load switch and on to the dump load: 4 mm².
6. Charger battery-full signal to the dump-load switch: 0.5 mm².

**Check before moving on.** Every wire continues end to end; with the battery fuse out and the generator disconnected, nothing on the DC bus reads below 1 kΩ to the post or the frame.

### 3.17 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Shaft and hub (line 2).** 20 mm ground 316 stainless bar, at least 300 mm; clamping shaft hub, 20 mm bore, about 56 mm flange with four 5.5 mm holes.
- **Bearings (line 3).** Two 4-bolt flange units, 20 mm bore, UCF204 class, sealed inserts with two set screws; rubber V-ring for a 20 mm shaft; 280 x 280 x 8 mm aluminium plate; 160 mm PVC pipe offcut.
- **Coupling (line 4).** Jaw coupling, L-075 class, with an elastomer spider, bores to suit the shaft and the generator.
- **Generator (line 5).** Low-speed three-phase permanent magnet motor used as a generator, about 500 W, about 10 rpm per volt, face mounting with a spigot and a shaft at least 50 mm long, overspeed rating at least 800 rpm.
- **Housing and lid (line 6).** 315 mm SN4 sewer pipe offcut at least 310 mm long; 400 x 400 x 12 mm HDPE sheet.
- **Pipework (line 7).** 125 x 90 mm reducing tee, 125 x 90 mm reducer, three 90 mm 90° elbows, 2 m of 90 mm PVC pipe, solvent cement, two 90 mm flexible couplings, PETG filament, 2 mm EPDM sheet.
- **Valve (line 8).** Full-bore 125 mm PVC-U gate valve, PN10 class, solvent-weld sockets for 125 mm pipe at both ends, multi-turn handwheel (never a quarter-turn valve); 175 mm of 125 mm pipe, cut from the penstock, for the pipe piece.
- **Forebay (line 10).** Tub, 125 mm tank connector, 6 mm stainless mesh, aluminium angle and rivets.
- **Rectifier, controller, resistors, wiring (lines 13 to 16).** As Table 2.
- **Fixings (line 19).** Stainless or galvanized: 2 m of M10 threaded rod, 24 M10 nuts, 16 penny washers 30 mm, four M10 x 80 bolts, eight M6 x 25 bolts with nuts and washers, four M6 x 20 screws, four M5 x 16 screws, four M4 x 12 screws, four M5 and four M4 heat-set inserts, four M12 anchors, M8 bolts for the stands.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: frame onto the pad

![Step 1](05-build-plan/step-01.png)

Set the frame level over the tailrace opening (shim the feet if needed) and fix it with four M12 anchors through the foot plates.

### Step 2: tie rods into the frame

![Step 2](05-build-plan/step-02.png)

Each rod through its corner hole with 12 mm below the angle; lock it with a nut above and a nut below, tight. The rods stand upright.

### Step 3: nozzles onto the housing (on the bench)

![Step 3](05-build-plan/step-03.png)

Lay the gasket on the saddle, pass the tip through the hole from outside and fit four M6 bolts from outside with washers and nuts inside. Tighten evenly until the gasket is just squeezed.

### Step 4: inserts into the nozzle tips

![Step 4](05-build-plan/step-04.png)

From inside the housing, slide each 34 mm insert into its tip and fit two M4 screws into the heat-set inserts.

### Step 5: housing onto the frame

![Step 5](05-build-plan/step-05.png)

Lower the housing between the four stops with jet 2's nozzle toward the penstock side and jet 1's toward the far side.

### Step 6: bearings onto the lid (on the bench)

![Step 6](05-build-plan/step-06.png)

Put the four M10 bolts up through the lid from below, then the lower unit, the four sleeves and the upper unit, with both units the same way up. Fit the nuts snug, not yet tight. Keep the V-ring by the lid; it goes onto the shaft in step 8.

### Step 7: clamping hub onto the runner (on the bench)

![Step 7](05-build-plan/step-07.png)

Flange down on the runner hub; four M5 screws into the heat-set inserts, even and firm.

### Step 8: shaft through the bearings

![Step 8](05-build-plan/step-08.png)

With the lid on trestles, slide the shaft down through both units and the lid, and push the V-ring onto it under the lid. Tighten the four bearing bolts. Leave the bearing set screws loose.

### Step 9: runner onto the shaft

![Step 9](05-build-plan/step-09.png)

Slide the runner's hub up the shaft until the shaft end is flush with the runner underside; tighten the hub clamp screw. Set the height so the top of the upper bearing is 30 mm below the shaft top, then spot and tighten the bearing set screws. Slide the V-ring up until its lip just touches the lid.

### Step 10: lid assembly onto the housing

![Step 10](05-build-plan/step-10.png)

With a helper, lower the lid with its bearings, shaft and runner over the tie rods, runner first, until the housing sits in the groove. Fit a 30 mm washer and nut on each rod and tighten them evenly in a cross pattern. **Hold point:** turn the runner by hand through the lid hole: it turns freely and touches nothing.

### Step 11: guard and posts onto the lid

![Step 11](05-build-plan/step-11.png)

Stand the guard in its groove. Put each post rod up through the lid from below with a 30 mm washer and nut under the lid, then slide a post over it.

### Step 12: generator onto the plate (on the bench)

![Step 12](05-build-plan/step-12.png)

Stand the generator on the plate with its spigot in the centre hole and fit four M6 screws from below into its face.

### Step 13: coupling onto the shaft

![Step 13](05-build-plan/step-13.png)

Fit the lower coupling hub on the shaft 10 mm above the upper bearing, and the upper hub on the generator shaft, with the spider between them; tighten the hub screws once the jaws are engaged in step 14.

### Step 14: generator and plate onto the posts

![Step 14](05-build-plan/step-14.png)

Lower the plate over the post rods, engaging the coupling jaws, until it sits on the posts over the guard. Fit a washer and nut on each rod. Check the shaft turns by hand with the generator, then tighten the coupling hubs.

### Step 15: pipe stands

![Step 15](05-build-plan/step-15.png)

Set the three stands on the pad under the line of the pipework, clips 290 mm up to their lowest point; fit the anchors loosely.

### Step 16: pipework onto the stands and nozzles

![Step 16](05-build-plan/step-16.png)

Lay the solvent-welded pipework in the clips with the tee on the penstock side. Slide the flexible couplings over the nozzle spigots and pipe ends and tighten the band clamps snug. Then tighten the stand anchors and clips.

### Step 17: inlet valve and penstock

![Step 17](05-build-plan/step-17.png)

Solvent weld the pipe piece into the free end of the tee's 125 mm run, then the valve onto the pipe piece, stem straight up; solvent weld the penstock into the valve's upstream socket and support it within 300 mm of the valve. Let the joints cure for the time on the cement tin, then close the valve fully.

### Step 18: forebay (at the top of the drop)

![Step 18](05-build-plan/step-18.png)

Fit the outlet connector, bed the tub level at the top of the drop with its overflow notch upstream, join the penstock, and set the screen frame on the rim.

### Step 19: equipment post and electrical boxes

![Step 19](05-build-plan/step-19.png)

Set the post anchor on ground above flood level, at least 1 m from the bank; fit the post, the rectifier and controller boxes on the face toward the turbine and the resistor guard on the side. Wire as Figure 31. **Hold point:** safety stop S4 in section 6.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of PCF-REQ-001.

*Table 3. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Setting height | R13 | Measure from normal tailwater (or the pad top) to the centre of a nozzle tip | 300 mm or less (280 mm in the model) |
| Parts fit the printer | R9 | Print the runner and both nozzles on a 220 x 220 x 250 mm printer | Each prints in one piece; runner in 24 h or less |
| Free running | R11 | Turn the runner by hand with the generator coupled | Turns smoothly; nothing rubs |
| Screen and inserts | R10 | Gauge the screen mesh and the smallest insert | Mesh 6 mm or less; smallest insert 20 mm or more |
| Valve closing | R17 | Count the turns from open to closed | About ten turns, so it cannot close in under 10 s |
| Clamp | R8 | Bench supply on the DC bus, generator disconnected, raised slowly from 30 to 50 V and back | Clamp switches in at 48 V and out at 40 V, whatever the charger does |
| Diversion | R7 | Bench supply in place of the generator; disconnect the battery | The dump load takes the output within 1 s |
| Output at low flow | R1, R3 | Admit water slowly with the valve; measure head, flow and power into the battery | The bus charges the battery; output recorded against head and flow (80 W at 2.0 m and 10 L/s is the target) |
| Service time | R11 | Time a runner or insert change and a bearing change with hand tools | 30 min and 60 min or less |
| Mass | R14 | Weigh the turbine unit (frame, housing, lid, rotor, bearings, plate, guard, generator, coupling, fixings) | 25 kg or less (24.5 kg estimated); no single item over 15 kg |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before any work in or beside the stream.** Flow is low, a second person is present, the intake is closed or diverted, and nobody stands on the weir crest.
- **S2. Before the lid goes on (step 10).** No tools, nuts or offcuts inside the housing; every saddle nut tight; the runner turns freely by hand.
- **S3. Before the generator plate goes on (step 14).** The guard is in its groove; the coupling hubs are tight on both shafts.
- **S4. Before any wire is connected to the battery.** The DC side is enclosed in its boxes; the clamp check of section 5 has passed on a bench supply; the battery fuse is out; the isolator is off; the resistor guard is mounted with clear air above it.
- **S5. Before water is admitted.** The generator is wired to the rectifier and the clamp and dump load are connected; nobody is near the runner, coupling or resistors; the valve is opened slowly, a turn at a time.
- **S6. Before opening the housing or removing the plate.** The valve is fully closed (over at least ten turns), the runner has stopped, and the isolator is off. The coupling spider is checked only in this state.
- **S7. Never.** Never weld galvanized steel; never fit an acrylic guard or a window in the housing; never fit a quarter-turn valve; never run with the clamp or dump load disconnected; never leave the screen uncleared, since a nozzle blocked all at once can add about 18 m of head to the drainage pipe.

## 7. Tools, skills and workspace

**Tools.** Hacksaw or bandsaw; angle grinder with cutting and flap discs; welder (or a local fabricator's welding); bench drill or a drill in a stand; drills 3 to 13 mm; jigsaw with fine plastic and metal blades; router with a 6 mm straight bit and a trammel jig; files; deburring tool; steel rule, square, calipers and a 45° mitre square; disc sander; 3D printer with a 220 x 220 x 250 mm bed that prints PETG; soldering iron for heat-set inserts; spanners and sockets 8 to 19 mm; hex keys; masonry drill for the anchors; spirit level; crimper and wire strippers; multimeter; bench power supply to 60 V with a current limit; scale to 30 kg; stopwatch.

**Skills.** A fabricator for the frame and stand welds; basic metalwork and plastics work; 3D printing; solvent welding of PVC; extra-low-voltage DC wiring. All circuits are DC below 60 V in normal running and below 100 V on a double fault; no mains wiring is part of this build.

**Workspace.** A bench about 1.5 x 0.8 m; a ventilated place for welding, grinding and printing; trestles to hold the lid assembly at waist height; at the site, a level pad over the tailrace and firm ground for the stands and post.

**Personal protective equipment.** Safety glasses for cutting, drilling and grinding; welding helmet and gloves for welding; hearing protection when grinding; gloves for sheet and mesh edges; a life jacket and non-slip boots for work beside the stream.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 74 checks); STEP and STL exports in `cad/step/` and `cad/stl/`, including `picoflow-nozzle`, `picoflow-runner`, `picoflow-insert-pair-34mm` and `picoflow-saddle-gaskets`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/PCF-DWG-101` to `PCF-DWG-114`. Hole template: `docs/05-build-plan/nozzle-hole-template.pdf`.
- General arrangement: `cad/drawings/PCF-DWG-001.pdf`, Rev P5.
- Calculations: `docs/04-calcs/01-sizing.md` (PCF-CAL-001) and `docs/04-calcs/sizing.py`.
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (PCF-DDR-003), with PCF-DDR-001 and PCF-DDR-002.
- Requirements: `docs/03-requirements.md` (PCF-REQ-001 v0.7).
