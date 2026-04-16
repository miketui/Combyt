# Variant Report — flat_handle / A_flat_01

## Metrics
- Bounding box: {'xlen': 10.0, 'ylen': 5.000000000000001, 'zlen': 172.5, 'xmin': -5.0, 'xmax': 5.0, 'ymin': -2.500000000000001, 'ymax': 2.5, 'zmin': -75.5, 'zmax': 97.0}
- Volume (mm^3): 7686.191
- Estimated mass (g): 30.668
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
- step: /mnt/session/taylkomb/taylkomb-cad-agent-scaffold/data/exports/A_flat_01/flat_handle_A_flat_01.step
- stl: /mnt/session/taylkomb/taylkomb-cad-agent-scaffold/data/exports/A_flat_01/flat_handle_A_flat_01.stl

## Notes
- Phase 2 geometry introduces dedicated handle and comb modules plus simple assembly generation.
- Tooth geometry and release-button internals are still placeholder approximations and need CAD refinement.
- This report stays deterministic and spec-driven so Claude can iterate without drifting locked datums.