"""Rev D part generators. Compose comb_blank + locking_module + part-specific features.

Changes vs. original scaffold:
 - Tooth cutting: wider slots (0.65×pitch), deeper (24 mm), larger field (85%)
   to bring scaffold mass estimates closer to production PPS-CF40 combs.
 - Double handle: added grip section between fork and connector to reach target
   OAL; prong thickness scaled to research-backed 32 mm outer width.
"""
from __future__ import annotations

from typing import Any

import cadquery as cq

from taylkomb_mcp.cad.comb_blank import (
    BODY_THICKNESS_MM,
    SPINE_WIDTH_MM,
    build_comb_blank,
)
from taylkomb_mcp.cad.locking_module import (
    CONNECTOR_BLOCK_D_MM,
    CONNECTOR_BLOCK_H_MM,
    CONNECTOR_BLOCK_W_MM,
    STEM_LENGTH_MM,
    build_driver_connector_block,
    build_driver_stem,
    build_receiver_socket_features,
)

DENSITY_G_PER_MM3 = {
    "PPS-CF40": 1.40e-3,
    "316L_stainless": 7.98e-3,
}


def build_main_comb(spec, overrides: dict[str, Any]) -> cq.Workplane:
    oal = overrides.get("oal_mm", spec.part_targets["main_comb"].oal_mm_target)
    blank = build_comb_blank(oal)
    socket_center = (0.0, SPINE_WIDTH_MM / 2.0 - 18.0, 0.0)
    blank = build_receiver_socket_features(blank, socket_center)
    blank = _stamp_mixed_tooth_field(blank, oal)
    return blank


def build_wide_comb(spec, overrides: dict[str, Any]) -> cq.Workplane:
    oal = overrides.get("oal_mm", spec.part_targets["wide_comb"].oal_mm_target)
    pitch = overrides.get(
        "tooth_pitch_mm",
        getattr(spec.part_targets["wide_comb"], "tooth_pitch_mm_target", None) or 5.0,
    )
    blank = build_comb_blank(oal)
    blank = _stamp_uniform_tooth_field(blank, oal, pitch)
    blank = _attach_stem_down(blank, oal)
    return blank


def build_narrow_comb(spec, overrides: dict[str, Any]) -> cq.Workplane:
    oal = overrides.get("oal_mm", spec.part_targets["narrow_comb"].oal_mm_target)
    pitch = overrides.get(
        "tooth_pitch_mm",
        getattr(spec.part_targets["narrow_comb"], "tooth_pitch_mm_target", None) or 2.0,
    )
    blank = build_comb_blank(oal)
    blank = _stamp_uniform_tooth_field(blank, oal, pitch)
    blank = _attach_stem_down(blank, oal)
    return blank


def build_round_handle(spec, overrides: dict[str, Any]) -> cq.Workplane:
    oal = overrides.get("oal_mm", spec.part_targets["round_handle"].oal_mm_target)
    tip_d = overrides.get(
        "tip_diameter_mm",
        spec.part_targets["round_handle"].tip_diameter_mm_target,
    )
    tail_len = oal - STEM_LENGTH_MM
    body = (
        cq.Workplane("XY")
        .workplane(offset=0)
        .rect(10.0, 5.0)
        .workplane(offset=-tail_len)
        .circle(tip_d / 2.0)
        .loft(combine=True)
    )
    body = body.union(build_driver_connector_block().translate((0, 0, 2.5)))
    body = body.union(
        build_driver_stem().translate((0, 0, 5.0 + STEM_LENGTH_MM / 2.0))
    )
    return body


def build_flat_handle(spec, overrides: dict[str, Any]) -> cq.Workplane:
    oal = overrides.get("oal_mm", spec.part_targets["flat_handle"].oal_mm_target)
    tail_len = oal - STEM_LENGTH_MM
    body = (
        cq.Workplane("XY")
        .box(10.0, 5.0, tail_len)
        .edges("|Z")
        .fillet(1.5)
    )
    body = body.union(
        build_driver_connector_block().translate((0, 0, tail_len / 2.0 + 2.5))
    )
    body = body.union(
        build_driver_stem().translate(
            (0, 0, tail_len / 2.0 + 5.0 + STEM_LENGTH_MM / 2.0)
        )
    )
    return body


def build_double_handle(spec, overrides: dict[str, Any]) -> cq.Workplane:
    """Build a double-prong fork handle sized to hit the target OAL.

    Geometry stacks (bottom → top):
      fork prongs  →  yoke bridge  →  grip section  →  connector block  →  stem + ball

    Research basis (professional two-prong tools):
      outer_width ≈ 32 mm, prong gap ≈ 13-16 mm, OAL 150-200 mm.
    """
    oal = overrides.get("oal_mm", spec.part_targets["double_handle"].oal_mm_target)
    outer_w = overrides.get(
        "fork_outer_width_mm",
        getattr(spec.part_targets["double_handle"], "outer_width_mm_target", None) or 32.0,
    )
    fork_len = overrides.get(
        "fork_length_mm",
        getattr(spec.part_targets["double_handle"], "fork_length_mm_target", None) or 125.0,
    )
    fork_fillet = (
        getattr(spec.part_targets["double_handle"], "root_fillet_mm_target", None) or 1.5
    )

    # Prong proportions scaled to outer width (research: ~25% each prong)
    prong_thickness = min(max(outer_w * 0.25, 5.0), 8.0)
    prong_depth = 9.0
    gap = outer_w - 2.0 * prong_thickness

    left_prong = (
        cq.Workplane("XY")
        .box(prong_thickness, prong_depth, fork_len)
        .translate((-(gap / 2.0 + prong_thickness / 2.0), 0, -fork_len / 2.0))
    )
    right_prong = (
        cq.Workplane("XY")
        .box(prong_thickness, prong_depth, fork_len)
        .translate((gap / 2.0 + prong_thickness / 2.0, 0, -fork_len / 2.0))
    )

    # Yoke bridges the two prongs
    yoke_height = 5.0
    yoke = (
        cq.Workplane("XY")
        .box(outer_w, prong_depth, yoke_height)
        .edges("|Z")
        .fillet(fork_fillet)
    )

    # Grip section fills the gap between fork top and connector block to reach OAL
    grip_height = max(
        oal - fork_len - STEM_LENGTH_MM - CONNECTOR_BLOCK_D_MM - yoke_height,
        2.0,
    )
    grip_width = min(outer_w * 0.55, 14.0)
    grip = (
        cq.Workplane("XY")
        .box(grip_width, prong_depth, grip_height)
        .translate((0, 0, yoke_height / 2.0 + grip_height / 2.0))
    )

    # Position connector block and stem on top of grip
    connector_z = yoke_height / 2.0 + grip_height + CONNECTOR_BLOCK_D_MM / 2.0
    stem_z = yoke_height / 2.0 + grip_height + CONNECTOR_BLOCK_D_MM + STEM_LENGTH_MM / 2.0

    body = yoke.union(left_prong).union(right_prong).union(grip)
    body = body.union(build_driver_connector_block().translate((0, 0, connector_z)))
    body = body.union(build_driver_stem().translate((0, 0, stem_z)))
    return body


# ── tooth-cutting helpers ─────────────────────────────────────────────────

# Parameters tuned so scaffold combs remove meaningful material, producing
# mass estimates within ~2× of production (final calibration via the scaffold
# tooth-field factor in server_logic._estimate_mass_g).

_FIELD_FRACTION = 0.85       # tooth field covers 85 % of OAL
_SLOT_WIDTH_RATIO = 0.65     # each slot is 65 % of pitch (tooth is 35 %)
_SLOT_DEPTH_MM = 24.0        # Y-axis depth of each slot cut
_SLOT_Y_CENTER_OFFSET = 5.0  # slot centre offset from body bottom edge


def _stamp_uniform_tooth_field(
    blank: cq.Workplane, oal: float, pitch: float
) -> cq.Workplane:
    tooth_field_len = oal * _FIELD_FRACTION
    n_teeth = int(tooth_field_len // pitch)
    start_x = -tooth_field_len / 2.0 + pitch / 2.0
    slot_y = -SPINE_WIDTH_MM / 2.0 + _SLOT_Y_CENTER_OFFSET
    for i in range(n_teeth):
        x = start_x + i * pitch
        slot = (
            cq.Workplane("XY")
            .box(pitch * _SLOT_WIDTH_RATIO, _SLOT_DEPTH_MM, BODY_THICKNESS_MM + 1)
            .translate((x, slot_y, 0))
        )
        blank = blank.cut(slot)
    return blank


def _stamp_mixed_tooth_field(blank: cq.Workplane, oal: float) -> cq.Workplane:
    """Main-comb mixed field: fine teeth on one side, wide on the other."""
    half = oal / 2.0
    blank = _stamp_uniform_tooth_field_partial(blank, -half + 8, -3, 2.0)
    blank = _stamp_uniform_tooth_field_partial(blank, 3, half - 8, 5.0)
    return blank


def _stamp_uniform_tooth_field_partial(
    blank: cq.Workplane, x_start: float, x_end: float, pitch: float
) -> cq.Workplane:
    length = x_end - x_start
    n_teeth = int(length // pitch)
    slot_y = -SPINE_WIDTH_MM / 2.0 + _SLOT_Y_CENTER_OFFSET
    for i in range(n_teeth):
        x = x_start + pitch / 2.0 + i * pitch
        slot = (
            cq.Workplane("XY")
            .box(pitch * _SLOT_WIDTH_RATIO, _SLOT_DEPTH_MM, BODY_THICKNESS_MM + 1)
            .translate((x, slot_y, 0))
        )
        blank = blank.cut(slot)
    return blank


def _attach_stem_down(blank: cq.Workplane, oal: float) -> cq.Workplane:
    """Attach the driver stem + connector block at the bottom edge of a comb body."""
    block = build_driver_connector_block().translate(
        (-oal / 2.0 + 20.0, -SPINE_WIDTH_MM / 2.0 - 2.5, 0)
    )
    stem = build_driver_stem().translate(
        (-oal / 2.0 + 20.0, -SPINE_WIDTH_MM / 2.0 - 5.0 - STEM_LENGTH_MM / 2.0, 0)
    )
    return blank.union(block).union(stem)


def build_part(part_name: str, spec, overrides: dict[str, Any]) -> cq.Workplane:
    dispatch = {
        "main_comb": build_main_comb,
        "wide_comb": build_wide_comb,
        "narrow_comb": build_narrow_comb,
        "round_handle": build_round_handle,
        "flat_handle": build_flat_handle,
        "double_handle": build_double_handle,
    }
    if part_name not in dispatch:
        raise ValueError(f"Unknown part_name: {part_name}")
    return dispatch[part_name](spec, overrides)
