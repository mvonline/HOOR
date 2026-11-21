# Connected campaign spine and media — 0.4.0-dev

This build connects the camp prototype to Chapter 3 through Chapter 10. It is a
playable campaign blockout, not a finished high-fidelity game. It preserves the
existing Chapter 1 route and camp sequence. Scene transitions load proposed
chapter layouts; they are not a measured continuous reconstruction of the Lut.

## Playable coverage

| Chapter | Implemented actions |
| --- | --- |
| 3 | Drive to tunnel parking; geophone, strap, boards/winch choice, recovery hold/release, cargo straps, report uncertainty and return |
| 4 | Anchor inspection, frame extraction, Bahram state, hooked notebook, marked-water bowl calibration across two cycles, mandatory dawn rule record and rear-seat handoff |
| 5 | Engine-off search, plate practice/carry restriction, transmitter on/off choice, recording-case pickup, contact barrier and Kian record |
| 6 | Slow approach to Dara, water and felt, leading, walk/ski choice, board-location choice, service-road recovery and rejoin |
| 7 | Ordinary key and battery, corresponding report-line selection, physical locator test, two cloth markers and exit lock |
| 8 | Normal-time perimeter, five release controls, retention of the service supports, stress-timed work, retreat check, Sara state and shared support action |
| 9 | Vehicle approach, separate companion route, rope aim, interrupted first pull, second base, recovery, cover/decoy choice, cut/bandage record and stable gate |
| 10 | Three preparations, explicit readiness, live 4:45 countdown plus ten-second window, engine/unit controls, cold-reach release, circle/cabin/crevice outcomes, failure records and English aftermath panels |

Sounds have an actual source position and radius; contact protection is checked
separately. Search state retains its last source. Carrier and mechanical audio
reuse the credited assets. The original and second record copy, companion flags,
report comparison, board location and live dawn-clock state are checkpointed.
Checkpoint return does not rewind an active dawn countdown.

The chapter clock now uses visible narrative anchors and elapsed section time.
Chapter 4's surface exit advances to 22:30 and Sara's release to 04:00. Final
preparation remains labelled story time; only explicit readiness starts 05:00:15.

## Requested speed and sound changes

The earlier 5.6 m/s cap (about 20 km/h) was an early handling choice. The new cap
is 80 km/h. Acceleration, braking, speed-dependent steering, engine RPM mapping
and the 100 km/h instrument range have been updated. The verification driver now
slows for route curvature and actual stopping distance. Faster driving shortens
Chapter 1; its older ten-minute automated-drive measurements are historical.

The continuous wind layer is muted in the menu and main game. The original
103.33-second score uses synthetic plucked strings, a two-drone role, bowed/bass
textures, membrane percussion and stereo reflections. A one-bar overlap smooths
the loop. Source: `game/RadEHoor/Tools/Compose-DesertScore.py`; master:
`builds/audio/OriginalDesertScore.wav`; runtime: `OriginalDesertScore.ogg`.

The regional reference is documented dotar practice, including the relationship
between drone and melody, described by [UNESCO's Bakhshi entry](https://ich.unesco.org/en/RL/music-of-the-bakhshis-of-khorasan-00381)
and [UNESCO's instrument entry](https://ich.unesco.org/en/RL/traditional-skills-of-crafting-and-playing-dotar-01492).
Those traditions are associated with documented dotar regions, not evidence of
one universal ancient Lut soundtrack. This score is an original synthetic
composition with a spacious cinematic-desert brief, not an archival performance
or a quotation of a Dune score. No film music or external performance is sampled.

Music has its own saved slider, fades below danger/voice cues, and becomes silent
during the live dawn test. It is nondiegetic and emits no hearing/Bang event.
Perceived musical quality and headphone balance still require human review.

## Existing video intro

The project's existing `Rad-e-Hoor-story-animation-60s.mp4` is copied unchanged to
StreamingAssets as `StoryIntro.mp4`. A new game plays it before gameplay. Continue
loads the save directly. Watch Story Intro replays it from the menu. Enter, Space,
Esc or the button skips it. A prepare timeout/error falls back to the menu/game.

The video uses Unity's built-in video module, a render texture and an audio
source. An automated test checks decoded frames, screenshot output and the skip
continuation. The initial test's accidental recursive coroutine registration
was corrected; the original video did not need transcoding.

## Outstanding production work

Actors and many tools/locations are staging models. Many actions have placeholder
prop geometry rather than final animation, and companion locomotion is simplified.
English record/aftermath panels stand in for full performed scenes. The full
Chapter 10 vehicle-impact timeline, optional branches H05/H06/H07, prologue,
recorded E01–E07/dialogue/tape encounters, Persian shaping/localization and final
ending cinematics are not complete. The camp tape remains a labelled transcript.

The rescue ledge now has an actual floor opening, but the new chapter layouts
need continuous human navigation and collision review. Contact AI has local
movement/obstruction checks, not production pathfinding. Hardware performance,
difficulty, pacing and accessibility have not received a full campaign playtest.
Automated controlled placements do not establish that review.

## Final verification

The final combined Windows build passed all 40 existing native rule checks,
the full Chapter 1 route, camp progression, the new Chapter 3-10 controlled
progression sequence, and video decode/seek-to-end/skip. The route test recorded
80.0 km/h peak speed over 3,374 m in 159.1 simulated seconds.

Selected alternative tests cover the 30 m winch source and release, ski-board
transfer, leaving the board at the slope, and resumed inventory state. Ending
tests cover half-open T/E registration, quiet circle, quiet cabin, released unit
and crevice, active engine, continued anchor output, cold-reach release and
live-clock save/resume. A finite-radius test checks that an in-range adult hears
the ledge source, an out-of-range one does not, and emitting does not teleport it.

Logs: `builds/chapter-one-build.log` and the player logs under
`builds/checks/chapter-one`, `campaign`, `spine`, and `intro`. The main-menu,
intro-playback and fast-driving composited captures were visually inspected.
The fast-driving capture shows 74 km/h; the continuous test log records the
80.0 km/h peak. This does not establish human handling quality or frame pacing.

Player instructions are bundled as `builds/windows/READ-ME.txt`. The portable
development ZIP is `builds/releases/Rad-e-Hoor-0.4.0-dev-Windows.zip`.
The 135,087,238-byte ZIP passed its required-entry check (235 entries), including
the executable, Unity runtime, game assembly, intro and player instructions.
A SHA-256 sidecar is included in `builds/releases`.
