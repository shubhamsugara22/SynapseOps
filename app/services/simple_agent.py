"""Minimal simple agent service for immediate Cloud Run deployment."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import ClassVar
from uuid import uuid4

from app.config import Settings


@dataclass(slots=True)
class SessionMessage:
    role: str
    content: str


class SimpleAgentService:
    """Simple text agent with optional Gemini-backed generation."""

    _sessions: ClassVar[dict[str, list[SessionMessage]]] = {}

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @staticmethod
    def _build_prompt(user_message: str, history: list[SessionMessage]) -> str:
        recent = history[-6:]
        context_lines = [f"{msg.role}: {msg.content}" for msg in recent]
        context = "\n".join(context_lines)
        return (
            "You are SynapseOps, a concise cloud operations assistant. "
            "Respond in 3-5 lines with practical next steps.\n"
            "Use the session context if it exists.\n\n"
            f"Session context:\n{context if context else 'none'}\n\n"
            f"User request: {user_message.strip()}"
        )

    @staticmethod
    def _fallback_response(user_message: str) -> str:
        return (
            "Simple agent is running on Cloud Run. "
            "I received your message and the service is healthy. "
            f"Message preview: {user_message.strip()[:120]}"
        )

    def _resolve_session_id(self, session_id: str | None) -> str:
        if session_id and session_id.strip():
            resolved = session_id.strip()
        else:
            resolved = str(uuid4())

        if resolved not in self._sessions:
            self._sessions[resolved] = []
        return resolved

    def get_session_messages(self, session_id: str) -> list[SessionMessage]:
        return list(self._sessions.get(session_id, []))

    def _append_message(self, session_id: str, role: str, content: str) -> None:
        self._sessions.setdefault(session_id, []).append(SessionMessage(role=role, content=content))

    def chat(self, message: str, session_id: str | None = None) -> tuple[str, str, str]:
        cleaned = message.strip()
        if not cleaned:
            raise ValueError("message cannot be empty")

        resolved_session_id = self._resolve_session_id(session_id)
        history = self.get_session_messages(resolved_session_id)
        self._append_message(resolved_session_id, "user", cleaned)

        try:
            from google import genai

            client = genai.Client()
            result = client.models.generate_content(
                model=self.settings.adk_model,
                contents=self._build_prompt(cleaned, history),
            )

            if result and getattr(result, "text", None):
                agent_response = result.text.strip()
                self._append_message(resolved_session_id, "assistant", agent_response)
                return agent_response, "gemini", resolved_session_id
        except Exception:
            # Keep startup and demo flow resilient when credentials or model access are missing.
            pass

        agent_response = self._fallback_response(cleaned)
        self._append_message(resolved_session_id, "assistant", agent_response)
        return agent_response, "fallback", resolved_session_id

    def stream_chat(self, message: str, session_id: str | None = None) -> Iterator[str]:
        response, provider, resolved_session_id = self.chat(message, session_id=session_id)

        for token in response.split():
            yield token + " "

        yield f"\n[source={provider} session_id={resolved_session_id}]"
