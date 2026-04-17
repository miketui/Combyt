from __future__ import annotations

import json
from pathlib import Path

from taylkomb_mcp.server_logic import generate_connector_variant_logic


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "taylkomb_revC_master.json"


DEMO_RUNS = [
    {
        "variant_id": "phase2_round_A",
        "part_name": "round_handle",
        "overrides": {"tip_diameter_mm": 2.0, "tail_length_mm": 128.0},
    },
    {
        "variant_id": "phase2_flat_A",
        "part_name": "flat_handle",
        "overrides": {"grip_width_mm": 24.0, "blade_height_mm": 34.0},
    },
    {
        "variant_id": "phase2_double_A",
        "part_name": "double_handle",
        "overrides": {"outer_width_mm": 35.0, "prong_x_mm": 8.0, "prong_y_mm": 9.0},
    },
    {
        "variant_id": "phase2_precision_combo",
        "part_name": "main_comb+round_handle",
        "overrides": {
            "comb": {},
            "handle": {"tip_diameter_mm": 2.0, "tail_length_mm": 128.0, "engagement_length_mm": 20.0},
        },
    },
]


def main() -> None:
    results = []
    for run in DEMO_RUNS:
        result = generate_connector_variant_logic(
            spec_path=str(SPEC),
            variant_id=run["variant_id"],
            part_name=run["part_name"],
            backend="cadquery",
            overrides=run["overrides"],
            output_formats=["step", "stl"],
        )
        results.append(result)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
