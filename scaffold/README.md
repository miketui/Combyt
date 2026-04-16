# Scaffold — TAYLKOMB MCP CAD Pipeline

This is the **working** Rev D scaffold. All code has been patched to support  
the ball-stud architecture and passes Sweep A (6/6 variants).

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Run MCP Server

```bash
# stdio (for Claude Code)
python -m taylkomb_mcp.server --transport stdio

# HTTP (for remote / tunnel access)
python -m taylkomb_mcp.server --transport streamable-http --port 3333
```

## Run Tests

```bash
pip install pytest
pytest tests/ -v
```

## Key Files

| File | Purpose |
|------|---------|
| `specs/taylkomb_revD_master.json` | **Active spec** — all geometry derives from this |
| `agent/policies/locked_datums.json` | Locked dimensions — human-only edits |
| `agent/policies/pass_fail_rules.json` | Validation thresholds |
| `src/taylkomb_mcp/cad/parts.py` | Rev D part generators (6 parts) |
| `src/taylkomb_mcp/cad/locking_module.py` | Ball-stud + socket CAD |
| `specs/variant_sweeps/sweep_A.json` | Tight tolerance sweep definition |
