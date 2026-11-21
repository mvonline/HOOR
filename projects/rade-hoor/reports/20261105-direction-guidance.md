# Objective direction guidance and interaction review / 2026-11-05

User request: indicate when an object is behind the player or to either side,
then review project quality against the user's 3/10 assessment.

## Implemented

`LevelOneGuidance.cs` supplies a common current-objective marker for camp, cargo
memory, prologue, later chapters and playable aftermath. It includes distance,
turn-back/right/left/up/down instructions, an on-screen diamond and a rotated
screen-edge arrow. English/Persian labels are registered in the existing catalog.
Side/back instructions use horizontal camera bearing so looking up or down does
not incorrectly swap left/right. GUI coordinates account for letterboxing at
ultrawide and 4:3 aspect ratios. Existing duplicated markers were removed.

Known final-dawn targets use the same guidance: output unit before release,
independent crevice after release, stable circle when outside it, and cabin when
on foot. Guidance does not expose enemies or undiscovered optional evidence.
Documents, choices, pause and completion screens suppress it.

This is direction to a known objective, not pathfinding around walls or a floor
route. The larger navigation and visual-clarity review remains necessary.

## Physical interaction improvement

Reach checks now reject intervening layer-8 contact obstacles. A target collider's
own surface is accepted when the authored point lies in/on that collider; it must
not be mistaken for an unrelated barrier. This replaces a broad distance-to-hit
allowance that could accept a nearby wall.

The stricter test exposed the Chapter 3 report target inside the abandoned car's
contact envelope. The target is now at the accessible open side, and its test
approaches from that side rather than warping into the vehicle. The prologue pale
stone also verifies that a target's own contact surface remains usable.

## Validation

Runtime/Editor compilation passes. The final Editor camp, spine, prologue and
epilogue suites pass, including physical obstruction and existing interaction,
save and ending checks. Guidance tests verify front/back/left/right, turning to
face the same target, vertical targets, edge bounds, aspect mapping, Persian text
and selection of the current camp objective.

These tests establish logic and regression coverage. They are not complete visible
HUD QA across every display or an unassisted continuous navigation playtest.

The review is in `20261105-quality-review.md`. Overall delivery remains assessed
at 3/10, with explicit criteria for an eventual 8/10 claim. No new executable,
release ZIP or version increment was produced; the existing 0.5.1 release is unchanged.
