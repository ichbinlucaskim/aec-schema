# Unit Conventions

All numeric values in aec-schema use the following units unless explicitly noted.

| Quantity | Unit | Notes |
|---|---|---|
| Coordinates (x, y, z) | mm | Origin at structural grid intersection |
| Lengths, widths, heights | mm | |
| Areas | m² | sheathing_area_m2 in BOM only |
| Angles | degrees | (not currently used) |

## Common member cross-sections (nominal → actual)

| Nominal | Actual (mm) | Actual (in) |
|---|---|---|
| 2x3 | 38 × 64 | 1.5 × 2.5 |
| 2x4 | 38 × 89 | 1.5 × 3.5 |
| 2x6 | 38 × 140 | 1.5 × 5.5 |
| 2x8 | 38 × 184 | 1.5 × 7.25 |
| 2x10 | 38 × 235 | 1.5 × 9.25 |
| 2x12 | 38 × 286 | 1.5 × 11.25 |

## Stud spacing

Standard North American light wood framing: **400mm (16" o.c.)** or 610mm (24" o.c.).

## Wall height reference

| Description | mm | Imperial |
|---|---|---|
| Standard 8ft wall (total) | 2438 | 8′-0″ |
| Standard 9ft wall (total) | 2743 | 9′-0″ |
| Precut stud — 8ft wall | 2286 | 92-5/8″ |
| Precut stud — 9ft wall | 2629 | 103-5/8″ |

Total wall height = bottom plate (38mm) + stud + top plate 1 (38mm) + top plate 2 (38mm).
