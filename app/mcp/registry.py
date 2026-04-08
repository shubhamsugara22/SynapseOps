"""Registry for remote MCP servers referenced by the starter project."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from app.config import Settings


@dataclass(slots=True)
class MCPServer:
    name: str
    capability: str
    enabled: bool
    url: str
    notes: str


def build_mcp_registry(settings: Settings) -> list[MCPServer]:
    return [
        MCPServer(
            name="bigquery-toolbox",
            capability="BigQuery datasets exposed through MCP Toolbox for Databases",
            enabled=settings.mcp_bigquery_enabled,
            url=settings.mcp_bigquery_toolbox_url,
            notes="Matches the MCP Toolbox and ADK BigQuery codelabs.",
        ),
        MCPServer(
            name="google-maps",
            capability="Location validation and geospatial enrichment",
            enabled=settings.mcp_maps_enabled,
            url=settings.mcp_google_maps_url,
            notes="Matches the ADK + MCP + Maps codelab tool pattern.",
        ),
    ]


def registry_as_dict(settings: Settings) -> list[dict[str, object]]:
    return [asdict(server) for server in build_mcp_registry(settings)]
