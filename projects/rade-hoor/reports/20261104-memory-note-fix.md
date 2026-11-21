# Chapter 2 dashboard-note exception / 0.4.2-dev

The player's Player.log identifies CampMemoryPrompt at LevelOneCampMemory.cs:63.
Collecting the dashboard note saves CampBeat.Memory, but the memory world is
only constructed when that document closes. The camp HUD queried the absent
crate every GUI frame while the note remained open.

The pending-memory objective and prompt now describe closing the note without
accessing memory transforms. Memory interaction also requires an active memory.
No save migration or deletion is required.

The campaign regression now renders frames with the note open before any memory
world exists, checks the HUD, saves/reloads the pending checkpoint and proceeds
through the cargo handoff, garage ledger and camp return.

Verification: Verify-ChapterOne.ps1 -Visible passed the Chapter 1 route, Chapter 2
campaign, Chapters 3-10 spine and intro regressions. These are controlled automated
checks, not a full manual campaign playtest. The proposed wind-erased tracking
mechanic is not implemented in this bug-fix release.
