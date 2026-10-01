# BOM notes

All costs are indicative USD prices for TRL 3 (a priced BOM on paper), not quotes. Every line has a unit cost and a supplier or supplier type. Item numbers match the exploded view (`media/exploded.png`), the general arrangement drawing PCF-DWG-001 and the component table in `docs/02-concept.md`. The totals are computed by `docs/04-calcs/sizing.py` (PCF-CAL-001 section 11).

| Group | Items | Cost |
| --- | --- | --- |
| Turbine kit, new generator | 1 to 8, 10 to 16, 18, 19 | USD 614.00 |
| Turbine kit, salvaged washing machine motor (about USD 40) | 1 to 8, 10 to 16, 18, 19 | USD 544.00 |
| Penstock, 20 m of 125 mm (excluded, site-dependent) | 9 | USD 140.00 |
| Battery (excluded, household item) | 17 | USD 160.00 |

Value-engineering target: USD 450 (`budget_usd` in `project.yaml`; a hypothetical control target, not a limit, Amish, 2026-10-01). Estimated cost of the constructable design: USD 614 (USD 164 over the target); USD 544 with a salvaged motor (USD 94 over). The penstock and battery are outside the target, as decided on 2026-09-25 (PCF-DDR-001 D1). Prices are to be firmed with quotes before any build (TRL 4, on hold).

Changes for the constructable design (PCF-DDR-003, 2026-10-01), from USD 448.00: fixings, new line 19 (+USD 28); pipe stands, new line 18 (+USD 15); 125 x 90 reducer, flexible couplings and gaskets in line 7 (+USD 12); flange bearing units, sleeves, V-ring and 160 mm guard in line 3 (+USD 10); valve reducer, expander and nipples in line 8 (+USD 8); forebay tank connector and screen frame in line 10 (+USD 8); post anchor in line 12 (+USD 3); clamping hub in line 2 (+USD 2).

Earlier changes: the design-point penstock changed from 110 mm to 125 mm on 2026-09-25 (PCF-DDR-002 N1), outside the kit; from TRL 2 (USD 424): 90 mm branches (+USD 8), multi-turn gate valve (+USD 2), coupling guard (+USD 3), independent clamp in the controller (+USD 3), 8.2 ohm clamp resistor (+USD 13), shorter frame (-USD 5).

Full-bore inlet valve (decided by Amish, 2026-10-01, N6 option a; `docs/06-design-decisions.md`), from USD 534.00: line 8 rises from USD 40 (90 mm gate valve, reducer, expander and two nipples) to USD 120 (+USD 80). Price basis: an estimate, not a quote. Full-bore PVC-U gate valves with socket ends are made in sizes up to DN300 (for example by Petron Thermoplast, PN10, handwheel), but no published price was found for the 125 mm size; US-made 4 in PVC gate valves list at over USD 1,000 (Spears 2022-040, USD 1,700.91 at pvcfittingsonline.com, read 2026-10-01). USD 115 is assumed for an imported metric PVC-U valve, with no published price behind it, and USD 5 for the 175 mm pipe piece (cut from the penstock) and solvent cement. The line must be quoted before any build; it buys back about 3.9 W at the design point (PCF-CAL-001).
