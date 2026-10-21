# Production Plan — rade-hoor

Plan ID: `plan-437c67b787`
Status: **approved**
Updated (UTC): 2026-10-21T18:03:58.493189+00:00

## Summary
Rad-e Hoor production plan: prove hearing core (C0), then mechanical vertical slice (C1), then campaign blockout (C2), content (C3), and PC ship prep (C4). No mass final art before C0–C1 clearance. Analysis cites 7 source paths.

## Phases
- C0 audio playtests + Go/No-Go
- C1 mechanical vertical slice
- C2 campaign blockout
- C3 content & integration
- C4 PC ship prep

## Deliverables
### `C0-T1` — Playtest 1 — echo discrimination (Web Audio)
- Layer: C0
- Role: Audio Director
- Depends on: —
- Acceptance: 5-minute corridor build with timed logs + CSV; left/right/front/back balanced

### `C0-T3` — Playtest 3 — hand-in-darkness + 10s window
- Layer: C0
- Role: Gameplay Engineer
- Depends on: C0-T1
- Acceptance: Black-screen reachable window interaction; completable without mic

### `C0-T2` — Playtest 2 — night stealth gray-box
- Layer: C0
- Role: Gameplay Engineer
- Depends on: C0-T1
- Acceptance: Shelter + hearing radii prototype on ADR engine or Unity; CPU/audio latency logged

### `C0-GONOGO` — Document Go/No-Go from tests 1–3
- Layer: C0
- Role: QA / Playtest Lead
- Depends on: C0-T1, C0-T2, C0-T3
- Acceptance: English report with counts (e.g. 8/12); decision recorded under reports/

### `C1-SHELTER` — Vertical slice — vehicle shelter
- Layer: C1
- Role: Gameplay Engineer
- Depends on: C0-GONOGO
- Acceptance: Breath/normal cabin sound does not Bang; contact vs sound separated

### `C1-PLATE` — Vertical slice — plate defense
- Layer: C1
- Role: Gameplay Engineer
- Depends on: C1-SHELTER
- Acceptance: Metal plate blocks contact and allows retreat; quiet path remains valid

### `C1-STRAP` — Vertical slice — strap rescue
- Layer: C1
- Role: Gameplay Engineer
- Depends on: C1-PLATE
- Acceptance: Camera shows hazard/goal/anchor; reading pause is not hidden punishment

### `C1-SILENCE` — Vertical slice — three silence paths
- Layer: C1
- Role: Game Designer
- Depends on: C1-STRAP
- Acceptance: Circle / escape / ledge gray-box reachable; no out-of-pack echoes

### `C2-BLOCKOUT` — Campaign blockout SE→NW
- Layer: C2
- Role: Technical Director
- Depends on: C1-SILENCE
- Acceptance: Readable path/danger/sound; vehicle 7 + winch placeholders; no illegal companion teleport

### `C3-CONTENT` — Content integration from screenplay/bibles
- Layer: C3
- Role: Narrative Lead
- Depends on: C2-BLOCKOUT
- Acceptance: Dialogue/tapes/sheets integrated; E01–E07 only unless approved

### `C4-SHIP` — PC ship prep
- Layer: C4
- Role: Technical Director
- Depends on: C3-CONTENT
- Acceptance: Perf on target HW, Steam packaging path, broader playtests documented

## Risks
- Loop + Bang + radii teachability
- Audio latency / direction discrimination
- Chapter 9 companion routing
- Bahram resource balance if slice depends on it
- Eleven-chapter scope creep before C0 proof
- Early engine lock

## Human gates
- Approve this production plan before executing production tasks
- Main engine ADR after C0 signal (or signed exception)
- API spend over configured cap
- Destructive operations / public release
- Changes to loop, Bang, or ending rules
- Any new echo outside E01–E07

## Approval
- Note: Approved by human
- At: 2026-10-21T18:03:58.493071+00:00
