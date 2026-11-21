# Interaction and first-person arms / 0.5.1-dev

The user reported obstructive spread arms on foot and unreliable object approach
and pickup in 0.5.0-dev.

The hands used fixed rotations that assumed a different anatomical bind pose.
They now solve arm joints toward camera-relative targets below the center of
view, with the shoulders lowered. Normal exploration hides the viewmodel; actual
held-tool work raises it. The normal walking camera remains unobstructed.

Camp and later chapter interactions now share an aim-area check, with a bounded
close-object angular allowance. Range and facing requirements remain. A center
reticle indicates eligible E/G actions. Missing an item interaction no longer
silently enters a nearby vehicle. F retains explicit vehicle entry/exit.
The visible dashboard paper was inside the vehicle contact envelope while its
target was elsewhere; both now coincide on the accessible driver's-door side.

## Verification

- Unity Windows 0.5.1-dev build succeeded in its own output directory.
- Camp regression now walks the CharacterController from four metres away up to
  the physical worktable, verifies approach and interaction, rejects facing away
  and out-of-range targets, verifies no idle hands, checks compact hand positions
  and rejects accidental vehicle entry after a missed E interaction.
- Camp, prologue and Chapters 3–10 player regressions all pass.
- Actual camera renders were inspected: `05-walking-clear-view.png` and
  `06-tool-hands-view.png` in `builds/checks/release-campaign/`. The scene is clear
  while walking, with working hands at the bottom edge instead of across the view.

These are controlled checks and image review, not a complete human playtest of
every object. This repair does not finish the remaining production art/animation.

Output: `builds/releases/Rad-e-Hoor-0.5.1-dev-Windows.zip`.
Earlier releases remain unchanged; no running user game was closed.
