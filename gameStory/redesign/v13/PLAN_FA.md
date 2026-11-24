# v13 plan (draft template)

Status: plan only, nothing drafted. Based on `claude-review.md` and `code-review.md` (repo root), dated 2026-11-24.
Unverified review findings (marked ◇ in `claude-review.md`) must be checked against the text before they enter the canon ledger.

## 1. Premise and base

- **Base:** v11's spine, which is name and guilt (Sam, the receipt, the rabbit sticker, six names, shout-the-name mechanic, the offer to forget, the door-knock epilogue).
- **Transplant from v12:** the operational goal (stop the shipment), one clock, the D01–D04 camp-move chain, Pouya as broker, Sara as risk-fixer, Soren's turn, Bahram's betrayal (repaired), the "hidden secret" character format.
- **Rule for v13:** every element must either cost the hero a trace/name or protect one. Anything else is cut.
- **Open decisions (yours, see §6):** Mk-3, aircraft, Site hook, Danyal's complicity.

## 2. Folder template

```
v13/
  00_CANON_LEDGER_FA.md      single source of truth (see §3)
  01_STORY_BIBLE_FA.md       premise, rules of the world, villain plan, ending
  02_CHARACTERS_FA.md        one block per character (§4)
  03_TIMELINE_FA.md          one calendar (§5)
  04_SCREENPLAY_FA.md        15 chapters + prologue + epilogue
  05_GAMEPLAY_FA.md          verbs, missions M01–M40, unlock curve
  06_WORLD_AND_PLACES_FA.md  zones, camps, vehicles, weapons
  07_DIRECTION_FA.md         tone rules, dialogue standard, scope gate
  CHANGELOG.md               every decision, who/when/why
  README.md                  map of docs, no premise text (links only)
```

README holds no story claims, so it can't go stale again.

## 3. Canon ledger (prevents the v12 contradictions)

One table; every other doc links to it and never restates a value.

| Field | Value (fill once) | Used in |
|---|---|---|
| Chapter titles (15 + prologue + epilogue) | final list | all docs, site |
| Bahram: status at start, capture, betrayal, death (chapter) | | |
| Subject-09 / Farhad: first meeting chapter | | |
| Drive: origin, who has it, layers 1–3 and what each shows | | |
| Shipment deadline: date, hour, landing, loading, takeoff | | |
| Key validity windows | | |
| Danyal's past: what he did, what he knew, what it cost | | |
| Arash's weapon in the finale | | |
| Names/spelling/ages for every character | | |
| Item codes (BM01–BM04, D01–D04) and lock rules | | |
| Mk-1 appearances (list) | | |

Rule: a change to the ledger is the first commit of any edit; docs follow.

## 4. Character block template

```
Name · age · role · what they want · what they lie about
Hidden secret (and in which chapter it surfaces)
Moral grey: one likable act, one unlikable act, one self-interested act
How they speak: rhythm, tic, what they never say aloud
Object that carries their story (prop)
Arc beats by act (3 lines max)
Camp function: what they give, what they ask for
```

Camp NPCs keep their own stories. No "pure white / pure black" labels. Cold is one register, not everyone's default.

## 5. Timeline template (one calendar)

A table with columns: day, clock time, chapter, location, event, what Danyal knows, what Sara knows, deadline status. Every "48 hours", "72 hours", "tonight 22:00" must appear here or nowhere.

## 6. Decisions to make before drafting

1. **Danyal's complicity:** (a) v11-style guilty bystander, (b) v12-style former commander, (c) hybrid: a specific past decision with cost, revealed once.
2. **Shipment/aircraft:** keep with a clock and a finale, or replace with a convoy/ground finale.
3. **Mk-3:** cut, or keep with rules (daylight stability, what destroys the sample vs the formula vs the data).
4. **Site hook:** cut, or seed it in chapters 13–15 and drop the contradiction with "network zeroed".
5. **Tone:** which warm beats are allowed (one earned quiet beat per act is the default).
6. **Demo slice:** prologue, ch1, ch3, ch6.

## 7. Chapter template

```
Chapter N — title (final, from ledger)
Day/hour · place · zone · mission(s) Mxx
Goal of the player / obstacle / cost (trace, ammo, water, time)
Story turn (what changes for the audience)
Setups planted here → payoff chapter
Who is on screen · who knows what (3 lines)
Verb introduced or required
Set-piece (physical, not talk only)
```

Horror chapters (6, 12): built, not told: one full page of the thermal/ceiling beat, ammo-limited siege, no instant kills.

## 8. Dialogue rules

- Subtext, half-sentences, humor, info by objects.
- No aphorisms, no speeches, no plan announcements, no CV introductions.
- One line of exposition per scene maximum; the rest by prop or action.
- Each speaker tested against the character block's "how they speak".

## 9. Work plan

| Phase | Output | Gate |
|---|---|---|
| 0 | Decisions §6 resolved | You sign off |
| 1 | Canon ledger + timeline | No blank cells |
| 2 | Bible + characters | Every secret has a chapter |
| 3 | Chapter beat sheets (15) | Setup→payoff table has no orphans |
| 4 | Screenplay draft | Checks in §10 |
| 5 | Gameplay doc: M01–M40 mapped to scenes, verb unlock curve | Every scene maps to one mission |
| 6 | Dialogue pass | Tone checklist |
| 7 | Site/tools update | continuity script passes |

## 10. Acceptance checks (to automate where possible)

- All chapter titles identical across docs (script).
- Every setup has a payoff and every payoff a setup (table).
- No character knows a fact before its reveal scene (per-character knowledge grid).
- Timeline contains every time reference in the screenplay.
- Each scene maps to exactly one mission; each mission to ≥1 scene.
- Verb unlock: no mission requires a verb before its teaching scene.
- Vehicle/weapon roster in docs equals what the screenplay uses.
