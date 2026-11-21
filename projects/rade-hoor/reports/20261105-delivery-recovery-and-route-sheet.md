# Delivery interaction recovery and route-sheet pass — 2026-11-05

Source changes after 0.7.0-preview; no new player build or ZIP produced.

- Restored checkpoints now reconstruct the R-17 indicator, case placement/open state and canonical actor starting positions. An interrupted carry resumes as a ground pickup. Invalid stage/version values are rejected; invalid elapsed values are normalised.
- Restart resets the cast routes/positions, instrument state and look controls.
- Physical placement acceptance uses the actual bench footprint rather than a radius around its front approach point. A safely supported off-centre placement now counts. Missed or obstructed placements return control for another pickup instead of trapping the player in placement mode. Automatic joint releases restore player/case contact.
- Replaced the three-row route sheet with an interactive field sketch: numbered pins, landmark symbols and matching clickable legend. It is explicitly schematic and not to scale; English/Persian strings remain available. Added a short progress strip for existing hold-to-work actions, without extending their duration.

Validation: runtime and Editor C# compilation passed. Full delivery Play Mode check passed, including wrong map rejection, checkpoint device reconstruction, invalid checkpoint rejection, safe carry resume, actor restart, missed-placement retry and separate save. Log: builds/checks/source-delivery-recovery.log. The first run exposed a safe off-centre landing incorrectly rejected by the old circular threshold; the corrected footprint check passed the complete route.

Visual limitation: batch Editor produced actual scene-camera captures but no HUD screenshots for the route sheet; its appearance still needs visual review. These source changes are not in the already packaged 0.7.0-preview release. Final animation, character art, recorded dialogue, audio mix, measured duration and performance acceptance remain open.
