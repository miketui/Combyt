from taylkomb_mcp.spec_models import load_spec


def test_load_spec():
    spec = load_spec("specs/taylkomb_revC_master.json")
    assert spec.project == "TAYLKOMB"
    assert spec.connector.dovetail_angle_deg == 60.0
    assert spec.connector.rail_profile_mm.width == 8.0
