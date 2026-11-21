# Rad-e Hoor 0.7.1-preview — delivery completion and prop pass

The user requested continued autonomous work and another executable without waiting for review. This release includes the source changes made after 0.7.0-preview. Previous releases and campaign saves remain available.

## Playable delivery

The complete Day 1 camp delivery remains independently launchable from PLAY CAMP DELIVERY. It includes ignition shutdown and pedestrian exit; Sara's delivery exchange; real rigidbody carry and bench placement; Rostam's key exchange; physical lid opening; R-17 limited-output check; route marking with rejected incorrect choices; report and pottery exchanges; physical observation; southeast departure survey; and signing. Text is English/Persian and its checkpoint files are separate from campaign progress.

Checkpoint restoration reconstructs the indicator and equipment state, rejects invalid stages and safely returns interrupted carries to ground pickup. Restart resets cast placement and routes. Placement is checked against the bench footprint, accepts safe off-centre landings and recovers from a miss without trapping the player. Automatic carry releases restore player/case collision.

The route sheet now contains a numbered, clickable schematic and matching legend. Existing hold-to-work interactions have a progress strip; no added waiting time is used to manufacture duration. Pause includes look sensitivity, FOV, invert look, music/master/ambience/effects and independent language preferences. Pause freezes the case bodies and cast motion, then restores physical velocities on resume. Speakers turn toward a nearby player during their dialogue; this is procedural staging, not authored performance animation. Walking speed is reduced in this delivery area; Shift remains available without a carried case.

## Original props

Editable Blender source: projects/rade-hoor/artifacts/quality-slice/source/DeliveryFieldProps.blend.
Reproducible authoring: game/RadEHoor/Tools/Author-DeliveryProps.py.

The metric workbench has individual chamfered boards, recessed fixing heads, trestle pivots, braces and rubber feet (1,768 triangles). The pottery fragment has inner/outer curvature, fracture edges and archival support (432 triangles). The observation stone replaces the cube with an irregular 1,280-triangle surface. A first close-up review caught excessive faceting; smooth normals and increased density were applied before final packaging. Materials reuse existing permitted project surfaces; no Marvelous/Substance output or purchased assets are claimed.

## Evidence and limits

Source Play Mode completed the delivery and new pause/recovery checks. The final Windows player's regression logs are in builds/checks/release-071-*/player.log. Actual Unity camera captures provide the workbench/pottery/stone close-up review. Native window capture timed out again; hidden-window GUI screenshot files are black and do not establish visual acceptance of the new map or settings.

This is a playable preview, not a final professional-quality sign-off. Final likenesses, authored acting/contact cleanup, recorded bilingual dialogue, final audio/art mix, measured target-hardware frame timing and observed first-play duration remain open. Existing approved music is retained; no Suno download credits or purchases were used.

Final validation: all eight final executable modes passed after the prop-normal correction (prologue, chapter-one, campaign, spine, epilogue, intro, delivery-slice, quality-case). Successful build receipt SHA-256 checks passed. ZIP CRC and required-file checks passed. The packaged credits file is ASSET-CREDITS.md. Runtime and Editor source compilation passed. An asset-only incremental build exposed the old DLL-timestamp guard's false rejection; the build script now validates a fresh successful-build receipt and content hashes, including correct UTC handling by PowerShell.
