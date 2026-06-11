"""Week 10 — Observability, Evaluation & Governance.

Advice Quality Monitoring: every answer is traced, evaluated, and flagged when it
drops below quality thresholds; aggregate metrics feed a dashboard. Run:  uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.service import (
    AdviseRequest,
    AdviseResponse,
    get_backend,
    get_settings,
    metrics_summary,
    recent_traces,
)

settings = get_settings()
app = FastAPI(title="Week 10 — Observability (Advice Quality)", version="0.2.0")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok", "week": "10", "tracing": "on" if settings.tracing_enabled else "off"}


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {
        "service": "agentic-ai-azure-week10-observability",
        "endpoint": "/api/v1/advise",
        "docs": "/docs",
    }


@app.post("/api/v1/advise", response_model=AdviseResponse, tags=["week10"])
def advise(payload: AdviseRequest) -> AdviseResponse:
    return get_backend().advise(payload)


@app.get("/api/v1/metrics", tags=["week10"])
def metrics() -> dict:
    """Aggregate quality metrics for the dashboard / alerting."""
    return metrics_summary()


@app.get("/api/v1/traces", tags=["week10"])
def traces() -> dict:
    """Recent per-request traces (groundedness/relevance/safety/coherence)."""
    return {"traces": recent_traces()}
