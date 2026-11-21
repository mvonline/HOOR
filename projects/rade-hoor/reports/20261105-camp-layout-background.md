# Camp layout and background pass / source work / 2026-11-05

The user identified the layout/background quality as too low. The current camp
was reviewed against `gameStory/images/env-c02-expedition-camp-v1.png`. This pass
rebuilds the spatial composition; it does not claim parity with that concept.

## Visible changes

- Work alcove: scanned sediment faces, high rock shelf, low stone boundary,
  ground cloth, folding seat, stored water, connected leads and visible papers.
- Yard: separated parked vehicles, maintained walk/drive clearances, soft paired
  tire impressions and restrained edge rubble rather than an entirely bare floor.
- Background: a physically accessible stone shelter with an entrance practical,
  layered distant valley relief and a scenic continuation of the valley floor.
- Corrected tent triangle winding and added a closed rear, ridge and guy lines;
  the old inverted faces appeared as disconnected dark wedges.
- Rock material now uses world-space triplanar albedo/normal/AO sampling rather
  than stretched wall UVs. Distant relief uses simpler atmospheric materials to
  avoid visible texture repetition.
- Twilight fill makes the rock forms readable while keeping warm practical light
  localized. Camp-only fill is disabled away from the camp and in other scenes.
- Upgraded the existing Poly Haven sky source from 1K to checksum-verified 4K.

Five camp rock placements use Dario Barresi's CC0
[Rock Face 01](https://polyhaven.com/a/rock_face_01) geometry, 20,174 triangles per
source mesh. The original lichen-bearing appearance is not used: the existing
project rock material is applied. This is not a scan of a Lut location. Reproducible
download/conversion is in `Tools/Import-CampRock.py`; source hashes and URLs are in
`Resources/WorldKit/Scans/RockFace01-source.json`. See the asset credits.

## Verification and limits

Actual Unity camera renders were inspected repeatedly during this pass. Camp
checks cover the five scan instances, 4K sky, open doorway/solid side wall, real
walking approach and all required interaction/evidence steps. Full route and
campaign regression coverage is run by `Tools/Check-Editor.ps1` without a player
build. The first-chapter suite now uses the existing Editor-safe frame helper.

Camera previews are under `projects/rade-hoor/artifacts/environment`. They are
actual scene renders without the gameplay HUD, not AI concept images or proof
of complete UI QA. Final vehicle/prop art, richer terrain dressing, character
performances and target-PC rendering/memory profiling remain open. Other chapters
have not all received this environment pass. Overall quality is not rated 8/10.

No new executable, ZIP or version increment was produced; distributed 0.5.1 is
unchanged and does not contain this source work.

Final check result: Chapter 1 full-route, camp, spine, prologue and epilogue Editor suites all pass on the final source. Stable previews: `../artifacts/environment/camp-layout-20261105.png` and `../artifacts/environment/camp-approach-20261105.png`.
