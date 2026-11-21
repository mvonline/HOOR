# Character, NPC and chapter scenery improvements

Source changes on 2026-11-05; no new executable or version increment. Windows 0.6.1-dev remains unchanged.

## Models and surfaces

Removed overlapping body-derived clothing beneath the fitted outfit, retaining exposed anatomical neck/head and distal hands. Corrected torso skin weights: the nearest-bone method had assigned chest fabric to upper arms, pulling the shirt when arms lowered. Added fitted vest panels instead of jagged face-by-face material patches. Those panels use their own fabric detail rather than the outfit texture atlas, which produced unrelated dark shapes on custom UVs. Added fitted pockets, fasteners and clipped radios; moved equipment clear of the clothing. Backpack straps follow the shoulder and chest instead of intersecting the shirt. Female work hairstyles now expose the face. Clothing shader adds restrained hem dust and variable roughness while keeping crease occlusion from turning fully black.

Generated cast prefabs and editable mesh assets refreshed; first-person hands were rebaked through the existing crop and validation pipeline. Previews now show a posed idle stance rather than the relaxed bind pose. These remain project-adapted character bases, not final likeness-matched sculpts or production motion capture.

## NPC motion

Walking phase follows actual displacement; stopped actors stop marching. Added foot roll and per-character breathing phase. Nearby human actors smoothly turn neck/head toward the player within limited angles and distance, with wall occlusion checks at a bounded cadence. Actors behind them do not trigger backward staring. Quest-controlled root movement, companion routing, interactions and protected right-hand poses remain separate from attention. Attention is assigned across opening actors, campaign companions, memory Rostam, optional Yunus and aftermath actors, including support Farhad.

## Scenery

Chapters 3-10 stone uses the textured canyon sediment shader. Natural tunnel boxes have rounded eroded visual shells over their existing conservative contact envelopes. Added visible lamp stands, diffusers and hoods, plus peripheral talus away from authored lanes. This improves surface response and scale cues; the later chapters still require authored terrain, final architecture, props and lighting polish.

## Evidence

All five Editor suites passed after the functional/model changes: Chapter 1, camp, spine, prologue and epilogue. The new NPC regression verifies bounded attention, rear-target rejection, physical wall occlusion, stopped locomotion and protected right hand. Existing interaction, first-person hands, companion routes, saves and dawn rules passed. Final cast bake validated skin geometry and saved-mesh deformation after the last fabric-only cleanup; no shader or compiler errors reported in that bake. Fresh renders of Sara, Rostam and Chapter 4 were visually inspected. Controlled checks and preview cameras do not replace continuous human playtesting or target-PC profiling.

Stable preview copies: ../artifacts/characters/20261105-polish/index.html. These are actual Unity mesh/scene renders, without gameplay HUD; not concept art. Music was not changed and no Suno credits used.
