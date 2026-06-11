"""Week 10 — Observability, Evaluation & Governance: Advice Quality Monitoring.

Demonstrates the three pillars of production agent ops:

* **Tracing** — each request gets a trace id and a recorded span (OpenTelemetry →
  Application Insights when configured; an in-memory trace log otherwise).
* **Evaluation** — every answer is scored for groundedness / relevance / safety /
  coherence (Foundry Evaluations in prod; deterministic heuristics here).
* **Governance** — answers that fall below thresholds are flagged, and aggregate
  quality metrics are exposed for a dashboard/alerts.
"""

from __future__ import annotations

import re
import time
import uuid
from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# ── settings ────────────────────────────────────────────────────────────
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "local"
    applicationinsights_connection_string: str = ""
    quality_threshold: float = 0.6

    @property
    def tracing_enabled(self) -> bool:
        return bool(self.applicationinsights_connection_string)


@lru_cache
def get_settings() -> Settings:
    return Settings()


# ── schemas ─────────────────────────────────────────────────────────────
class AdviseRequest(BaseModel):
    client_question: str = Field(..., min_length=1, description="A client question for the advice agent.")


class Scores(BaseModel):
    groundedness: float
    relevance: float
    safety: float
    coherence: float


class AdviseResponse(BaseModel):
    answer: str
    scores: Scores
    flagged: bool
    trace_id: str
    mode: str


# ── grounding context + safety rules ────────────────────────────────────
_CONTEXT = {
    "pension": "Pension transfers depend on your risk tolerance, fees, and time horizon.",
    "fund": "Higher-growth funds carry more volatility and are better suited to longer horizons.",
    "savings": "Emergency savings should typically cover three to six months of expenses.",
}
_BANNED = ("guaranteed returns", "get rich", "risk-free profit")
_WORD_RE = re.compile(r"[a-z]{3,}")


def _tokens(text: str) -> set[str]:
    return set(_WORD_RE.findall(text.lower()))


# ── trace + metrics store (Application Insights in prod) ─────────────────
_TRACES: list[dict] = []


def _record_trace(trace_id: str, question: str, scores: Scores, flagged: bool, latency_ms: float) -> None:
    _TRACES.append(
        {
            "trace_id": trace_id,
            "question": question,
            "scores": scores.model_dump(),
            "flagged": flagged,
            "latency_ms": round(latency_ms, 2),
        }
    )
    _emit_span(trace_id, scores, flagged)  # best-effort OTel export


def _emit_span(trace_id: str, scores: Scores, flagged: bool) -> None:
    """Best-effort OpenTelemetry span; no-ops if OTel/App Insights not set up."""
    if not get_settings().tracing_enabled:
        return
    try:  # pragma: no cover - exercised only when OTel is installed/configured
        from opentelemetry import trace

        tracer = trace.get_tracer("advice-agent")
        with tracer.start_as_current_span("advise") as span:
            span.set_attribute("trace_id", trace_id)
            span.set_attribute("eval.groundedness", scores.groundedness)
            span.set_attribute("eval.flagged", flagged)
    except Exception:
        pass


def recent_traces(limit: int = 20) -> list[dict]:
    return _TRACES[-limit:]


def metrics_summary() -> dict:
    if not _TRACES:
        return {"count": 0, "flagged": 0, "flagged_rate": 0.0, "avg_scores": {}}
    n = len(_TRACES)
    flagged = sum(1 for t in _TRACES if t["flagged"])
    keys = ["groundedness", "relevance", "safety", "coherence"]
    avg = {k: round(sum(t["scores"][k] for t in _TRACES) / n, 3) for k in keys}
    return {"count": n, "flagged": flagged, "flagged_rate": round(flagged / n, 3), "avg_scores": avg}


# ── evaluation ──────────────────────────────────────────────────────────
def evaluate(question: str, answer: str, context: str | None) -> Scores:
    q, a = _tokens(question), _tokens(answer)
    relevance = round(len(q & a) / (len(q) or 1), 3)
    groundedness = 0.92 if context and context.lower() in answer.lower() else 0.45
    safety = 0.2 if any(b in answer.lower() for b in _BANNED) else 1.0
    coherence = 0.88 if 5 <= len(answer.split()) <= 80 else 0.55
    return Scores(groundedness=groundedness, relevance=relevance, safety=safety, coherence=coherence)


# ── backend ─────────────────────────────────────────────────────────────
class AdviceBackend:
    mode = "mock"

    def advise(self, req: AdviseRequest) -> AdviseResponse:
        start = time.perf_counter()
        trace_id = uuid.uuid4().hex
        context = next((v for k, v in _CONTEXT.items() if k in req.client_question.lower()), None)
        if context:
            answer = f"{context} Consider speaking with an adviser for your specific situation."
        else:
            answer = "I don't have grounded guidance for that; please consult an adviser."
        scores = evaluate(req.client_question, answer, context)
        threshold = get_settings().quality_threshold
        flagged = any(v < threshold for v in scores.model_dump().values())
        latency = (time.perf_counter() - start) * 1000
        _record_trace(trace_id, req.client_question, scores, flagged, latency)
        return AdviseResponse(answer=answer, scores=scores, flagged=flagged, trace_id=trace_id, mode=self.mode)


def get_backend() -> AdviceBackend:
    return AdviceBackend()
