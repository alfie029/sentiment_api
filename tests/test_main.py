from fastapi.testclient import TestClient
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

from sentiment_api.agent import get_agent
from sentiment_api.main import app
from sentiment_api.models import BatchSentiment


def _client_with(results: list[dict]) -> TestClient:
    model = TestModel(custom_output_args={"results": results})
    app.dependency_overrides[get_agent] = lambda: Agent(model, output_type=BatchSentiment)
    return TestClient(app)


def _item(i: int) -> dict:
    return {"index": i, "label": "positive", "score": 0.5, "rationale": "ok"}


def test_healthz():
    assert TestClient(app).get("/healthz").json() == {"status": "ok"}


def test_one_call_returns_verdict_per_review():
    try:
        resp = _client_with([_item(0), _item(1)]).post("/sentiment", json={"reviews": ["fine", "good"]})
    finally:
        app.dependency_overrides.clear()
    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 2


def test_missing_verdict_is_a_502():
    try:
        resp = _client_with([_item(0)]).post("/sentiment", json={"reviews": ["fine", "good"]})
    finally:
        app.dependency_overrides.clear()
    assert resp.status_code == 502
