"""Schemas for read-only query endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    sql: str = Field(..., description="Read-only SQL query.")
    limit: int = Field(default=20, ge=1, le=500)


class QueryResponse(BaseModel):
    service: str
    rows: list[dict[str, object]]
