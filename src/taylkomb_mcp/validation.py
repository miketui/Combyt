"""Measurement validation and variant ranking — Rev C + Rev D compatible."""
from __future__ import annotations

from typing import Any

from taylkomb_mcp.spec_models import TaylkombSpec


# Rev D length bands derived from part_targets ± tolerance.
# Updated from Rev C values to match shorter Rev D OAL targets.
PART_LENGTH_BANDS: dict[str, tuple[float, float]] = {
    "main_comb":     (195.0, 210.0),
    "wide_comb":     (172.0, 186.0),
    "narrow_comb":   (172.0, 186.0),
    "round_handle":  (150.0, 170.0),
    "flat_handle":   (158.0, 175.0),
    "double_handle": (150.0, 170.0),
}

# Per-part weight ceilings (grams).  Scaffold geometry is intentionally
# heavier than production because tooth fields and hollowing are placeholder.
PART_WEIGHT_LIMITS: dict[str, float] = {
    "main_comb":     22.0,
    "wide_comb":     25.0,
    "narrow_comb":   18.0,
    "round_handle":  42.0,
    "flat_handle":   45.0,
    "double_handle": 55.0,
}


def _longest_axis(bbox: dict[str, Any]) -> float | None:
    """Return the longest bounding-box axis length, regardless of orientation."""
    candidates = [bbox.get("xlen"), bbox.get("ylen"), bbox.get("zlen")]
    real = [v for v in candidates if isinstance(v, (int, float))]
    return max(real) if real else None


def validate_measurements(spec: TaylkombSpec, measurements: dict[str, Any], part_name: str) -> dict[str, Any]:
    failures: list[str] = []
    checks: dict[str, bool] = {}

    # ── clearance ────────────────────────────────────────────────────
    clearance = measurements.get("clearance_per_side_mm")
    if clearance is not None:
        in_range = spec.connector.clearance_per_side_mm_range[0] <= clearance <= spec.connector.clearance_per_side_mm_range[1]
        checks["clearance_per_side"] = in_range
        if not in_range:
            failures.append(f"clearance_per_side_mm={clearance} outside {spec.connector.clearance_per_side_mm_range}")

    # ── seam step ────────────────────────────────────────────────────
    seam_step = measurements.get("seam_step_mm")
    if seam_step is not None:
        in_range = seam_step <= spec.rules.reject_if_seam_step_gt_mm
        checks["seam_step"] = in_range
        if not in_range:
            failures.append(f"seam_step_mm={seam_step} exceeds {spec.rules.reject_if_seam_step_gt_mm}")

    # ── engagement length ────────────────────────────────────────────
    engagement = measurements.get("engagement_length_mm")
    if engagement is not None:
        in_range = spec.connector.engagement_length_mm_range[0] <= engagement <= spec.connector.engagement_length_mm_range[1]
        checks["engagement_length"] = in_range
        if not in_range:
            failures.append(f"engagement_length_mm={engagement} outside {spec.connector.engagement_length_mm_range}")

    # ── part length band (longest bounding-box axis) ─────────────────
    bbox = measurements.get("bounding_box_mm") or {}
    length_value = _longest_axis(bbox)
    if length_value is not None and part_name in PART_LENGTH_BANDS:
        min_len, max_len = PART_LENGTH_BANDS[part_name]
        in_range = min_len <= length_value <= max_len
        checks["part_length_band"] = in_range
        if not in_range:
            failures.append(f"{part_name} length={round(length_value, 2)} outside {min_len}-{max_len} mm")

    # ── part weight limit ────────────────────────────────────────────
    est_mass = measurements.get("estimated_mass_g")
    if isinstance(est_mass, (int, float)) and part_name in PART_WEIGHT_LIMITS:
        in_range = est_mass <= PART_WEIGHT_LIMITS[part_name]
        checks["part_weight_limit"] = in_range
        if not in_range:
            failures.append(f"{part_name} estimated_mass_g={est_mass} exceeds {PART_WEIGHT_LIMITS[part_name]} g")

    # ── round-handle tip diameter ────────────────────────────────────
    if part_name == "round_handle":
        tip = measurements.get("tip_diameter_mm")
        tip_range = spec.part_targets["round_handle"].tip_diameter_mm_range
        if tip is not None and tip_range is not None:
            in_range = tip_range[0] <= tip <= tip_range[1]
            checks["tip_diameter"] = in_range
            if not in_range:
                failures.append(f"tip_diameter_mm={tip} outside {tip_range}")

    # ── double-handle fork width ─────────────────────────────────────
    if part_name == "double_handle":
        outer_width = measurements.get("outer_width_mm")
        target = spec.part_targets["double_handle"].outer_width_mm_target
        if outer_width is not None and target is not None:
            in_range = outer_width >= 25.0
            checks["outer_width_minimum"] = in_range
            if not in_range:
                failures.append(f"outer_width_mm={outer_width} below 25.0 mm ergonomic minimum (research-backed)")

    # ── assembled length ─────────────────────────────────────────────
    assembled_length = measurements.get("assembled_length_mm")
    if isinstance(assembled_length, (int, float)):
        min_len, max_len = spec.assembly_targets.assembled_length_mm_range
        in_range = min_len <= assembled_length <= max_len
        checks["assembled_length"] = in_range
        if not in_range:
            failures.append(f"assembled_length_mm={assembled_length} outside {min_len}-{max_len} mm")

    # ── assembled weight ─────────────────────────────────────────────
    assembled_weight = measurements.get("assembled_estimated_mass_g")
    if isinstance(assembled_weight, (int, float)):
        max_weight = spec.assembly_targets.assembled_weight_g_max
        in_range = assembled_weight <= max_weight
        checks["assembled_weight_max"] = in_range
        if not in_range:
            failures.append(f"assembled_estimated_mass_g={assembled_weight} exceeds {max_weight} g")

    return {"passed": not failures, "checks": checks, "failures": failures}


def rank_variants(variants: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def score(v: dict[str, Any]) -> tuple[int, int, float, float]:
        validation = v.get("validation", {})
        metrics = v.get("metrics", {})
        passed = 1 if validation.get("passed") else 0
        failure_count = len(validation.get("failures", []))
        seam_penalty = float(metrics.get("seam_step_mm", 0.0) or 0.0)
        weight_penalty = float(metrics.get("assembled_estimated_mass_g", metrics.get("estimated_mass_g", 0.0)) or 0.0)
        return (passed, -failure_count, -seam_penalty, -weight_penalty)

    return sorted(variants, key=score, reverse=True)
