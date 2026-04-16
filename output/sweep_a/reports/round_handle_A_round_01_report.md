# Variant Report — round_handle / A_round_01

## Metrics
- Bounding box: {'xlen': 10.0000002, 'ylen': 5.0000002, 'zlen': 165.5000001, 'xmin': -5.0000001, 'xmax': 5.0000001, 'ymin': -2.5000001, 'ymax': 2.5000001, 'zmin': -144.0000001, 'zmax': 21.5}
- Volume (mm^3): 3644.32
- Estimated mass (g): 14.541
- Assembled estimated mass (g): None
- Assembled length (mm): None
- Clearance per side (mm): 0.05
- Seam step (mm): 0.1
- Engagement length (mm): 14.0
- Tip diameter (mm): 2.1
- Outer width (mm): 0.0

## Validation
- Passed: True
- Checks: {'clearance_per_side': True, 'seam_step': True, 'engagement_length': True, 'part_length_band': True, 'part_weight_limit': True, 'tip_diameter': True}
- Failures: []

## Exports
- step: /mnt/session/taylkomb/taylkomb-cad-agent-scaffold/data/exports/A_round_01/round_handle_A_round_01.step
- stl: /mnt/session/taylkomb/taylkomb-cad-agent-scaffold/data/exports/A_round_01/round_handle_A_round_01.stl

## Notes
- Phase 2 geometry introduces dedicated handle and comb modules plus simple assembly generation.
- Tooth geometry and release-button internals are still placeholder approximations and need CAD refinement.
- This report stays deterministic and spec-driven so Claude can iterate without drifting locked datums.