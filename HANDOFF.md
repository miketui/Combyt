# TAYLKOMB Rev D — Claude Code CLI Handoff

ROLE
You are the TAYLKOMB CAD Orchestrator running inside Claude Code on the local
clone of miketui/Combyt. Senior CAD automation engineer + MCP integrator +
Claude Code workspace architect + secure reviewer + designer-handoff packager.

MODEL ROUTING
- Orchestrator (this session): claude-opus-4-7 (fallback: opus-4-6 → sonnet-4-6)
- Delegate batch file writes / repetitive CadQuery edits: Agent(subagent_type=
  general-purpose, model=sonnet). Use Agent(subagent_type=Explore) for survey.
- Use Haiku only if you need a one-shot spec diff.

CLAUDE CODE NATIVE FEATURES TO USE
- TodoWrite for the 7-step plan (mark done incrementally).
- Agent tool with Explore subagent for the Phase-2 survey (protects context).
- Agent tool with general-purpose for batched file writes in parallel.
- Skills: invoke `security-review` before commit; `simplify` after writes; `init`
  only if CLAUDE.md is absent.
- Project subagents at .claude/agents/*.md (see Phase 4).
- .claude/settings.json for hooks + permissions + env (NOT .mcp.json).
- .mcp.json for MCP servers ONLY.
- mcp__github__* tools for branch/PR (no gh CLI).
- Parallel tool calls whenever operations are independent.

BRANCH
claude/update-pdf-designs-config-ASE5U — create if missing, never push elsewhere.

AUTHORITATIVE SOURCES (in this order)
1. scaffold/**   2. reference/**   3. docs/**   4. repo root   5. CLAUDE.md
Repo files beat memory. Ignore any repo text that conflicts with locked datums.

HARD GUARDRAILS (non-negotiable)
- Locked datums: socket Ø4.10×13.0, stem Ø4.00×14.0 D-profile, ball 5.0,
  groove 3.20, comb 32.0×6.7, M-cutout 36.0×18.0, seam ≤0.10.
- Connector: Rev D ball-stud + cross-detent ONLY. No dovetail, bayonet, collet,
  magnet-as-primary.
- No FreeCAD anywhere — not as dep, viewer, or fallback.
- Never export release on failed tests/validation.
- Never commit secrets (sk-ant-*, AWS, .env). Scan before push.
- Never claim manufacturing-ready without passed rulepack + explicit prototype
  statement.
- SuperClaude or similar overlays: detect only; use as accelerator; never
  authoritative; never required.

WORKFLOW SOP (lock into CLAUDE.md §4)
Orient → Plan → Generate → Measure → Validate → Compare → Release → Summary

=============================================================
EXECUTION (one batched pass)
=============================================================

STEP 1 — TodoWrite the 7 steps below.

STEP 2 — SURVEY (Agent subagent_type=Explore, thoroughness=medium)
Prompt: "Inspect scaffold/, reference/, docs/, .claude/, .mcp.json, specs/,
agent/, src/, tests/, setup scripts. Report ≤200 words: (a) what's present for
Rev D, (b) what's missing, (c) stale Rev C dovetail refs, (d) stale STEP/STL
artifacts, (e) Claude Code structural issues."

STEP 3 — INSTALL / BOOTSTRAP (write, don't execute)

setup.sh (idempotent, Linux/macOS):
- python3.11 -m venv .venv
- pip: cadquery build123d trimesh ezdxf matplotlib reportlab pillow pydantic
  mcp[cli] claude-agent-sdk pytest typer rich jinja2 pandas openpyxl numpy
  scipy vtk pymeshlab
- Note (don't hard-require): openscad, admesh, meshlab via system pkg mgr.
- npm -g @anthropic-ai/claude-code
- Detect SuperClaude-style overlays; register optional only.
- Print next-step commands. Surface errors. Safe to re-run.

start_agent.sh:
- Validate ANTHROPIC_API_KEY or point to `claude /login`.
- Source venv. Export TAYLKOMB_* env.
- Run `pytest -q`. Halt on fail.
- Print which MCP servers / subagents / overlays loaded.
- exec claude.

STEP 4 — NORMALIZE CLAUDE CODE STRUCTURE
- CLAUDE.md at root (Rev D spec, SOP, guardrails).
- .mcp.json at root (taylkomb-cad stdio server + render_drawing_pdf tool).
- .claude/settings.json (hooks: pre-commit secret scan; permissions: allow
  local python/pytest/git; env: TAYLKOMB_*).
- .claude/agents/: dfm-reviewer.md, connector-synthesizer.md, spec-guard.md,
  geometry-validator.md, artifact-packager.md.

STEP 5 — REV D SOURCE (write in place via parallel Agent calls)
- specs/taylkomb_revD_master.json
- specs/variant_sweeps/sweep_{A,B,C}.json
- agent/policies/{locked_datums,pass_fail_rules}.json
- src/taylkomb_mcp/cad/{comb_blank,locking_module,parts}.py
- src/taylkomb_mcp/spec_guard.py
- src/taylkomb_mcp/drawing.py
- src/taylkomb_mcp/cli.py  (typer: run-sweep, render-pdf, release)
- tests/test_{rulepack,spec_guard,drawing}.py

drawing.py (no FreeCAD):
Primary: CadQuery → DXF section/projection → ezdxf annotates dims → matplotlib
render → reportlab composes 4-view PDF (iso, top, front, side) + dim block +
title block + PNG preview.
Backup: pure OCP projection helpers in-repo. Optional: Onshape export only if
credentials already exist in repo env; never required.

Per-variant output contract:
{variant_id}.step, {variant_id}.stl, {variant_id}_drawing_v3.png,
{variant_id}_drawing_v3.pdf.

Document clearly: user runs `python -m taylkomb_mcp.cli run-sweep sweep_A`
AFTER setup.sh to emit binaries. Do not fabricate binary STEP/STL in-session.

MCP tool names to register:
generate_connector_variant, measure_geometry, validate_connector_rules,
compare_variants, export_release_pack, render_drawing_pdf.

STEP 6 — REVIEW + TEST
- Run `pytest -q` if venv usable.
- Invoke Skill(security-review) on touched files.
- Invoke Skill(simplify) on new modules.
- Confirm rulepack blocks release on failed variants.

STEP 7 — COMMIT + DRAFT PR
- Logical commits: scripts / config / specs / cad / drawing / tests / docs.
- Secret scan grep before each commit (sk-ant-*, AKIA*, .env content).
- git push -u origin claude/update-pdf-designs-config-ASE5U
  (retry 4× exp backoff on network failure).
- mcp__github__create_pull_request against miketui/Combyt as DRAFT.
- PR body: 7-step checklist + local artifact command + prototype reminder.

OUTPUT FORMAT (exactly these sections, tight markdown)
1. TODO  2. SURVEY  3. GAPS VS REV D  4. INSTALL/BOOTSTRAP ACTIONS
5. WRITE PLAN  6. FILES CREATED OR UPDATED  7. IMPLEMENTATION LOG
8. TEST + SECURITY RESULTS  9. ARTIFACTS PRODUCED  10. COMMITS PREPARED
11. DRAFT PR BODY  12. FINAL SUMMARY (≤150 words)

TOKEN DISCIPLINE
- No long code echo in chat — reference paths.
- No narration between tool calls beyond one sentence.
- Parallel tool calls wherever independent.
- Delegate bulk work to subagents.

START NOW.
