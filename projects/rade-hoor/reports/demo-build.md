# C0 echo corridor demo — implementation report

Date: 2026-10-21

## Usability correction

Front/back follow-up: pitch codes did not solve player confusion. All four
directions are retained. Broad-spectrum noise bursts replace the narrow pitched
source, and Q/E/C virtual listening-angle controls replay the unchanged sources
from another angle. A left turn shifts front sources toward the right ear and
rear sources toward the left; answers retain the original corridor reference.
Yaw and turn events are logged. Visual cues remain optional. This is keyboard
controlled, not physical head tracking. No perceptual success is claimed until
the player verifies it. The default never removes front/back trials.
Reference: [Resolving front-back ambiguity with head rotation](https://pubmed.ncbi.nlm.nih.gov/30981050/).

Player feedback identified unexplained paired sounds and an unclear waiting
period. Guided mode is now the default: labelled examples, stereo checks,
explicit first/second-sound status, response gating until both finish, immediate
direction feedback and a Next button. The original five-minute mode is an
explicit selection, with a next-round countdown and hidden correctness.
CSV tags the mode so training and timed observations can be distinguished.
Lifecycle checks cover early-response rejection, two sound events, all 16 guided
rounds, pause cancellation and replay on resume, and timed completion.

Reference read: [A forest never recorded](https://zaghaghi.github.io/spore-and-skog-dev-log/).
Its individually playable sound examples inform the onboarding interaction.
No source code or creature recipes were copied and no Rust migration was made.

## Delivered

`game/demo/` contains a local browser implementation of roadmap test 1:
procedural canyon corridor, synthesized HRTF cues, four directional responses,
five active minutes, 16 balanced randomized trials, optional visual cues and
reduced motion, pause/resume, facilitator-only result reveal, and CSV export.
Launch with `venv/Scripts/python.exe -m studio.cli demo` or `demo.cmd`.
The server binds only to 127.0.0.1 and serves the demo directory.

## Verification

- Model checks exercised 200 randomized schedules: four trials per current
  direction and two louder echoes per direction. Trial boundary and CSV
  quote/newline escaping checks passed.
- Headless lifecycle simulation passed: start/audio invocation, one-answer
  limit, pause time exclusion, resume, next trial, early finish, hidden answers,
  clean restart and a full 300-second session with 16 unanswered events.
- HTTP checks returned 200 with appropriate MIME types for index.html,
  style.css, demo.js and model.mjs. JavaScript syntax check passed.
- No connected browser was available. Rendered UI, audible output, actual HRTF
  discrimination and device performance remain unverified.

## Scope and assumptions

The roadmap explicitly recommends a Web Audio prototype for test 1. This is
that prototype, not a native engine build or campaign demo. Synthesized pulse
and delayed-tail sounds are implementation assumptions, not new approved
campaign echoes. No story files were modified, player studies performed, or
Go/No-Go decision issued. Test 2, test 3, gamepad input and final audio remain
future work. Export session data before starting a new session.
