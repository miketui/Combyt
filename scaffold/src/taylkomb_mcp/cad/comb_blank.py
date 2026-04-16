"""Shared comb silhouette + M-cutout. Used by main, wide, narrow comb generators."""
from __future__ import annotations

import cadquery as cq

SPINE_WIDTH_MM = 32.0
BODY_THICKNESS_MM = 6.7
M_PEAK_TO_PEAK_MM = 36.0
M_DEPTH_MM = 18.0


def build_comb_blank(oal_mm: float) -> cq.Workplane:
    """Build a flat-plate comb body with the M-shaped dorsal cutout.

    Orientation:
      X axis = length (OAL)
      Y axis = spine width (32 mm)
      Z axis = plate thickness (6.7 mm)
    Origin at center of comb.
    """
    blank = (
        cq.Workplane("XY")
        .box(oal_mm, SPINE_WIDTH_MM, BODY_THICKNESS_MM)
    )

    m_cx = 0.0
    m_top_y = SPINE_WIDTH_MM / 2.0
    m_valley_y = m_top_y - M_DEPTH_MM
    peak_half = M_PEAK_TO_PEAK_MM / 2.0

    m_points = [
        (m_cx - peak_half, m_top_y + 1),
        (m_cx - peak_half / 2.0, m_valley_y),
        (m_cx, m_top_y + 1),
        (m_cx + peak_half / 2.0, m_valley_y),
        (m_cx + peak_half, m_top_y + 1),
        (m_cx + peak_half, m_top_y + 2),
        (m_cx - peak_half, m_top_y + 2),
    ]
    m_cutout = (
        cq.Workplane("XY")
        .polyline(m_points)
        .close()
        .extrude(BODY_THICKNESS_MM + 2, both=True)
    )
    blank = blank.cut(m_cutout)
    return blank
