#!/usr/bin/env bash
# ============================================================================
# TAYLKOMB Rev D — Production Bootstrap Script
# ----------------------------------------------------------------------------
# One-shot, idempotent environment setup. Installs every tool, dependency,
# skill, and workflow needed for the agent to produce CAD (STEP/STL) + drawing
# (PDF/PNG) outputs end-to-end.
#
# Usage:
#   ./setup.sh
#
# Re-run safe. Safe to pipe through CI.
# ============================================================================
set -euo pipefail

# ---------------------------------------------------------------------------
# Locate repo root (directory containing this script)
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

echo "==> TAYLKOMB Rev D bootstrap starting in ${SCRIPT_DIR}"

# ---------------------------------------------------------------------------
# 1. Python version gate (>= 3.11)
# ---------------------------------------------------------------------------
echo "==> Checking Python >= 3.11"

PYTHON_BIN=""
if command -v python3.11 >/dev/null 2>&1; then
    PYTHON_BIN="python3.11"
elif command -v python3.12 >/dev/null 2>&1; then
    PYTHON_BIN="python3.12"
elif command -v python3.13 >/dev/null 2>&1; then
    PYTHON_BIN="python3.13"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
else
    echo "ERROR: python3 not found on PATH."
    echo "       Install Python 3.11+ (e.g. via pyenv, apt, or python.org) and retry."
    exit 1
fi

PY_VERSION="$("${PYTHON_BIN}" -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')"
PY_MAJOR="$("${PYTHON_BIN}" -c 'import sys; print(sys.version_info.major)')"
PY_MINOR="$("${PYTHON_BIN}" -c 'import sys; print(sys.version_info.minor)')"

if [ "${PY_MAJOR}" -lt 3 ] || { [ "${PY_MAJOR}" -eq 3 ] && [ "${PY_MINOR}" -lt 11 ]; }; then
    echo "ERROR: Python ${PY_VERSION} detected; TAYLKOMB requires Python >= 3.11."
    echo "       Install Python 3.11+ and ensure it's on PATH (python3.11 preferred)."
    exit 1
fi

echo "    Python ${PY_VERSION} OK (${PYTHON_BIN})"

# ---------------------------------------------------------------------------
# 2. Virtual environment (idempotent)
# ---------------------------------------------------------------------------
echo "==> Provisioning .venv"

if [ ! -d ".venv" ]; then
    echo "    Creating .venv with ${PYTHON_BIN}"
    "${PYTHON_BIN}" -m venv .venv
else
    echo "    .venv already present — reusing"
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "==> Upgrading pip / setuptools / wheel"
python -m pip install --upgrade pip setuptools wheel

# ---------------------------------------------------------------------------
# 3. Package install (editable + all extras)
# ---------------------------------------------------------------------------
echo "==> Installing package in editable mode with extras [dev,mesh,sdk]"
if [ -f "pyproject.toml" ]; then
    pip install -e ".[dev,mesh,sdk]"
else
    echo "WARNING: pyproject.toml not found at repo root; skipping editable install."
fi

# ---------------------------------------------------------------------------
# 4. Explicit dependency backstop
#    (extras resolution varies across environments — pin the full set here)
# ---------------------------------------------------------------------------
echo "==> Installing explicit dependency set (CAD, mesh, reporting, agent SDK)"
pip install \
    cadquery \
    build123d \
    trimesh \
    ezdxf \
    matplotlib \
    reportlab \
    pillow \
    pydantic \
    "mcp[cli]" \
    claude-agent-sdk \
    pytest \
    pytest-cov \
    typer \
    rich \
    jinja2 \
    pandas \
    openpyxl \
    numpy \
    scipy \
    python-dotenv

# ---------------------------------------------------------------------------
# 5. Optional high-fidelity mesh tools (non-fatal)
# ---------------------------------------------------------------------------
echo "==> Installing optional mesh tools (pymeshlab, vtk) — non-fatal"
pip install pymeshlab || echo "WARNING: optional mesh tool skipped (pymeshlab)"
pip install vtk       || echo "WARNING: optional mesh tool skipped (vtk)"

# ---------------------------------------------------------------------------
# 6. Claude Code CLI (non-fatal)
# ---------------------------------------------------------------------------
echo "==> Installing Claude Code CLI (@anthropic-ai/claude-code) if npm available"
if command -v npm >/dev/null 2>&1; then
    npm install -g @anthropic-ai/claude-code \
        || echo "NOTE: global claude-code install skipped (permissions / already installed)"
else
    echo "NOTE: npm not found — skipping global Claude Code CLI install."
    echo "      Install Node.js/npm and re-run setup.sh to get the CLI."
fi

# ---------------------------------------------------------------------------
# 7. Claude Code plugins / skills / workflows (non-fatal)
# ---------------------------------------------------------------------------
echo "==> Installing Claude Code plugins (superpowers, code-review) — non-fatal"
if command -v claude >/dev/null 2>&1; then
    claude plugin install superpowers@anthropic  || echo "NOTE: superpowers plugin install skipped (registry/command variance)"
    claude plugin install code-review@anthropic  || echo "NOTE: code-review plugin install skipped (registry/command variance)"
else
    echo "NOTE: 'claude' CLI not on PATH — skipping plugin install."
    echo "      Install @anthropic-ai/claude-code and re-run to pick up plugins."
fi

# ---------------------------------------------------------------------------
# 8. Required output / data directories
# ---------------------------------------------------------------------------
echo "==> Creating required project directories"
mkdir -p \
    output/sweep_a/step \
    output/sweep_a/stl \
    output/sweep_a/drawings \
    output/sweep_a/reports \
    output/sweep_a/metrics \
    output/sweep_a/release_packs \
    data

# ---------------------------------------------------------------------------
# 9. Smoke test — import every critical library
# ---------------------------------------------------------------------------
echo "==> Smoke-testing critical imports"
python -c "import cadquery, ezdxf, matplotlib, reportlab, trimesh, pydantic; print('✓ all imports ok')"

# ---------------------------------------------------------------------------
# 10. Done
# ---------------------------------------------------------------------------
echo ""
echo "✓ TAYLKOMB Rev D environment ready. Next: source .venv/bin/activate && ./start_agent.sh"
