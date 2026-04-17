"""TAYLKOMB MCP Server — Rev D ball-stud architecture.

Exposes five CAD tools + two read-only resources via MCP (stdio or streamable-http).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
from mcp.server.fastmcp import FastMCP

from taylkomb_mcp.io_utils import project_root
from taylkomb_mcp.server_logic import (
    compare_variants_logic,
    export_release_pack_logic,
    generate_connector_variant_logic,
    measure_geometry_logic,
    render_drawing_pdf_logic,
    validate_connector_rules_logic,
)

app = typer.Typer(add_completion=False)


def _build_mcp(host: str = "127.0.0.1", port: int = 3333) -> FastMCP:
    """Construct the FastMCP instance with host/port baked into settings."""
    server = FastMCP(
        "TAYLKOMB CAD Agent",
        json_response=True,
        host=host,
        port=port,
    )

    # ── Resources ────────────────────────────────────────────────────

    @server.resource("spec://taylkomb/rev-d")
    def rev_d_spec_resource() -> str:
        """Active spec — Rev D vertical ball-stud architecture."""
        spec_path = project_root() / "specs" / "taylkomb_revD_master.json"
        return spec_path.read_text(encoding="utf-8")

    @server.resource("spec://taylkomb/rev-c")
    def rev_c_spec_resource() -> str:
        """Retired Rev C spec — kept for reference only."""
        spec_path = project_root() / "specs" / "taylkomb_revC_master.json"
        return spec_path.read_text(encoding="utf-8")

    @server.resource("policy://taylkomb/locked-datums")
    def locked_datums_resource() -> str:
        policy_path = project_root() / "agent" / "policies" / "locked_datums.json"
        return policy_path.read_text(encoding="utf-8")

    # ── Tools ────────────────────────────────────────────────────────

    @server.tool()
    def generate_connector_variant(
        spec_path: str,
        variant_id: str,
        part_name: str,
        backend: str = "cadquery",
        overrides: dict[str, Any] | None = None,
        output_formats: list[str] | None = None,
    ) -> dict[str, Any]:
        """Generate a TAYLKOMB CAD variant from a locked JSON spec."""
        return generate_connector_variant_logic(
            spec_path=spec_path,
            variant_id=variant_id,
            part_name=part_name,
            backend=backend,
            overrides=overrides or {},
            output_formats=output_formats or ["step", "stl"],
        )

    @server.tool()
    def measure_geometry(model_path: str, checks: list[str]) -> dict[str, Any]:
        """Measure geometry from scaffold-generated artifacts or sidecar metric files."""
        return measure_geometry_logic(model_path=model_path, checks=checks)

    @server.tool()
    def validate_connector_rules(spec_path: str, measurement_path: str, part_name: str) -> dict[str, Any]:
        """Validate a measurement payload against the TAYLKOMB rule pack."""
        return validate_connector_rules_logic(
            spec_path=spec_path,
            measurement_path=measurement_path,
            part_name=part_name,
        )

    @server.tool()
    def compare_variants(variant_records: list[dict[str, Any]]) -> dict[str, Any]:
        """Rank variant records by pass/fail status and severity of issues."""
        return compare_variants_logic(variant_records)

    @server.tool()
    def export_release_pack(variant_id: str, include: list[str]) -> dict[str, Any]:
        """Zip release artifacts for a chosen variant."""
        return export_release_pack_logic(variant_id=variant_id, include=include)

    @server.tool()
    def render_drawing_pdf(
        variant_id: str,
        spec_path: str | None = None,
        out_dir: str | None = None,
    ) -> dict[str, Any]:
        """Render the Rev D v3 drawing pack (PDF + PNG + 4 DXF views) for a variant."""
        return render_drawing_pdf_logic(
            variant_id=variant_id,
            spec_path=spec_path,
            out_dir=out_dir,
        )

    return server


# Default instance for stdio (used by .mcp.json / Claude Code)
mcp = _build_mcp()


# ── CLI ──────────────────────────────────────────────────────────────────

@app.command()
def run(
    transport: str = typer.Option("stdio", help="stdio or streamable-http"),
    host: str = typer.Option("127.0.0.1", help="Bind address for HTTP transport"),
    port: int = typer.Option(3333, help="Port for HTTP transport"),
) -> None:
    if transport == "stdio":
        mcp.run(transport="stdio")
    elif transport == "streamable-http":
        server = _build_mcp(host=host, port=port)
        server.run(transport="streamable-http")
    else:
        raise typer.BadParameter("transport must be 'stdio' or 'streamable-http'")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
