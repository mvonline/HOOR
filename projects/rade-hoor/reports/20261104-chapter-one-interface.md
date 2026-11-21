# Chapter One interface — 0.2.3-dev

The driving interface replaces its full-width control strip with a compact speed
and gear panel, contextual action prompts and an H-toggle control guide. The guide
changes between driving and walking. Its open layout leaves room for the initial
clock/radio instruction and subtitles.

The main menu promotes Continue when a checkpoint exists, with a separate action
to start from the beginning. The reference canvas is centered vertically as well
as horizontally for taller windows.

Verification now captures the real composited player screen, including IMGUI,
at the initial cabin and completion screen. Existing camera-only captures remain
available for scenery inspection.

The Windows build succeeded. All 40 native rule checks passed, as did the full
3,374 m automated route, cabin interactions, safe exits, camp exploration and
completion save/load regressions. See `builds/chapter-one-build.log` and
`builds/checks/chapter-one/player.log`.

The first hidden-player screen captures were black. Running the verification
script with its new `-Visible` switch produced valid composited screenshots.
The cabin/help layout and completion screen were visually inspected:
`builds/checks/chapter-one/07-cabin-interface.png` and
`builds/checks/chapter-one/08-completion-interface.png`. The help panel, cabin
instruction and subtitle fit without overlapping at 1280 × 720.

Enter and keypad Enter now follow Continue when a checkpoint exists, matching
the primary menu action. Manual menu navigation, other display sizes, subjective
control feel and headphone balancing remain unverified. This pass retains the
prototype art and does not add voice recordings.
