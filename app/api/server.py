"""FastAPI surface for the SynapseOps starter project."""

from __future__ import annotations

from collections.abc import Iterator

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from app.config import Settings
from app.db.alloydb import AlloyDBService
from app.integrations.bigquery_client import BigQueryService
from app.mcp.registry import registry_as_dict
from app.schemas.agent import (
    AgentChatRequest,
    AgentChatResponse,
    AgentSessionMessage,
    AgentSessionResponse,
)
from app.schemas.query import QueryRequest, QueryResponse
from app.services.bootstrap import build_bootstrap_summary
from app.services.simple_agent import SimpleAgentService


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

    @app.post("/agent/chat", response_model=AgentChatResponse)
    def agent_chat(request: AgentChatRequest) -> AgentChatResponse:
        service = SimpleAgentService(app_settings)
        try:
            response_text, provider, resolved_session_id = service.chat(
                request.message,
                session_id=request.session_id,
            )
        except Exception as exc:  # pragma: no cover - runtime integration path
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        return AgentChatResponse(
            agent="simple-agent",
            model=app_settings.adk_model,
            response=response_text,
            provider=provider,
            session_id=resolved_session_id,
        )

    @app.post("/agent/chat/stream")
    def agent_chat_stream(request: AgentChatRequest) -> StreamingResponse:
        service = SimpleAgentService(app_settings)

        def event_stream() -> Iterator[str]:
            try:
                for chunk in service.stream_chat(request.message, session_id=request.session_id):
                    yield f"data: {chunk}\n\n"
                yield "event: done\ndata: [DONE]\n\n"
            except Exception as exc:  # pragma: no cover - runtime integration path
                yield f"event: error\ndata: {str(exc)}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    @app.get("/agent/sessions/{session_id}", response_model=AgentSessionResponse)
    def get_agent_session(session_id: str) -> AgentSessionResponse:
        service = SimpleAgentService(app_settings)
        messages = [
            AgentSessionMessage(role=msg.role, content=msg.content)
            for msg in service.get_session_messages(session_id)
        ]
        return AgentSessionResponse(
            session_id=session_id,
            messages=messages,
        )

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
