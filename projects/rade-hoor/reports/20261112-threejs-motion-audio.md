# Motion and audio fixes — 12 November 2026

User-reported issues: crude camel, floating corpse/aiming arms, missing cover
animation, missing movement/mount sounds and poor synthesized gunfire.

## Changes

- Refined the original Blender camel: leaner body, tapered hump, curved neck,
  narrower muzzle, shorter ears, textured short coat, split padded toes, reins,
  girth, stirrups and saddle. Reworked distance-based ipsilateral gait, knees,
  head/tail motion and rider height. Moved the transfer point into the valley
  and backdrop scans away from the riding space after visual inspection.
- Stopped all aiming actions on death, relaxed the skeleton, ran a one-shot
  authored fall and aligned the rendered body with the ground. The sidearm
  follows the hand alive, then falls separately and settles. This is not a
  full physical ragdoll. The full body cannot remain in a looping aim/death pose.
- Added Q cover entry/exit, blended crouched-body pose, shoulder camera,
  movement along cover and right-mouse peek. Firing from cover requires peeking.
  Actual world geometry still decides bullet occlusion; cover adds no invisible
  invulnerability. Corrected bind transforms and ignored unused mesh vertices
  when finding ground contact. Cover geometry bounds now match visible stones.
- Replaced nearly inaudible synthesized steps with eight recorded gravel
  variants and separate run cadence/gain. Added padded camel tread/rustle and
  three-layer vehicle idle/load/rolling audio. Added separate effects volume.
- Replaced the synthesized gun burst with a CC0 Colt pistol recording, stereo
  enemy direction, restrained echo and recorded reload foley. Music ducks
  briefly under shots. Effects resume/suspend with the game, independently of
  the music checkbox. Existing user music remains unchanged.

## Verification

`builds/checks/three-audio-check.json`: eight passing real-time browser signal
checks for walking, running, driving, camel tread, gunfire, reload and pause /
resume. Samples were decoded and nonzero effects signals measured downstream
of the limiter. Test browser output was muted; this is not a listening review.

`builds/checks/three-motion-check.json` and screenshots in `builds/checks/` record
cover entry/ground contact/peek, settled death and grounded dropped sidearm.
Unit tests cover root-transform consistency, ignoring unused mesh vertices,
ammunition, collision, directional hints and invalid checkpoints.

Audio source pages, author/license details and hashes are retained under
`game/DesertSlice/public/credits/audio-sources.json`. No paid download, Suno
generation, music replacement or new numbered game release was made.

These fixes do not certify final animation quality, sustained laptop performance
or completion of the ten-minute pacing target. Subjective sound/control review
and the remaining mission-depth work are separate acceptance tasks.
