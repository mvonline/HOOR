# Chapter One dusk reveal — 0.2.6-dev

The screenplay's first sensory leg at dusk now uses an articulated, tapered mesh
instead of two rigid rods scaled from their origin. Its base stays below the
sand, the joint rises as dusk advances, and a restrained probing motion animates
the tip. The surface uses matte, sand-dark cuticle with ring variation.

The reveal stands in the shaded side of the existing approach, outside the clear
driving lane. It adds no attack, dialogue, mission, or Chapter Two event.

Verification adds an emergence/bounds check at dusk and a driver-approach render,
`builds/checks/chapter-one/09-dusk-sensory-leg.png`.
The final Windows build passed all 40 native rule checks and the full 3,374 m
automated route, including the new emergence check. Existing audio, exit and
completion persistence checks passed as well. Logs are in
`builds/chapter-one-build.log` and `builds/checks/chapter-one/player.log`.

The initial close inspection at completed-camp lighting was too dark. Cuticle
albedo was raised and the final render uses the actual approach's dusk level,
vehicle position and headlights. Visual inspection confirms the limb silhouette
is visible beside the clear lane. This remains a simple prototype model, with
human playtesting and final creature art outstanding.
