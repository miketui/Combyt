from taylkomb_mcp.spec_models import load_spec
from taylkomb_mcp.validation import validate_measurements


def test_round_handle_tip_rule_passes():
    spec = load_spec("specs/taylkomb_revC_master.json")
    result = validate_measurements(
        spec,
        {
            "clearance_per_side_mm": 0.12,
            "seam_step_mm": 0.10,
            "tip_diameter_mm": 2.2,
        },
        "round_handle",
    )
    assert result["passed"] is True


def test_round_handle_tip_rule_fails():
    spec = load_spec("specs/taylkomb_revC_master.json")
    result = validate_measurements(
        spec,
        {
            "clearance_per_side_mm": 0.12,
            "seam_step_mm": 0.10,
            "tip_diameter_mm": 3.2,
        },
        "round_handle",
    )
    assert result["passed"] is False
