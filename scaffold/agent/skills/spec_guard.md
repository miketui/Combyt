# Skill — Spec Guard

Purpose:
Protect TAYLKOMB locked datums and system invariants.

Rules:
- Treat `locked_datums` as non-editable.
- Reject requests that change the connector standard unless the spec explicitly unlocks them.
- Always compare proposed overrides against the master spec before geometry generation.
