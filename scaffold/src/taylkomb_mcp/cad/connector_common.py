from __future__ import annotations

from pathlib import Path
from typing import Iterable

import cadquery as cq

from taylkomb_mcp.spec_models import TaylkombSpec


class GeometryBuildError(RuntimeError):
    """Raised when CAD generation fails."""


def _safe_fillet(shape: cq.Workplane, selector: str, radius: float) -> cq.Workplane:
    """Apply a fillet only when the edge selection is non-empty."""
    try:
        return shape.edges(selector).fillet(radius)
    except Exception:
        return shape


def _safe_shell(shape: cq.Workplane, thickness: float) -> cq.Workplane:
    """Shell a body, falling back to the solid if shelling fails."""
    try:
        return shape.faces(">X").shell(-abs(thickness))
    except Exception:
        return shape


def _make_dovetail_polygon(width: float, height: float, included_angle_deg: float) -> list[tuple[float, float]]:
    """Return a 2D trapezoid suitable for a dovetail profile.

    The polygon is oriented with the larger face toward +Y. This is not a manufacturing-truth
    representation of the profile root, but it is stable and deterministic for agentic CAD work.
    """
    half_width = width / 2.0
    half_height = height / 2.0
    taper = height * max(0.10, min(0.32, included_angle_deg / 180.0))
    top_half = half_width + taper / 2.0
    bottom_half = max(half_width - taper / 2.0, width * 0.20)
    return [
        (-bottom_half, -half_height),
        (bottom_half, -half_height),
        (top_half, half_height),
        (-top_half, half_height),
    ]


def make_dovetail_sketch(width: float, height: float, included_angle_deg: float) -> cq.Sketch:
    return cq.Sketch().polygon(_make_dovetail_polygon(width, height, included_angle_deg))


def build_male_rail(spec: TaylkombSpec, engagement_length_mm: float | None = None) -> cq.Workplane:
    rail = spec.connector.rail_profile_mm
    engagement = engagement_length_mm or spec.connector.engagement_length_mm_target
    return cq.Workplane("XY").placeSketch(
        make_dovetail_sketch(rail.width, rail.height, spec.connector.dovetail_angle_deg)
    ).extrude(engagement)


def build_female_socket(
    spec: TaylkombSpec,
    engagement_length_mm: float | None = None,
    clearance_per_side_mm: float | None = None,
    block_padding_xy_mm: float = 4.0,
    back_extra_mm: float = 2.0,
) -> cq.Workplane:
    rail = spec.connector.rail_profile_mm
    engagement = engagement_length_mm or spec.connector.engagement_length_mm_target
    clearance = clearance_per_side_mm or spec.connector.clearance_per_side_mm_range[0]
    outer = cq.Workplane("XY").box(
        rail.width + block_padding_xy_mm * 2.0,
        rail.height + block_padding_xy_mm * 2.0,
        engagement + back_extra_mm,
        centered=(True, True, False),
    )
    inner = cq.Workplane("XY").placeSketch(
        make_dovetail_sketch(
            rail.width + clearance * 2.0,
            rail.height + clearance * 2.0,
            spec.connector.dovetail_angle_deg,
        )
    ).extrude(engagement + back_extra_mm + 0.5)
    return outer.cut(inner)


def build_comb_socket_block(
    spec: TaylkombSpec,
    engagement_length_mm: float | None = None,
    clearance_per_side_mm: float | None = None,
) -> cq.Workplane:
    engagement = engagement_length_mm or spec.connector.engagement_length_mm_target
    block = build_female_socket(
        spec,
        engagement_length_mm=engagement,
        clearance_per_side_mm=clearance_per_side_mm,
        block_padding_xy_mm=4.0,
        back_extra_mm=4.0,
    )
    block = add_detent_pocket(block, spec, z_pos=engagement - 1.25)
    block = add_lead_in_chamfer(block, spec)
    block = add_hair_shed_perimeter(block, spec)
    return block


def build_handle_connector_block(
    spec: TaylkombSpec,
    engagement_length_mm: float | None = None,
    add_release_slot: bool = True,
) -> cq.Workplane:
    engagement = engagement_length_mm or spec.connector.engagement_length_mm_target
    rail = build_male_rail(spec, engagement_length_mm=engagement)
    body = cq.Workplane("XY").box(16.0, 8.0, engagement + 6.0, centered=(True, True, False))
    body = body.union(rail.translate((0.0, 0.0, 2.0)))
    body = drill_ball_bore(body, spec, z_height=engagement - 1.4)
    if add_release_slot:
        body = add_release_button_slot(body, z_center=engagement - 1.4)
    body = add_lead_in_chamfer(body, spec)
    body = add_hair_shed_perimeter(body, spec)
    return body


def add_release_button_slot(
    body: cq.Workplane,
    width_mm: float = 6.5,
    length_mm: float = 12.0,
    depth_mm: float = 1.0,
    z_center: float = 16.0,
) -> cq.Workplane:
    slot = (
        cq.Workplane("XZ")
        .center(0.0, z_center)
        .rect(width_mm, length_mm)
        .extrude(depth_mm, both=False)
        .translate((0.0, 4.0, 0.0))
    )
    return body.cut(slot)


def drill_ball_bore(
    body: cq.Workplane,
    spec: TaylkombSpec,
    x_offset: float = 0.0,
    z_height: float | None = None,
) -> cq.Workplane:
    z_pos = z_height if z_height is not None else spec.connector.engagement_length_mm_target - 3.0
    return (
        body.faces(">Y")
        .workplane(centerOption="CenterOfMass")
        .transformed(offset=(x_offset, 0.0, z_pos))
        .hole(spec.connector.ball_diameter_mm + 0.6)
    )


def add_detent_pocket(body: cq.Workplane, spec: TaylkombSpec, z_pos: float | None = None) -> cq.Workplane:
    z = z_pos if z_pos is not None else spec.connector.engagement_length_mm_target - 1.5
    return (
        body.faces(">Z")
        .workplane(centerOption="CenterOfMass")
        .center(0.0, 0.0)
        .pushPoints([(0.0, 0.0)])
        .cskHole(
            diameter=spec.connector.detent_pocket_diameter_mm,
            depth=spec.connector.detent_pocket_depth_mm,
            cskDiameter=spec.connector.detent_pocket_diameter_mm,
            cskAngle=90.0,
        )
    )


def add_lead_in_chamfer(body: cq.Workplane, spec: TaylkombSpec) -> cq.Workplane:
    try:
        return body.edges("|Z and >Z").chamfer(spec.connector.lead_in_chamfer["length_mm"])
    except Exception:
        return body


def add_hair_shed_perimeter(body: cq.Workplane, spec: TaylkombSpec) -> cq.Workplane:
    try:
        return body.edges("<Z or >Z").chamfer(spec.connector.hair_shed_chamfer["size_mm"])
    except Exception:
        return body


def add_hard_stop_shoulder(
    body: cq.Workplane,
    shoulder_length_mm: float = 2.0,
    shoulder_height_mm: float = 1.5,
    body_width_mm: float = 16.0,
) -> cq.Workplane:
    shoulder = (
        cq.Workplane("XY")
        .box(body_width_mm, 8.0 + shoulder_height_mm, shoulder_length_mm, centered=(True, True, False))
        .translate((0.0, 0.0, 0.0))
    )
    return body.union(shoulder)


def make_rounded_box(length: float, width: float, height: float, fillet: float = 1.0) -> cq.Workplane:
    solid = cq.Workplane("XY").box(length, width, height, centered=(False, True, False))
    return _safe_fillet(solid, "|Z", fillet)


def make_capsule_prism(length: float, width: float, height: float, fillet: float = 1.5) -> cq.Workplane:
    body = (
        cq.Workplane("XY")
        .moveTo(height / 2.0, 0.0)
        .threePointArc((height / 2.0, width / 2.0), (0.0, width / 2.0))
        .lineTo(length - fillet * 2.0, width / 2.0)
        .radiusArc((length, 0.0), -width / 2.0)
        .lineTo(0.0, -width / 2.0)
        .radiusArc((0.0, width / 2.0), width / 2.0)
        .close()
        .extrude(height)
    )
    return _safe_fillet(body, "|Z", fillet)


def make_lofted_oval_handle(
    length: float,
    start_major: float,
    start_minor: float,
    end_major: float,
    end_minor: float,
    mid_major: float | None = None,
    mid_minor: float | None = None,
) -> cq.Workplane:
    mid_major = mid_major if mid_major is not None else (start_major + end_major) / 2.0
    mid_minor = mid_minor if mid_minor is not None else (start_minor + end_minor) / 2.0
    wp = cq.Workplane("XZ")
    wp = wp.workplane(offset=0.0).ellipse(start_major / 2.0, start_minor / 2.0)
    wp = wp.workplane(offset=length * 0.45).ellipse(mid_major / 2.0, mid_minor / 2.0)
    wp = wp.workplane(offset=length * 0.55).ellipse(mid_major / 2.0, mid_minor / 2.0)
    wp = wp.workplane(offset=length).ellipse(end_major / 2.0, end_minor / 2.0)
    return wp.loft(combine=True)


def apply_index_flat(
    body: cq.Workplane,
    depth_mm: float = 0.6,
    width_mm: float = 5.0,
    z_offset: float = 0.0,
) -> cq.Workplane:
    cut = (
        cq.Workplane("YZ")
        .center(0.0, z_offset)
        .rect(width_mm, 200.0)
        .extrude(depth_mm)
        .translate((0.0, 0.0, 0.0))
    )
    return body.cut(cut)


def hollow_handle(body: cq.Workplane, wall_thickness_mm: float = 1.3) -> cq.Workplane:
    return _safe_shell(body, wall_thickness_mm)


def export_shape(shape: cq.Workplane, output_path: str | Path) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    suffix = path.suffix.lower()
    if suffix == ".step":
        cq.exporters.export(shape, str(path))
    elif suffix == ".stl":
        cq.exporters.export(shape, str(path), tolerance=0.01, angularTolerance=0.1)
    elif suffix == ".svg":
        cq.exporters.export(shape, str(path))
    else:
        raise GeometryBuildError(f"Unsupported export format: {suffix}")
    return str(path)


def bounding_box(shape: cq.Workplane) -> dict[str, float]:
    bb = shape.val().BoundingBox()
    return {
        "xlen": bb.xlen,
        "ylen": bb.ylen,
        "zlen": bb.zlen,
        "xmin": bb.xmin,
        "xmax": bb.xmax,
        "ymin": bb.ymin,
        "ymax": bb.ymax,
        "zmin": bb.zmin,
        "zmax": bb.zmax,
    }


def volume_mm3(shape: cq.Workplane) -> float:
    return float(shape.val().Volume())
