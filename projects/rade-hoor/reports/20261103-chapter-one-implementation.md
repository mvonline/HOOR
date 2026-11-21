# Chapter 1 implementation and acceptance record

Date: 2026-11-03
Request: implement the entire first level as a playable experience, fixing controls, sound, graphics and gameplay.

## Owning source

- `gameStory/Rad-e-Hoor_Full_Screenplay_FA.md`, chapter 1, sections 1.1 and 1.2.
- `gameStory/Rad-e-Hoor_Layout_Background_Bible_EN.md`, ENV-C01 and the camp approach of ENV-C02.
- Existing original concept art, especially canyon-day-v1.png, env-c02-expedition-camp-v1.png and Pirmard-7 references.

The new primary entry is a separate ChapterOne.LevelOneDirector, not the legacy walking sandbox. Chapter 1 ends at camp arrival; chapter 2's worktable/evidence scene is not represented as part of its completion.

## Functional sequence

1. First-person cabin control at the canyon entry, round 7. Compare the wristwatch and dashboard: both show 17:40. This corrects the old demo's incorrect disagreement between the clocks.
2. Daniyal's “It was morning” is currently subtitled. E switches off a soft audible radio carrier; no invented voice or echo is played.
3. Drive Pirmard-7 through a continuous winding canyon using W/S throttle, brake/reverse and A/D steering. Space is the handbrake. Mouse looks independently in the cabin; Q re-centers the view. F exits only when stopped, E enters a nearby vehicle.
4. The original collapse blocks the vehicle while leaving a narrow pedestrian passage. Ground extends behind the opening; the mission's refusal-to-leave boundary is explained before and during exploration rather than implemented as a hidden death.
5. Team tire tracks lead inward. Sand movement is visible in the first shaded gully and stops at the sunlit edge. The first mistake stops the vehicle before a protective stone; the player can reverse and steer into the clear lane without dying.
6. The cue repeats at a second gully. A narrow visible sunlit route remains drivable.
7. As the final approach progresses, light falls, natural bird activity recedes and a sensory leg rises from the sand. Recorded engine reflections are played from the opposite wall at bends. No duplicate “I arrived” voice is introduced.
8. Slow down and park at the lit expedition camp. Completion records the chapter; the player may explore the camp on foot or save and return to the menu.

## Controls and persistence

The driving model is a kinematic bicycle model with acceleration, smooth steering, braking, reverse, off-road resistance and contact casts. It is not a WheelCollider suspension simulation. On-foot motion uses a CharacterController with acceleration and continuous mouse look. There is no forced head bob or camera shake.

Safe bends and both teaching sections have checkpoints. Checkpoints persist locally in chapter-one-save.json; the main menu provides Continue Chapter 1. Automated tests use a separate chapter-one-test-save.json and do not overwrite player progress. Settings expose look sensitivity, inversion, field of view, master/engine/ambience/effects levels.

The measured route is about 3,374 m. The scripted driver needs about 609 seconds without human inspection stops. The screenplay's 15-minute duration is a human pacing target, not a measured playtest result. No arbitrary timed waits were added to force fifteen minutes.

## Graphics and audio changes

- The canyon is a continuous collidable mesh following an authored route, with foot slopes, sedimentary ledges, shoulders, rubble chunks, dry vegetation and a complete camp clearing. It is no longer the small rectangular arena.
- Cliff and dry ground materials use diffuse, normal and AO maps. A real HDR sky, linear color rendering, dusk lighting, practical camp lamps and tone mapping replace the old flat ambient presentation.
- Rubble is grouped in spatial chunks so distant stones can be culled; small vehicle parts use the existing material-combined prefabs.
- The primary chapter uses recorded engine, desert wind, birds and footsteps. The earlier broadband test burst and synthetic footstep tones are not used in this chapter. Radio-off, loop transitions and engine reflections have controlled volume/fades. Independent volume controls are available.
- Asset sources, derivatives and license records are in `game/RadEHoor/THIRD_PARTY_ASSETS.md`.

## Verification

Reproduction: `game/RadEHoor/Tools/Verify-ChapterOne.ps1`.

Build: Unity 6000.3.7f1, Windows x64, local `.tools/UnityEditor/Editor/Unity.exe`, isolated validation project.

- `builds/chapter-one-build.log`: core rule checks and Windows build.
- `builds/checks/chapter-one/player.log`: chapter test result.
- `builds/checks/chapter-one/01-cockpit.png`: explicit first-person camera render.
- `builds/checks/chapter-one/02-shadow-warning.png`: first gully.
- `builds/checks/chapter-one/03-canyon-drive.png`: midpoint.
- `builds/checks/chapter-one/04-camp-arrival.png`: completed camp clearing at dusk.

The automated test uses the production driving code to traverse the whole route. It also checks initial movement lock, clock/radio progression, acceleration, braking/reverse, leaving/entering, the pedestrian passage, first-mistake safe stop, both gully passes, dusk/camp completion, recorded audio presence and save/reload. It is not a substitute for a human controller/keyboard playtest or headphone review.

A direct UI review was attempted using the computer-use skill and its supported sky API. Window capture failed with “FrameArrived timed out: timed out waiting on channel”, then “window capture timed out: timed out waiting on channel” after refreshed window selection. The documented retry was exhausted; no stale-coordinate input was used and no UI-quality pass is claimed from it. Skill: C:/Users/raziy/.codex/plugins/cache/openai-bundled/computer-use/26.1016.51333/skills/computer-use/SKILL.md; guidance: ../../docs/guidance.md, “If state capture or window activation fails ... refresh the app/window selection and retry once; report the exact error if recovery fails.”

## Remaining limitations — not to be represented as finished details

The complete gameplay route and required teaching sequence are implemented, but final-art fidelity has not reached the concept renders. The cockpit, creatures and geology still need professional asset/detail polish. Daniyal's Persian voice line is not recorded; the current UI/subtitle adaptation is English, and Persian text shaping/localization and gamepad support remain unfinished. The fifteen-minute pacing target, perceptual sound mix, input feel, accessibility and hardware performance need human playtesting. These limits prevent calling this a final-quality, fully detailed release of Level 1.

Final verification result: Unity Windows build succeeded; all 40 existing core checks passed; the final chapter test passed including pedestrian exit/return and the entire 3,374 m drive. Scripted elapsed play was 609.3 seconds. All four camera renders were regenerated; final inspection included the terrain-normal-map tangent fix and the grounded camp clearing. This verifies functional traversal and source-beat progression, not final art quality, a fifteen-minute human playtest, recorded Persian voice, or a passed visible-window UI review.
