from __future__ import annotations

import json
from pathlib import Path

import typer

from taylkomb_mcp.io_utils import write_json
from taylkomb_mcp.server_logic import generate_connector_variant_logic

app = typer.Typer(add_completion=False)


@app.command()
def run_variant(
    spec: Path = typer.Argument(..., exists=True),
    part_name: str = typer.Argument(...),
    variant_id: str = typer.Option("manual"),
    overrides_json: str = typer.Option("{}"),
):
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


if __name__ == "__main__":
    app()
