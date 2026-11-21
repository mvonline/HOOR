# Chapter One terrain — 0.2.4-dev

Canyon walls now include broad lateral erosion and height variation seeded
independently on the two sides. The variation blends in above the road shoulder
and fades out before the widened camp clearing. An initial render showed unwanted
deformation in that clearing; the fade was added to preserve it.
The driveable road and gully height function remain the same.

The continuous terrain is split into sections of 24 route-sample intervals, each
with its own renderer and collision mesh. Adjacent sections share boundary vertex
positions and normals calculated on the complete source mesh. This permits
frustum culling by section rather than retaining one renderer for the full route.
An actual frame-rate improvement has not been measured.

Dusk ambient sky/equator fill is slightly brighter, and the ground ambient colour
now transitions with dusk as well. The camp's practical lights remain in place.

The final Windows build passed all 40 native rule checks and the full 3,374 m
automated drive in 608.7 simulated seconds. The terrain section-count and finite
vertex checks also passed. The verification script found no runtime exception or
shader-error matches.

The canyon-drive and corrected camp-arrival renders were visually inspected at
`builds/checks/chapter-one/03-canyon-drive.png` and `04-camp-arrival.png`.
Build/runtime logs are `builds/chapter-one-build.log` and
`builds/checks/chapter-one/player.log`. Art remains at prototype fidelity;
hardware performance and human movement/audio reviews remain outstanding.
