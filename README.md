# Week 10 — Observability, Evaluation & Governance

> **Standalone lab** from the *Agentic AI on Azure — Enterprise Master Class* (12 weeks).
> Each lab is an independent, runnable FastAPI starter. Part of the
> [course series](https://github.com/satyajeetaiml-hue?tab=repositories&q=agentic-ai-azure).

---

## 🎯 Learning goal
Trace, evaluate, and continuously improve agents in production.

## 🏢 Enterprise use case — "Regulated Advice Quality Monitoring" (Financial Services)
Every agent interaction is traced end-to-end, scored for groundedness/relevance/safety, and flagged when quality drops — feeding a quality dashboard auditors can review.

---

## 🧪 What you'll build (lab)
1. Instrument FastAPI + agents with **OpenTelemetry** → Application Insights.
2. Run **Foundry Evaluations** (groundedness, relevance, coherence, safety) offline + online.
3. Build a quality dashboard and set alerts on metric thresholds.
4. Add a regression eval gate to CI on a golden dataset.

> This starter ships with a **runnable mock** of the endpoint so you can run and test
> immediately, then progressively replace the mock with the real Azure implementation.

## 🏗️ Architect's lens
- Distributed tracing across agent hops and tool calls (trace/span per agent).
- Offline eval (regression gates in CI) vs. online eval (production sampling).
- Golden datasets, A/B prompts, drift detection; cost & latency per token / per tool.

## 🧰 Tech stack
OpenTelemetry, Azure Application Insights, Azure Monitor, Foundry Evaluation SDK, Azure Content Safety, FastAPI middleware.

---

## 🚀 Quick start

```bash
# 1. Create & activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) copy the env template — runs in MOCK mode without it
copy .env.example .env        # Windows
# cp .env.example .env        # macOS/Linux

# 4. Run the API
uvicorn app.main:app --reload
```

Open the interactive docs at **http://127.0.0.1:8000/docs**.

### Try the endpoint
```bash
curl -X POST http://127.0.0.1:8000/api/v1/advise \
  -H "Content-Type: application/json" \
  -d '{"client_question": "Should I move my pension into a higher-growth fund this year?"}'
```

### Run the tests
```bash
pytest -q
```

### Run with Docker
```bash
docker build -t agentic-ai-azure-week10-observability .
docker run -p 8000:8000 agentic-ai-azure-week10-observability
```

---

## 📁 Project structure
```
agentic-ai-azure-week10-observability/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI app + the /api/v1/advise endpoint
├── tests/
│   └── test_smoke.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

---

## 🗺️ Where this fits
This repo covers **Week 10 — Observability, Evaluation & Governance**. The full 12-week path and reference architecture
live in the master-class companion repo:
**[azure-agentic-ai-masterclass](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass)**.

## 📄 License
MIT — see [`LICENSE`](LICENSE).
