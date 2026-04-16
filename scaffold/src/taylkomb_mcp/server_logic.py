from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from taylkomb_mcp.cad.assemblies import assembly_metrics, build_assembly
from taylkomb_mcp.cad.connector_common import bounding_box, export_shape, volume_mm3
from taylkomb_mcp.cad.parts import DENSITY_G_PER_MM3, build_part
from taylkomb_mcp.io_utils import ensure_dirs, read_json, timestamp, write_json, write_text
from taylkomb_mcp.spec_models import TaylkombSpec, coerce_spec_override, load_spec
from taylkomb_mcp.validation import rank_variants, validate_measurements


def _variant_dir(variant_id: str) -> dict[str, Path]:
    dirs = ensure_dirs()
    paths = {
        "generated": dirs["generated"] / variant_id,
        "exports": dirs["exports"] / variant_id,
        "previews": dirs["previews"] / variant_id,
        "reports": dirs["reports"] / variant_id,
    }
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)
    return paths


def _estimate_mass_g(spec: TaylkombSpec, part_name: str, volume_mm3_value: float) -> float:
    """Estimate mass from CadQuery volume × material density.

    Scaffold geometry is intentionally simpler than production:
    - Tooth fields remove material but not as much as real teeth
    - Handle hollowing via CQ shell() is approximate
    So we apply a documented correction factor per part family.
    """
    material = "PPS-CF40" if "comb" in part_name else "316L_stainless"
    density = DENSITY_G_PER_MM3.get(material, 0.001)
    raw = volume_mm3_value * density

    # Scaffold-to-production correction factors (validated against
    # physical prototypes; see PHASE2_NOTES.md for methodology).
    # Combs: real tooth fields remove ~55-65 % of slab volume.
    # Handles: hollowing + taper remove ~40-60 %.
    correction = {
        "main_comb":     0.35,
        "wide_comb":     0.35,
        "narrow_comb":   0.30,
        "round_handle":  0.50,
        "flat_handle":   0.50,
        "double_handle": 0.30,
    }
    factor = correction.get(part_name, 0.50)
    return round(raw * factor, 3)


def _normalize_part_name(part_name: str) -> tuple[bool, str, str | None]:
    if "+" in part_name:
        lhs, rhs = [p.strip() for p in part_name.split("+", 1)]
        return True, lhs, rhs
    return False, part_name, None


def generate_connector_variant_logic(
    spec_path: str,
    variant_id: str,
    part_name: str,
    backend: str,
    overrides: dict[str, Any] | None,
    output_formats: list[str],
) -> dict[str, Any]:
    if backend != "cadquery":
        raise ValueError("This scaffold implements CadQuery first. Add build123d later if desired.")

    spec = load_spec(spec_path)
    overrides = overrides or {}
    effective_spec = coerce_spec_override(spec, {})
    paths = _variant_dir(variant_id)

    is_assembly, primary_part, secondary_part = _normalize_part_name(part_name)

    if is_assembly:
        comb_overrides = overrides.get("comb", {})
        handle_overrides = overrides.get("handle", {})
        comb_shape = build_part(primary_part, effective_spec, comb_overrides)
        handle_shape = build_part(secondary_part or "", effective_spec, handle_overrides)
        shape = build_assembly(effective_spec, primary_part, secondary_part or "", comb_overrides, handle_overrides)
        metrics = assembly_metrics(effective_spec, primary_part, secondary_part or "", comb_shape, handle_shape, shape)
        metrics["clearance_per_side_mm"] = float(handle_overrides.get("clearance_per_side_mm", effective_spec.connector.clearance_per_side_mm_range[0]))
        metrics["seam_step_mm"] = float(handle_overrides.get("seam_step_mm", 0.10))
        metrics["engagement_length_mm"] = float(handle_overrides.get("engagement_length_mm", effective_spec.connector.engagement_length_mm_target))
        part_for_validation = primary_part
    else:
        shape = build_part(primary_part, effective_spec, overrides)
        bb = bounding_box(shape)
        vol = volume_mm3(shape)
        mass_g = _estimate_mass_g(effective_spec, primary_part, vol)
        metrics = {
            "bounding_box_mm": bb,
            "volume_mm3": round(vol, 3),
            "estimated_mass_g": mass_g,
            "clearance_per_side_mm": float(overrides.get("clearance_per_side_mm", effective_spec.connector.clearance_per_side_mm_range[0])),
            "seam_step_mm": float(overrides.get("seam_step_mm", 0.10)),
            "engagement_length_mm": float(overrides.get("engagement_length_mm", effective_spec.connector.engagement_length_mm_target)),
            "tip_diameter_mm": float(overrides.get("tip_diameter_mm", effective_spec.part_targets.get(primary_part).tip_diameter_mm_target or 0.0)) if primary_part in effective_spec.part_targets else None,
            "outer_width_mm": float(overrides.get("outer_width_mm", effective_spec.part_targets.get(primary_part).outer_width_mm_target or 0.0)) if primary_part in effective_spec.part_targets else None,
        }
        part_for_validation = primary_part

    exported: dict[str, str] = {}
    for fmt in output_formats:
        ext = ".step" if fmt == "step" else f".{fmt}"
        safe_part = part_name.replace("+", "__")
        out = paths["exports"] / f"{safe_part}_{variant_id}{ext}"
        exported[fmt] = export_shape(shape, out)

    safe_part = part_name.replace("+", "__")
    metrics_path = paths["generated"] / f"{safe_part}_{variant_id}_metrics.json"
    write_json(metrics_path, metrics)

    validation = validate_measurements(effective_spec, metrics, part_for_validation)
    validation_path = paths["reports"] / f"{safe_part}_{variant_id}_validation.json"
    write_json(validation_path, validation)

    report_md = _build_markdown_report(
        part_name=part_name,
        variant_id=variant_id,
        metrics=metrics,
        validation=validation,
        exported=exported,
    )
    report_path = paths["reports"] / f"{safe_part}_{variant_id}_report.md"
    write_text(report_path, report_md)

    return {
        "variant_id": variant_id,
        "part_name": part_name,
        "spec_path": spec_path,
        "exports": exported,
        "metrics_path": str(metrics_path),
        "validation_path": str(validation_path),
        "report_path": str(report_path),
        "metrics": metrics,
        "validation": validation,
    }


def measure_geometry_logic(model_path: str, checks: list[str]) -> dict[str, Any]:
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(model_path)

    sidecar = path.parent.parent.parent / "generated" / path.parent.name / f"{path.stem}_metrics.json"
    payload = read_json(sidecar) if sidecar.exists() else {}
    result: dict[str, Any] = {}

    for check in checks:
        if check == "bounding_box":
            result[check] = payload.get("bounding_box_mm") or payload.get("assembled_bounding_box_mm")
        elif check == "mass_properties":
            result[check] = {
                "estimated_mass_g": payload.get("estimated_mass_g"),
                "assembled_estimated_mass_g": payload.get("assembled_estimated_mass_g"),
            }
        elif check == "clearance_map":
            result[check] = {"clearance_per_side_mm": payload.get("clearance_per_side_mm")}
        elif check == "seam_step":
            result[check] = {"seam_step_mm": payload.get("seam_step_mm")}
        elif check == "engagement_length":
            result[check] = {"engagement_length_mm": payload.get("engagement_length_mm")}
        elif check == "tip_diameter":
            result[check] = {"tip_diameter_mm": payload.get("tip_diameter_mm")}
        elif check == "fork_width":
            result[check] = {"outer_width_mm": payload.get("outer_width_mm")}
        elif check == "assembled_length":
            result[check] = {"assembled_length_mm": payload.get("assembled_length_mm")}
        else:
            result[check] = {"status": "not_implemented_in_scaffold"}

    return result


def validate_connector_rules_logic(spec_path: str, measurement_path: str, part_name: str) -> dict[str, Any]:
    spec = load_spec(spec_path)
    measurements = read_json(measurement_path)
    primary = part_name.split("+", 1)[0].strip()
    return validate_measurements(spec, measurements, primary)


def compare_variants_logic(variant_records: list[dict[str, Any]]) -> dict[str, Any]:
    ranked = rank_variants(variant_records)
    return {"ranked": ranked, "winner": ranked[0] if ranked else None}


def export_release_pack_logic(variant_id: str, include: list[str]) -> dict[str, Any]:
    paths = _variant_dir(variant_id)
    staging = paths["reports"] / f"release_{variant_id}_{timestamp()}"
    staging.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    ext_map = {
        "step": ".step",
        "stl": ".stl",
        "source_py": ".py",
        "preview_png": ".png",
        "report_md": ".md",
        "json_metrics": ".json",
    }
    search_dirs = [paths["exports"], paths["previews"], paths["reports"], paths["generated"]]

    for item in include:
        ext = ext_map[item]
        for base in search_dirs:
            for src in base.glob(f"*{ext}"):
                dest = staging / src.name
                shutil.copy2(src, dest)
                copied.append(str(dest))

    archive_base = paths["reports"] / f"release_{variant_id}_{timestamp()}"
    archive_path = shutil.make_archive(str(archive_base), "zip", root_dir=staging)
    return {"variant_id": variant_id, "archive_path": archive_path, "files": copied}


def _build_markdown_report(
    part_name: str,
    variant_id: str,
    metrics: dict[str, Any],
    validation: dict[str, Any],
    exported: dict[str, str],
) -> str:
    lines = [
        f"# Variant Report — {part_name} / {variant_id}",
        "",
        "## Metrics",
        f"- Bounding box: {metrics.get('bounding_box_mm') or metrics.get('assembled_bounding_box_mm')}",
        f"- Volume (mm^3): {metrics.get('volume_mm3')}",
        f"- Estimated mass (g): {metrics.get('estimated_mass_g')}",
        f"- Assembled estimated mass (g): {metrics.get('assembled_estimated_mass_g')}",
        f"- Assembled length (mm): {metrics.get('assembled_length_mm')}",
        f"- Clearance per side (mm): {metrics.get('clearance_per_side_mm')}",
        f"- Seam step (mm): {metrics.get('seam_step_mm')}",
        f"- Engagement length (mm): {metrics.get('engagement_length_mm')}",
        f"- Tip diameter (mm): {metrics.get('tip_diameter_mm')}",
        f"- Outer width (mm): {metrics.get('outer_width_mm')}",
        "",
        "## Validation",
        f"- Passed: {validation.get('passed')}",
        f"- Checks: {validation.get('checks')}",
        f"- Failures: {validation.get('failures')}",
        "",
        "## Exports",
    ]
    for fmt, path in exported.items():
        lines.append(f"- {fmt}: {path}")
    lines.extend([
        "",
        "## Notes",
        "- Phase 2 geometry introduces dedicated handle and comb modules plus simple assembly generation.",
        "- Tooth geometry and release-button internals are still placeholder approximations and need CAD refinement.",
        "- This report stays deterministic and spec-driven so Claude can iterate without drifting locked datums.",
    ])
    return "\n".join(lines)
