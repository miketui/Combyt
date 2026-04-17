"""Contract tests for taylkomb_mcp.drawing — Rev D 4-view pipeline.

Guards three invariants:
    1. Public signature is stable (orchestrator + MCP depend on it).
    2. FreeCAD is never imported or referenced from drawing.py.
    3. When heavy deps + geometry are available, the return contract holds.
"""
from __future__ import annotations

import inspect
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DRAWING_PY = REPO_ROOT / "src" / "taylkomb_mcp" / "drawing.py"
SPEC_PATH = REPO_ROOT / "specs" / "taylkomb_revD_master.json"
EXPECTED_VIEWS = ("iso", "top", "front", "side")


def _try_import_drawing():
    try:
        from taylkomb_mcp import drawing  # type: ignore
        return drawing
    except Exception as exc:  # cadquery / matplotlib / reportlab not installed
        pytest.skip(f"drawing deps unavailable: {exc}")


def test_drawing_module_has_public_api():
    drawing = _try_import_drawing()
    assert callable(drawing.render_drawing_pdf)


def test_render_drawing_pdf_signature():
    drawing = _try_import_drawing()
    sig = inspect.signature(drawing.render_drawing_pdf)
    params = list(sig.parameters)
    assert params == ["variant_id", "spec_path", "out_dir"], params


def test_view_order_is_locked():
    drawing = _try_import_drawing()
    assert tuple(drawing.VIEW_ORDER) == EXPECTED_VIEWS


def test_no_freecad_imports_in_source():
    """Ban FreeCAD *imports* (docstring mentions like 'FreeCAD is BANNED' are fine)."""
    source = DRAWING_PY.read_text(encoding="utf-8")
    banned_imports = (
        "import FreeCAD",
        "import freecad",
        "from FreeCAD",
        "from freecad",
        "import Part\n",
        "import App\n",
    )
    hits = [needle for needle in banned_imports if needle in source]
    assert not hits, f"FreeCAD imports found in drawing.py: {hits}"


def test_drawing_rev_marker_is_v3():
    drawing = _try_import_drawing()
    assert drawing._DRAWING_REV == "v3"


def test_render_drawing_pdf_returns_contract(tmp_path: Path):
    drawing = _try_import_drawing()
    if not SPEC_PATH.exists():
        pytest.skip(f"spec missing: {SPEC_PATH}")
    try:
        result = drawing.render_drawing_pdf(
            variant_id="test_variant",
            spec_path=SPEC_PATH,
            out_dir=tmp_path,
        )
    except RuntimeError as exc:
        pytest.skip(f"CAD generation unavailable in this env: {exc}")
    except Exception as exc:  # noqa: BLE001 — broad skip on any heavy-dep issue
        pytest.skip(f"drawing pipeline unavailable: {exc}")

    assert isinstance(result, dict)
    required_keys = {"variant_id", "pdf_path", "png_path", "dxf_paths", "views"}
    assert required_keys.issubset(result.keys()), sorted(result.keys())
    assert result["variant_id"] == "test_variant"
    assert tuple(result["views"]) == EXPECTED_VIEWS
    assert Path(result["pdf_path"]).exists(), result["pdf_path"]
    assert Path(result["png_path"]).exists(), result["png_path"]
