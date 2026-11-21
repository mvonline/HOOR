# Reference-based game production pass 01

Date: 2026-11-03
User correction: the goal is the designed native 3D game, not a collection of small gameplay exercises.

## Source assets and actual gaps

The image library documents 56 planned 2D concept assets. No FBX, GLB, OBJ or Blender model files were found under gameStory, game or projects. These references are visual targets, not automatically usable 3D models. The previous playable build did not consume them.

This pass connects these actual source images:

| Source | Use in project |
| --- | --- |
| gameStory/images/env-c02-expedition-camp-v1.png | Main-menu artwork; authored camp composition reference; reference archive |
| gameStory/images/canyon-day-v1.png | Canyon material/scale reference; archive; source guide for derived sediment texture |
| gameStory/images/pirmard-7-intact-v1.png | Pirmard-7 model reference; archive |
| gameStory/images/demo/tange-rotail-expedition-camp-night-v1.png | Lighting/reference archive |

Source images remain unchanged. Consumed copies live under `game/RadEHoor/Assets/Resources/ConceptArt`.

## Implemented

- The main menu uses the actual expedition-camp artwork and makes the story the primary entry. The two earlier gameplay exercises are secondary tests.
- Four original reference images are inspectable in the art archive, explicitly labeled as concepts rather than completed-level screenshots.
- `Resources/Layouts/ExpeditionCamp.json` now owns explicit prop positions. Dimensions and coordinates remain proposed Unity placements, not authoritative geography.
- Pirmard-7 and a distinct damaged earlier vehicle are modeled in 3D with body, windows, grille, round lamps, bumpers, spare wheel, roof rack, tied cargo, treaded tires and shared individual repair seam. The damaged vehicle has an open door and missing rear glass. It is not a new shelter.
- Workstation and awning are saved as reusable Unity prefabs alongside the vehicle models in `Resources/WorldKit/V02`. Geometry is combined by material to avoid a draw call per small tread/bolt/rail. V01 is retained as a previous generated version.
- Camp dressing includes the canvas shade, worktable, notebook, radio, lamp, cases, rug, folding chair, tents, tripodal light, water cans and an entrance-frame study.
- Story scenery uses continuous sedimentary walls and a distant floor instead of the repeated blockout columns. The gameplay tests retain their original rules/layout.
- A new sediment texture was generated with the built-in image tool using the canyon image as a material guide. Its full prompt is in `20261103-sediment-texture-prompt.txt`. Final project asset: `game/RadEHoor/Assets/Resources/ArtTextures/Sediment-v1.png`.
- The camp is no longer an immediate end screen: the player connects the low-power worktable lamp, inspects the earlier vehicle repair seam and reads its dashboard note. Source: screenplay section 2.3 and layout bible ENV-C02. The note has a temporary English adaptation; Persian text shaping/localization remains unfinished. These actions do not implement every intervening chapter beat.

## Verification

Reproduce: `game/RadEHoor/Tools/Verify-Iteration.ps1`.

Evidence paths:

- `builds/iteration-build.log`: rule checks, prefab bake and Windows build.
- `builds/checks/iteration-02/player.log`: movement, shelter, darkness rules, ordered cabin interactions, physical camp route, lamp/weld/note sequence, required reference assets, sky/mode reset.
- `builds/checks/iteration-02/reference-camp.png`: explicit camera render of the actual 3D scene.
- `builds/windows/Rad-e-Hoor.exe`: playable Windows output.

During visual iteration, black tent shading was corrected by removing opposite winding on shared vertices, repeated cliff columns were replaced for the story view, and a missing distant-floor region was filled. The hidden-window full-screen UI capture limitation still applies; those black images are not visual acceptance evidence. Headphone mix, visible-window UI and controller/input usability still need human review.

## Full-game production remaining

This pass is an editable reference-based reconstruction, not final-art quality or a completed campaign. The screenshot must not be represented as matching the concept render's fidelity.

1. Complete the ENV-C01/ENV-C02 art quality target: sculpted silhouettes, terrain transitions, detailed materials/normal maps, vehicle interior and coherent physical collision. Review game capture beside source art.
2. Build a complete chapter slice with the authored scene order, companions, evidence interactions, animation, sound design, persistence and driving; validate route and shelter behavior in the actual environment.
3. Produce remaining character, creature, vehicle-state and environment assets from their owning references; keep shared kits and distinct story boundaries.
4. Connect the campaign's authored chapters and time/ending rules, implement proper saves, input/gamepad settings, Persian typography/localization and accessibility.
5. Run performance, headphone, navigation and player studies before treating the game as production-complete.

No original story source was edited. No new ending, sound radius, Bang/time-window law or narrative character was invented. The parked support and damaged vehicles are environment reconstruction props; companion AI, driving and the full evidence system are not claimed complete.

Final verification: the Windows build succeeded, all 40 core checks passed, and the expanded native test passed including the lamp/weld/note sequence and required reference assets. The final reference-camp camera render was inspected after the distant-floor repair. It remains visibly below the source concept's fidelity; full-game completion is not claimed.
