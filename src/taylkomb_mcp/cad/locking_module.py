"""Rev D — vertical ball-stud + cross-detent locking module.

The canonical socket (on Main Comb only) and stem (on the 5 driver parts) are
generated from this module so every part inherits an identical interface.
"""
from __future__ import annotations

import cadquery as cq

# ── Locked Rev D dimensions (mm) ──────────────────────────────────────────
SOCKET_DIAMETER_MM = 4.10
SOCKET_DEPTH_MM = 13.00
SOCKET_LEADIN_CHAMFER_MM = 0.8

STEM_DIAMETER_MM = 4.00
STEM_LENGTH_MM = 14.00
STEM_BALL_HEAD_DIAMETER_MM = 5.00
STEM_GROOVE_DIAMETER_MM = 3.20
STEM_GROOVE_LENGTH_MM = 1.00
STEM_GROOVE_OFFSET_FROM_BALL_MM = 0.40
STEM_D_CHORD_MM = 3.20
STEM_ROOT_FILLET_MM = 0.80

CONNECTOR_BLOCK_W_MM = 10.0
CONNECTOR_BLOCK_H_MM = 5.0
CONNECTOR_BLOCK_D_MM = 5.0

CROSS_BORE_DIAMETER_MM = 3.00
RELEASE_BUTTON_DIAMETER_MM = 6.00
RELEASE_BUTTON_TRAVEL_MM = 0.80


def build_driver_stem() -> cq.Workplane:
    """Build the male stem (used on Wide, Narrow, Round, Flat, Double)."""
    stem = (
        cq.Workplane("XY").cylinder(STEM_LENGTH_MM, STEM_DIAMETER_MM / 2.0)
    )
    ball = (
        cq.Workplane("XY")
        .workplane(offset=STEM_LENGTH_MM / 2.0)
        .sphere(STEM_BALL_HEAD_DIAMETER_MM / 2.0)
    )
    stem = stem.union(ball)

    groove_z = (
        STEM_LENGTH_MM / 2.0
        - STEM_BALL_HEAD_DIAMETER_MM / 2.0
        - STEM_GROOVE_OFFSET_FROM_BALL_MM
        - STEM_GROOVE_LENGTH_MM / 2.0
    )
    outer = (
        cq.Workplane("XY")
        .workplane(offset=groove_z)
        .cylinder(STEM_GROOVE_LENGTH_MM, STEM_DIAMETER_MM / 2.0)
    )
    inner = (
        cq.Workplane("XY")
        .workplane(offset=groove_z)
        .cylinder(STEM_GROOVE_LENGTH_MM, STEM_GROOVE_DIAMETER_MM / 2.0)
    )
    stem = stem.cut(outer.cut(inner))

    chord_offset = STEM_D_CHORD_MM - (STEM_DIAMETER_MM / 2.0)
    cutter = (
        cq.Workplane("XY")
        .box(STEM_DIAMETER_MM * 2, STEM_DIAMETER_MM * 2, STEM_LENGTH_MM + 2)
        .translate((0, -STEM_DIAMETER_MM - chord_offset, 0))
    )
    stem = stem.cut(cutter)
    return stem


def build_receiver_socket_features(
    host: cq.Workplane, socket_center: tuple[float, float, float]
) -> cq.Workplane:
    """Cut a Rev D socket into `host` at `socket_center` (insertion axis +Z)."""
    cx, cy, cz = socket_center

    bore = (
        cq.Workplane("XY")
        .workplane(offset=cz + SOCKET_DEPTH_MM / 2.0)
        .cylinder(SOCKET_DEPTH_MM, SOCKET_DIAMETER_MM / 2.0)
        .translate((cx, cy, 0))
    )
    host = host.cut(bore)

    chamfer_r1 = SOCKET_DIAMETER_MM / 2.0 + SOCKET_LEADIN_CHAMFER_MM * 0.577
    chamfer_r2 = SOCKET_DIAMETER_MM / 2.0
    chamfer = (
        cq.Workplane("XY")
        .workplane(offset=cz + SOCKET_DEPTH_MM - SOCKET_LEADIN_CHAMFER_MM / 2.0)
        .circle(chamfer_r1)
        .workplane(offset=SOCKET_LEADIN_CHAMFER_MM)
        .circle(chamfer_r2)
        .loft(combine=False)
        .translate((cx, cy, 0))
    )
    host = host.cut(chamfer)

    cross_bore_z = (
        cz
        + SOCKET_DEPTH_MM
        - STEM_GROOVE_OFFSET_FROM_BALL_MM
        - STEM_GROOVE_LENGTH_MM / 2.0
        - STEM_BALL_HEAD_DIAMETER_MM / 2.0
    )
    cross_bore = (
        cq.Workplane("YZ")
        .workplane(offset=CROSS_BORE_DIAMETER_MM * 3)
        .cylinder(CROSS_BORE_DIAMETER_MM * 6, CROSS_BORE_DIAMETER_MM / 2.0)
        .translate((cx, cy, cross_bore_z))
    )
    host = host.cut(cross_bore)

    button = (
        cq.Workplane("YZ")
        .workplane(offset=CONNECTOR_BLOCK_W_MM / 2.0)
        .cylinder(RELEASE_BUTTON_TRAVEL_MM * 2, RELEASE_BUTTON_DIAMETER_MM / 2.0)
        .translate((cx, cy, cross_bore_z))
    )
    host = host.cut(button)

    return host


def build_driver_connector_block() -> cq.Workplane:
    """The small block at the base of the stem on every driver part."""
    return (
        cq.Workplane("XY")
        .box(CONNECTOR_BLOCK_W_MM, CONNECTOR_BLOCK_H_MM, CONNECTOR_BLOCK_D_MM)
        .edges(">Z")
        .chamfer(0.5)
    )
