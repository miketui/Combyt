# TAYLKOMB Phase 2 Files

This Phase 2 pass adds real geometry modules and assembly support to the Claude Code/MCP scaffold.

## Added in this phase

- dedicated `cad/handles.py` modules for round, flat, and double handles
- dedicated `cad/combs.py` modules for main, wide, and narrow comb bodies
- `cad/assemblies.py` to build `main_comb+handle` assemblies and compute assembly metrics
- upgraded validation for part length bands, assembly length, and estimated mass
- two new sweep files for precision and power-family exploration
- a batch demo script

## Important limits

- the tooth geometry is still a **placeholder engineering envelope**, not final production tooth math
- the release-button internals are a placeholder cavity, not a production spring/button subassembly
- assembled mating is deterministic and useful for automation, but still needs real CAD fit verification

## Suggested next phase

1. Replace placeholder tooth bands with exact GDP tooth geometry from your designer's spline/section data.
2. Add mass/balance measurement using the real material densities and center-of-mass extraction.
3. Add interference checks around the seam, button path, and detent-ball path.
4. Add export previews/renders for rapid visual QA inside Claude Code.
