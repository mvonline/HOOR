# Playable aftermath / source development / 2026-11-05

Replaced the successful dawn ending's three text-only pages with a connected,
walkable aftermath. No new player executable, release archive or version increment
was made during this pass. The existing 0.5.1 release remains unchanged.

## Connected content

`Campaign/Epilogue.json`, authored by `Tools/Author-Epilogue.py`, contains three
locations and ten English/Persian tasks adapted from screenplay H07 and 10.6:

1. Outside the boundary: first aid, proposed receipt, evidence decision and exit.
2. Independent aid: four water containers, original report/cultivation notebook,
   the omitted loss of consciousness, signed statement and departure.
3. Shahdad garage: repaired fitting, conversation and wrench returned to the bench.

The three valid receipt choices affect the world and next target: cleared passage
with complete receipt, marked independent watercourse, or independent support
arriving after an explicit story-time cut. Evidence is not confiscated. First aid
does not accept a receipt. The rescue result is not turned into a morality score.

Yunus appears only if his rescue and store exit were recorded, with his right hand
still protected and bandaged. Otherwise the evidence record marks rescue as
unconfirmed and retains the location for aid; it invents neither a death nor exit.
Sharing the covered map with Sara is a separate optional interaction. Only then
is her question to a present Yunus shown. No reply is invented for an absent actor.
Unimplemented pulley-block ownership is not fabricated by this sequence.

The outside scenes contain no Hoor enemies or dawn countdown. Explicit scene
transitions, physical actors, reachable work targets, hold/release interactions,
choice panels, evidence archive and an end screen are connected. Completed and
in-progress aftermath states resume through the existing version-2 save format;
older saves default to the pre-aftermath dawn screen. The prior dawn failure
branches remain separate and cannot enter the survivor sequence.

Human idle arms now use joint targets down beside the body instead of inheriting
the base mesh's spread-arm pose. Seated/riding hands have resting targets, the
injured right arm stays protected, and existing crate contact/first-person tests
continue to pass. Character likeness, skin weighting and animation remain bases.

## Validation

- Runtime and Editor C# compilation pass.
- Unity Editor camp, Chapter 3–10 spine, prologue and new epilogue suites pass.
- The epilogue suite checks all bilingual task/record/choice mappings, three scene
  checkpoints, held/released work, rejection of omitted evidence, optional map
  sharing, conditional Yunus injury, distinct exit choices, physical walking on
  the independent route, relaxed idle arms and completed-record input/resume.
- Actual camera renders of the three locations were inspected. Props remain
  staging assets; this is not final environment art or cinematic performance.

Logs and captures: `builds/checks/source-{camp,spine,prologue,epilogue}`.
`Tools/Check-Editor.ps1` runs those checks without building a player.
The player-check script also recognizes `--epilogue-test` for the next authorized
player build. No claim is made that the distributed 0.5.1 includes this source work.

## Remaining production work

Recorded performances in both languages, final locations/characters, additional
optional missions and witnesses, full impact/locator timeline, companion navigation,
continuous human playtesting, performance work and measured campaign duration are
still unfinished. This pass does not establish a finished five-hour game.
