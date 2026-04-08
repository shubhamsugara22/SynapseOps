"""FastAPI surface for the SynapseOps starter project."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from app.config import Settings
from app.db.alloydb import AlloyDBService
from app.integrations.bigquery_client import BigQueryService
from app.mcp.registry import registry_as_dict
from app.schemas.query import QueryRequest, QueryResponse
from app.services.bootstrap import build_bootstrap_summary


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or Settings.from_env()
    app = FastAPI(title=app_settings.app_name, version="0.1.0")

    @app.get("/")
    def index() -> dict[str, object]:
        return build_bootstrap_summary(app_settings)

    @app.get("/health")
    def health() -> dict[str, object]:
        return {
            "status": "ok",
            "environment": app_settings.app_env,
            "google_auth_configured": app_settings.has_google_auth(),
            "alloydb_configured": AlloyDBService(app_settings).is_configured(),
            "mcp_servers": registry_as_dict(app_settings),
        }

    @app.get("/mcp/servers")
    def mcp_servers() -> list[dict[str, object]]:
        return registry_as_dict(app_settings)

    @app.post("/bigquery/query", response_model=QueryResponse)
    def bigquery_query(request: QueryRequest) -> QueryResponse:
        service = BigQueryService(app_settings)
        try:
            rows = service.run_query(request.sql, limit=request.limit)
        except Exception as exc:  # pragma: no cover - runtime integration path
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return QueryResponse(service="bigquery", rows=rows)

    @app.post("/alloydb/query", response_model=QueryResponse)
    def alloydb_query(request: QueryRequest) -> QueryResponse:
        service = AlloyDBService(app_settings)
        try:
            rows = service.run_query(request.sql)
        except Exception as exc:  # pragma: no cover - runtime integration path
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return QueryResponse(service="alloydb", rows=rows)

    return app
