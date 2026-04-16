# Connector Synthesizer (skill) — Rev D

Generate only vertical ball-stud + cross-detent connector variants within the allowed sweep bands.

## Architecture (locked)
- Vertical insertion axis (driver stem slides up into Main Comb socket).
- Ø 4.00 D-profile stem with Ø 5.00 ball-head and 3.20 retention groove.
- Ø 4.10 socket with cross-bore for Ø 3.00 ball plunger (8–12 N spring).
- Flush release button (Ø 6.00, 0.80 mm travel) on Main Comb spine face.

## Allowed overrides (sweep-tunable)
- `clearance_per_side_mm ∈ [0.03, 0.07]` — tight-to-nominal fit
- `insertion_force_N_target ∈ [10, 15]`
- `retention_force_N_target ∈ [30, 40]`
- `release_force_N_target ∈ [1, 2]`

## Hard restrictions
- Never propose: dovetail, bayonet, collet, magnetic, press-fit without detent,
  or any new architecture.
- Never touch socket/stem/ball-head/groove/chord dimensions (all locked).
- Always call `spec_guard.assert_overrides_safe(overrides)` before generating.
- If an override key is not in the allowed list above, REFUSE and log the attempt.
