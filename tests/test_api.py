from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

MOCK_RESPONSE = {
    "story_points": 3,
    "priority": "normal",
    "justification": "This is a medium-complexity feature with clear requirements and no major unknowns.",
}


def _make_openai_mock(payload: dict) -> MagicMock:
    """Build a minimal mock that looks like an OpenAI ChatCompletion response."""
    import json

    mock_message = MagicMock()
    mock_message.content = json.dumps(payload)

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_completion
    return mock_client


class TestHealth:
    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestAnalyze:
    @patch("app.ai.OpenAI")
    def test_analyze_returns_expected_shape(self, mock_openai_cls):
        mock_openai_cls.return_value = _make_openai_mock(MOCK_RESPONSE)

        response = client.post("/api/analyze", json={"description": "Add a copy link button to the entity page header."})

        assert response.status_code == 200
        body = response.json()
        assert body["story_points"] == 3
        assert body["priority"] == "normal"
        assert "justification" in body

    @patch("app.ai.OpenAI")
    def test_analyze_all_priority_values_accepted(self, mock_openai_cls):
        for priority in ("blocker", "critical", "major", "normal", "minor"):
            payload = {**MOCK_RESPONSE, "priority": priority}
            mock_openai_cls.return_value = _make_openai_mock(payload)

            response = client.post("/api/analyze", json={"description": "Some issue description."})
            assert response.status_code == 200
            assert response.json()["priority"] == priority

    def test_analyze_rejects_empty_description(self):
        response = client.post("/api/analyze", json={"description": "   "})
        assert response.status_code == 422

    def test_analyze_rejects_missing_description(self):
        response = client.post("/api/analyze", json={})
        assert response.status_code == 422

    @patch("app.ai.OpenAI")
    def test_analyze_returns_502_on_openai_failure(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("upstream error")
        mock_openai_cls.return_value = mock_client

        response = client.post("/api/analyze", json={"description": "Some issue."})
        assert response.status_code == 502
