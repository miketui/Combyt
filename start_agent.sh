#!/usr/bin/env bash
# ============================================================================
# TAYLKOMB Rev D — Agent Launch Script
# ----------------------------------------------------------------------------
# Verifies environment, runs the test gate, and exec's into Claude Code so the
# CLI auto-loads CLAUDE.md, .mcp.json, and .claude/*.
#
# Usage:
#   ./start_agent.sh
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

# ---------------------------------------------------------------------------
# 1. API key gate (honor .env if present)
# ---------------------------------------------------------------------------
echo "==> Checking ANTHROPIC_API_KEY"

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    if [ -f ".env" ]; then
        echo "    ANTHROPIC_API_KEY not in environment — sourcing .env"
        set -a
        # shellcheck disable=SC1091
        source .env
        set +a
    fi
fi

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    echo "ERROR: ANTHROPIC_API_KEY is not set."
    echo "       Export it (e.g. export ANTHROPIC_API_KEY=sk-ant-...) or add it to .env"
    exit 1
fi

# ---------------------------------------------------------------------------
# 2. Activate virtualenv
# ---------------------------------------------------------------------------
echo "==> Activating .venv"

if [ ! -f ".venv/bin/activate" ]; then
    echo "ERROR: .venv not found. Run ./setup.sh first to bootstrap the environment."
    exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate

# ---------------------------------------------------------------------------
# 3. Project environment variables
# ---------------------------------------------------------------------------
echo "==> Exporting TAYLKOMB_* environment"
export TAYLKOMB_PROJECT_ROOT="$(pwd)"
export TAYLKOMB_DATA_DIR="$(pwd)/data"
export TAYLKOMB_DEFAULT_SPEC="$(pwd)/specs/taylkomb_revD_master.json"
export PYTHONPATH="$(pwd)/src:${PYTHONPATH:-}"

# ---------------------------------------------------------------------------
# 4. Test gate — do not launch agent on a broken tree
# ---------------------------------------------------------------------------
echo "==> Running test gate (pytest -q tests/)"
pytest -q tests/ || { echo "TESTS FAILED — aborting agent launch"; exit 1; }

# ---------------------------------------------------------------------------
# 5. Launch Claude Code (auto-loads CLAUDE.md, .mcp.json, .claude/*)
# ---------------------------------------------------------------------------
echo "==> Launching Claude Code"
exec claude
