"""Starter workflow outline derived from the referenced codelabs."""

from __future__ import annotations


def get_workflow_outline() -> dict[str, list[str]]:
    return {
        "ingest": [
            "Load operational and reference data into BigQuery.",
            "Store transactional and operational state in AlloyDB.",
        ],
        "reason": [
            "Use the ADK root agent to route requests to read-only tools.",
            "Add specialized sub-agents after the base tool paths are stable.",
        ],
        "enrich": [
            "Attach remote MCP servers for BigQuery Toolbox and Maps.",
            "Push semantic search and in-database AI patterns into AlloyDB later.",
        ],
        "deploy": [
            "Run locally with FastAPI during development.",
            "Package for Cloud Run once environment variables are set.",
        ],
    }
