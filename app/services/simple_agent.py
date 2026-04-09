"""Minimal simple agent service for immediate Cloud Run deployment."""

from __future__ import annotations

from app.config import Settings


class SimpleAgentService:
    """Simple text agent with optional Gemini-backed generation."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @staticmethod
    def _build_prompt(user_message: str) -> str:
        return (
            "You are SynapseOps, a concise cloud operations assistant. "
            "Respond in 3-5 lines with practical next steps.\n\n"
            f"User request: {user_message.strip()}"
        )

    @staticmethod
    def _fallback_response(user_message: str) -> str:
        return (
            "Simple agent is running on Cloud Run. "
            "I received your message and the service is healthy. "
            f"Message preview: {user_message.strip()[:120]}"
        )

    def chat(self, message: str) -> tuple[str, str]:
        cleaned = message.strip()
        if not cleaned:
            raise ValueError("message cannot be empty")

        try:
            from google import genai

            client = genai.Client()
            result = client.models.generate_content(
                model=self.settings.adk_model,
                contents=self._build_prompt(cleaned),
            )

            if result and getattr(result, "text", None):
                return result.text.strip(), "gemini"
        except Exception:
            # Keep startup and demo flow resilient when credentials or model access are missing.
            pass

        return self._fallback_response(cleaned), "fallback"
