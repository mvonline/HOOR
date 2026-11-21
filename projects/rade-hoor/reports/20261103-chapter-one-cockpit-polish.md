# Chapter 1 cockpit and cue polish — 0.2.0-dev

Date: 2026-11-03
Scope: continue the playable Level 1 build, focusing on first-person presentation, warning animation, sound cues and persistence.

## Delivered behavior

- The driving camera now sits farther back in the cabin. The steering wheel, instruments and dashboard remain visible in the normal driving view.
- The cockpit reference informed the new speedometer/RPM needles, instrument bezels, dashboard clock, air vents, radio controls, glove box, switches, red cutoff-cap prop, transmission levers, visors and wipers. The floor, bulkhead, pedals, passenger seat and visible bonnet close the gaps seen in camera renders. These are still project-authored, simplified models rather than final asset fidelity.
- The speedometer follows actual vehicle speed and the RPM needle follows the engine-speed proxy. The clock starts at 17:40, advances with active play time and matches the clock comparison text.
- Static added cockpit fittings are combined by material. Needles, steering wheel and clock digits remain independently updateable.
- Sand warnings use a deforming surface with normals and tangents, sampled against the local canyon ground. The movement approaches and pauses at the sunlit boundary instead of moving disconnected spheres at a fixed height.
- Engine reflections require an approaching bend. They originate from the opposite wall, with delay derived from the reflection path distance. The rolling-gravel layer has a low-pass filter to soften distinct footfall transients in the source recording.
- Checkpoints now retain elapsed play time, preserving the dashboard clock on load. Normal application quit saves settings and the safe checkpoint. Automated test runs skip the application-quit player-preference write.
- The main menu identifies the build as 0.2.0-dev.

The red cutoff cap and transmission levers are visual fittings; this pass does not claim additional interactive vehicle systems or a physical engine/RPM simulation. No story source, voice line, ending or sound-law change was introduced.

## Source references

- gameStory/images/pirmard-7-cockpit-v1.png
- gameStory/images/daniyal-v1.png (identity/reference check; no new character model added)
- Existing chapter 1 screenplay and ENV-C01/ENV-C02 layout references.

Original concepts were not modified. Existing project material/texture assets were reused; no new external media or image generation was needed in this pass.

## Verification

Command: `game/RadEHoor/Tools/Verify-ChapterOne.ps1`.

The final Windows build succeeded. All 40 existing core checks passed. The chapter test drove the entire 3,374 m route, including cabin checks, acceleration, brake/reverse, pedestrian exit/return, re-entry, the safe first-hazard stop, both gullies, dusk, camp completion and checkpoint reload. It additionally checked live speedometer movement, preserved clock time and multiple bend-reflection triggers. Scripted elapsed play was 609.4 seconds; this is not a human pacing measurement.

Evidence:

- builds/chapter-one-build.log
- builds/checks/chapter-one/player.log
- builds/checks/chapter-one/01-cockpit.png
- builds/checks/chapter-one/02-shadow-warning.png
- builds/checks/chapter-one/03-canyon-drive.png
- builds/checks/chapter-one/04-camp-arrival.png
- builds/checks/chapter-one/05-dashboard-detail.png
- builds/windows/Rad-e-Hoor.exe

The cockpit and warning camera renders were inspected. The footwell/bulkhead seam seen during review was closed before the final verification run.

## Live UI review limitation

A fresh live review was attempted using the computer-use skill and its supported sky API. The game was launched and uniquely selected from returned window objects. Capture failed with “FrameArrived timed out: timed out waiting on channel”, then “window capture timed out: timed out waiting on channel” after refreshed selection and one retry. No blind coordinate input was used. The test instance was closed afterward; no passed live UI or manual keyboard/mouse review is claimed.

The skill's guidance requires refreshing window selection and retrying once after capture failure, then reporting the exact error if recovery fails. Skill: C:/Users/raziy/.codex/plugins/cache/openai-bundled/computer-use/26.1016.51333/skills/computer-use/SKILL.md; referenced guidance: ../../docs/guidance.md.

## Still open

Final environment/character asset fidelity, Persian voice recording, Persian typography/localization, gamepad support, perceptual headphone mix review, live UI/input review and hardware performance validation remain outstanding. The existing playable chapter and this polish pass must not be represented as final-quality completion of those items.
