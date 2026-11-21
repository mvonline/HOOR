# Current native campaign delivery register

Updated: 2026-11-05. The user authorized continued full-game development and
routine decisions without repeated approval. This register supplements the
historical 2026-10-21 studio plan; it does not mark its unperformed gates complete.

The screenplay and layout bible in `gameStory/` remain the narrative inputs.
English UI/transcript adaptations are implementation assets, not replacements
for the Persian originals. Unknown physical dimensions remain proposed layouts.

| Section | Native implementation | Required next work |
| --- | --- | --- |
| Prologue / outside journey | Connected 15 locations / 51 bilingual tasks; Editor and 0.5.0/0.5.1 player checks pass | Final scene art, remaining optional branches, recorded dialogue and human navigation playtest |
| Chapter 1 / unexpected dusk | Complete route can be driven; automated progression passes | Human control/audio review, final art, Persian dialogue and typography |
| Chapter 2 / camp | Connected camp investigation, held physical work with saved progress, visible pickups, evidence save and cargo memory | Tape 1 voice and sound-radius safety encounter, E01 sourced voice/empty-case response, final actors/locations, full pacing/navigation playtest |
| Chapter 3 / erosion-tunnel approach | Connected 0.4.0 blockout; controlled progression test passes | Recorded sources/tapes, vehicle-recovery animation and continuous navigation review |
| Chapter 4 / Bahram | Connected 0.4.0 blockout; controlled progression test passes | Final natural-tunnel/facility art, Bahram rig/locomotion, water/tool animation and source dialogue |
| Chapter 5 / caravanserai | Connected 0.4.0 blockout; controlled progression test passes | H05 rescue/negotiation/jack branches now pass controlled Editor checks; final recordings and contact/pathfinding review remain |
| Chapter 6 / companionship | Connected 0.4.0 blockout; controlled progression test passes | Final Dara rig/behaviour, descent route art, board transfer animation and human handling test |
| Chapter 7 / R-17 | Connected 0.4.0 blockout; controlled progression test passes | Full field archive presentation, source dialogue and locator/marker navigation review |
| Chapter 8 / heart perimeter | Connected 0.4.0 blockout; controlled progression test passes | Final structural geometry, Sara performance, support-load validation and full scene playtest |
| Chapter 9 / parallel rescue | Connected 0.4.0 blockout; controlled progression test passes | Final rescue animation/geometry, companion pathfinding, falling-rock sequence and full playtest |
| Chapter 10 / boundary | Connected 0.4.0 blockout; controlled progression test passes | H07/aid/garage now connected and Editor-verified; impact/locator timeline, voice/cinematics and final continuity polish remain |
| Optional missions / ending archive | H05/H06 plus H07 aftermath connected; controlled persistence checks pass | Remaining H01/H02/H04 and optional scenes; performed endings; no mandatory optional quest |

Do not describe the campaign as complete until all connected sections, persistent
world choices, endings, audio, localization, performance and human playtests have
evidence. A transcript does not count as implemented dialogue playback; a test
warp does not count as a human navigation playtest.

Next production order: finish recorded source encounters and continuous human
navigation across the connected blockout, replace staging models/locations, then
complete optional branches and performed endings. The current Chapter 3-10
coverage and exceptions are recorded in `../reports/20261104-campaign-spine-and-media.md`. Keep the
working Chapter 1 route regression and campaign save checks passing at each step.

Deferred user-approved concepts are tracked in [Development ideas](development-ideas.md).
This includes wind-erased footprints and skilled tracking, reserved for future
scenario and gameplay development; it is not part of the current build.

2026-11-05 character update (source project only): 16 editable base assets now
exist, including human states, Dara, Hoor sizes and first-person hands. Existing
camp/later actor roles use them; camp and spine Editor checks pass. Locations
remain blockouts and character likenesses/materials/animations remain unfinished.
See `../reports/20261105-character-assets.md`. No new player release was made.

See `../reports/20261105-overnight-source-progress.md` for clothing, localization, music, prologue and menu changes, validation limits and the Unity license block. Five hours of player gameplay remains unmeasured.

The subsequent user-authorized 0.5.0-dev Windows build succeeded. The license
block cleared, and the opening plus all existing player suites passed after
fixing the night detour. See `../reports/20261105-windows-050.md`. The source-only
and unverified-prologue notes above describe the earlier checkpoint; final art,
remaining content and continuous human playtesting are still outstanding.

Source aftermath update: three walkable locations and ten bilingual tasks now replace the successful ending pages. Exit choices, signed evidence, optional map sharing and rescued Yunus continuity pass Editor checks. See `../reports/20261105-playable-aftermath.md`. No release was produced for this pass.

Navigation/quality update: common bilingual objective direction arrows and physical obstruction checks are implemented in source; all four Editor suites pass. The current delivery remains rated 3/10, with the quality gates in `../reports/20261105-quality-review.md`. Source-only pass; no new release.

Camp feedback source update: held battery/cleaning actions, interrupted-work persistence, physical paper removal, exposed matching welds and close inspection lighting are Editor-verified. See `../reports/20261105-camp-work-feedback.md`. No new release.

2026-11-05 environment and companion source pass: camp spatial zones, scanned rock faces, triplanar materials, 4K sky, corrected tents and a stone shelter are rendered and Editor-verified. Companion detours, saved positions and continued post-release final exit are connected. Final five Editor suites pass. See `../reports/20261105-camp-layout-background.md` and `../reports/20261105-companion-routes.md`. No new release; all final-art/performance gates remain open.

2026-11-05 release update: the accumulated environment, guidance, work feedback, companion routes and aftermath changes are now included in user-authorized Windows 0.6.0-dev. All five Editor and six fresh Windows player suites passed. Twenty new Suno alternatives were generated; the user chose to preserve download credits, so they remain unimported. Existing approved music is retained. See ../reports/20261105-windows-060.md. Final production quality and human playtesting gates remain open.

0.6.1-dev correction: imported camp rock runtime collider cooking now retains readable mesh data; fresh player collision probes and all six suites pass with stricter log scanning. The 0.6.0 PASS scan had missed CollisionMeshData errors. See ../reports/20261105-windows-061-collision-fix.md.

Character/NPC graphics source pass: fitted outfit overlap and torso weights corrected; separate vest panels, field equipment, visible faces and fabric weathering added. Motion follows displacement and humans attend to nearby visible players within angle limits. Later chapter sediment surfaces, tunnel shells and practical fixtures improved. All five Editor suites passed and final character bake validated; actual renders reviewed. No new executable. See ../reports/20261105-models-npc-graphics.md and ../artifacts/characters/20261105-polish/index.html. Final likenesses, environments, animation and human playtesting remain unfinished.

User-selected vehicle/object quality pass: Pirmard side skins now have real wheel clearance, curved arches, shaped bonnet, glass-backed cabin, detailed wheels, hardware and rounded cargo. Damaged vehicle has a framed open door, dent and windscreen fractures. Cases/workstation detailed; vertical UV collapse fixed; paint finish added. All five Editor suites passed; affected camp/spine suites passed after door changes, and final rim optimisation passed asset review. Source only; 0.6.1 executable unchanged. See ../reports/20261105-vehicle-object-models.md and ../artifacts/vehicles/20261105-model-pass/index.html. Models remain in progress; final textures, detailed damage and target-PC performance/LOD work remain open.

Vehicle surface/optics continuation: persistent normal and finish maps, tangent-safe baking, smoother paint, hex fasteners and shaped/fluted headlamp glass are implemented and asset-verified. Five Editor suites passed after materials; driving/camp passed after optics, with final camp check after surface tuning. No new executable. Current vehicle geometry is 49,860 / 50,188 triangles. See ../reports/20261105-vehicle-surface-optics.md and ../artifacts/vehicles/20261105-model-pass/details.html. Final artist textures, human visual playtesting and target-PC profiling remain open.

Production direction changed by user approval: freeze chapter expansion and build one quality-first ten-minute slice. The scene is canon-aligned Day 1 camp delivery at 15:30, not Chapter 2 with invented companions. Free toolchain only. Verified Blender toolchain, first DCC case/atlas and physical-carry/lid tests now exist; Sara cloth fitting is an offline study, not final costume. Five existing Editor suites and the new asset physics check passed. The actual ten-minute scene, final characters/animation/audio and human duration/performance tests remain pending. No new release. See quality-slice.md, ../reports/20261105-quality-slice-production-start.md and ../artifacts/quality-slice/production-status.json.

2026-11-05 / 0.7.0-preview: separate Day 1 camp-delivery flow integrated and Windows executable built at the user's request. Eight final executable regressions passed. The existing campaign remains available. Quality acceptance, measured duration, final acting/art and performed dialogue remain open. See reports/20261105-delivery-preview-070.md.

2026-11-05 / source after 0.7.0-preview: delivery checkpoint reconstruction, cast restart and physical placement recovery corrected; bilingual interactive route sketch and hold progress added. Runtime/Editor compilation and full delivery/recovery Play Mode checks passed. No new release built. See reports/20261105-delivery-recovery-and-route-sheet.md; route-sheet visual review remains pending.

2026-11-05 / 0.7.1-preview released at user's explicit request: full Day 1 delivery with checkpoint/placement recovery, pause/settings, interactive bilingual route sketch and three original Blender field props. All eight final Windows player modes passed; build content hashes and portable ZIP CRC verified. Old releases retained. Final character/animation/voice art, map/settings visual acceptance, observed duration and measured performance remain open. See reports/20261105-delivery-preview-071.md.

2026-11-06 / source after 0.7.1: at the user's explicit request, Blender now supplies the delivery canopy, field shelters and staged/reduced existing CC0 rock backdrop. Editable DeliveryCampLayout.blend and overhead Blender review saved. Dialogue speaker/rewind/history and Kian contact pose integrated. Runtime/Editor compile, Blender imports, full delivery and existing camp Play Mode regressions passed. No new executable produced. See reports/20261106-blender-camp-and-conversations.md.

7 November. Equipment layout now includes actual case, bench, worktable, sample, observation stone and two intact vehicle meshes. Blender bench dimensions verified and a framed material-colour viewport saved. The overhead roof-cutaway review shows the same waypoints traversed by the CharacterController collision check. An intermittent inverted landing found during verification was corrected with bounded world-space grip torque and supported low-speed set-down. Full delivery and walking-corridor checks passed twice after the correction. Independent upright carry, wall contact and release checks passed. Logs are source-delivery-walk-layout.log, source-delivery-walk-repeat.log and quality-slice-case-physics.log. Changes are retained in source after release 0.7.1-preview.
