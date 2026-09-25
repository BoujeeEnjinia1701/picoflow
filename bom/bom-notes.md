# BOM notes

All costs are indicative USD prices for TRL 3 (a priced BOM on paper), not quotes. Every line has a unit cost and a supplier or supplier type. Item numbers match the exploded view (`media/exploded.png`), the general arrangement drawing PCF-DWG-001 and the component table in `docs/02-concept.md`. The totals are computed by `docs/04-calcs/sizing.py` (PCF-CAL-001 section 11).

| Group | Items | Cost |
| --- | --- | --- |
| Turbine kit, new generator | 1 to 8, 10 to 16 | $448.00 |
| Turbine kit, salvaged washing machine motor (about $40) | 1 to 8, 10 to 16 | $378.00 |
| Penstock, 20 m of 110 mm (excluded, site-dependent) | 9 | $100.00 |
| Battery (excluded, household item) | 17 | $160.00 |

The budget in `project.yaml` is $450, set by Amish on 2026-09-25 (PCF-DDR-001 D1); the penstock and battery are excluded from it. The kit with a new generator is $2.00 under budget, which is within the error of indicative prices, so R15 is at risk.

Changes from TRL 2 ($424): 90 mm branches instead of 63 mm (+$8), multi-turn gate valve (+$2), coupling guard (+$3), independent clamp in the controller (+$3), 8.2 ohm 300 W clamp resistor (+$13), shorter frame (-$5).
