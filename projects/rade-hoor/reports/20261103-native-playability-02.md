# Native playability iteration 02

Date: 2026-11-03
Scope: continue development of the existing Unity PC prototype after the first movement/audio/menu fixes.

## Delivered

- Replaced visible rectangular canyon boundaries with deterministic, faceted sediment meshes. Existing boundary colliders and core playable coordinates remain intact.
- Added a resource-backed dusk sky shader, rippled sand mesh, stone crossing surface, dry-wash details, and vehicle/camp dressing.
- Added distance-driven creature leg animation and segmented silhouettes without changing AI or hearing/contact rules.
- Replaced the crowded gameplay overlay and pause/results UI with objective, context, movement/surface and separate hearing/Bang panels.
- Added H help, L exploration-light toggle, mouse sensitivity, vertical inversion and local settings persistence. Arrow keys now move; Q/E turn.
- Removed the click-anywhere pause dismissal that interfered with settings controls.
- Replaced duplicate footsteps with one playback path driven by simulation events. Sand, stone, impacts and transmitter output have distinct synthesized clips.
- Added a visual distraction arc matching the existing 0.55-second simulation delay.
- Extracted story interactions into a shared production path and extended the native test to verify ordered clock/radio/vehicle interactions and actual CharacterController traversal to camp.
- Fixed the sky material reference after copying between source and isolated validation projects. Build preparation repairs an outdated reference and explicitly retains the shader in Resources.

## Verification

Reproduction: `game/RadEHoor/Tools/Verify-Iteration.ps1`.

The script copies Assets, Packages and ProjectSettings into `builds/validation-project`, uses the local Unity 6000.3.7f1 editor, runs the 40 core gameplay checks, builds `builds/windows/Rad-e-Hoor.exe`, then launches an automated native journey test.

Evidence:

- `builds/iteration-build.log`: Unity build and core rule results.
- `builds/checks/iteration-02/player.log`: movement, shelter, darkness/window rules, ordered story interaction, physical camp traversal, audio initialization, sky reset and menu reset.
- `builds/checks/iteration-02/canyon.png`: explicit camera render, visually inspected.

The first straight-line route test was obstructed near the vehicle. The test now follows a navigable sequence around the intact vehicle, across the existing crossing and into camp; it fails with position/waypoint diagnostics if any section is blocked.

Full-screen menu/HUD/pause capture requests return black images in the hidden Windows test process. Those files are not visual acceptance evidence. Manual visible-window UI/input review and headphone listening remain outstanding. Automated audio checks establish initialization, not perceived quality or device playback.

## Assumptions and limits

Procedural cliff scale, surface patterns, dry-wash placement, dusk timing (25 seconds), the navigation marker and the exploration light are prototype presentation choices. They do not establish real-world geography or add approved story devices. No story source was modified, no dialogue added and no hearing radii, Bang registration, shelter law or endings changed.

The existing camp approach and narrative opening remain short. Driving, companions, final character/environment assets, Persian shaping/localization, the full campaign, gamepad support and performance/player studies remain unfinished. English UI text is temporary.

Final result: Unity Windows build succeeded; 40 core checks passed; the expanded native journey test passed with no matched runtime exceptions or shader errors. The final camera render was inspected after the sky reference repair. Full-screen UI captures remain excluded as described above.
