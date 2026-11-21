# Companion routes and final exit / source work / 2026-11-05

Replaced straight movement through scenery for Yunus's H05 exit, Dara's Chapter 6
following/descent and Sara's Chapter 8 retreat with bounded grid route planning.
Cells respect capsule clearance, eight-neighbour routes cannot cut blocked corners,
and movement sweeps the body against actual contact geometry. Unavailable paths
stop an actor rather than teleporting it. Moving companions are considered when
planning and following paths so the group can route around congestion.

Route workspaces and heap storage are reused. Planning has a 2,400-expansion cap;
actor routes are invalidated at scene changes and rebuilt when needed. This is
custom navigation, not a production NavMesh/crowd-animation system. Target-PC
profiling and broader human playtesting are still required.

Version-2 campaign saves now retain Sara, Bahram, Dara and active Yunus positions,
including Yunus's heading. Older saves without these fields retain their authored
spawn behaviour. Mid-route reloads no longer reset these actors to the start.

## Final exit correction

The old final-route interpolation depended on output-on time. Releasing the unit
froze companions partway along the exit. Once the locator confirms passage, Sara,
Bahram and Dara now continue walking independently of the output to distinct safe
positions beyond the gate. The former solid gate block is replaced with two piers
and an overhead lintel, leaving real clearance underneath.

The dawn timing/Bang rules are unchanged. Companion navigation does not rewind
the live clock or make noise a magical condition. Scripted rescue pulls, enemy
movement and every offscreen transition are not claimed to be fully finished here.

## Validation

Editor regressions check an actual wall detour, blocked-route stop, movement
distance limits, the entire Yunus exit around the alcove, mid-route position
reload, Dara's wider downhill clearance, an open gate/solid pier, and all three
companions completing their exit after output release. Existing dawn outcomes
continue to pass. These are controlled simulations, not a full human playtest.

No executable, release archive or version increment was made.
