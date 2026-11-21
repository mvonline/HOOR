# Chapter transition cursor fix — 0.4.1-dev

The completion screen could regain mouse capture through the ordinary Escape
pause toggle. Loading a completed checkpoint also ended with an unconditional
request to capture the mouse. Either path left the completion buttons visible
while the pointer was locked and hidden.

Cursor capture now checks whether a pointer-driven overlay is open. Completion,
pause, documents, choices, section-completion and failure screens keep the
pointer released. LateUpdate synchronizes that policy with application focus.
Movement and vehicle input also stop behind those overlays.

Chapter 1 completion handles Enter and keypad Enter as a direct continuation to
Chapter 2. Escape cannot re-lock the completion screen. Starting Chapter 2 resets
its pause state and restores the gameplay capture policy.

Regression checks cover a capture request while completed, Escape at completion,
completed-save reload, and Enter invoking the real Chapter 2 transition. Tests
assert the actual released cursor state at completion and the gameplay policy
after transition; they do not claim a manual desktop mouse-click playtest.

The Windows build succeeded. All 40 existing native checks and the full Level 1
route passed, including the added cursor and transition assertions. Camp,
Chapter 3-10 state progression, dawn outcomes and intro decode/end/skip tests
also passed. Evidence remains in `builds/chapter-one-build.log` and player logs
under `builds/checks`. The updated portable ZIP is
`builds/releases/Rad-e-Hoor-0.4.1-dev-Windows.zip`.
