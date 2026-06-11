"""Smoke tests for Week 10 — Observability, Evaluation & Governance."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_endpoint_accepts_input():
    r = client.post("/api/v1/advise", json={"client_question": "Should I move my pension into a higher-growth fund this year?"})
    assert r.status_code == 200


def test_endpoint_rejects_empty():
    r = client.post("/api/v1/advise", json={"client_question": ""})
    assert r.status_code == 422
