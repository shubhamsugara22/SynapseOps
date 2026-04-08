"""Bootstrap summaries used by the local API and docs."""

from __future__ import annotations

from app.config import Settings
from app.mcp.registry import registry_as_dict
from app.workflows.synapse_flow import get_workflow_outline


def build_bootstrap_summary(settings: Settings) -> dict[str, object]:
    return {
        "service": settings.app_name,
        "environment": settings.app_env,
        "model": settings.adk_model,
        "google_cloud_project": settings.google_cloud_project,
        "workflow": get_workflow_outline(),
        "mcp_servers": registry_as_dict(settings),
    }
