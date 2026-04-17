from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from taylkomb_mcp.io_utils import project_root
from taylkomb_mcp.server_logic import (
    export_release_pack_logic,
    generate_connector_variant_logic,
    measure_geometry_logic,
    render_drawing_pdf_logic,
    validate_connector_rules_logic,
)

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()


@app.command("run-variant")
def run_variant(
    spec: Path = typer.Argument(..., exists=True),
    part_name: str = typer.Argument(...),
    variant_id: str = typer.Option("manual"),
    overrides_json: str = typer.Option("{}"),
) -> None:
    """Generate a single variant (STEP + STL) from a spec file."""
    overrides = json.loads(overrides_json)
    result = generate_connector_variant_logic(
        spec_path=str(spec),
        variant_id=variant_id,
        part_name=part_name,
        backend="cadquery",
        overrides=overrides,
        output_formats=["step", "stl"],
    )
    typer.echo(json.dumps(result, indent=2))


@app.command("render-pdf")
def render_pdf(
    variant_id: str = typer.Argument(..., help="Variant ID to render."),
    spec: Path | None = typer.Option(None, "--spec", help="Spec JSON (defaults to specs/taylkomb_revD_master.json)."),
    out: Path | None = typer.Option(None, "--out", help="Output dir (defaults to output/sweep_a/drawings)."),
) -> None:
    """Render Rev D v3 drawing PDF + PNG + 4 DXF views for a variant."""
    result = render_drawing_pdf_logic(
        variant_id=variant_id,
        spec_path=str(spec) if spec else None,
        out_dir=str(out) if out else None,
    )
    if result.get("success") is False:
        console.print(f"[red]✗[/red] render failed for {variant_id}: {result.get('error')}")
        raise typer.Exit(code=1)
    console.print(f"[green]✓[/green] rendered {variant_id}")
    console.print(f"  pdf: {result.get('pdf_path')}")
    console.print(f"  png: {result.get('png_path')}")


@app.command("release")
def release(
    sweep_id: str = typer.Argument("sweep_a", help="Sweep directory under output/."),
    include: str = typer.Option(
        "step,stl,preview_png,report_md,json_metrics",
        help="Comma-separated artifact kinds to include.",
    ),
) -> None:
    """Bundle release packs for every variant in a sweep."""
    root = project_root()
    sweep_dir = root / "output" / sweep_id
    variants_dir = sweep_dir / "generated"
    if not variants_dir.exists():
        console.print(f"[red]✗[/red] no generated variants under {variants_dir}")
        raise typer.Exit(code=1)

    include_list = [x.strip() for x in include.split(",") if x.strip()]
    table = Table(title=f"Release packs — {sweep_id}")
    table.add_column("variant")
    table.add_column("archive")
    table.add_column("files", justify="right")

    for variant_path in sorted(p for p in variants_dir.iterdir() if p.is_dir()):
        result = export_release_pack_logic(variant_id=variant_path.name, include=include_list)
        table.add_row(
            result["variant_id"],
            result["archive_path"],
            str(len(result["files"])),
        )
    console.print(table)


@app.command("run-sweep")
def run_sweep(
    sweep_file: Path = typer.Argument(..., exists=True, help="JSON file listing variants to generate."),
) -> None:
    """Run generate → measure → validate → render for each variant in a sweep file."""
    plan = json.loads(sweep_file.read_text(encoding="utf-8"))
    spec_path = str(Path(plan.get("spec_path", project_root() / "specs" / "taylkomb_revD_master.json")))
    variants = plan.get("variants", [])

    table = Table(title=f"Sweep — {sweep_file.name}")
    table.add_column("variant")
    table.add_column("part")
    table.add_column("generate")
    table.add_column("validate")
    table.add_column("pdf")

    for v in variants:
        variant_id = v["variant_id"]
        part_name = v["part_name"]
        overrides = v.get("overrides", {})

        gen = generate_connector_variant_logic(
            spec_path=spec_path,
            variant_id=variant_id,
            part_name=part_name,
            backend="cadquery",
            overrides=overrides,
            output_formats=v.get("output_formats", ["step", "stl"]),
        )
        metrics_path = gen["metrics_path"]
        val = validate_connector_rules_logic(
            spec_path=spec_path,
            measurement_path=metrics_path,
            part_name=part_name,
        )
        pdf_result = render_drawing_pdf_logic(variant_id=variant_id)
        pdf_ok = pdf_result.get("success") is not False and pdf_result.get("pdf_path")

        table.add_row(
            variant_id,
            part_name,
            "✓" if gen.get("exports") else "✗",
            "✓" if val.get("passed") else "✗",
            "✓" if pdf_ok else "✗",
        )
        # measure is exercised via the stored metrics sidecar
        _ = measure_geometry_logic(
            model_path=next(iter(gen["exports"].values())) if gen.get("exports") else "",
            checks=["bounding_box"],
        ) if gen.get("exports") else None

    console.print(table)


if __name__ == "__main__":
    app()
