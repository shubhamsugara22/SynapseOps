"""ADK root agent scaffold for SynapseOps."""

from __future__ import annotations

from typing import Any

from app.config import Settings
from app.integrations.bigquery_client import run_bigquery_sql_tool
from app.mcp.registry import registry_as_dict

try:
    from google.adk.agents import Agent
except ModuleNotFoundError:  # pragma: no cover - handled at runtime after deps install
    Agent = None


def build_root_agent(settings: Settings | None = None) -> Any:
    settings = settings or Settings.from_env()
    if Agent is None:
        raise RuntimeError("google-adk is not installed. Run 'pip install -r requirements.txt'.")

    def list_mcp_servers() -> list[dict[str, object]]:
        return registry_as_dict(settings)

    return Agent(
        name="synapseops_root",
        model=settings.adk_model,
        instruction=(
            "You are SynapseOps, an operations and analytics agent built on Google Cloud. "
            "Use BigQuery for analytical read-only questions and consult MCP registry metadata "
            "before assuming an external "
            "capability exists. Be explicit about missing configuration."
        ),
        tools=[
            run_bigquery_sql_tool,
            list_mcp_servers,
        ],
    )
