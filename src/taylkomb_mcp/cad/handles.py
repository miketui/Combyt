from __future__ import annotations

from typing import Any

import cadquery as cq

from taylkomb_mcp.cad.connector_common import (
    add_hard_stop_shoulder,
    apply_index_flat,
    build_handle_connector_block,
    hollow_handle,
    make_lofted_oval_handle,
    make_rounded_box,
)
from taylkomb_mcp.spec_models import TaylkombSpec


def build_round_handle(spec: TaylkombSpec, overrides: dict[str, Any] | None = None) -> cq.Workplane:
    """Phase 2 round handle.

    This is not final manufacturing geometry, but it is much closer to the Rev C intent:
    shortened overall length, stainless-friendly tail proportions, and a tactile index flat.
    """
    overrides = overrides or {}
    target = spec.part_targets["round_handle"]
    oal = float(overrides.get("oal_mm", target.oal_mm_target))
    tail_length = float(overrides.get("tail_length_mm", target.tail_length_mm_target or 130.0))
    tip = float(overrides.get("tip_diameter_mm", target.tip_diameter_mm_target or 2.0))
    base_dia = float(overrides.get("base_diameter_mm", 11.0))
    mid_dia = float(overrides.get("mid_diameter_mm", 4.8))
    wall = float(overrides.get("wall_thickness_mm", spec.materials.handles.wall_thickness_mm_range[0]))

    connector = build_handle_connector_block(spec, engagement_length_mm=spec.connector.engagement_length_mm_target)
    connector = add_hard_stop_shoulder(connector, shoulder_length_mm=2.0, shoulder_height_mm=1.0)

    shoulder_len = max(oal - tail_length, 44.0)
    shaft = make_lofted_oval_handle(
        length=shoulder_len,
        start_major=14.0,
        start_minor=10.0,
        mid_major=base_dia,
        mid_minor=max(base_dia * 0.80, 8.0),
        end_major=mid_dia,
        end_minor=max(mid_dia * 0.80, 3.6),
    )
    shaft = apply_index_flat(shaft, depth_mm=0.5, width_mm=4.0)

    tail = (
        cq.Workplane("XZ")
        .workplane(offset=0.0)
        .circle(mid_dia / 2.0)
        .workplane(offset=tail_length * 0.55)
        .circle(max(mid_dia * 0.55, tip + 0.6) / 2.0)
        .workplane(offset=tail_length * 0.45)
        .circle(tip / 2.0)
        .loft(combine=True)
    )

    body = connector.union(shaft.translate((0.0, 0.0, 8.0)))
    body = body.union(tail.translate((0.0, 0.0, 8.0 + shoulder_len - 2.0)))
    body = hollow_handle(body, wall_thickness_mm=wall)
    return body


def build_flat_handle(spec: TaylkombSpec, overrides: dict[str, Any] | None = None) -> cq.Workplane:
    overrides = overrides or {}
    target = spec.part_targets["flat_handle"]
    oal = float(overrides.get("oal_mm", target.oal_mm_target))
    work = float(overrides.get("work_section_mm", target.work_section_mm_target or 130.0))
    width = float(overrides.get("grip_width_mm", 24.0))
    thickness = float(overrides.get("grip_thickness_mm", 10.0))
    blade_height = float(overrides.get("blade_height_mm", 34.0))
    wall = float(overrides.get("wall_thickness_mm", spec.materials.handles.wall_thickness_mm_range[0]))

    connector = build_handle_connector_block(spec, engagement_length_mm=spec.connector.engagement_length_mm_target)
    connector = add_hard_stop_shoulder(connector, shoulder_length_mm=2.0, shoulder_height_mm=1.0)

    grip_len = max(oal - work, 52.0)
    grip = make_lofted_oval_handle(
        length=grip_len,
        start_major=max(width - 4.0, 16.0),
        start_minor=max(thickness - 2.0, 7.0),
        mid_major=width,
        mid_minor=thickness,
        end_major=max(width * 0.92, 18.0),
        end_minor=max(thickness * 0.90, 7.0),
    )

    blade = make_rounded_box(work, blade_height, max(thickness * 0.82, 8.0), fillet=1.8)
    blade = blade.translate((0.0, 0.0, grip_len + 6.0))

    body = connector.union(grip.translate((0.0, 0.0, 8.0)))
    body = body.union(blade)
    body = hollow_handle(body, wall_thickness_mm=wall)
    return body


def build_double_handle(spec: TaylkombSpec, overrides: dict[str, Any] | None = None) -> cq.Workplane:
    overrides = overrides or {}
    target = spec.part_targets["double_handle"]
    oal = float(overrides.get("oal_mm", target.oal_mm_target))
    fork_len = float(overrides.get("fork_length_mm", target.fork_length_mm_target or 130.0))
    outer_width = float(overrides.get("outer_width_mm", target.outer_width_mm_target or 35.0))
    prong = target.prong_section_mm_target or {"x": 8.0, "y": 9.0}
    prong_x = float(overrides.get("prong_x_mm", prong["x"]))
    prong_y = float(overrides.get("prong_y_mm", prong["y"]))
    inner_gap = float(overrides.get("inner_gap_mm", max(outer_width - prong_x * 2.0, 12.0)))
    wall = float(overrides.get("wall_thickness_mm", spec.materials.handles.wall_thickness_mm_range[0]))

    connector = build_handle_connector_block(spec, engagement_length_mm=spec.connector.engagement_length_mm_target)
    connector = add_hard_stop_shoulder(connector, shoulder_length_mm=2.0, shoulder_height_mm=1.0)

    grip_block = make_lofted_oval_handle(
        length=max(oal - fork_len, 56.0),
        start_major=22.0,
        start_minor=11.0,
        mid_major=28.0,
        mid_minor=13.0,
        end_major=30.0,
        end_minor=13.0,
    )
    grip_block = apply_index_flat(grip_block, depth_mm=0.5, width_mm=6.0)

    center_offset = inner_gap / 2.0 + prong_x / 2.0
    prong_left = make_rounded_box(fork_len, prong_x, prong_y, fillet=1.2).translate((0.0, -center_offset, 0.0))
    prong_right = make_rounded_box(fork_len, prong_x, prong_y, fillet=1.2).translate((0.0, center_offset, 0.0))
    yoke = make_rounded_box(28.0, outer_width, prong_y + 1.0, fillet=1.5)

    fork = yoke.union(prong_left.translate((26.0, 0.0, 0.0))).union(prong_right.translate((26.0, 0.0, 0.0)))
    fork = fork.translate((0.0, 0.0, max(oal - fork_len, 56.0) + 6.0))

    body = connector.union(grip_block.translate((0.0, 0.0, 8.0)))
    body = body.union(fork)
    body = hollow_handle(body, wall_thickness_mm=wall)
    return body
