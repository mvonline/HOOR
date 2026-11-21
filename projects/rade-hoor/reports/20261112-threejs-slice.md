# Three.js connected mechanics slice — 12 November 2026

Implemented in `game/DesertSlice`, launched with `DesertSlice.cmd`. The server
is local-only at http://127.0.0.1:8777. Three.js 0.184.0 is installed and locked;
the game uses local GLB models, textures and existing user music.

## Delivered behavior

- First-person walking, sprint/stamina, crouching, jumping and solid-object
  collision; directional guidance explicitly handles targets behind the player.
- A continuous desert scene with original/credited camp models, eroded rock
  formations, textured sand, HDR sky, shadows and a stone archive station.
- Arcade vehicle driving with acceleration, reverse, braking and safe dismount;
  the top speed is approximately 79 km/h, not the old 20 km/h limit.
- Original Blender dromedary with saddle, panniers, articulated legs and a
  seated, anatomically modelled rider; walk/trot and dismount.
- Sidearm, aim, recoil, line-of-sight hit detection, finite ammunition, reload,
  crouch/cover, close defense, armed NPC damage/death and player death.
- The armed NPC has two finite twelve-round magazines, reload gaps, cover
  occlusion and an approach behavior when ammunition is exhausted.
- Eight connected objectives from case pickup through transport, recovery,
  armed encounter and delivery; separate local checkpoints and restart.
- Persian/English UI and objectives, music toggle, sensitivity, low/balanced
  graphics and mouse release/pause on focus loss. No recorded bilingual voices.

## Evidence

Four unit checks pass: ammunition conservation, wall resolution, left/right/rear
guidance and invalid-checkpoint rejection, including invalid mount state.

Sixteen connected checks passed in Chrome: walking; faster sprint; case pickup;
vehicle entry; complete drive through both markers; safe vehicle exit; camel
mount; complete valley ride; safe camel exit; pause freeze; combat activation;
actual raycast hits defeating the armed NPC; finite reload transfer; player
death; checkpoint recovery; final delivery. No runtime or asset-request errors
were recorded in the passing runs.

Route evidence: `builds/checks/three-route-check.json` and corresponding `.log`.
Cold-load evidence: `builds/checks/three-browser.log`. Screenshots include
`three-menu.png`, `three-camp.png`, `three-camel.png`, `three-driving.png`,
`three-archive-combat.png` and `three-complete.png` in `builds/checks/`.

The connected check accelerates the same simulation at 1/60 s fixed steps and
uses explicit test-only relocation for interactions and combat setup. Driving
and camel travel are traversed by steering inputs through the actual movement
code. These checks are not a continuous human playthrough. They do not establish
ten-minute pacing or final quality. The renderer runs in a separate headless
Chrome process; its frame counts, especially across accelerated test loops,
are not accepted as a player-device performance benchmark.

Visual inspection caught and corrected a clipped sky dome producing a black
centre, an incorrectly scaled scan, and a floating/incorrectly posed rider.
HDR sky, lower pixel ratio, bounded scan instances and instanced vegetation
reduce the rendering burden. The sky export is reduced to 1024 by 512.

## Acceptance still open

The ten-minute target is not met by an evidenced human playtest. The transport
simulation alone takes approximately 95 accelerated simulation seconds in the
automated route; interactions and most foot travel use test setup relocations.
This must not be presented as ten minutes of completed gameplay. The next
design iteration needs meaningful encounter/mission depth and observed pacing,
not a longer empty road or a mandatory wait.

Control feel, camel animation, enemy tactics, sustained laptop frame rate,
zero-ammunition completion, full-route navigation without assistance and the
quality of sound effects remain acceptance work. The original source/model
pipeline remains available for those revisions. The combined route is a
standalone proposed staging exercise, not a full implementation of canonical
screenplay 6.2 or a final performance of Kamran's duel.

Unity and its releases remain preserved. No new native Windows executable,
Suno generation or credit-spending action was performed.
