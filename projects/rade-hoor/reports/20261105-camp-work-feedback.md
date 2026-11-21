# Camp interaction feedback / source pass / 2026-11-05

Chapter 2's lamp connection, dust clearing and final battery check now require
short held G actions instead of completing immediately with E. Release, looking
away, leaving reach, documents and pause stop the action. Partial progress is
retained and saved on interruption; old version-1 camp saves load with zero work.

## Visible feedback

- Lamp work reveals connected insulated leads and terminal clips, then enables
  the practical lamp and changes the battery indicator to green.
- Dust recedes across the repair seam. Matching irregular weld beads exist on
  both vehicles for the subsequent comparison.
- A short-range chest inspection light helps read the bumper details while
  examining the relevant target. It is disabled outside those camp interactions.
- The service sheet and dashboard note disappear from their physical positions
  when retained. The notebook stays on the table as the read source.
- A progress bar and G prompt display work state; the compact first-person hands
  appear during active work. The final battery target is at an accessible front
  service point rather than inside the vehicle contact envelope.
- Practical-lamp intensity/range were reduced after image review to avoid flooding
  the canopy and table. Thin battery leads do not cast exaggerated close shadows.

This remains staging geometry and procedural hand positioning. There is no final
connector/cloth animation, recorded tool performance, Tape 1 playback or E01 voice
performance in this pass. It does not establish an 8/10 overall experience.

## Validation

Runtime and Editor compilation pass. Camp, spine, prologue and epilogue Editor
regressions passed after the interaction changes. The camp suite passed again
after lighting refinement. Tests check E cannot bypass work, released work stops,
looking away stops, partial progress reloads, light/cable/dust completion applies,
physical papers disappear, and the existing memory/evidence/campaign flow remains.

Actual camera renders were inspected under `builds/checks/source-camp`:
`07-connected-lamp.png` and `08-weld-partial.png`. These are scene renders;
complete visible HUD and continuous human playtesting remain required.

No new executable, release ZIP or version increment was made. The existing 0.5.1
player does not include these source changes.
