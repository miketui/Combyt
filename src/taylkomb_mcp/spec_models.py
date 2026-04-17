"""Pydantic spec models — Rev C + Rev D compatible.

Rev C supplies an explicit ``connector`` object (dovetail architecture).
Rev D omits ``connector`` and stores everything inside ``locked_datums``
plus a top-level ``connector_forces_N`` block.

A ``model_validator`` synthesises a backward-compatible ``ConnectorSpec``
from Rev D datums so that downstream code (server_logic, validation,
assemblies) can keep using ``spec.connector.*`` unchanged.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ── Leaf models ──────────────────────────────────────────────────────────

class RailProfile(BaseModel):
    width: float
    height: float


class RangeSpec(BaseModel):
    min: float
    max: float


class MaterialSpec(BaseModel):
    primary: str
    wall_thickness_mm_range: list[float] | None = None


class Materials(BaseModel):
    comb_heads: MaterialSpec
    stems: MaterialSpec | None = None          # Rev D adds this
    handles: MaterialSpec


class ConnectorSpec(BaseModel):
    """Dovetail-era spec (Rev C) or synthesised shim (Rev D)."""
    dovetail_angle_deg: float = 0.0
    rail_profile_mm: RailProfile = Field(default_factory=lambda: RailProfile(width=0, height=0))
    engagement_length_mm_target: float = 14.0
    engagement_length_mm_range: list[float] = Field(default_factory=lambda: [13.0, 15.0])
    clearance_per_side_mm_range: list[float] = Field(default_factory=lambda: [0.05, 0.15])
    ball_diameter_mm: float = 3.0
    ball_protrusion_mm: float = 0.0
    detent_pocket_diameter_mm: float = 3.5
    detent_pocket_depth_mm: float = 0.8
    detent_force_N_range: list[float] = Field(default_factory=lambda: [8.0, 12.0])
    lead_in_chamfer: dict[str, float] = Field(default_factory=lambda: {"angle_deg": 30.0, "length_mm": 0.8})
    hair_shed_chamfer: dict[str, float] = Field(default_factory=lambda: {"size_mm": 0.3, "angle_deg": 45.0})
    seam_step_max_mm: float = 0.10
    cycle_life_target_min: int = 15000


class ConnectorForces(BaseModel):
    """Rev D top-level force targets."""
    insertion_target: list[float]
    retention_target: list[float]
    release_target: list[float]
    cycle_life_min: int


class PartTarget(BaseModel):
    """Flexible part-target model that accepts both Rev C and Rev D field names.

    A ``model_validator`` maps Rev D shorthand names (``tail_length_mm``,
    ``fork_outer_width_mm``, …) to the ``_target`` convention the existing
    CAD generators and validators expect.
    """
    model_config = ConfigDict(extra="allow")

    oal_mm_target: float
    oal_mm_range: list[float] | None = None

    # common target fields (some filled from RevD mapping below)
    tail_length_mm_target: float | None = None
    work_section_mm_target: float | None = None
    fork_length_mm_target: float | None = None
    outer_width_mm_target: float | None = None
    tip_diameter_mm_target: float | None = None
    tip_diameter_mm_range: list[float] | None = None
    prong_section_mm_target: dict[str, float] | None = None
    root_fillet_mm_target: float | None = None

    # Rev D extras (kept for round-trip fidelity)
    tooth_pattern: str | None = None
    tooth_pitch_mm_target: float | None = None
    tooth_count: int | None = None
    cross_section_mm: list[float] | None = None

    @model_validator(mode="before")
    @classmethod
    def _map_revd_shorthand(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        mappings = {
            "tail_length_mm":       "tail_length_mm_target",
            "fork_outer_width_mm":  "outer_width_mm_target",
            "fork_length_mm":       "fork_length_mm_target",
            "fork_root_fillet_mm":  "root_fillet_mm_target",
        }
        for src, dst in mappings.items():
            if src in data and dst not in data:
                data[dst] = data[src]
        return data


class AssemblyTargets(BaseModel):
    assembled_length_mm_range: list[float]
    assembled_length_mm_reject_below: float | None = None
    assembled_length_mm_reject_above: float | None = None
    assembled_weight_g_target_range: list[float]
    assembled_weight_g_max: float


class RulePack(BaseModel):
    allow_changes_to_locked_datums: bool = False
    require_step_export: bool = True
    require_measurement_report: bool = True
    reject_if_seam_step_gt_mm: float
    reject_if_clearance_outside_range: bool = True
    reject_if_tip_diameter_outside_range: bool = True
    # Rev D additions
    reject_if_insertion_force_outside_range: bool | None = None
    reject_if_retention_force_outside_range: bool | None = None
    reject_if_stem_or_socket_dims_out_of_tolerance: bool | None = None


# ── Root model ───────────────────────────────────────────────────────────

class TaylkombSpec(BaseModel):
    project: str
    revision: str
    units: Literal["mm"]
    architecture: str
    locked_datums: dict[str, Any]
    materials: Materials
    connector: ConnectorSpec | None = None
    connector_forces_N: ConnectorForces | None = None
    part_targets: dict[str, PartTarget]
    assembly_targets: AssemblyTargets
    rules: RulePack

    @model_validator(mode="after")
    def _synthesize_connector_from_datums(self) -> "TaylkombSpec":
        """If the spec has no explicit ``connector`` (Rev D), build one from locked datums."""
        if self.connector is not None:
            return self

        ld = self.locked_datums
        socket = ld.get("socket_mm", {})
        stem = ld.get("stem_mm", {})
        bp = ld.get("ball_plunger", {})
        forces = self.connector_forces_N

        clearance = socket.get("clearance_per_side", 0.05)
        engagement = stem.get("length", 14.0)
        ball_d = bp.get("ball_diameter", 3.0)

        self.connector = ConnectorSpec(
            dovetail_angle_deg=0.0,
            rail_profile_mm=RailProfile(
                width=stem.get("diameter", 4.0),
                height=stem.get("diameter", 4.0),
            ),
            engagement_length_mm_target=engagement,
            engagement_length_mm_range=[engagement - 1.0, engagement + 1.0],
            clearance_per_side_mm_range=[clearance, clearance * 3],
            ball_diameter_mm=ball_d,
            ball_protrusion_mm=0.0,
            detent_pocket_diameter_mm=ball_d + 0.5,
            detent_pocket_depth_mm=0.8,
            detent_force_N_range=[
                bp.get("spring_force_N_min", 8.0),
                bp.get("spring_force_N_max", 12.0),
            ],
            lead_in_chamfer={"angle_deg": 30.0, "length_mm": 0.8},
            hair_shed_chamfer={"size_mm": 0.3, "angle_deg": 45.0},
            seam_step_max_mm=ld.get("seam_step_max_mm", 0.10),
            cycle_life_target_min=forces.cycle_life_min if forces else 15000,
        )
        return self


# ── Helpers ──────────────────────────────────────────────────────────────

def load_spec(path: str | Path) -> TaylkombSpec:
    import json
    with Path(path).open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return TaylkombSpec.model_validate(raw)


def save_spec(spec: TaylkombSpec, path: str | Path) -> None:
    import json
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(spec.model_dump(mode="json"), f, indent=2)


def coerce_spec_override(base: TaylkombSpec, overrides: dict[str, Any]) -> TaylkombSpec:
    merged = base.model_dump(mode="json")
    _deep_merge(merged, overrides)
    return TaylkombSpec.model_validate(merged)


def _deep_merge(target: dict[str, Any], patch: dict[str, Any]) -> None:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _deep_merge(target[key], value)
        else:
            target[key] = value
