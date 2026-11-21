# Chapter One audio feedback — 0.2.5-dev

Each moving-sand surface now has a local, filtered gravel-foley source. It follows
the animated ridge's position, fades as the movement stops at the sunlit boundary,
and follows the effects volume setting. A separate low-frequency wheel cue rises
when the vehicle is close to the gully in the shaded lane. Completed camp
exploration silences both hazard layers.

The layers reuse the existing CC0 RoadGravel asset; they are designed foley, not
recordings of a creature. No new dialogue or voice asset is introduced.

Engine load now responds to throttle demand, with a smooth release during braking
or coasting. Cabin engine layers use lower low-pass cutoffs. Wind and rolling
levels interpolate when entering/exiting, and rolling gravel uses a positional
source outside the vehicle.

The completion transition now explicitly silences engine, rolling, radio and
hazard layers and cancels a pending bend reflection. Loading a completed save
applies the same silence. Previously, the completion screen stopped the update
loop before it could reduce source volumes.

The Windows build passed all 40 native rule checks and the full 3,374 m route
regression. Added checks passed for an active local sand source and exposed-wheel
cue, their fade after movement stops at sunlight, and immediate vehicle-layer
silence on completion. Source and volume checks do not establish perceived sound
quality, spatial clarity or headphone balance; those still need human review.

Evidence: `builds/chapter-one-build.log`, `builds/checks/chapter-one/player.log`.
Reproduce with `game/RadEHoor/Tools/Verify-ChapterOne.ps1 -Visible`.
