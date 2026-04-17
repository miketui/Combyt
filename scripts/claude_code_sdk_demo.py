from __future__ import annotations

import asyncio
from pathlib import Path

from claude_code_sdk import ClaudeCodeOptions, query

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROMPT = """
Use the TAYLKOMB MCP tools to generate two round-handle variants from specs/taylkomb_revC_master.json.
Keep locked datums fixed.
Sweep only clearance_per_side_mm and tip_diameter_mm.
Export STEP, STL, metrics JSON, validation JSON, and markdown report.
Then compare the variants and recommend the better prototype candidate.
""".strip()


async def main() -> None:
    options = ClaudeCodeOptions(
        cwd=PROJECT_ROOT,
        mcp_config=PROJECT_ROOT / ".mcp.json",
        max_turns=6,
        permission_mode="acceptEdits",
        allowed_tools=[
            "Read",
            "Write",
            "Glob",
            "LS",
            "mcp__taylkomb-cad__generate_connector_variant",
            "mcp__taylkomb-cad__measure_geometry",
            "mcp__taylkomb-cad__validate_connector_rules",
            "mcp__taylkomb-cad__compare_variants",
            "mcp__taylkomb-cad__export_release_pack"
        ]
    )

    async for message in query(prompt=PROMPT, options=options):
        if hasattr(message, "result"):
            print(message.result)
        elif hasattr(message, "content"):
            print(message.content)


if __name__ == "__main__":
    asyncio.run(main())
