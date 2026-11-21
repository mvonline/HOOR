# Quality review and recovery criteria / 2026-11-05

The user rates the current game 3/10 and requests an 8–9/10 result. My assessment
of my delivery on this project is also **3/10**. This is an editorial assessment
of the delivered experience, not a measured score of general development ability.
Code volume, ten chapter headings and passing simulations do not establish polish.
The changes below do not justify relabelling the game 8/10.

## Findings

| Area | Current assessment | Evidence and consequence |
| --- | --- | --- |
| Visuals and animation | 2/10 | `CampaignSpineWorld.cs` builds repeated flat floors, box targets and staging walls. Human/camel/Hoor assets remain bases. Source epilogue camera renders show sparse staging, not the approved concept quality. |
| Control and interaction | 4/10 | Working movement and driving, but the user found spread first-person arms and unreliable pickup. Those regressions required repair. Guidance previously disappeared behind the camera, and reach checks lacked obstruction checks. |
| Interface and navigation | 3/10 before this pass | Many instructions and exact points, little directional assistance. The previous marker logic only drew targets inside the camera view. Panels and Persian layout have not had comprehensive visible-window QA. |
| Sound and recorded dialogue | 3/10 | Supplied music is integrated; dialogue performances are absent. `LevelOneCampaign.cs` explicitly contains transcripts instead of Tape 1 playback. `LevelOneMusic.cs` has no chapter-specific scores beyond 1 and 2. Final audio mixing is unreviewed. |
| Play depth and pacing | 3/10 | Many tasks still reduce to approach/inspect/hold. Several meaningful branches are connected, but controlled warps and simulated clocks do not prove engaging navigation or five hours of content. |
| Reliability | 5/10, provisional | Saves and deterministic regressions cover useful cases. They did not catch the user's visual/control complaints. There is no complete human playtest or measured performance/memory budget. |

The principal development mistake was broadening chapter coverage before bringing
one complete playable section to the expected quality. The remedy is observable
quality gates, not more claims of completion or more frequent release ZIPs.

## Changes made in response

- One objective guidance system replaces the inconsistent camp/spine/aftermath
  markers. It shows turn-back/right/left/up/down, a screen-edge arrow and distance.
  It follows the current known task, not an enemy or an undiscovered secret.
- World-to-HUD mapping accounts for the UI's letterboxing on ultrawide and 4:3
  screens. Pause, documents, choices and completed sections suppress guidance.
- Interaction reach now checks physical layer-8 obstacles before accepting a
  target, while recognizing a target prop's own collider surface.
- Added directional, facing, edge-bound, aspect-ratio and Persian-label checks,
  plus an actual collider test for obstructed pickup. Existing real walking and
  compact-hand tests remain in the camp suite.

These changes are source improvements. They are not in the unchanged 0.5.1 ZIP.

## Criteria before an 8/10 claim

1. **Control:** a full continuous Chapter 1–2 playthrough without external
   instructions, accidental vehicle entry, blocked required interactions,
   obstructive arms or lost objective direction. Fix every reproduced blocker.
2. **Visuals:** a complete representative location matching the established art
   references, including intentional terrain, props, lighting, character poses,
   material response and transition continuity. Generic marker boxes cannot count
   as finished interactive objects.
3. **Interface:** inspect real English and Persian gameplay at 1280×720,
   1920×1080 and an ultrawide aspect. No clipped choices, detached markers or
   overlapping objective/action/subtitle panels. Confirm guidance visually.
4. **Audio:** actual bilingual dialogue assets where the scenario requires a
   voiced source, clear captions, positional foley, consistent music transitions
   and an audible mix review. A transcript or synthetic placeholder is not proof.
5. **Gameplay:** each chapter needs a distinct observed problem and useful
   feedback, not repeated E/G gates. Test successful and failed choices in motion,
   including companion navigation and visible world consequences.
6. **Stability and performance:** continuous play plus profiling on the target
   PC. Establish and measure a frame-time and memory budget; scene transitions
   must not accumulate generated materials, textures or meshes indefinitely.
7. **Duration:** record unassisted player time. Do not advertise five hours based
   on screenplay targets, mandatory waits or simulated-test time.

An 8–9/10 judgement ultimately needs the user's review of the actual game. Final
art, performed dialogue and continuous human playtesting remain open production
work. The current source work is progress toward those criteria, not completion.

Final verification for this pass: camp, spine, prologue and epilogue Editor suites pass after correcting the inaccessible Chapter 3 report target and the pale-stone own-surface check. See `20261105-direction-guidance.md`.
