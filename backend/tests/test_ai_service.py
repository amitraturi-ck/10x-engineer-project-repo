import pytest
from app.ai_service import run_prompt


def test_run_prompt_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError) as exc:
        run_prompt("Hello")

    assert "OPENAI_API_KEY" in str(exc.value)

def test_run_prompt_success(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    class MockResponse:
        class Choice:
            class Message:
                content = "Mocked AI response"
            message = Message()
        choices = [Choice()]

    class MockClient:
        class Chat:
            class Completions:
                @staticmethod
                def create(**kwargs):
                    return MockResponse()
            completions = Completions()
        chat = Chat()

    monkeypatch.setattr("app.ai_service.OpenAI", lambda api_key: MockClient())

    result = run_prompt("Hello")
    assert result == "Mocked AI response"
def test_run_prompt_openai_error(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    class MockClient:
        class Chat:
            class Completions:
                @staticmethod
                def create(**kwargs):
                    raise Exception("API failure")
            completions = Completions()
        chat = Chat()

    monkeypatch.setattr("app.ai_service.OpenAI", lambda api_key: MockClient())

    with pytest.raises(RuntimeError) as exc:
        run_prompt("Hello")

    assert "OpenAI API error: API failure" in str(exc.value)
