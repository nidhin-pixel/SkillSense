# SkillSense — AI Layer

Standalone FastAPI microservice covering everything under the "AI Layer"
box of the SkillSense tech stack: LLM-based question generation and
AI-driven competency analysis (gap detection, scoring, decay, prediction,
explainability). The main backend calls this service over HTTP.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env          # fill in your GROQ_API_KEY
```

## Run

```bash
uvicorn app.main:app --reload --port 8001
```

Interactive API docs: http://localhost:8001/docs

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/generate/mcq` | Generate MCQs from content |
| POST | `/generate/scenario` | Generate applied scenario-based questions |
| POST | `/analyze/gaps` | Concept-level gap detection from responses |
| POST | `/analyze/explain-gap` | Explainable AI: why a mastery level was assigned |
| POST | `/analyze/score` | Evidence-based competency scoring (+ confidence) |
| POST | `/analyze/decay` | Competency decay detection over a score history |
| POST | `/analyze/predict-gaps` | Predictive department-level skill gaps |
| POST | `/ingest/upload` | Upload a PDF/PPTX/TXT, get back clean text chunks |

## Folder structure

```
app/
├── main.py                      # FastAPI app, all routes
├── llm/
│   ├── groq_client.py           # Groq (llama-3.3) wrapper, retries, JSON mode
│   └── prompts.py                # All prompt templates in one place
├── question_gen/
│   ├── mcq_generator.py         # Recall-style MCQs
│   └── scenario_generator.py    # Applied/scenario-based questions
├── competency/
│   ├── knowledge_graph.py       # Domain -> Topic -> Concept graph + prerequisites
│   ├── gap_analyzer.py          # Concept-level gap detection + explainability
│   ├── scorer.py                # Multi-signal scoring engine + confidence
│   └── decay_detector.py        # Decay detection + predictive gap forecasting
├── schemas/
│   └── models.py                 # All Pydantic request/response models
└── ingestion/
    └── content_parser.py         # PDF/PPTX/TXT -> clean, chunked text
```

## Typical end-to-end flow

1. Frontend/backend uploads a training doc → `POST /ingest/upload` → returns
   text chunks.
2. For each chunk, call `POST /generate/mcq` (or `/generate/scenario`) to
   get questions.
3. Officer takes the assessment; backend collects responses and calls
   `POST /analyze/score` and `POST /analyze/gaps`.
4. For any weak concept, call `POST /analyze/explain-gap` to get a
   human-readable reason + next step for the Competency Passport.
5. Periodically, call `POST /analyze/decay` with score history to check
   for competency decay, and `POST /analyze/predict-gaps` at the
   department level for capacity planning.

## Design notes

- **Scoring is deterministic where it matters.** `scorer.py` and the trend
  classification in `decay_detector.py` compute numbers in plain Python —
  the LLM is only used to *explain* results in natural language, not to
  invent the numbers. This keeps scores auditable and reproducible.
- **Scenario questions are weighted higher** than recall MCQs in scoring
  (`SCENARIO_WEIGHT` in `scorer.py`), matching the vision doc's distinction
  between "knows the definition" vs "can apply it."
- **Confidence is separate from score.** A 90% score from 2 questions is
  reported with `confidence: "low"`, not treated the same as 90% from 10+
  questions — see `CONFIDENCE_THRESHOLDS` in `scorer.py`.
- **`knowledge_graph.py` is a placeholder in-memory graph.** Swap it for a
  real DB-backed graph once the integration teammate's data is ready; keep
  the same function signatures so nothing else has to change.

## Still to build
- Swap `knowledge_graph.py`'s in-memory `_GRAPH` for the real graph/DB once
  the integration teammate's data is ready (function signatures already match)
- Multilingual prompt variants (Hindi/regional) if that feature is prioritized
- OCR fallback in `content_parser.py` for scanned/image-based PDFs
