# Variant Report — narrow_comb / A_narrow_01

## Metrics
- Bounding box: {'xlen': 178.0, 'ylen': 46.29128784747793, 'zlen': 16.5, 'xmin': -89.0, 'xmax': 89.0, 'ymin': -30.29128784747792, 'ymax': 16.00000000000001, 'zmin': -7.0, 'zmax': 9.5}
- Volume (mm^3): 25468.588
- Estimated mass (g): 10.697
- Assembled estimated mass (g): None
- Assembled length (mm): None
- Clearance per side (mm): 0.05
- Seam step (mm): 0.1
- Engagement length (mm): 14.0
- Tip diameter (mm): 0.0
- Outer width (mm): 0.0

## Validation
- Passed: True
- Checks: {'clearance_per_side': True, 'seam_step': True, 'engagement_length': True, 'part_length_band': True, 'part_weight_limit': True}
- Failures: []

## Exports
- step: /mnt/session/taylkomb/taylkomb-cad-agent-scaffold/data/exports/A_narrow_01/narrow_comb_A_narrow_01.step
- stl: /mnt/session/taylkomb/taylkomb-cad-agent-scaffold/data/exports/A_narrow_01/narrow_comb_A_narrow_01.stl

## Notes
- Phase 2 geometry introduces dedicated handle and comb modules plus simple assembly generation.
- Tooth geometry and release-button internals are still placeholder approximations and need CAD refinement.
- This report stays deterministic and spec-driven so Claude can iterate without drifting locked datums.