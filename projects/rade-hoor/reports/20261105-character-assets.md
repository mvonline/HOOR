# Character asset work / 2026-11-05

## Delivered scope

Sixteen editable character prefabs: Daniyal, Sara, Bahram62, Bahram (encounter
age), Kian, Rostam, Farhad, Qasem, Roya, Yunus, supported-seated Nader, Dara,
HoorYoung, HoorAdult, HoorGiant and DaniyalHands. Skinned meshes, named joint
hierarchies, materials, saved prefabs and a CharacterGallery scene are provided.
Actual rendered previews and mesh counts are in
`../artifacts/characters/previews/index.html` and `validation.md`.

Human anatomy derives from the MakeHuman hm08 CC0 base mesh. Project-authored
code applies proportions, simple clothing/material regions, attached equipment,
hair and basic joint weights. These are base production assets, not approved
final likenesses or reference-matched character sculpts. Sara's hair remains
uncovered. Nader's supported work seat does not establish a diagnosis or select
a permanent mobility aid. Bahram's two states share one topology and face
architecture; detailed age sculpting is still required.

Surface refinement adds four official CC0 skin atlases, three fitted hair meshes
and their opacity/strand textures. Sara uses bob hair, Roya tied hair, and the
male states short hair. Hair is fitted from the original .mhclo barycentric
references rather than placed from an unrelated head. A two-sided cutout shader
allows profile tint (including gray/white hair) with strand detail. Clothing is
still a simple project-authored base; the downloaded clothing meshes are not
silently substituted for the reference outfits.

Earlier primitive human generation was inspected and rejected as insufficient.
The continuous human topology replaces it as the active generation path.
During iteration, stale native Mesh skinning buffers caused corrupt saved
previews. Explicit vertex, weight, bind-pose and triangle copying fixes this;
the baker checks baked-vertex parity before and after saving.

The hair surface's initial compiler error was corrected before delivery. Asset
validation now explicitly checks shader compiler errors, and the preparation
script rejects logs containing Shader error. Texture/tint assignment is applied
after the material's shader is selected.

## Connections

- Chapter 2: Rostam replaces the box figure. Two-bone arm aiming follows the
  crate grip points; a crouch accompanies lowering. The existing signal/hold/
  release, ledger and checkpoint sequence remains authoritative.
- Existing later chapters: Sara and Bahram use the new character prefabs.
  Bahram uses a seated pose in the cabin and on Dara without shrinking his body.
- Dara now has one-hump camel anatomy and secured panniers. Rider and board
  attachments use the new saddle height. These are visual attachment choices,
  not a load-safety certification.
- Camp and later hearing-source adults use HoorAdult. Hearing/search/contact
  rules and collision thresholds are unchanged. Young/giant prefabs are available
  in the gallery; no new encounters are invented to display them.
- First-person Daniyal arms derive from the same topology and clothing. They
  display on foot and hide in menus/cabin. Dedicated steering/tool animation,
  complete finger skinning and hand-contact polish remain unfinished.
- Other named characters are gallery assets for their existing planned scenes.
  Their unfinished narrative scenes are not falsely marked implemented.

## Validation contract

CharacterAssetBaker validates finite vertices, normalized weights, valid joint
indices, materials, skinned baking and a basic articulated pose. It renders all
15 full-body states and saves native Mesh/material/texture assets plus prefabs.
CharacterPlayChecks runs the existing camp and campaign-spine regressions in
Editor Play Mode, without BuildPipeline.BuildPlayer. The camp regression adds
rig/hand presence and upper/lowered crate-grip checks.

Batch Editor does not dispatch WaitForEndOfFrame; Editor regression frame waits
therefore yield to the next frame instead. Player screenshot waits are unchanged.
An unrelated UnityEditor.Search.SearchDatabase startup exception is retained in
the log and excluded from game failure classification. Other errors/exceptions
still fail the check. Editor batch captures do not constitute a human UI review.

Final result: asset generation and before/after-save skinning parity passed.
Both camp and spine Editor Play Mode checks passed, including both crate grip
positions. Logs: `builds/character-assets.log`,
`builds/checks/character-camp/editor.log`, and
`builds/checks/character-spine/editor.log`. Prefabs, geometry/material assets,
gallery scene and generated metadata were copied back to the source project.

## Remaining quality work

Exact reference likenesses, stronger silhouette differentiation, realistic hair,
properly tailored clothing and accessories, authored skin/normal/roughness maps,
facial expressions and lip sync, production locomotion/IK, seated/riding/contact
polish, LODs, performance budgets and continuous human playtesting remain open.
The procedural camel and Hoor meshes also need an anatomy/animation art pass.
This work does not complete the full game's art or its five-hour content target.

No executable, release ZIP, version increment or player build is authorized or
performed for this work. Existing 0.4.3 downloads remain unchanged.
