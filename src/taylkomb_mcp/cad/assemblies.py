from __future__ import annotations

from typing import Any

import cadquery as cq

from taylkomb_mcp.cad.connector_common import bounding_box, volume_mm3
from taylkomb_mcp.cad.parts import DENSITY_G_PER_MM3, build_part
from taylkomb_mcp.spec_models import TaylkombSpec


HANDLE_PARTS = {"round_handle", "flat_handle", "double_handle"}
COMB_PARTS = {"main_comb", "wide_comb", "narrow_comb"}


def build_assembly(
    spec: TaylkombSpec,
    comb_part: str,
    handle_part: str,
    comb_overrides: dict[str, Any] | None = None,
    handle_overrides: dict[str, Any] | None = None,
) -> cq.Workplane:
    if comb_part not in COMB_PARTS:
        raise KeyError(f"Assembly requires a comb part, got {comb_part!r}")
    if handle_part not in HANDLE_PARTS:
        raise KeyError(f"Assembly requires a handle part, got {handle_part!r}")

    comb = build_part(comb_part, spec, comb_overrides or {})
    handle = build_part(handle_part, spec, handle_overrides or {})
    comb_bb = comb.val().BoundingBox()
    handle_bb = handle.val().BoundingBox()

    # Simple mating convention: rails are generated along +Z from the connector block.
    # Bring the handle rail into the comb socket by aligning origins and moving the handle
    # so the two connector blocks overlap by the engagement length.
    engagement = (handle_overrides or {}).get("engagement_length_mm", spec.connector.engagement_length_mm_target)
    z_shift = comb_bb.zmin - handle_bb.zmin - 2.0
    assembled_handle = handle.translate((0.0, 0.0, z_shift))

    return comb.union(assembled_handle)


def estimate_part_mass_g(part_name: str, shape: cq.Workplane) -> float:
    material = "PPS-CF40" if "comb" in part_name else "316L_stainless_hollow"
    density = DENSITY_G_PER_MM3.get(material, 0.001)
    return round(volume_mm3(shape) * density, 3)


def assembly_metrics(
    spec: TaylkombSpec,
    comb_part: str,
    handle_part: str,
    comb_shape: cq.Workplane,
    handle_shape: cq.Workplane,
    assembly_shape: cq.Workplane,
) -> dict[str, float | dict[str, float]]:
    comb_mass = estimate_part_mass_g(comb_part, comb_shape)
    handle_mass = estimate_part_mass_g(handle_part, handle_shape)
    assembled_mass = round(comb_mass + handle_mass, 3)
    bb = bounding_box(assembly_shape)
    return {
        "comb_estimated_mass_g": comb_mass,
        "handle_estimated_mass_g": handle_mass,
        "assembled_estimated_mass_g": assembled_mass,
        "assembled_length_mm": round(bb["zlen"], 3),
        "assembled_bounding_box_mm": bb,
    }
