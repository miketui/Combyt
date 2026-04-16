# TAYLKOMB Modular Comb System — Combyt Repository

**Patent Pending:** USPTO #19362254  
**Principal Engineer / Founder:** Michael David Warren Jr. / TAYLKOMB LLC  
**Active Revision:** Rev D — Vertical Ball-Stud + Cross-Detent Architecture

---

## Repository Structure

```
Combyt/
│
├── scaffold/                    ← 🔧 WORKING CAD PIPELINE (start here)
│   ├── .mcp.json                   MCP server config (Claude Code)
│   ├── pyproject.toml              Python package definition
│   ├── src/taylkomb_mcp/           Server + CAD generation source
│   │   ├── server.py               MCP server (stdio + HTTP)
│   │   ├── server_logic.py         Tool implementations
│   │   ├── spec_models.py          Pydantic spec models (Rev C + D)
│   │   ├── validation.py           Rulepack validation + ranking
│   │   ├── spec_guard.py           Locked datum guard
│   │   ├── cad/
│   │   │   ├── parts.py            Rev D part generators (6 parts)
│   │   │   ├── locking_module.py   Ball-stud + socket geometry
│   │   │   ├── comb_blank.py       Comb silhouette + M-cutout
│   │   │   ├── connector_common.py Shared CAD helpers
│   │   │   ├── combs.py            Phase 2 comb geometry
│   │   │   ├── handles.py          Phase 2 handle geometry
│   │   │   └── assemblies.py       Comb+handle assembly
│   │   └── ...
│   ├── specs/
│   │   ├── taylkomb_revD_master.json    ← ACTIVE SPEC
│   │   ├── taylkomb_revC_master.json    (retired, reference only)
│   │   └── variant_sweeps/
│   │       ├── sweep_A.json             Tight tolerance
│   │       ├── sweep_B.json             Nominal
│   │       └── sweep_C.json             Loose tolerance
│   ├── agent/policies/
│   │   ├── locked_datums.json       NEVER edit without human approval
│   │   └── pass_fail_rules.json     Validation thresholds
│   ├── tests/
│   └── scripts/
│
├── output/                      ← 📦 GENERATED CAD FILES (use these)
│   └── sweep_a/
│       ├── SWEEP_A_SUMMARY.md       Full results report
│       ├── step/                    ← STEP files for manufacturing / CAD import
│       ├── stl/                     ← STL files for 3D printing / preview
│       ├── reports/                 Per-variant markdown reports
│       ├── metrics/                 Measurements + validation JSONs
│       └── release_packs/           Zipped release bundles per variant
│
├── reference/                   ← 📐 ORIGINAL / LEGACY FILES
│   ├── original_cad/
│   │   ├── step/                TC-001 through TH-003 (Rev C originals)
│   │   ├── stl/                 Original mesh exports
│   │   └── pdf/                 (empty, PDFs in docs/)
│   ├── revD_samples/            Early Rev D stem + comb samples
│   └── patches/                 Scaffold + patch zip archives
│
├── docs/                        ← 📄 DOCUMENTATION
│   ├── design_plans/            Rev D plan, PRD, prompts, audits
│   ├── engineering_studies/     Size/weight/ergonomics studies
│   ├── pdfs/                    Per-part drawing PDFs
│   └── images/                  Photos, renders
│
└── README.md                    ← You are here
```

---

## Which files do I use?

### For manufacturing / CAD review
→ **`output/sweep_a/step/`** — these are the latest Rev D STEP files, validated against the rulepack.

| File | Part | OAL | Mass |
|------|------|-----|------|
| `main_comb_A_main_01.step` | Main comb (mixed teeth) | 202 mm | 13.7 g |
| `wide_comb_A_wide_01.step` | Wide-tooth comb | 178 mm | 12.5 g |
| `narrow_comb_A_narrow_01.step` | Narrow-tooth comb | 178 mm | 10.7 g |
| `round_handle_A_round_01.step` | Round tail handle | 165.5 mm | 14.5 g |
| `flat_handle_A_flat_01.step` | Flat handle | 172.5 mm | 30.7 g |
| `double_handle_A_double_01.step` | Double-prong fork | 158 mm | 49.4 g |

### For 3D printing / quick preview
→ **`output/sweep_a/stl/`** — same parts as above, triangulated mesh format.

### For comparison to original designs
→ **`reference/original_cad/step/`** — Rev C originals (TC-001, TC-002, TC-003, TH-001, TH-002, TH-003). **These are retired.**

### When you run a new sweep
New files will appear in `output/sweep_b/`, `output/sweep_c/`, etc. — same subfolder structure.

---

## Quick Start — Run the Pipeline

```bash
cd scaffold
python -m venv .venv && source .venv/bin/activate
pip install -e .

# Verify MCP server
python -m taylkomb_mcp.server --transport stdio

# Or run HTTP for remote access
python -m taylkomb_mcp.server --transport streamable-http --port 3333
```

Then use Claude Code or call the MCP tools directly.

---

## Locked Datums (DO NOT CHANGE without human approval)

| Datum | Value |
|-------|-------|
| Comb silhouette | 32.0 × 6.7 mm |
| M-cutout | 36.0 peak-to-peak × 18.0 depth |
| Socket | Ø 4.10 × 13.0 mm |
| Stem | Ø 4.00 × 14.0 mm, D-profile chord 3.20 |
| Ball head | Ø 5.00, groove Ø 3.20 |
| Seam step max | 0.10 mm |

---

## Architecture

Rev D: **Vertical ball-stud + spring cross-detent with D-profile anti-rotation.**  
Rev C (horizontal dovetail) is retired.  
Bayonet, collet, magnet variants are ruled out.
