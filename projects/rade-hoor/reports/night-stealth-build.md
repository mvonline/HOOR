# Night stealth — browser interaction prototype

Date: 2026-10-21

## Delivered

`game/demo/stealth.html`: first-person canyon gray-box, three sound-seeking
creatures, intact vehicle contact shelter, reusable throwable distraction, fixed
limited-output transmitter, northeast exit, keyboard/pointer controls, pause,
hidden failure cause and session CSV. Procedural rendering and the accepted
broadband/HRTF sound approach require no external assets or provider key.

The rules model separates hearing from Bang. It uses the approved radii for
sand, stone, running, impact, door and limited transmitter (proposal 3.3), last
heard source investigation and 20-second search (3.4), continuous-source orbit
at five metres, and the two-second output shutdown delay. Shelter blocks
contact while leaving door sounds audible. Bang in this night-only scene
does not activate a dawn-window result. There is a continuous viable quiet path.

## Evidence

Rule checks cover radius boundaries, quiet sound rejection, independent Bang,
last heard source selection, stone/sand movement, 20-second search/return,
shelter audibility/protection, contact without hearing, delayed impact,
continuous-source orbit, output tail, exit and a quiet route through the actual
layout. Headless UI checks exercise the renderer API path, audio setup,
enter/exit controls, pause/resume, movement, throw/HUD classification, stopped
and contact outcomes, and facilitator reveal.

These are automated simulations. No connected browser was available for visual
inspection, and audible output for this new scene has not been player-verified.
Earlier approval of the sound approach is not evidence that this scene passed
playtesting. No Go/No-Go decision or native performance claim is made.

## Explicit limits and assumptions

The roadmap recommends Unity for test 2. This browser rules prototype does not
replace that deliverable or its ten-minute player protocol. A Unity project and
native CPU/audio-latency measurements remain outstanding. Render timings and
browser-reported audio latency are diagnostic data only; actual device output
latency is not measured. Other open work: driving, final art/audio, inventory,
gamepad validation and campaign integration.

The layout, movement/enemy speeds, interaction/contact distances, throw range,
and 0.55-second impact delay are labelled prototype tuning. Mapping throwable
stone impacts to the tool-impact sound category is a prototype assumption.
Unlimited reusable throws are for training, not approved campaign inventory.
