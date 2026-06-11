"""Hermetic tests for the Week 10 observability service."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["tracing"] == "off"


def test_grounded_advice_scores_well():
    r = client.post("/api/v1/advise", json={"client_question": "Should I move my pension this year?"})
    assert r.status_code == 200
    body = r.json()
    assert body["scores"]["groundedness"] >= 0.9
    assert body["scores"]["safety"] == 1.0
    assert body["trace_id"]


def test_ungrounded_advice_is_flagged():
    r = client.post("/api/v1/advise", json={"client_question": "What's the weather tomorrow?"})
    body = r.json()
    assert body["scores"]["groundedness"] < 0.6
    assert body["flagged"] is True


def test_metrics_aggregate():
    client.post("/api/v1/advise", json={"client_question": "How much emergency savings?"})
    m = client.get("/api/v1/metrics").json()
    assert m["count"] >= 1
    assert "groundedness" in m["avg_scores"]


def test_traces_recorded():
    client.post("/api/v1/advise", json={"client_question": "Tell me about funds"})
    t = client.get("/api/v1/traces").json()
    assert len(t["traces"]) >= 1
    assert "scores" in t["traces"][-1]


def test_validation_rejects_empty():
    assert client.post("/api/v1/advise", json={"client_question": ""}).status_code == 422
