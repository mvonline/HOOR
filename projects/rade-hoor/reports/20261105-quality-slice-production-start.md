# Ten-minute quality slice — production start

User accepted a ten-minute quality-first slice and confirmed no Marvelous/Substance access. Scope is now Day 1 camp delivery, 15:30, from screenplay 0.4–0.5, preserving Sara/Kian/Rostam/Bahram62 continuity. The former generic dusk Chapter 2 proposal would have invented their presence. Acceptance gates and explicit exclusions are in planning/quality-slice.md. The slice itself is NOT complete or verified as ten minutes.

## Actual work

Installed official portable Blender 4.5.15 LTS inside .tools, verified against the official SHA-256 manifest: 52dd02fd74877fa08e74b67d7854cf32468a232c02aaa19b6844c91285574f8d. No licences, subscriptions, Suno downloads or purchases were used. Existing player log identifies GeForce GTX 860M with 4064 MB VRAM; it is a preliminary performance baseline, not a measured new-slice result.

Authored a measured delivery case and R-17 prop in Blender, retaining .blend source, FBX game export, shared 2K packed UV atlas, base colour/AO/roughness/metallic bake outputs and independent body/lid/device pivots. Source has four packed images. This is first-asset art for review, not a finished hero-prop quality declaration. The case mesh currently has 8,116 body + 3,144 lid + 2,712 recorder triangles before Unity import splitting. Runtime prefab batches each part to one atlas material. Editor-only FBX and roughness/metallic inputs were moved out of Resources; runtime finish data is DXT5-compressed, and colour/AO use compressed import settings. No exact RAM or frame-time claim is made.

Implemented compound contacts, a 7.2 kg case body, 1.15 kg physical hinged lid and bounded ConfigurableJoint carrying. The saved prefab uses interpolation; the isolated manual-step probe disables render interpolation during measurement. Runtime tests now reject invalid poses, verify settling, actual relative opening angle and stops, closed-carry acquisition, gravity-loaded following, barrier contact and gravity release. HingeJoint.angle returned NaN in the local manual-step probe despite finite body/lid poses; closed-state logic now measures actual relative rigidbody rotation. This observation is not a general Unity bug diagnosis. A release test exposed deferred Destroy retaining hand forces during same-frame manual steps; forces now zero immediately on release, then the joint is destroyed. Final runtime physics check passed.

Created an offline Blender cloth-fit study using the already attributed CC0 body/garment sources at Sara's 1.71 m fit scale. The first study found 71 shirt vertices over 3 mm inside the body, maximum about 22.7 mm. Initial cloth contact and pinned cuffs were corrected before simulating 70 frames. The final sampled-vertex result found zero penetrations over 3 mm in shirt/trousers. Actual average displacement was about 8.50 mm / 7.87 mm, maxima 81.27 mm / 46.55 mm. This is ONE static fit study, not a newly drafted Marvelous costume, final likeness, triangle-intersection proof, runtime cloth system or multi-pose animation approval. Source and evaluated mesh are saved; rig transfer and visual review remain open.

## Verification and isolation

Current runtime/Editor scripts compile, and all five existing Editor suites passed after the isolated test hook and preference-save guard. The final compressed case import passed metric dimension/axis checks. Its final Unity Play Mode physics probe passed. Fresh open/closed Unity camera renders were inspected, and framing was corrected to include the whole asset. Test-only launch flag bypasses the campaign; Native preference writes are suppressed for that asset check. Existing executable and ZIP remain unchanged; no fresh standalone player checks are claimed.

Reproducible entry points: Tools/Author-SliceCase.py and Study-SliceCloth.py with the portable Blender; Tools/Check-QualitySlice.ps1 -Prepare with Unity. Earlier failed logs are superseded by the final pass, not counted as successful tests. No first-play duration has been measured.

## Remaining production

Hero character likeness/costume, authored animation/contact cleanup, continuous delivery scene/gameplay, performed English/Persian dialogue, sound/music mix, named target-hardware frame capture and three unfamiliar-player observations remain pending. Do not market an asset/physics bench or existing staging campaign as the accepted ten-minute experience. Status and actual renders are in artifacts/quality-slice/index.html and production-status.json.
