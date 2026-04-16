from taylkomb_mcp.spec_models import load_spec
from taylkomb_mcp.validation import PART_LENGTH_BANDS, PART_WEIGHT_LIMITS


def test_phase2_length_bands_cover_all_parts():
    spec = load_spec("specs/taylkomb_revC_master.json")
    assert set(spec.part_targets.keys()).issubset(set(PART_LENGTH_BANDS.keys()))


def test_phase2_weight_limits_cover_all_parts():
    spec = load_spec("specs/taylkomb_revC_master.json")
    assert set(spec.part_targets.keys()).issubset(set(PART_WEIGHT_LIMITS.keys()))
