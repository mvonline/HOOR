# Chapter 1 environment and warning pass — 0.2.1-dev

Date: 2026-11-03
Scope: continue Level 1 presentation and resolve a visible gully-shadow defect while preserving the complete drive.

## Implemented

- Added 32 broad, eroded sandstone shoulder formations with varied heights and proportions. They have actual collision and sit outside the vehicle lane. Dimensions remain proposed production choices, not geological survey claims.
- Added a sediment shader using the existing PBR rock albedo/normal/AO assets, broad vertex tints and subtle height-based strata. Terrain, rubble and generated formations supply finite vertex colours.
- Added soft, low-opacity disturbed-sand dust along the existing warning surface. It follows the same approach toward the sunlit boundary and fades with emergence/daylight. No new threat or story rule was introduced.
- Fixed the black strip at the gully shadow edge. The old fractional power of a tiny negative sine value at a mesh boundary produced NaN vertex colours. Clamping the input removes the invalid value. Verification now checks the actual shadow mesh colours for invalid or out-of-range values.
- Added a ready-to-use voice playback hook for the existing Persian line, with an optional voice-level setting and engine ducking. The voice control is shown only if a clip is actually present. No clip has been generated or bundled.
- Prepared the exact-text voice brief at projects/rade-hoor/artifacts/audio/chapter-one/DaniyalMorning.voice.md.

## Verification

Reproduction: game/RadEHoor/Tools/Verify-ChapterOne.ps1.

Final result: Windows build succeeded; all 40 core checks passed. The full chapter test passed including the 3,374 m drive, pedestrian passage, both gullies, completion, checkpoint/clock reload, live instruments, bend-reflection cues, sediment scenery and finite shadow colours. Scripted play was 608.1 seconds; this remains a scripted duration rather than a human pacing measurement.

Evidence:

- builds/chapter-one-build.log
- builds/checks/chapter-one/player.log
- builds/checks/chapter-one/03-canyon-drive.png
- builds/checks/chapter-one/06-sand-warning-detail.png
- builds/checks/chapter-one/04-camp-arrival.png
- builds/windows/Rad-e-Hoor.exe

The camera renders were inspected. The black strip visible in the first review is absent from the final gully render. The driving path remains clear after widening the shoulder formations.

## Voice provider status

The plugin-management skill was used to search for a voice-generation capability. HeyGen is available, but the confirmed search state was not added/linked; no HeyGen tools were available afterward. The user was offered the option to add it and link an account. No generation request or purchase was made, and no Persian voice availability is claimed.

The exact skill read was C:/Users/raziy/.codex/plugins/cache/openai-curated-remote/plugin-management/0.1.0/skills/plugin-management/SKILL.md. Its rule is: “Use its tools only after its individual connection is confirmed.” The skill also states that suggestions do not block independent work. The game build and verification were therefore completed while voice production remains pending the connection and voice-catalogue check.

## Still outstanding

Final art fidelity, Persian voice generation/recording, Persian text shaping/localization, gamepad support, headphone mix review and direct UI/input review remain open. Previous live window capture failed; no new successful live UI review is claimed in this pass. Camera renders and automated driving are the validation actually performed.
