# Variant Report — double_handle / A_double_01

## Metrics
- Bounding box: {'xlen': 32.0, 'ylen': 9.0, 'zlen': 158.0, 'xmin': -16.0, 'xmax': 16.0, 'ymin': -4.5, 'ymax': 4.5, 'zmin': -125.0, 'zmax': 33.0}
- Volume (mm^3): 20637.006
- Estimated mass (g): 49.405
- Assembled estimated mass (g): None
- Assembled length (mm): None
- Clearance per side (mm): 0.05
- Seam step (mm): 0.1
- Engagement length (mm): 14.0
- Tip diameter (mm): 0.0
- Outer width (mm): 32.0

## Validation
- Passed: True
- Checks: {'clearance_per_side': True, 'seam_step': True, 'engagement_length': True, 'part_length_band': True, 'part_weight_limit': True, 'outer_width_minimum': True}
- Failures: []

## Exports
- step: /mnt/session/taylkomb/taylkomb-cad-agent-scaffold/data/exports/A_double_01/double_handle_A_double_01.step
- stl: /mnt/session/taylkomb/taylkomb-cad-agent-scaffold/data/exports/A_double_01/double_handle_A_double_01.stl

## Notes
- Phase 2 geometry introduces dedicated handle and comb modules plus simple assembly generation.
- Tooth geometry and release-button internals are still placeholder approximations and need CAD refinement.
- This report stays deterministic and spec-driven so Claude can iterate without drifting locked datums.