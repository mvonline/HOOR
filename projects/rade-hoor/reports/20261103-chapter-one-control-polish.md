# Chapter One control polish — 0.2.2-dev

The vehicle now has a separate rendered rig. Its exterior, cockpit, camera and
headlight interpolate between fixed physics poses; collision and route progression
continue to use the authoritative chassis. Checkpoint restores snap both poses
and clear throttle, steering, braking and foot movement.

Exiting checks four candidate positions for walkable ground and capsule clearance.
If the driver side is obstructed, another clear position is used. If all positions
are blocked, the player stays in the vehicle with an explanatory prompt. The camp's
parked vehicles now have collision boxes.

Completed-camp exploration retains a separate completion flag. Re-entering the
vehicle no longer triggers the completion overlay again. Saving during exploration
retains chapter completion; loading returns to the completion screen. Existing
version 2 completion saves remain supported.

## Verification

The Windows build succeeded using `game/RadEHoor/Tools/Verify-ChapterOne.ps1`.
All 40 native rule checks passed. The automated player drove the complete 3,374 m
route in 608.1 simulated seconds, passed both gullies and completed at camp.
New regression coverage passed for an obstructed driver-side exit, checkpoint
visual snap, camp exploration, vehicle re-entry after completion and saving/reloading
that completed exploration. The player log contained no exception or shader-error
matches checked by the verification script.

Evidence: `builds/chapter-one-build.log`, `builds/checks/chapter-one/player.log`.
Fresh cockpit and camp camera renders were visually inspected at
`builds/checks/chapter-one/01-cockpit.png` and `04-camp-arrival.png`.
These captures do not establish interactive control feel or frame pacing.

The interpolation change still needs a human input and frame-pacing review.
This pass does not add a Persian voice recording or replace the prototype models.
