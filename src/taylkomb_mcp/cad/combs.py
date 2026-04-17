from __future__ import annotations

from typing import Any

import cadquery as cq

from taylkomb_mcp.cad.connector_common import build_comb_socket_block, make_rounded_box
from taylkomb_mcp.spec_models import TaylkombSpec


def _tooth_band(length: float, body_width: float, tooth_depth: float, tooth_count: int, body_thickness: float) -> cq.Workplane:
    """Simplified placeholder tooth zone.

    This intentionally does not claim final tooth geometry. It creates a repeatable visual and
    dimensional placeholder so variant exports are more realistic than a plain rectangle.
    """
    base = cq.Workplane("XY")
    pitch = length / max(tooth_count, 2)
    tooth = (
        cq.Workplane("XY")
        .polyline([(0.0, 0.0), (pitch * 0.65, 0.0), (pitch * 0.45, tooth_depth), (pitch * 0.15, tooth_depth)])
        .close()
        .extrude(body_thickness)
    )
    teeth = None
    for idx in range(tooth_count):
        inst = tooth.translate((idx * pitch, body_width / 2.0 - tooth_depth, 0.0))
        teeth = inst if teeth is None else teeth.union(inst)
    return teeth if teeth is not None else base.box(length, body_width, body_thickness)


def _build_comb_body(
    length: float,
    body_width: float,
    body_thickness: float,
    tooth_depth: float,
    tooth_count: int,
    fillet: float,
) -> cq.Workplane:
    spine = make_rounded_box(length, body_width, body_thickness, fillet=fillet)
    teeth = _tooth_band(length * 0.92, body_width, tooth_depth, tooth_count, body_thickness * 0.92)
    teeth = teeth.translate((length * 0.04, 0.0, body_thickness * 0.04))
    return spine.union(teeth)


def build_main_comb(spec: TaylkombSpec, overrides: dict[str, Any] | None = None) -> cq.Workplane:
    overrides = overrides or {}
    target = spec.part_targets["main_comb"]
    oal = float(overrides.get("oal_mm", target.oal_mm_target))
    body_length = float(overrides.get("body_length_mm", spec.locked_datums["comb_body_length_mm"]))
    width = float(overrides.get("body_width_mm", 50.8))
    thickness = float(overrides.get("spine_thickness_mm", 3.0))
    tooth_depth = float(overrides.get("tooth_depth_mm", 10.0))
    tooth_count = int(overrides.get("tooth_count", 23))
    root_fillet = float(overrides.get("root_fillet_mm", target.root_fillet_mm_target or 0.8))

    connector = build_comb_socket_block(spec)
    body = _build_comb_body(body_length, width, thickness, tooth_depth, tooth_count, fillet=root_fillet)
    return connector.union(body.translate((16.0, 0.0, 0.0)))


def build_wide_comb(spec: TaylkombSpec, overrides: dict[str, Any] | None = None) -> cq.Workplane:
    overrides = overrides or {}
    target = spec.part_targets["wide_comb"]
    body_length = float(overrides.get("body_length_mm", spec.locked_datums["comb_body_length_mm"]))
    width = float(overrides.get("body_width_mm", 58.0))
    thickness = float(overrides.get("spine_thickness_mm", 3.2))
    tooth_depth = float(overrides.get("tooth_depth_mm", 12.5))
    tooth_count = int(overrides.get("tooth_count", 15))
    connector = build_comb_socket_block(spec)
    body = _build_comb_body(body_length, width, thickness, tooth_depth, tooth_count, fillet=0.8)
    return connector.union(body.translate((16.0, 0.0, 0.0)))


def build_narrow_comb(spec: TaylkombSpec, overrides: dict[str, Any] | None = None) -> cq.Workplane:
    overrides = overrides or {}
    target = spec.part_targets["narrow_comb"]
    oal = float(overrides.get("oal_mm", target.oal_mm_target))
    connector_len = float(spec.locked_datums["comb_connector_protrusion_mm_range"][0])
    body_length = max(oal - connector_len, 175.0)
    width = float(overrides.get("body_width_mm", 36.0))
    thickness = float(overrides.get("spine_thickness_mm", 2.8))
    tooth_depth = float(overrides.get("tooth_depth_mm", 8.5))
    tooth_count = int(overrides.get("tooth_count", 35))
    connector = build_comb_socket_block(spec)
    body = _build_comb_body(body_length, width, thickness, tooth_depth, tooth_count, fillet=0.8)
    return connector.union(body.translate((16.0, 0.0, 0.0)))
