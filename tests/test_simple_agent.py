from app.config import Settings
from app.services.simple_agent import SimpleAgentService


def test_simple_agent_creates_session_and_persists_history() -> None:
    service = SimpleAgentService(Settings())

    response, provider, session_id = service.chat("hello")

    assert response
    assert provider in {"gemini", "fallback"}
    assert session_id

    messages = service.get_session_messages(session_id)
    assert len(messages) >= 2
    assert messages[0].role == "user"
    assert messages[1].role == "assistant"


def test_simple_agent_reuses_given_session_id() -> None:
    service = SimpleAgentService(Settings())
    forced_session_id = "demo-session"

    _, _, session_id = service.chat("one", session_id=forced_session_id)
    _, _, same_session_id = service.chat("two", session_id=forced_session_id)

    assert session_id == forced_session_id
    assert same_session_id == forced_session_id
    assert len(service.get_session_messages(forced_session_id)) >= 4
