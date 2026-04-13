"""Starter workflow outline derived from the referenced codelabs."""

from __future__ import annotations


def get_workflow_outline() -> dict[str, list[str]]:
    return {
        "ingest": [
            "Load operational and reference data into BigQuery.",
            "Expose selected datasets through MCP Toolbox for Databases.",
        ],
        "reason": [
            "Use the ADK root agent to route requests to read-only tools.",
            "Add specialized sub-agents after the base tool paths are stable.",
        ],
        "enrich": [
            "Attach remote MCP servers for BigQuery Toolbox and Maps.",
            "Add tool-level safeguards, schema-aware prompting, and routing policies.",
        ],
        "deploy": [
            "Run locally with FastAPI during development.",
            "Package for Cloud Run once environment variables are set.",
        ],
    }
