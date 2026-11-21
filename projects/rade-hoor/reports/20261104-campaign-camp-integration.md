# Connected camp campaign — 0.3.0-dev

The main game's Chapter 1 completion screen now continues into a separate camp
investigation state machine. Main-menu Continue loads the campaign checkpoint
when one exists. Starting from the beginning archives the old campaign checkpoint
as `.previous`. Campaign writes use a temporary file and atomic replacement with
a `.bak` copy.

## Implemented sequence

- Switch off the engine in the intact cabin. An adult staging model searches
  around the last engine position for 20 simulated seconds. The player can look
  normally; exiting is held until the introductory search finishes.
- Leave the cabin, approach the worktable and connect the spare battery to its
  lamp. Interaction requires proximity and looking toward the target.
- Read Sara's notebook route, retain the service sheet and access Tape 1's
  explicitly labelled English transcript through T. J opens collected evidence.
- Clean the abandoned vehicle's actual repair seam, compare it at the current
  vehicle, then collect the dashboard note. The dust cover disappears after
  inspection. The damaged vehicle is never offered as intact shelter.
- Enter a clearly labelled personal memory two years earlier: signal Rostam,
  hold E to lower a customer crate together, release to stop, then transition to
  the same-day garage repair ledger. Return to the same camp and check the battery.

The memory uses blockout architecture and actor staging, not final character art
or a surveyed reconstruction of the reference caravanserai. The cube/cylinder
figure and simple adult model are temporary. The courtyard has separate daylight
and hides the present-day canyon while active. The actor's hands follow the crate.

## Material limitations

This is a connected Chapter 2 prototype, not a finished full campaign. Chapters
3–10 and the prologue are not connected. Tape 1 playback, its safety encounter,
E01 voice and response, final dialogue performances, Persian shaping/localization,
full pacing and human navigation remain outstanding. These are tracked in
`projects/rade-hoor/planning/campaign-current.md`.

The introductory search currently protects the tutorial by holding the player
inside the cabin; a free-exit enemy/contact encounter is not implemented here.
Tape 1 is readable as a transcript and does not pretend to be audible playback.

## Verification

The final Windows build succeeded. All 40 native rule checks passed. The original
3,374 m Chapter 1 route regression passed, including audio, safe exits and camp
completion persistence. The new camp regression passed transition, 20-second
search timing, blocked remote interactions, lamp, evidence collection, separate
weld comparison, cargo hold/release, memory return, battery and full resume-entry
checks. It uses isolated `campaign-test-save.json`, not the player's campaign save.

Evidence: `builds/chapter-one-build.log`, `builds/checks/chapter-one/player.log`,
`builds/checks/campaign/player.log`. Reproduce with
`game/RadEHoor/Tools/Verify-ChapterOne.ps1 -Visible`.

Composited worktable, courtyard and ledger captures were visually inspected under
`builds/checks/campaign`. Inspection found and corrected the hidden notebook
target, clipped document heading, present-day scenery behind the memory and
disconnected actor staging. The actor remains visibly a blockout.

The automated camp test uses controlled player placement to check state/proximity
gates, rather than claiming a continuous human walk through the camp. Human
navigation, hardware performance, audio perception and complete campaign playtests
remain open. The final crate collision and hand-follow changes passed the repeated
regression; they have not received a human interaction playtest.
