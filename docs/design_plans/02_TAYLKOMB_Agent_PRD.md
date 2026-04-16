# TAYLKOMB CAD Agent — Product Requirements Document (Rev D)
**Locking mechanism overhaul + full parametric pipeline**
Owner: Michael David Warren Jr. / TAYLKOMB LLC
Date: April 16, 2026

---

## 1. Problem statement

TAYLKOMB's six-part modular comb system moved from Rev C (horizontal dovetail) to **Rev D (vertical ball-stud + cross-detent)** based on new render intent and current render-verified STL geometry. The old STEP files are obsolete. Manual CAD rework for every parameter sweep across 6 parts (Main Comb + 2 comb drivers + 3 handle drivers) is too slow and loses the locked-datum guarantee needed for interchangeability.

**Goal.** Build a Claude-powered CAD agent that regenerates any of the six parts from a Rev D master spec, applies controlled sweeps, validates every variant against a deterministic rulepack, and produces manufacturer-ready STEP/STL/report bundles — with zero drift on the locked socket/stem interface.

## 2. Recommended workflow (highest priority — read first)

This is the specific sequence of work I recommend you follow, with the tool for each stage.

### 2.1 Phased workflow

```
PHASE 0 — Environment stand-up (1 day)
  Tool: your laptop + VS Code + Terminal
  → Clone existing scaffold (taylkomb-cad-agent-scaffold.zip — you already have it)
  → Python venv + install CadQuery + MCP SDK + Pydantic
  → Install Claude Code CLI (Node)
  → Install claude-agent-sdk (Python) for scripted runs
  → `pytest` passes

PHASE 1 — Spec migration Rev C → Rev D (0.5 day)
  Tool: your text editor
  → Fork specs/taylkomb_revC_master.json → specs/taylkomb_revD_master.json
  → Replace connector section with Rev D socket + stem module (see Deliverable 1 §2.3)
  → Update agent/policies/locked_datums.json
  → Update agent/policies/pass_fail_rules.json with Rev D rules
  → `pytest` still passes (test_rulepack.py reads from rulepack, so it'll auto-update)

PHASE 2 — Geometry rebuild (2–3 days)
  Tool: Claude Code (local) running Opus 4.7 + Sonnet 4.6
  → Author a shared comb-silhouette-blank generator (M-cutout included)
  → Author the Rev D locking module (socket + stem families)
  → Author 6 part generators that compose blank + locking module + part-specific features
  → Each generator exports STEP + STL + PNG preview + metrics JSON
  → Rulepack validation on every output

PHASE 3 — Variant sweep + ranking (1 day)
  Tool: Claude Code with sweep files
  → Run sweep_A (tight fit), sweep_B (nominal), sweep_C (loose)
  → Compare 3 × 6 = 18 variants
  → Release pack the winners

PHASE 4 — Physical prototype (2 weeks)
  Tool: SLS-nylon print (FormLabs / i.Materialise / Shapeways) for combs,
        CNC 316L from a local machine shop for stem + handle
  → Fit check: assemble all 5 drivers into Main, cycle 100 swaps by hand
  → Measure seam step with feeler gauges
  → If fit is good, move to Phase 5

PHASE 5 — Agent Builder wiring (0.5 day, once Phase 4 lands)
  Tool: platform.claude.com Agent Builder
  → Expose local MCP server over Cloudflare Tunnel
  → Register as remote MCP in Agent Builder
  → Import Manager Agent prompt (Deliverable 4)
  → End-to-end test from web

PHASE 6 — Manufacturer handoff (ongoing)
  Tool: email / Slack + zipped release packs
  → Send STEP + STL + metrics + report to injection-mold vendor (combs)
  → Send STEP + DXF + tolerance block to Swiss CNC shop (stems + handles)
  → Coordinate ball-plunger sub-assy sourcing (Carr Lane CL-6-BPN or equivalent)
```

### 2.2 Workflow rationale — why this order

1. **Spec before geometry.** Rev D is a real architecture change. Lock the spec first or you'll rewrite geometry twice.
2. **Shared comb blank before individual parts.** Three comb heads share the silhouette; writing it once saves ~60% of the CAD time.
3. **Claude Code local before Agent Builder remote.** Debugging geometry generation works much better against local files with stdio MCP. Once it's stable, flip to remote.
4. **SLS-nylon prototypes before PPS-CF40 molds.** PPS-CF40 molding requires tooling ($30–80k). Nylon SLS ($15–30 per part) proves the locking mechanism, then you commit to tooling.
5. **Manager Agent last.** The web agent is the user-facing convenience layer. Don't build it until the Claude Code pipeline is proven.

## 3. Users

| User | Goal | Access |
|---|---|---|
| **Principal (Michael, TAYLKOMB LLC)** | Drive iteration, approve releases, edit specs. | Agent Builder (web) for day-to-day; Claude Code for deep work |
| **CAD contractor / engineer** | Generate variants, inspect STEPs, run prototypes. | Claude Code |
| **Manufacturer / MIM vendor** | Receive release packs. | Zipped bundle only |

## 4. Success metrics

| Metric | Target | Measurement |
|---|---|---|
| Spec edit → validated STEP for 1 part | ≤ 90 s | `generate_connector_variant` wall clock |
| Locked-datum drift events | 0 | Spec Guard audit every run |
| False-pass rate (CAD passes, prototype fails) | < 5% | Prototype QA vs. validator verdict |
| Variants evaluated per session | ≥ 18 (= 3 sweeps × 6 parts) | Release log |
| Full-family rebuild (6 parts) | ≤ 15 min end-to-end | CLI `run-all` timer |
| Insertion force accuracy (CAD vs. actual) | ±20% | Prototype instrumented test |

## 5. Functional requirements

- **F1** — Load Rev D master spec into validated Pydantic model.
- **F2** — Generate CadQuery solid for any of 6 parts + optional overrides.
- **F3** — Enforce locked datums (socket geometry, stem geometry, comb silhouette).
- **F4** — Export STEP + STL + 3MF + PNG preview.
- **F5** — Measure bounding box, volume, mass, insertion force est., retention force est., seam step, tip diameter, fork geometry.
- **F6** — Validate against `pass_fail_rules.json`.
- **F7** — Rank variants by pass then proximity-to-target.
- **F8** — Export release pack zip.
- **F9** — Run sweep files in batch.
- **F10** — Refuse STEP export on failed variants (unless human `--force` logged).

## 6. Non-functional requirements

- **NF1** — Determinism: same spec + overrides → byte-identical STEP.
- **NF2** — Auditability: every run emits `.md` + `.json` report.
- **NF3** — No network required for geometry (pure local).
- **NF4** — Pinned versions in `pyproject.toml`.
- **NF5** — MCP server works under both stdio (Claude Code) and streamable-http (Agent Builder).
- **NF6** — Model routing: Opus 4.7 orchestration, Sonnet 4.6 worker, Haiku 4.5 quick checks.

## 7. System architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  MANAGER AGENT  (Claude Opus 4.7, platform.claude.com)           │
│  — accepts natural-language task                                 │
│  — writes/edits the JSON spec (via human approval)               │
│  — dispatches to Claude Code worker via MCP-over-HTTP            │
│  — surfaces validation reports + release packs                   │
└──────────────────────────┬───────────────────────────────────────┘
                           │ MCP (streamable-http via Cloudflare Tunnel)
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│  CLAUDE CODE ORCHESTRATOR  (Claude Opus 4.7, local)              │
│  — reads spec + policies                                         │
│  — decides part order + sweep                                    │
│  — calls MCP tools, never bypasses them                          │
└───┬────────────────────┬─────────────────────────────┬───────────┘
    ▼                    ▼                             ▼
┌──────────┐      ┌──────────────┐           ┌────────────────────┐
│ Geometry │      │ Deterministic│           │ DFM Reviewer       │
│ Author   │      │ Validator    │           │ (Sonnet 4.6 +      │
│ (Sonnet  │      │ (Python only │           │  rulepack)         │
│  4.6 +   │      │  — no LLM)   │           │                    │
│ CadQuery)│      │              │           │                    │
└──────────┘      └──────────────┘           └────────────────────┘
    │                    │                             │
    ▼                    ▼                             ▼
    data/generated · data/exports · data/previews · data/reports
```

## 8. Recommended tool / API stack

### 8.1 Must install locally (all free unless noted)

| Tool | Purpose | Install | Cost |
|---|---|---|---:|
| Python 3.11+ | Runtime | system | — |
| Node 20+ | Claude Code CLI | system | — |
| **CadQuery 2.5.2+** | Primary code-to-CAD (BREP via OpenCascade/OCP) | `pip install cadquery` | free |
| **build123d** (optional fallback) | Secondary backend | `pip install build123d` | free |
| **MCP SDK (Python)** | MCP server runtime | `pip install "mcp[cli]"` | free |
| **Pydantic 2.x** | Spec validation | `pip install pydantic` | free |
| **Typer + Rich** | CLI + pretty output | `pip install typer rich` | free |
| **trimesh** | STL inspection | `pip install trimesh` | free |
| **claude-agent-sdk** | Python scripted orchestration | `pip install claude-agent-sdk` | free |
| **@anthropic-ai/claude-code** | Local agent harness | `npm i -g @anthropic-ai/claude-code` | free |
| **pytest** | Tests | `pip install pytest` | free |

### 8.2 Must sign up for

| Service | Purpose | Action | Cost |
|---|---|---|---:|
| **Anthropic API key** | Opus 4.7 / Sonnet 4.6 / Haiku 4.5 | console.anthropic.com → API Keys → set `ANTHROPIC_API_KEY` | usage-based |
| **Anthropic Agent Builder** | Manager Agent hosting | console.anthropic.com → Agents → New | usage-based |
| **Cloudflare Tunnel** | Expose local MCP over HTTPS | `cloudflared tunnel` or `brew install cloudflared` | free tier |
| **GitHub private repo** | Version the agent + specs | `taylkomb-cad-agent` | free |
| **FreeCAD** (free, open-source) | Human visual QA of STEPs | freecad.org | free |
| **OnShape** (free personal) | Optional 2nd QA tool | onshape.com | free personal |

### 8.3 Monthly cost estimate (dev phase)

| Line | Estimate |
|---|---:|
| Anthropic API (Opus 4.7 orch + Sonnet 4.6 worker, ~5M input + 500k output tokens/mo) | $40 – $90 |
| Cloudflare Tunnel | $0 |
| GitHub | $0 |
| Visual QA tools | $0 |
| **Total dev-phase** | **~$40 – $90 / mo** |

Production phase adds only outbound STEP transfer to manufacturers — negligible.

### 8.4 Sourcing BOM (parts you need to buy for prototypes)

| Item | Spec | Vendor | Est. price |
|---|---|---|---:|
| Ball plunger (stainless, 3 mm ball, 8–12 N) | Carr Lane CL-6-BPN or Vlier SVB51 | carrlane.com / mcmaster.com | $6–10 ea |
| 316L 4 mm round bar (for stems) | 1m length | McMaster 89095K47 or local | $8–15 |
| 316L 10 × 5 mm flat bar (for handles) | 1m length | McMaster 6528K52 or local | $15–25 |
| SLS nylon comb prototype | 3 combs, 1 each | i.Materialise / Shapeways | $60–120 |
| CNC stem + handle prototype | 3 handles, 1 each | local Swiss CNC shop | $150–400 for 3 |
| Injection-mold tool (production only) | PPS-CF40 3-cav mold | offshore mold-maker | $18k–40k |

## 9. MCP tool contracts (locked)

| Tool | Inputs | Outputs | Locked behavior |
|---|---|---|---|
| `generate_connector_variant` | `spec_path`, `variant_id`, `part_name`, `backend`, `overrides`, `output_formats` | `{exports, metrics_path, validation_path, report_path, metrics, validation}` | Spec Guard blocks overrides on locked keys |
| `measure_geometry` | `model_path`, `checks[]` | measurement dict | Pure measurement |
| `validate_connector_rules` | `spec_path`, `measurement_path`, `part_name` | `{passed, checks, failures}` | Rulepack-only |
| `compare_variants` | `variant_records[]` | `{ranked, winner}` | Pass-first sort |
| `export_release_pack` | `variant_id`, `include[]` | `{archive_path, files}` | Refuses failed variants |

## 10. Data contracts

- `specs/taylkomb_revD_master.json` — source of truth (Rev D).
- `specs/variant_sweeps/sweep_{A,B,C}.json` — controlled sweeps.
- `agent/policies/locked_datums.json` — locked-key list.
- `agent/policies/pass_fail_rules.json` — rulepack.

All files are Pydantic-validated on load.

## 11. Milestones (aligned with §2.1 workflow)

| M | Deliverable | ETA |
|---|---|---|
| M0 | Scaffold stand-up, tests pass | Day 1 |
| M1 | Rev D spec merged, rulepack updated | Day 2 |
| M2 | Shared comb blank + locking module generate + validate | Day 4 |
| M3 | All 6 parts generate + validate at Rev D targets | Day 6 |
| M4 | 3 sweeps × 6 parts = 18 variants, ranked, release-packed | Day 7 |
| M5 | SLS nylon + CNC stem prototypes, physical fit check | Day 21 |
| M6 | Agent Builder Manager Agent live on web | Day 23 |
| M7 | First manufacturer handoff (MIM or injection mold) | Day 30 |

## 12. Risks + mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM edits a locked datum | Med | High | Spec Guard + Pydantic + unit test |
| CadQuery version bump breaks geometry | Low | Med | Pin in `pyproject.toml` |
| Ball plunger wear on PPS-CF40 bore past 15k cycles | Med | High | Add optional 316L insert sleeve if wear > 0.05 mm |
| Assembled length > 380 mm rejected by user | Low | Med | Deliverable 1 §5 surfaces the decision explicitly |
| Manager Agent can't reach local MCP via Cloudflare Tunnel | Low | Low | Fallback: pure local Claude Code flow |
| PPS-CF40 molding requires 3-cav tooling = $30k+ upfront | Med | Med | Prototype in SLS nylon first; only commit tooling after fit proven |

## 13. Out of scope (v1)

- FEA / stress simulation (v2, via separate MCP tool)
- Mold-flow analysis (vendor-side in v1)
- Tooth pitch optimization beyond Rev D's locked ranges
- Any connector architecture other than Rev D ball-stud + cross-detent

---

*End — Deliverable 2 (Rev D).*
