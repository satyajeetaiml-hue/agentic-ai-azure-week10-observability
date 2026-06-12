# Week 10 — Observability, Evaluation & Governance

[![CI](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week10-observability/actions/workflows/ci.yml/badge.svg)](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week10-observability/actions/workflows/ci.yml)

> ▶️ **Run in VS Code — no Azure needed.** `pip install -r requirements.txt`, then `uvicorn app.main:app --reload` and open http://127.0.0.1:8000/docs. Runs in **mock mode** by default — no `az login`, keys, or `.env` required. Wiring real Azure (below) is optional.

> **Standalone lab** from the *Agentic AI on Azure — Enterprise Master Class*.
> Course hub: [azure-agentic-ai-masterclass](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass).

---

## 🎯 Learning goal
Trace, **evaluate**, and govern agents in production.

## 🏢 Enterprise use case — "Regulated Advice Quality Monitoring" (Financial Services)
Every interaction is traced end-to-end, scored for groundedness/relevance/safety, and **flagged** when
quality drops — feeding a dashboard auditors can review.

## ✅ What this repo implements
- **Tracing** — a trace id + span per request (OpenTelemetry → Application Insights when configured;
  in-memory trace log otherwise).
- **Evaluation** — deterministic scoring (groundedness, relevance, safety, coherence). Foundry
  Evaluations in prod.
- **Governance** — answers below `QUALITY_THRESHOLD` are `flagged`; aggregate metrics at `/api/v1/metrics`.

## 🚀 Quick start
```bash
python -m venv .venv && .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
```bash
curl -X POST http://127.0.0.1:8000/api/v1/advise \
  -H "Content-Type: application/json" \
  -d '{"client_question": "Should I move my pension this year?"}'
curl http://127.0.0.1:8000/api/v1/metrics
curl http://127.0.0.1:8000/api/v1/traces
```
Run tests: `pytest -q`

## 🔌 Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/advise` | Answer + per-request eval scores |
| GET | `/api/v1/metrics` | Aggregate quality + flagged rate |
| GET | `/api/v1/traces` | Recent traces |

## ☁️ Enable App Insights
Set `APPLICATIONINSIGHTS_CONNECTION_STRING` to export spans via OpenTelemetry. `GET /health` reports
`"tracing": "on"`.

## 🏗️ Architect's lens
- Distributed tracing across agent hops and tool calls (trace/span per agent).
- Offline eval (CI regression gates) vs. online eval (production sampling).
- Golden datasets, A/B prompts, drift detection; cost & latency per token / per tool.

## 🧰 Tech stack
OpenTelemetry, Azure Application Insights, Azure Monitor, Foundry Evaluation SDK, Content Safety, FastAPI.

## 🗺️ Series
Prev: [Week 9](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week09-hosting-scale) ·
Next: [Week 11 — Security](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week11-security) ·
[All labs](https://github.com/satyajeetaiml-hue?tab=repositories&q=agentic-ai-azure)

## 📄 License
MIT — see [`LICENSE`](LICENSE).

## 📊 Teaching slides

Download the **7-slide deck** for classroom use: [`agentic-ai-azure-week10-observability.pptx`](slides/agentic-ai-azure-week10-observability.pptx)

Prefer PDF? Download the **handout (slides + speaker notes)**: [`agentic-ai-azure-week10-observability-handout.pdf`](slides/agentic-ai-azure-week10-observability-handout.pdf)

> Slides: Title · Learning goal · Enterprise use case · Architecture/flow · Key concepts · Run it · Architect's takeaways.

