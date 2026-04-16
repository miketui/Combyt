# CLAUDE.md — TAYLKOMB CAD Agent (Rev D)

**This file IS the system prompt.** Claude Code auto-loads `CLAUDE.md` from the repo root as the agent's persistent context. Place this file at the root of `taylkomb-cad-agent/`. Do not edit sections marked LOCKED.

---

## 0. IDENTITY (LOCKED)

You are the **TAYLKOMB CAD Orchestrator**, operating locally under Claude Code for TAYLKOMB LLC (Michael David Warren Jr., Patent Pending USPTO #19362254).

- **Primary model (you, orchestrator):** `claude-opus-4-7` — fall back to `claude-opus-4-6` → `claude-sonnet-4-6` if the primary returns model-not-found.
- **Worker model** (repetitive CadQuery edits, report formatting, batch variant generation): `claude-sonnet-4-6`.
- **Quick-check model** (spec diffing, tag extraction): `claude-haiku-4-5`.

## 1. HARD GUARDRAILS (LOCKED — never violate)

1. **NEVER** modify locked datums. The Rev D socket (Ø 4.10 × 13.0), stem (Ø 4.00 × 14.0 D-profile, 5.0 ball-head, 3.20 groove), comb silhouette (32.0 × 6.7), and M-cutout (36.0 × 18.0) are system constants. If an override touches these, Spec Guard raises `SpecGuardError`. Do not route around it.
2. **NEVER** invent a new connector architecture. Rev D is **ball-stud + spring-loaded cross-detent with D-profile anti-rotation**. Bayonet, collet, magnetic, dovetail — all explicitly ruled out.
3. **NEVER** export a STEP for a failed variant. `export_release_pack` refuses; you do not force it.
4. **NEVER** execute bash or Python to edit CAD files outside the MCP tool surface.
5. **NEVER** claim a variant is manufacturing-ready without: (a) passing the rulepack AND (b) stating that physical prototyping is still required.
6. **NEVER** "average" conflicting numbers. Source precedence: Rev D master spec → render intent → new STL measurements → 2026 pro benchmarks.
7. **NEVER** edit `agent/policies/locked_datums.json` or `pass_fail_rules.json` yourself. Flag needed changes in a report.
8. **NEVER** use models other than the three listed in §0.

## 2. STACK (LOCKED)

- **Primary CAD backend:** CadQuery 2.5.2+ (Python / OpenCascade / OCP)
- **Fallback backend:** build123d (only when CadQuery cannot express a geometry)
- **Spec validation:** Pydantic 2.x
- **MCP transport:** stdio locally; streamable-http for remote Manager Agent
- **Density constants:** PPS-CF40 = 1.40e-3 g/mm³; 316L = 7.98e-3 g/mm³

## 3. MCP TOOL SURFACE (the only CAD actions you can take)

| Tool | Call when |
|---|---|
| `generate_connector_variant` | Build one part for one variant_id with overrides |
| `measure_geometry` | Read measurements from a generated variant |
| `validate_connector_rules` | Apply the rulepack to a metrics file |
| `compare_variants` | Rank a batch |
| `export_release_pack` | Zip a passing variant for hand-off |

**Resources** (read-only): `spec://taylkomb/rev-d`, `policy://taylkomb/locked-datums`.

## 4. STANDARD OPERATING PROCEDURE (LOCKED — execute in order, no branching)

### Step 1 — Orient
1. Read `specs/taylkomb_revD_master.json`.
2. Read `agent/policies/locked_datums.json` and `agent/policies/pass_fail_rules.json`.
3. Read the active sweep file under `specs/variant_sweeps/`.
4. Confirm `pytest -q` passes. If it fails, STOP and report.

### Step 2 — Plan
Produce a plan block containing:
- `variant_id` naming convention: `{sweep_tag}_{part_short}_{seq}` (e.g. `sweepA_round_01`).
- Part order: `main_comb → wide_comb → narrow_comb → round_handle → flat_handle → double_handle`.
- Overrides per part, drawn from the sweep file only.
- One-line rationale per override, tied to Rev D §.

### Step 3 — Generate
For each part, call:
```json
{
  "spec_path": "specs/taylkomb_revD_master.json",
  "variant_id": "<variant_id>",
  "part_name": "<part>",
  "backend": "cadquery",
  "overrides": { ... },
  "output_formats": ["step", "stl"]
}
```

### Step 4 — Measure
For each generated part, call:
```json
{
  "model_path": "<exports path from Step 3>",
  "checks": ["bounding_box", "mass_properties", "clearance_map", "seam_step", "tip_diameter", "fork_width", "stem_diameter", "socket_diameter", "insertion_force_est", "retention_force_est"]
}
```

### Step 5 — Validate
Call `validate_connector_rules` with `metrics_path` + `part_name`.
- `passed=true` → continue.
- `passed=false` → record failures, do NOT export release for that variant, move on.

### Step 6 — Compare
Once the whole sweep is built, call `compare_variants` with every record. Output the ranked list. Do not pick a winner if the top-ranked variant has any failure.

### Step 7 — Release
For each variant that passed Step 5, call:
```json
{
  "variant_id": "<variant_id>",
  "include": ["step", "stl", "source_py", "preview_png", "report_md", "json_metrics"]
}
```

### Step 8 — Summary
Write `data/reports/<sweep_tag>_summary.md` containing: plan, ranked list, release archive paths, "Human decision required" section for WARN-level issues, and a change-log entry (date, sweep tag, spec revision, variants generated, variants released).

## 5. REPORT CONVENTIONS (LOCKED)

- GitHub-flavored Markdown.
- All measurements mm, masses g, forces N.
- ISO 8601 dates (`YYYY-MM-DD`).
- Never quote code you did not just run; reference file paths.

## 6. IF YOU ARE STUCK (LOCKED)

1. Re-read spec and rulepack.
2. Trace the failing rule to its Rev D section in `docs/REV_D_PLAN.md`.
3. If genuinely ambiguous (e.g., "assembled length still over target for every feasible config"), STOP, write `data/reports/decision_request_<ts>.md` with options, and wait for human input. **Do not guess.**

---

# APPENDICES — DROP-IN CODE (copy into the repo as-is)

## Appendix A — One-time setup commands

```bash
# 1. Clone or stand up the scaffold
#    (Assumes you've already unzipped taylkomb-cad-agent-scaffold.zip)
cd taylkomb-cad-agent

# 2. Python env
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
pip install cadquery build123d trimesh claude-agent-sdk

# 3. Claude Code CLI (Node)
npm i -g @anthropic-ai/claude-code

# 4. Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...

# 5. Verify tests pass
pytest -q

# 6. Launch Claude Code with this CLAUDE.md auto-loaded
claude
```

## Appendix B — `.mcp.json` (repo root — verify or create)

```json
{
  "mcpServers": {
    "taylkomb-cad": {
      "command": "${PWD}/.venv/bin/python",
      "args": ["-m", "taylkomb_mcp.server", "--transport", "stdio"],
      "env": {
        "PYTHONPATH": "${PWD}/src",
        "TAYLKOMB_PROJECT_ROOT": "${PWD}",
        "TAYLKOMB_DATA_DIR": "${PWD}/data",
        "TAYLKOMB_DEFAULT_SPEC": "${PWD}/specs/taylkomb_revD_master.json"
      }
    }
  }
}
```

## Appendix C — Rev D master spec (`specs/taylkomb_revD_master.json`)

```json
{
  "project": "TAYLKOMB",
  "revision": "RevD_vertical_ball_stud",
  "units": "mm",
  "architecture": "vertical_ball_stud_cross_detent",
  "locked_datums": {
    "comb_silhouette_mm": { "width": 32.0, "thickness": 6.7 },
    "m_cutout_mm":        { "peak_to_peak": 36.0, "depth_from_spine": 18.0 },
    "socket_mm":          { "diameter": 4.10, "depth": 13.0, "clearance_per_side": 0.05 },
    "stem_mm":            { "diameter": 4.00, "length": 14.00, "ball_head_diameter": 5.00, "groove_diameter": 3.20, "groove_length": 1.00, "groove_offset_below_ball": 0.40, "d_profile_chord": 3.20 },
    "ball_plunger":       { "ball_diameter": 3.00, "spring_force_N_min": 8.0, "spring_force_N_max": 12.0 },
    "release_button_mm":  { "diameter": 6.00, "travel": 0.80, "protrusion_rest": 0.30 },
    "seam_step_max_mm":   0.10
  },
  "materials": {
    "comb_heads":  { "primary": "PPS-CF40" },
    "stems":       { "primary": "316L_stainless" },
    "handles":     { "primary": "316L_stainless_solid" }
  },
  "connector_forces_N": {
    "insertion_target":  [10, 15],
    "retention_target":  [30, 40],
    "release_target":    [1, 2],
    "cycle_life_min":    15000
  },
  "part_targets": {
    "main_comb":     { "oal_mm_target": 202.0, "oal_mm_range": [198, 205], "tooth_pattern": "mixed_fine_wide_plus_pick" },
    "wide_comb":     { "oal_mm_target": 178.0, "tooth_pitch_mm_target": 5.0, "tooth_count": 24 },
    "narrow_comb":   { "oal_mm_target": 178.0, "tooth_pitch_mm_target": 2.0, "tooth_count": 60 },
    "round_handle":  { "oal_mm_target": 158.0, "tail_length_mm": 130.0, "tip_diameter_mm_target": 2.3, "tip_diameter_mm_range": [1.8, 2.5] },
    "flat_handle":   { "oal_mm_target": 165.0, "cross_section_mm": [10.0, 5.0] },
    "double_handle": { "oal_mm_target": 158.0, "fork_outer_width_mm": 18.0, "fork_length_mm": 125.0, "fork_root_fillet_mm": 1.5 }
  },
  "assembly_targets": {
    "assembled_length_mm_range": [340, 380],
    "assembled_length_mm_reject_below": 320,
    "assembled_length_mm_reject_above": 410,
    "assembled_weight_g_target_range": [26, 46],
    "assembled_weight_g_max": 56
  },
  "rules": {
    "allow_changes_to_locked_datums": false,
    "require_step_export": true,
    "require_measurement_report": true,
    "reject_if_seam_step_gt_mm": 0.10,
    "reject_if_clearance_outside_range": true,
    "reject_if_tip_diameter_outside_range": true,
    "reject_if_insertion_force_outside_range": true,
    "reject_if_retention_force_outside_range": true,
    "reject_if_stem_or_socket_dims_out_of_tolerance": true
  }
}
```

## Appendix D — `agent/policies/locked_datums.json` (replace existing)

```json
{
  "comb_silhouette_mm": { "width": 32.0, "thickness": 6.7 },
  "m_cutout_mm":        { "peak_to_peak": 36.0, "depth_from_spine": 18.0 },
  "socket_mm":          { "diameter": 4.10, "depth": 13.0 },
  "stem_mm":            { "diameter": 4.00, "length": 14.00, "ball_head_diameter": 5.00, "groove_diameter": 3.20, "d_profile_chord": 3.20 },
  "seam_step_max_mm":   0.10,
  "allow_changes": false
}
```

## Appendix E — `agent/policies/pass_fail_rules.json` (replace existing)

```json
{
  "step_export_required": true,
  "seam_step_max_mm": 0.10,
  "stem_diameter_mm_tolerance": [3.97, 4.03],
  "socket_diameter_mm_tolerance": [4.07, 4.13],
  "ball_head_diameter_mm_tolerance": [4.95, 5.05],
  "d_profile_chord_mm_tolerance": [3.15, 3.25],
  "insertion_force_N_range": [10, 15],
  "retention_force_N_range": [30, 40],
  "release_force_N_range": [1, 2],
  "round_handle_tip_diameter_mm": [1.8, 2.5],
  "double_handle_fork_outer_width_mm_min": 16.0,
  "cycle_life_target_min": 15000,
  "assembled_length_mm_warn_below": 340,
  "assembled_length_mm_warn_above": 380,
  "assembled_length_mm_reject_below": 320,
  "assembled_length_mm_reject_above": 410,
  "assembled_weight_g_max": 56
}
```

## Appendix F — Rev D locking module code (`src/taylkomb_mcp/cad/locking_module.py`)

Create this new file — replaces the old `connector_common.py` dovetail logic for Rev D.

```python
"""Rev D — vertical ball-stud + cross-detent locking module.

The canonical socket (on Main Comb only) and stem (on the 5 driver parts) are
generated from this module so every part inherits an identical interface.
"""
from __future__ import annotations

import cadquery as cq


# ── Locked Rev D dimensions ────────────────────────────────────────────────
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

CROSS_BORE_DIAMETER_MM = 3.00   # for ball plunger
RELEASE_BUTTON_DIAMETER_MM = 6.00
RELEASE_BUTTON_TRAVEL_MM = 0.80


def build_driver_stem() -> cq.Workplane:
    """Build the male stem (used on Wide, Narrow, Round, Flat, Double)."""
    # 1. Base cylinder
    stem = (
        cq.Workplane("XY")
        .cylinder(STEM_LENGTH_MM, STEM_DIAMETER_MM / 2.0)
    )
    # 2. Add ball-head at top
    ball = (
        cq.Workplane("XY")
        .workplane(offset=STEM_LENGTH_MM / 2.0)
        .sphere(STEM_BALL_HEAD_DIAMETER_MM / 2.0)
    )
    stem = stem.union(ball)

    # 3. Cut retention groove just below ball
    groove_z = (STEM_LENGTH_MM / 2.0) - (STEM_BALL_HEAD_DIAMETER_MM / 2.0) - STEM_GROOVE_OFFSET_FROM_BALL_MM - STEM_GROOVE_LENGTH_MM / 2.0
    groove = (
        cq.Workplane("XY")
        .workplane(offset=groove_z)
        .cylinder(STEM_GROOVE_LENGTH_MM, STEM_DIAMETER_MM / 2.0)
    )
    groove_inner = (
        cq.Workplane("XY")
        .workplane(offset=groove_z)
        .cylinder(STEM_GROOVE_LENGTH_MM, STEM_GROOVE_DIAMETER_MM / 2.0)
    )
    stem = stem.cut(groove.cut(groove_inner))

    # 4. D-profile: flatten one side to the locked chord
    chord_offset = STEM_D_CHORD_MM - (STEM_DIAMETER_MM / 2.0)  # negative value
    cutter = (
        cq.Workplane("XY")
        .box(STEM_DIAMETER_MM * 2, STEM_DIAMETER_MM * 2, STEM_LENGTH_MM + 2)
        .translate((0, -STEM_DIAMETER_MM - chord_offset, 0))
    )
    stem = stem.cut(cutter)
    return stem


def build_receiver_socket_features(host: cq.Workplane, socket_center: tuple[float, float, float]) -> cq.Workplane:
    """Cut a Rev D socket into `host` at `socket_center` (insertion axis +Z)."""
    cx, cy, cz = socket_center
    # Main bore
    bore = (
        cq.Workplane("XY")
        .workplane(offset=cz + SOCKET_DEPTH_MM / 2.0)
        .cylinder(SOCKET_DEPTH_MM, SOCKET_DIAMETER_MM / 2.0)
        .translate((cx, cy, 0))
    )
    host = host.cut(bore)

    # Lead-in chamfer at mouth (top, i.e. −Z face if inserting from below)
    # For simplicity, represent as a cone cut 0.8 mm long at 30°
    chamfer_r1 = SOCKET_DIAMETER_MM / 2.0 + SOCKET_LEADIN_CHAMFER_MM * 0.577  # tan(30°)
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

    # Cross-bore for ball plunger (perpendicular to socket axis, along X)
    cross_bore = (
        cq.Workplane("YZ")
        .workplane(offset=CROSS_BORE_DIAMETER_MM * 3)  # extends through comb thickness
        .cylinder(CROSS_BORE_DIAMETER_MM * 6, CROSS_BORE_DIAMETER_MM / 2.0)
        .translate((cx, cy, cz + SOCKET_DEPTH_MM - STEM_GROOVE_OFFSET_FROM_BALL_MM - STEM_GROOVE_LENGTH_MM / 2.0 - STEM_BALL_HEAD_DIAMETER_MM / 2.0))
    )
    host = host.cut(cross_bore)

    # Release-button relief on one face
    button = (
        cq.Workplane("YZ")
        .workplane(offset=CONNECTOR_BLOCK_W_MM / 2.0)
        .cylinder(RELEASE_BUTTON_TRAVEL_MM * 2, RELEASE_BUTTON_DIAMETER_MM / 2.0)
        .translate((cx, cy, cz + SOCKET_DEPTH_MM - STEM_GROOVE_OFFSET_FROM_BALL_MM - STEM_GROOVE_LENGTH_MM / 2.0 - STEM_BALL_HEAD_DIAMETER_MM / 2.0))
    )
    host = host.cut(button)

    return host


def build_driver_connector_block() -> cq.Workplane:
    """The small block at the base of the stem on every driver part."""
    return (
        cq.Workplane("XY")
        .box(CONNECTOR_BLOCK_W_MM, CONNECTOR_BLOCK_H_MM, CONNECTOR_BLOCK_D_MM)
        .edges(">Z")
        .chamfer(0.5)   # hair-shed chamfer
    )
```

## Appendix G — Shared comb blank (`src/taylkomb_mcp/cad/comb_blank.py`)

```python
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
    # 1. Flat plate
    blank = (
        cq.Workplane("XY")
        .box(oal_mm, SPINE_WIDTH_MM, BODY_THICKNESS_MM)
    )

    # 2. M-cutout on the top edge (spine face, +Y side)
    # Represent as two triangular notches forming an M
    m_cx = 0.0
    m_top_y = SPINE_WIDTH_MM / 2.0
    m_valley_y = m_top_y - M_DEPTH_MM
    peak_half = M_PEAK_TO_PEAK_MM / 2.0
    # Left notch: triangle from (m_cx - peak_half, m_top_y) down to (m_cx, m_valley_y)
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
```

## Appendix H — Six part generators (`src/taylkomb_mcp/cad/parts.py` — replace the existing file)

```python
"""Rev D part generators. Compose comb_blank + locking_module + part-specific features."""
from __future__ import annotations

from typing import Any

import cadquery as cq

from taylkomb_mcp.cad.comb_blank import BODY_THICKNESS_MM, SPINE_WIDTH_MM, build_comb_blank
from taylkomb_mcp.cad.locking_module import (
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

    # Cut socket in center of M-valley
    socket_center = (0.0, SPINE_WIDTH_MM / 2.0 - 18.0, 0.0)
    blank = build_receiver_socket_features(blank, socket_center)

    # Stamp tooth field: mixed fine-left / wide-right + pick tip on left
    blank = _stamp_mixed_tooth_field(blank, oal)
    return blank


def build_wide_comb(spec, overrides: dict[str, Any]) -> cq.Workplane:
    oal = overrides.get("oal_mm", spec.part_targets["wide_comb"].oal_mm_target)
    pitch = overrides.get("tooth_pitch_mm", spec.part_targets["wide_comb"].tooth_pitch_mm_target or 5.0)
    blank = build_comb_blank(oal)
    blank = _stamp_uniform_tooth_field(blank, oal, pitch)
    blank = _attach_stem_down(blank, oal)
    return blank


def build_narrow_comb(spec, overrides: dict[str, Any]) -> cq.Workplane:
    oal = overrides.get("oal_mm", spec.part_targets["narrow_comb"].oal_mm_target)
    pitch = overrides.get("tooth_pitch_mm", spec.part_targets["narrow_comb"].tooth_pitch_mm_target or 2.0)
    blank = build_comb_blank(oal)
    blank = _stamp_uniform_tooth_field(blank, oal, pitch)
    blank = _attach_stem_down(blank, oal)
    return blank


def build_round_handle(spec, overrides: dict[str, Any]) -> cq.Workplane:
    oal = overrides.get("oal_mm", spec.part_targets["round_handle"].oal_mm_target)
    tip_d = overrides.get("tip_diameter_mm", spec.part_targets["round_handle"].tip_diameter_mm_target)
    # Taper from 10x5 rect at top to round Ø tip_d at bottom
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
    body = body.union(build_driver_stem().translate((0, 0, 5.0 + STEM_LENGTH_MM / 2.0)))
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
    body = body.union(build_driver_connector_block().translate((0, 0, tail_len / 2.0 + 2.5)))
    body = body.union(build_driver_stem().translate((0, 0, tail_len / 2.0 + 5.0 + STEM_LENGTH_MM / 2.0)))
    return body


def build_double_handle(spec, overrides: dict[str, Any]) -> cq.Workplane:
    oal = overrides.get("oal_mm", spec.part_targets["double_handle"].oal_mm_target)
    outer_w = overrides.get("fork_outer_width_mm", spec.part_targets["double_handle"].outer_width_mm_target or 18.0)
    fork_len = overrides.get("fork_length_mm", spec.part_targets["double_handle"].fork_length_mm_target or 125.0)
    fork_fillet = spec.part_targets["double_handle"].fork_root_fillet_mm_target or 1.5

    # Prong cross-section 5 x 9 mm, gap between prongs = outer_w - 2*5
    prong_thickness = 5.0
    prong_depth = 9.0
    gap = outer_w - 2 * prong_thickness

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
    yoke = (
        cq.Workplane("XY")
        .box(outer_w, prong_depth, 5.0)
        .edges("|Z")
        .fillet(fork_fillet)
    )
    body = yoke.union(left_prong).union(right_prong)
    body = body.union(build_driver_connector_block().translate((0, 0, 2.5 + 2.5)))
    body = body.union(build_driver_stem().translate((0, 0, 5.0 + STEM_LENGTH_MM / 2.0)))
    return body


# ── helpers ────────────────────────────────────────────────────────────────
def _stamp_uniform_tooth_field(blank: cq.Workplane, oal: float, pitch: float) -> cq.Workplane:
    tooth_field_len = oal * 0.78
    n_teeth = int(tooth_field_len // pitch)
    start_x = -tooth_field_len / 2.0 + pitch / 2.0
    for i in range(n_teeth):
        x = start_x + i * pitch
        slot = (
            cq.Workplane("XY")
            .box(pitch * 0.45, 20.0, BODY_THICKNESS_MM + 1)
            .translate((x, -SPINE_WIDTH_MM / 2.0 + 3.0, 0))
        )
        blank = blank.cut(slot)
    return blank


def _stamp_mixed_tooth_field(blank: cq.Workplane, oal: float) -> cq.Workplane:
    # Left half = fine pitch 2.0, right half = wide pitch 5.0, plus pick tip on left
    half = oal / 2.0
    blank = _stamp_uniform_tooth_field_partial(blank, -half + 10, -5, 2.0)
    blank = _stamp_uniform_tooth_field_partial(blank, 5, half - 10, 5.0)
    # Pick tip (small spike on left extremity) — leave as extension of leftmost tooth
    return blank


def _stamp_uniform_tooth_field_partial(blank: cq.Workplane, x_start: float, x_end: float, pitch: float) -> cq.Workplane:
    length = x_end - x_start
    n_teeth = int(length // pitch)
    for i in range(n_teeth):
        x = x_start + pitch / 2.0 + i * pitch
        slot = (
            cq.Workplane("XY")
            .box(pitch * 0.45, 20.0, BODY_THICKNESS_MM + 1)
            .translate((x, -SPINE_WIDTH_MM / 2.0 + 3.0, 0))
        )
        blank = blank.cut(slot)
    return blank


def _attach_stem_down(blank: cq.Workplane, oal: float) -> cq.Workplane:
    """Attach the driver stem + connector block at the bottom edge of a comb body."""
    block = build_driver_connector_block().translate((-oal / 2.0 + 20.0, -SPINE_WIDTH_MM / 2.0 - 2.5, 0))
    stem = build_driver_stem().translate((-oal / 2.0 + 20.0, -SPINE_WIDTH_MM / 2.0 - 5.0 - STEM_LENGTH_MM / 2.0, 0))
    return blank.union(block).union(stem)


def build_part(part_name: str, spec, overrides: dict[str, Any]) -> cq.Workplane:
    dispatch = {
        "main_comb":    build_main_comb,
        "wide_comb":    build_wide_comb,
        "narrow_comb":  build_narrow_comb,
        "round_handle": build_round_handle,
        "flat_handle":  build_flat_handle,
        "double_handle": build_double_handle,
    }
    if part_name not in dispatch:
        raise ValueError(f"Unknown part_name: {part_name}")
    return dispatch[part_name](spec, overrides)
```

## Appendix I — Spec Guard (`src/taylkomb_mcp/spec_guard.py`)

```python
"""Spec Guard — refuses overrides that touch locked datums. Called first in every generate op."""
from __future__ import annotations

LOCKED_KEYS = {
    "comb_silhouette_mm",
    "m_cutout_mm",
    "socket_mm",
    "stem_mm",
    "ball_plunger",
    "release_button_mm",
    "seam_step_max_mm",
    # nested locked keys that might appear in overrides
    "socket_diameter_mm",
    "stem_diameter_mm",
    "ball_head_diameter_mm",
    "d_profile_chord_mm",
}


class SpecGuardError(Exception):
    pass


def assert_overrides_safe(overrides: dict) -> None:
    if not overrides:
        return
    bad = sorted(k for k in overrides if k in LOCKED_KEYS)
    if bad:
        raise SpecGuardError(
            f"Overrides attempted to modify locked datums: {bad}. "
            f"Edit agent/policies/locked_datums.json (human-only) to change."
        )
```

Wire it into `server_logic.generate_connector_variant_logic` as the first call after the spec is loaded:
```python
from taylkomb_mcp.spec_guard import assert_overrides_safe
...
def generate_connector_variant_logic(...):
    spec = load_spec(spec_path)
    overrides = overrides or {}
    assert_overrides_safe(overrides)       # ← ADD THIS LINE
    ...
```

## Appendix J — Skill: DFM Reviewer (`agent/skills/dfm_reviewer.md`)

```markdown
# DFM Reviewer (skill) — Rev D

You are a Design-for-Manufacturing reviewer for TAYLKOMB. You receive a variant's
`metrics.json` and `validation.json`. Model: claude-sonnet-4-6.

Return a Markdown block with:

1. **Green flags** — what manufactures cleanly
   • PPS-CF40 walls ≥ 1.2 mm
   • fillets ≥ 0.8 mm
   • draft ≥ 0.5°
   • socket bore Ø 4.10 ± 0.03
   • stem Ø 4.00 ± 0.03

2. **Yellow flags** — risky but within tolerance
   • seam step 0.06–0.10 mm
   • fillets 0.5–0.8 mm
   • insertion force 14–15 N (near upper bound)

3. **Red flags** — will fail
   • wall < 1.0 mm
   • fillet < 0.5 mm
   • sharp internal corners
   • seam step > 0.10 mm
   • stem/socket out of tolerance band
   • retention force < 30 N (detent too soft)

4. **Specific recommended changes** in spec-override JSON form.

Never invent numbers. Source: Rev D master spec + Rev D pass_fail_rules.json.
```

## Appendix K — Skills: Spec Guard, Connector Synthesizer, Geometry Validator, Artifact Packager

Already exist in the scaffold at `agent/skills/`. Update each to reference **Rev D** architecture instead of Rev C.

Replace `agent/skills/connector_synthesizer.md`:
```markdown
# Connector Synthesizer (skill) — Rev D

Generate only vertical ball-stud + cross-detent connector variants within the allowed sweep bands.

Allowed overrides:
- `clearance_per_side_mm ∈ [0.03, 0.07]`  (tight → loose)
- `insertion_force_N ∈ [10, 15]`
- `retention_force_N ∈ [30, 40]`

Never propose: dovetail, bayonet, collet, magnetic, or any new architecture.
Always call `assert_overrides_safe` before generation.
```

## Appendix L — Sweeps (`specs/variant_sweeps/sweep_{A,B,C}.json`)

```json
{
  "description": "Rev D sweep A — tight fit, nominal retention",
  "variants": [
    { "variant_id": "A_main_01",   "part_name": "main_comb",    "overrides": {} },
    { "variant_id": "A_wide_01",   "part_name": "wide_comb",    "overrides": {} },
    { "variant_id": "A_narrow_01", "part_name": "narrow_comb",  "overrides": {} },
    { "variant_id": "A_round_01",  "part_name": "round_handle", "overrides": { "tip_diameter_mm": 2.1 } },
    { "variant_id": "A_flat_01",   "part_name": "flat_handle",  "overrides": {} },
    { "variant_id": "A_double_01", "part_name": "double_handle","overrides": { "fork_outer_width_mm": 17.0 } }
  ]
}
```

Create `sweep_B.json` (nominal) and `sweep_C.json` (loose) with `tip_diameter_mm` = 2.3 and 2.5 respectively and default everything else.

## Appendix M — First-run smoke test

After setup, run this as your very first agent task — it verifies every MCP tool and the full SOP:

```
Task: Run sweep_A end-to-end and produce a summary.

Follow the locked SOP:
1. Orient: read specs/taylkomb_revD_master.json + policies.
2. Plan: list variant_ids and overrides.
3. For each variant: generate_connector_variant → measure_geometry → validate_connector_rules.
4. compare_variants across the batch.
5. export_release_pack for each passing variant.
6. Write data/reports/A_summary.md.

If any tool errors, STOP and report the exact error. Do not retry blindly.
```

## Appendix N — Quick reference: model fallback pattern

```python
# In any call that routes to the API:
MODEL_CHAIN = ["claude-opus-4-7", "claude-opus-4-6", "claude-sonnet-4-6"]

def call_with_fallback(messages, **kwargs):
    last_err = None
    for model in MODEL_CHAIN:
        try:
            return client.messages.create(model=model, messages=messages, **kwargs)
        except anthropic.NotFoundError as e:
            last_err = e
            continue
    raise last_err
```

---

*End — Deliverable 3 (Claude Code CLAUDE.md).*
