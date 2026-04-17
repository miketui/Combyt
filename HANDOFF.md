# TAYLKOMB Rev D — CAD Product Designer Handoff

> **For:** the CAD product designer inheriting the Rev D ball-stud + cross-detent connector family.
> **From:** the orchestrator that generated the geometry, drawings, and release packs.
> **Status:** Rev D is frozen. This document describes what was built, how to regenerate it, and what changes (if any) are permitted.

---

## 1. Product Overview

**Part family:** TAYLKOMB decorative-comb hair accessory connector system.

**Connector archetype:** Rev D **ball-stud + cross-detent** — vertical ball-stud locks into a socket with a cross-pin cross-detent. **No other archetypes are permitted.** Dovetail, bayonet, collet, and magnet-as-primary retention are explicitly **blocked** in the validator (`agent/policies/pass_fail_rules.json`). Magnets may serve as secondary alignment aids only if the spec flag enables them.

**IP status:**
- **Patent Pending — USPTO Application #19362254**
- Inventor / Principal Engineer: **Michael David Warren Jr.**
- Assignee: **TAYLKOMB LLC**

Every PDF drawing carries this notice in the title block. **Do not remove or reword it** in any regenerated artifact.

---

## 2. Locked Datums (mm)

These dimensions are canonical. They live in `specs/taylkomb_revD_master.json` and are enforced by `validate_connector_rules`. **If a variant fails, fix the variant — never tune the datum to pass.**

| Feature | Dimension |
|---|---|
| Socket bore | Ø 4.10 × 13.0 |
| Stem (D-profile) | Ø 4.00 × 14.0 |
| Ball | Ø 5.0 |
| Groove | 3.20 |
| Comb body | 32.0 × 6.7 |
| M-cutout | 36.0 × 18.0 |
| Max seam tolerance | ≤ 0.10 |

**Tolerances / fits:**
- Socket-to-stem radial clearance: 0.05 mm per side (0.10 diametral), spec-driven in `connector.clearance_per_side_mm_range`.
- Engagement length target: `connector.engagement_length_mm_target` (see spec file).
- Seam step (part-to-part mating): ≤ 0.10 mm across every seam in the four-view drawing.

**Materials (informational — source of truth is the spec):**
- Combs: **PPS-CF40** (40% carbon-fiber PPS), density 1.42 g/cm³.
- Handles / metal inserts: **316L stainless**, density 7.98 g/cm³.

---

## 3. Drawing Package — Rev D v3

Every released variant carries **four** artifacts under `data/<variant_id>/`:

| Extension | Contents |
|---|---|
| `{variant_id}.step` | CadQuery-exported solid (import to SolidWorks, Fusion, Inventor, NX, Creo). |
| `{variant_id}.stl` | Mesh export for visualization, renderers, and SLA/FDM printing. |
| `{variant_id}_drawing_v3.png` | Matplotlib raster preview of the sheet (for PRs, Slack, Notion). |
| `{variant_id}_drawing_v3.pdf` | Reportlab-composed PDF — **the canonical drawing for vendors and fabricators.** |

### 3.1 PDF Sheet Layout

The `_drawing_v3.pdf` sheet contains, top-to-bottom:

1. **Four-view layout** (locked order, do not re-order):
   - **ISO** (top-left) — isometric pictorial, no dimensions
   - **TOP** (top-right) — plan projection, outer width + M-cutout width dims
   - **FRONT** (bottom-left) — elevation, stem height + ball position + groove
   - **SIDE** (bottom-right) — profile, comb depth + socket bore depth
2. **Dimensioned datum table** (center band) — reproduces §2 with the measured values for the variant, plus pass/fail flags from `validate_connector_rules`.
3. **Title block** (footer):
   - Revision marker: `v3` (always — this is Rev D, drawing revision 3)
   - Patent notice: `Patent Pending — USPTO App #19362254`
   - Principal Engineer signature line: `Michael David Warren Jr.`
   - Assignee: `TAYLKOMB LLC`
   - Generation timestamp + variant ID

### 3.2 Drawing Pipeline (locked)

```
CadQuery (solid model)
   → DXF           (2D projection, 4 views)
   → ezdxf         (DXF parsing + layout annotations)
   → matplotlib    (vector rendering → PNG preview)
   → reportlab     (PDF composition with title block)
```

**No substitutions.** No PIL-only raster paths for the PDF. No headless FreeCAD, OpenSCAD, or Fusion shell-outs. The `test_drawing.py` suite guards this with an explicit FreeCAD-import ban.

### 3.3 What the Designer May Change

Inside the drawing/rendering layer (`src/taylkomb_mcp/drawing.py`):

| Change | Allowed? | Notes |
|---|---|---|
| Title-block typography, logo, layout | ✅ | As long as the patent notice + revision marker + signature line remain readable. |
| View scale, margins, grid density | ✅ | Per-sheet tuning fine. |
| Adding a BOM / parts-list band | ✅ | Extend reportlab flowables; don't break the 4-view grid. |
| Swapping view order (iso/top/front/side) | ❌ | Locked by `VIEW_ORDER` + tested in `test_drawing.py::test_view_order_is_locked`. |
| Changing datum values to make a variant pass | ❌ | Locked — see §2. |
| Adding FreeCAD / OpenSCAD fallback | ❌ | Banned across the project. |

---

## 4. Regenerating a Variant (End-to-End)

### 4.1 One-time setup (from a fresh clone)

```bash
cd /path/to/Combyt
./setup.sh                      # idempotent: venv + deps + data dirs + smoke test
source .venv/bin/activate
pytest -q tests/                # existing suites + drawing contract tests
```

`setup.sh` installs everything from `pyproject.toml` including `[dev,mesh,sdk]` extras (pytest, pymeshlab, vtk, claude-agent-sdk) and the drawing-pipeline pins (ezdxf, matplotlib, reportlab, pillow, trimesh).

### 4.2 Single-variant drawing

```bash
python -m taylkomb_mcp.cli render-pdf <variant_id> \
    --spec specs/taylkomb_revD_master.json \
    --out  data/<variant_id>
```

Emits `<variant_id>_drawing_v3.pdf` + `<variant_id>_drawing_v3.png` + four DXF views.

### 4.3 Single-variant geometry

```bash
python -m taylkomb_mcp.cli run-variant \
    specs/taylkomb_revD_master.json \
    main_comb \
    --variant-id my_variant_01 \
    --overrides-json '{"outer_width_mm": 32.0, "seam_step_mm": 0.08}'
```

Emits STEP + STL under `data/exports/my_variant_01/`.

### 4.4 Full sweep (generate → measure → validate → render)

```bash
python -m taylkomb_mcp.cli run-sweep specs/variant_sweeps/sweep_A.json
```

Runs the full SOP (§5) across every variant in the sweep JSON. Output: a rich table with ✓/✗ per phase + the four-artifact set per variant.

### 4.5 Release packs

```bash
python -m taylkomb_mcp.cli release sweep_a
```

Zips each variant's STEP + STL + PDF + PNG + metrics JSON into `data/reports/<variant_id>/release_<variant_id>_<timestamp>.zip`.

### 4.6 Launching the agent

```bash
./start_agent.sh                # API-key gate + venv + env + pytest + exec claude
```

Inside Claude Code, the six MCP tools (see §6) are auto-registered from `.mcp.json`.

---

## 5. Workflow SOP (8 Steps — do not reorder)

1. **Orient** — Restate the request. Confirm Rev D. Load master spec. Read prior release state.
2. **Plan** — Enumerate variants + parameter deltas vs. master. Declare expected outputs + validation criteria.
3. **Generate** — Call `generate_connector_variant` per variant. Capture STEP/STL paths.
4. **Measure** — Call `measure_geometry` per variant. Capture actual datums.
5. **Validate** — Call `validate_connector_rules`. Any FAIL blocks release.
6. **Compare** — Call `compare_variants`. Surface deltas vs. master + prior release.
7. **Release** — Call `export_release_pack` and `render_drawing_pdf`. Confirm all four artifacts per variant.
8. **Summary** — Emit a structured report: variants, measurements, validation, delta table, artifact paths, next actions.

If any step fails, **stop and report**. Do not silently retry with mutated parameters.

---

## 6. MCP Tool Inventory

The `taylkomb-cad` server (registered in `.mcp.json`) exposes exactly these six tools:

| Tool | Purpose |
|---|---|
| `generate_connector_variant` | Build a Rev D variant from parameter deltas. Returns STEP + STL paths. |
| `measure_geometry` | Extract datums from a generated solid (or its sidecar metrics JSON). |
| `validate_connector_rules` | Enforce datum lock + connector-type lock + seam tolerance. Returns PASS/FAIL per rule. |
| `compare_variants` | Rank + diff two or more variant records. |
| `export_release_pack` | Bundle STEP + STL + PDF + PNG + metrics JSON into a release zip. |
| `render_drawing_pdf` | Drive the CadQuery → DXF → ezdxf → matplotlib → reportlab pipeline. |

Read-only resources: `spec://taylkomb/rev-d`, `spec://taylkomb/rev-c` (retired), `policy://taylkomb/locked-datums`.

---

## 7. Repo Map (what lives where)

```
Combyt/
├── CLAUDE.md                              # Orchestrator system prompt (10 sections)
├── HANDOFF.md                             # ← you are here
├── setup.sh                               # idempotent bootstrap
├── start_agent.sh                         # API-key gate + venv + pytest + exec claude
├── pyproject.toml                         # deps (CadQuery, ezdxf, matplotlib, reportlab, …)
├── .mcp.json                              # taylkomb-cad stdio server registration
├── .env.example                           # ANTHROPIC_API_KEY + TAYLKOMB_* env template
├── .claude/
│   ├── settings.json                      # tool allowlist + pre-commit secret-scan hook
│   └── agents/
│       ├── cad-generator.md               # owns generate_connector_variant
│       ├── metrology.md                   # owns measure_geometry
│       ├── validator.md                   # owns validate_connector_rules
│       ├── drawing-smith.md               # owns render_drawing_pdf
│       └── release-manager.md             # owns export_release_pack + PR packaging
├── specs/
│   ├── taylkomb_revD_master.json          # CANONICAL SPEC — locked datums live here
│   ├── taylkomb_revC_master.json          # retired, reference only
│   └── variant_sweeps/
│       ├── sweep_A.json                   # first release sweep (6 variants, 6/6 PASS)
│       ├── sweep_B.json
│       └── sweep_C.json
├── agent/
│   ├── policies/
│   │   ├── locked_datums.json             # §2 machine-readable
│   │   └── pass_fail_rules.json           # connector-type lock + tolerance rules
│   └── skills/                            # reference skills (not subagents)
├── src/taylkomb_mcp/
│   ├── server.py                          # FastMCP server, registers the 6 tools
│   ├── server_logic.py                    # business logic for each tool
│   ├── cli.py                             # typer CLI: run-variant, render-pdf, release, run-sweep
│   ├── drawing.py                         # Rev D v3 drawing pipeline (440 lines, no FreeCAD)
│   ├── spec_models.py                     # pydantic models for the master spec
│   ├── spec_guard.py                      # override-safety invariants
│   ├── validation.py                      # datum + rule-pack validation
│   ├── io_utils.py                        # project_root, data_dir, ensure_dirs, timestamp
│   └── cad/                               # parts, assemblies, combs, handles, locking module
├── scripts/
│   ├── generate_phase2_demo.py            # end-to-end smoke (generates a full sweep)
│   └── claude_code_sdk_demo.py
├── tests/
│   ├── test_spec_load.py
│   ├── test_rulepack.py
│   ├── test_phase2_contracts.py
│   └── test_drawing.py                    # drawing contract + no-FreeCAD guard
├── docs/
│   └── PHASE2_NOTES.md
└── data/                                  # output root (created by setup.sh, .gitignored)
    ├── generated/<variant_id>/            # metrics JSON sidecar
    ├── exports/<variant_id>/              # STEP + STL
    ├── previews/<variant_id>/             # PNG previews
    └── reports/<variant_id>/              # PDF + release zips + markdown report
```

---

## 8. Environment Variables

Defined in `.claude/settings.json` → surfaced to every MCP + CLI invocation via `.mcp.json`:

| Variable | Purpose |
|---|---|
| `TAYLKOMB_PROJECT_ROOT` | Absolute repo root (e.g. `/home/warrenm115/Combyt`). |
| `TAYLKOMB_DATA_DIR` | Release/artifact root (defaults to `${TAYLKOMB_PROJECT_ROOT}/data`). |
| `TAYLKOMB_DEFAULT_SPEC` | Path to `specs/taylkomb_revD_master.json`. |
| `PYTHONPATH` | Must include `${TAYLKOMB_PROJECT_ROOT}/src`. |
| `ANTHROPIC_API_KEY` | Required by `start_agent.sh`. Load via env or `.env` (see `.env.example`). |

**Do not hard-code equivalents in source files.** `settings.json` + `.mcp.json` are the only source of truth for paths.

---

## 9. Change Control for the Product Designer

### Permitted without a new spec revision
- Drawing-sheet cosmetics (typography, margins, logo, BOM band) — see §3.3.
- Adding new **variant sweeps** under `specs/variant_sweeps/` that reuse locked datums.
- Adding new non-lock parameter overrides (handle clearance, seam step, engagement length) within the ranges declared in the master spec.
- Adding new MCP tool-consumer scripts under `scripts/` that call the existing six tools.

### Requires a spec revision (Rev E) + full validator update
- Any change to the locked datums in §2.
- Any new connector archetype (dovetail, bayonet, collet, magnet-primary).
- Any change to the drawing pipeline dependency chain (CadQuery → DXF → ezdxf → matplotlib → reportlab).
- Any change to the four-artifact output contract (STEP + STL + PDF + PNG).

### Never permitted
- Importing or shelling out to FreeCAD (tested in `test_drawing.py::test_no_freecad_imports_in_source`).
- Removing or reshaping the patent-pending notice.
- Auto-merging PRs. PRs ship as DRAFT; a human approves.

---

## 10. Verification Checklist (run before handing off a new sweep)

```bash
# 1. Green test suite (after setup.sh)
pytest -q tests/

# 2. No FreeCAD leaks
grep -R "import FreeCAD\|from FreeCAD\|import freecad" src/ && echo LEAK || echo clean

# 3. Four-artifact contract per variant
for v in data/exports/*/; do
  id=$(basename "$v")
  for ext in step stl; do
    ls "data/exports/$id/"*.$ext >/dev/null || echo "MISSING $id.$ext"
  done
  ls "data/reports/$id/${id}_drawing_v3.pdf" >/dev/null || echo "MISSING ${id}_drawing_v3.pdf"
  ls "data/previews/$id/${id}_drawing_v3.png" >/dev/null || echo "MISSING ${id}_drawing_v3.png"
done

# 4. Validator PASS on every variant
python -m taylkomb_mcp.cli run-sweep specs/variant_sweeps/sweep_A.json

# 5. Patent + revision marker present in every PDF
pdftotext data/reports/*/*_drawing_v3.pdf - | grep -c "19362254"
pdftotext data/reports/*/*_drawing_v3.pdf - | grep -c "v3"
```

Every check must pass before publishing a release pack.

---

## 11. First-Run Instructions (copy/paste)

```bash
cd /path/to/Combyt
./setup.sh
source .venv/bin/activate
./start_agent.sh
```

Inside Claude Code, the orchestrator loads `CLAUDE.md`, binds the six MCP tools from `.mcp.json`, and drives the 8-step SOP end-to-end. Ask it plainly: *"Run sweep A and give me the release packs."*

---

## 12. Contacts & References

- **Repo:** `miketui/Combyt` · branch `main` (merged via PR #3)
- **Principal Engineer / Inventor:** Michael David Warren Jr.
- **Assignee:** TAYLKOMB LLC
- **Patent:** USPTO Application #19362254 — Patent Pending
- **Master spec:** `specs/taylkomb_revD_master.json`
- **Canonical drawing template:** `src/taylkomb_mcp/drawing.py` (rev `v3`)
- **Rule pack:** `agent/policies/pass_fail_rules.json`
- **Orchestrator prompt:** `CLAUDE.md`

If something is unclear, read the orchestrator prompt first — it is the source of truth that supersedes this handoff.
