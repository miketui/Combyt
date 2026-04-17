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
    """Raised when an override attempts to modify a locked datum."""


def assert_overrides_safe(overrides: dict) -> None:
    """Raise SpecGuardError if any override key collides with a locked datum."""
    if not overrides:
        return
    bad = sorted(k for k in overrides if k in LOCKED_KEYS)
    if bad:
        raise SpecGuardError(
            f"Overrides attempted to modify locked datums: {bad}. "
            f"Edit agent/policies/locked_datums.json (human-only) to change."
        )
