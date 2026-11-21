# Vehicle and object model revision / source only

The user selected vehicles and object models as the main quality weakness. This pass focuses on Pirmard-7, the earlier damaged vehicle and camp equipment. It does not produce another executable or change the version number.

## Geometry and surfaces

Replaced the solid lower-body block with pressed side skins containing real wheel openings. Added curved bolt-on arch flares, a crowned bonnet with returned edges, staggered tire treads, rim vents and continuous rolled rim lips. Added seating, dashboard and steering detail behind transparent glass, plus wipers, hinges, cowl vents, mud flaps, axle/spring detail, recovery fittings and plate geometry. Roof canvas now has a rounded roll silhouette. The damaged vehicle has a complete hinged open-door assembly with window frame, lining and pull, a local bonnet dent and windscreen fracture detail. The shared repair weld remains intact for the story comparison.

Corrected planar UV projection by face direction; the old x/z-only mapping collapsed vertical surfaces into stripes. Added a paint finish shader with subtle low-body dust and varying smoothness, restrained lens colour and metal response. Glass uses Standard premultiplied transparency and a visible cabin, rather than opaque blue panels. These remain authored game models; final hand-painted texture sets, cinematic close-up geometry and detailed damage sculpts are unfinished.

Equipment cases gain lids, corner protectors and carrying grips. Workstations gain folding braces, stretchers, plank fasteners, directional wood grain, radio controls/aerial and layered notebook edges. Existing interaction points and vehicle contact envelopes are retained.

The asset rebuilder now updates existing materials, textures and meshes in place. Prefab and paint-material GUID preservation is checked, avoiding broken references to the baked kit. Default project preparation still avoids rebuilding an existing kit unless explicitly requested.

## Validation and cost

All five Editor gameplay suites passed after the general vehicle/object update. Camp and spine suites passed again after the damaged-door changes, including close inspections, weld comparisons, memory interaction and later rescue progression. The final rim-only optimisation was rebaked and geometry-validated, without repeating unrelated gameplay suites.

The model review checks saved geometry for invalid vertices, raycasts the paint mesh to verify two real wheel openings and a solid door panel between them, checks transparent glass configuration and stable asset references. Final review passed. Matching old-asset studio views were rendered from the unchanged archived validation-project kit without rebuilding it. Final intact/damaged vehicle and workstation renders were inspected. There is no claim of continuous human playtesting or target-PC frame rate.

| Asset | Archived triangles | Current triangles |
|---|---:|---:|
| Pirmard7 | 15,464 | 45,836 |
| EarlierPirmard | 15,428 | 46,164 |
| Workstation | 1,760 | 4,048 |

The first detailed vehicle pass used 70,156 triangles. Replacing many cylinder pieces in rim lips with continuous shared-vertex meshes reduced the intact vehicle by 24,320 triangles (about 35%) while keeping the rounded rim detail. The current models still cost more than the old kit; target-PC profiling and future LODs remain necessary before claiming a production performance target. Geometry is batched by material into the existing prefab scheme.

Review: ../artifacts/vehicles/20261105-model-pass/index.html contains interactive comparisons using identical cameras and lights. These are actual Unity renders, not concept images. No Suno downloads or credits were used. The distributed 0.6.1 executable is unchanged.

Continuation: material maps, tangent support, hex fasteners and shaped headlamp optics are now added in source. Current triangle counts are 49,860 intact and 50,188 damaged. See 20261105-vehicle-surface-optics.md for validation and details.html for the fresh close-up/gameplay render review.
