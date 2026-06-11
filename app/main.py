"""Week 10 — Observability, Evaluation & Governance — starter FastAPI service.

Use case: Regulated Advice Quality Monitoring (Financial Services).
See README.md for the full lab brief. Run:  uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Week 10 — Observability, Evaluation & Governance", version="0.1.0")


class LabRequest(BaseModel):
    client_question: str = Field(..., min_length=1, description="A client question routed through the advice agent.")


@app.get("/health")
def health():
    return {"status": "ok", "week": "10", "use_case": "Regulated Advice Quality Monitoring"}


@app.get("/")
def root():
    return {
        "service": "agentic-ai-azure-week10-observability",
        "week": "10",
        "endpoint": "/api/v1/advise",
        "docs": "/docs",
    }


@app.post("/api/v1/advise")
def handler(payload: LabRequest):
    """Mock handler for the Regulated Advice Quality Monitoring.

    TODO (lab): replace this stub with the real implementation described in
    README.md (the Azure services for this week are listed in the Tech Stack).
    """
    return {
        "week": "10",
        "use_case": "Regulated Advice Quality Monitoring",
        "received": payload.client_question,
        "status": "accepted",
        "note": "Mock response — implement the real agent per README.md.",
    }
