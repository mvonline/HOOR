# C0 test 3 — hand-in-darkness interaction prototype

Date: 2026-10-21

## Delivered

`game/demo/reach.html` adds a short standalone playable attempt linked from the
echo corridor. It reuses the user-accepted broadband/HRTF sound approach and
Q/E/C virtual listening-angle controls, retains four directions, and adds
keyboard/pointer hold-to-reach with contact feedback, pause, retries and CSV.

Rules trace to `gameStory/Rad-e-Hoor_Proposal_v5.0.md` sections 2.2 and 6.2:
0.5-second cold warning, 1.5-second echo-triggered response, `[T,E)` registration,
irreversible Bang latch, result only at E, safe real contact and silent waiting.
No microphone is requested. Pausing stops simulation and releases contact.

## Verification

Pure-rule checks pass for all thresholds, exact T/E inclusion/exclusion,
pre-window response, release safety, real contact, quiet waiting, changing aim,
large frame steps and chronological events. Headless DOM/audio lifecycle checks
pass for start, clock, cold feedback, release, pause/resume, registered response,
deferred outcome, hidden/revealed cause, retry and the silent path.

These are simulations, not browser rendering or perceptual listening checks.
No player-study success or Go/No-Go decision is claimed. The earlier player
feedback accepted the audio approach; it did not validate this new interaction.

## Limits

Each attempt lasts 15 active seconds, from five seconds before T until E; this
is a practice segment rather than the roadmap's full five-minute test session.
Target layout is an explicit prototype assumption. Spoken response is logged
and represented with synthetic audio, not newly invented campaign dialogue.
The campaign and its endings are not implemented by this standalone exercise.
Night stealth test 2 and real player studies remain outstanding.
