from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def project_root() -> Path:
    value = os.getenv("TAYLKOMB_PROJECT_ROOT")
    return Path(value).resolve() if value else Path.cwd().resolve()


def data_dir() -> Path:
    value = os.getenv("TAYLKOMB_DATA_DIR")
    if value:
        return Path(value).resolve()
    return project_root() / "data"


def ensure_dirs() -> dict[str, Path]:
    base = data_dir()
    paths = {
        "generated": base / "generated",
        "exports": base / "exports",
        "previews": base / "previews",
        "reports": base / "reports",
        "inputs": base / "inputs",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def timestamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def read_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def write_text(path: str | Path, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
