# Variant Report — main_comb / A_main_01

## Metrics
- Bounding box: {'xlen': 202.0, 'ylen': 32.00000000000001, 'zlen': 6.700000000000001, 'xmin': -101.0, 'xmax': 101.0, 'ymin': -16.0, 'ymax': 16.000000000000007, 'zmin': -3.35, 'zmax': 3.3500000000000005}
- Volume (mm^3): 27914.634
- Estimated mass (g): 13.678
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
- step: /mnt/session/taylkomb/taylkomb-cad-agent-scaffold/data/exports/A_main_01/main_comb_A_main_01.step
- stl: /mnt/session/taylkomb/taylkomb-cad-agent-scaffold/data/exports/A_main_01/main_comb_A_main_01.stl

## Notes
- Phase 2 geometry introduces dedicated handle and comb modules plus simple assembly generation.
- Tooth geometry and release-button internals are still placeholder approximations and need CAD refinement.
- This report stays deterministic and spec-driven so Claude can iterate without drifting locked datums.