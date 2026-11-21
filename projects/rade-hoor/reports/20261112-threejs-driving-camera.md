# Continuous locomotion, driving collision and camera selection

User requests: less artificial movement, vehicles must not pass through cliffs
and rocks, selectable vehicle/camel cameras. Changes apply to the existing
Three.js slice; no new numbered release was made.

## Implemented

- Analytically integrated foot acceleration/deceleration, normalized diagonal
  input, collision-aware footstep speed, continuous distance-based head motion
  and a sprint-recovery latch. Mouse input remains direct.
- Blended mount/dismount and camera changes, progressively applied steering,
  smoothly settling camel gait and gradual enemy facing changes.
- Cannon 0.20.0, locked locally: 1,350 kg rigid chassis, gravity, four suspension
  ray wheels, brake/reverse/coasting forces, solid cliff/rock/building proxies
  and collision damage. Static scenery is no longer render-only. R recovers
  a vehicle on the dirt route. Proxies approximate rock silhouettes; they are
  not per-triangle scanned collision meshes. Camel/foot controllers remain
  kinematic, with obstacle collision.
- Chase / hood / cockpit vehicle cameras and chase / rider / side camel
  cameras. V cycles and 1–3 select directly. Pause-menu selectors persist the
  preference. Cockpit windows are transparent and the driver's head is hidden
  in cockpit view. Rider geometry is hidden in rider view.
- Batched static model siblings while preserving camel joint groups. Distant
  props are culled, shadow maps are cached between updates, and the lighter
  profile retains lower-resolution grounding shadows.
- A dedicated Chrome game window with a workspace-local profile and
  `--force_high_performance_gpu`. No Windows GPU preference or existing Chrome
  account/profile setting is changed. The separate play profile has its own
  local browser checkpoints; the previous browser's saves are preserved there.

## Evidence and limits

13 unit checks pass, including velocity integration at 30/60/144 Hz, suspension
settling, driving into a solid cliff, and wheel contact at z = -1200. A full
route check exposed lost wheel contacts with a rectangular heightfield; it was
replaced with the square terrain grid expected by wheel ray queries.

`builds/checks/three-camera-check.json`: all nine checks pass: six camera views,
V cycling, direct-key selection, and a driven collision with an actual cliff
from the generated world. Four collisions were recorded; chassis clearance
from the cliff face remained approximately 1.94 m. No runtime/request errors.
Screenshots: `three-car-view-0.png` through `-2.png` and corresponding camel
views under `builds/checks/`.

The same short, stationary mounted-camel render sample selected Intel HD 4600
without the GPU option, around 10–14 fps; with the option it selected GTX 860M
and recorded approximately 60 fps at 1280 by 720. This is a five-second
headless sample, not sustained full-level performance acceptance. The dedicated
launcher uses the tested option; the embedded chat browser is a different host.

Final connected-route, cover/death and audio signal evidence remains in
`three-route-check.json`, `three-motion-check.json` and `three-audio-check.json`.
These are controlled checks, not a human judgement that the game now feels good
or meets the complete ten-minute quality target.

References: [Cannon RaycastVehicle](https://github.com/pmndrs/cannon-es/blob/master/src/objects/RaycastVehicle.ts),
[Chromium high-performance GPU test configuration](https://chromium.googlesource.com/chromium/src/+/67ae0c4285011bd0a8fc69e979f5c0084b45d405/infra/config/targets/basic_suites.star).
