# Blender camp environment and conversation pass — 2026-11-06

Source changes after the packaged 0.7.1-preview. No additional executable or ZIP built.

## Blender deliverables

- Editable `projects/rade-hoor/artifacts/quality-slice/source/DeliveryCampLayout.blend`: tension-shaped work canopy, two field-shelter instances, staged sediment backdrop and named interaction/layout markers. Bench, pickup and departure markers are proposed staging values, not surveyed geography. This is a partial environment source, not a claim that every chapter or prop has been converted.
- `Tools/Author-DeliveryEnvironment.py` reproduces the geometry and exports DeliveryCanopy, DeliveryFieldTent and DeliveryRockBackdrop FBX assets.
- The canopy includes shaped fabric thickness, bindings, adjustable poles, guy lines and anchors (12,848 triangles). The field shelter includes fabric sides, folded front flaps, poles and anchor lines (7,636 triangles per instance). These are authored fabric rest shapes, not offline or runtime cloth simulation.
- The existing CC0 Poly Haven Rock Face 01 scan by Dario Barresi was staged and reduced in Blender. The five-piece backdrop has 45,385 triangles versus 100,870 for five original instances. This is geometry reduction evidence, not a frame-rate result.
- Initial OBJ round-tripping exposed wrong surface orientation. `DeliveryPropPreparation.ExportRockReference` exports the known-good Unity vertices/normals to `RockFace01-UnityReference.json`; Blender reconstructs winding against those normals before staging and exporting. The corrected actual Unity render was inspected.
- `Tools/Render-DeliveryLayout.py` renders an actual Blender overhead review at `previews/blender-camp-layout.png`. It is not a Unity gameplay screenshot. The layout only contains the staged environment geometry and interaction markers.

The delivery preview now substitutes these Blender assets for its earlier awning, tents and scan instances. Explicit canopy-pole and shelter-wall contacts preserve the pickup/bench route; the backdrop mesh retains readable collision data. Other campaign staging remains available.

## Conversation and work pose

Speaker labels and body text are separate. Previous-line review does not advance quest state. Escape pauses a conversation without skipping it; Escape closes notes/map without unintentionally pausing. The journal can display already-seen conversation lines, stored as neutral source keys so the selected text language remains changeable. Old version-1 checkpoints with no journal array are accepted.

Kian has a clipboard during the equipment-check phase. Opt-in two-arm IK, wrist direction and elbow pole controls support its contact points. The first actual render showed poor wrist/elbow alignment; those were corrected and the revised pose inspected. This is procedural contact posing, not authored acting or finger-grip animation. Restart clears the pose and prop visibility.

## Validation

Runtime and Editor C# compilation passed. Blender metric import and triangle-budget checks passed. Full delivery Play Mode passed with dialogue pause/rewind, transcript checkpoint persistence, measured hand-target distance under 4.5 cm, physical carry/place, map rejection and prior recovery checks. Log: `builds/checks/source-delivery-blender.log`. Actual Unity canopy/shelter/work-pose renders are under `builds/checks/source-delivery-blender/`.

Final character likeness, performed bilingual voice, authored acting/finger contacts, final materials, GUI visual acceptance, first-play duration and measured target-hardware frame timing remain open.

Additional regression: the existing camp campaign passed Editor Play Mode after the opt-in CharacterMotion hand-contact changes. Log: builds/checks/source-camp-contact-regression.log. No executable was built for this source pass.
