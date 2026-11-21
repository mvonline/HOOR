# Source development progress / 2026-11-05

No player build, executable, release archive or version increment was made.
The distributed 0.4.3 build does not include this work.

## Implemented in source

- Character wardrobe now uses fitted CC0 MakeHuman work clothes, practical shoes,
  skin atlases and cutout hair. Removed active floating collar/pocket/shoe boxes.
  Fixed native mesh buffer updates, first-person hand extraction, seated neutral
  hips, riding pose and Yunus's protected right arm. These remain base assets,
  with unfinished likenesses, tailoring, accessories and animation.
- Expanded Persian campaign text, translated dynamic labels, correct text wrapping
  widths and translated document height. Text and voice language selections are
  independent. Voice recordings remain absent; subtitles are not dubbed dialogue.
- User-supplied Escape013 now crossfades into two explicit escape beats. Chapter
  tracks select correctly, and the final live dawn countdown forces silence.
  Removed the rejected synthetic score as a later-chapter fallback.
- H05 has a real sliding gate, held puller, Yunus's own crossing, negotiation,
  three-catch jack trial, withdrawal and visible exit. His injury remains.
  H06 peels the map layer and records its evidence; it cannot open a gate without
  the H05 passage outcome. Both branches save without advancing the main task.
- Opening journey: 15 locations / 51 bilingual tasks, preparation cast, evidence
  uncertainty choices, water clock, vehicle recovery practice, check-ins, dune
  ski/rest branch, night return and explicit canyon crossing. New stories include
  the existing video intro and then this opening. Target duration is unmeasured.
- Simplified menu with a separate settings panel. Mouse settings now carry into
  the campaign. Debug experiments are limited to development builds.

## Verification evidence

Before the new prologue/menu wave, Unity Editor camp and Chapters 3–10 regressions
passed, including H05/H06 persistence, localization/music policies and character
assets. The optional-map test found and corrected its floating target height.
Character preview PNGs are actual rendered base meshes, not final character art.

Current runtime and Editor scripts compile with Unity's bundled Roslyn compiler.
`Tools/Check-Source.py` records this under `builds/checks/source-compile/`.
`Tools/Check-Prologue.py` passes bilingual records/options, cast asset references,
task bounds, scene ordering and ski/rest branch data checks.

**The latest prologue and menu changes have not passed Play Mode or visual QA.**
The latest Editor attempt reports: `No valid Unity Editor license found. Please
activate your license.` It exits with code 198 before compiling/importing gameplay.
This is logged in `builds/checks/character-camp/editor.log`. Local package-manager
IPC was also blocked under the sandbox; the permitted retry reached licensing.
No license bypass or account change was attempted.

`Tools/Prepare-Characters.ps1 -SkipBake -PlayChecks` now includes the new prologue
regression after camp and spine. It performs Editor checks only, never BuildPlayer.
Its prologue suite is authored but pending execution. Static C# compilation cannot
prove collisions, navigation, UI fit, sound mix or human control quality.

## Still unfinished

Final environment art, distinct finished character likenesses, recorded dialogue
in both languages, performed cinematics/endings, remaining optional missions,
continuous navigation/control/audio playtesting, performance tuning and a measured
long-form campaign are unfinished. This work does not establish a five-hour game
or a finished production release. Wind-erased tracking remains a deferred idea.
