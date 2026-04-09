"""Schemas for simple agent interactions."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AgentChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message for the simple agent.")
    session_id: str | None = Field(default=None, description="Optional caller session identifier.")


class AgentChatResponse(BaseModel):
    agent: str
    model: str
    response: str
    provider: str
    session_id: str | None = None
