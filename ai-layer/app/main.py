"""
main.py
-------
FastAPI entrypoint for the SkillSense AI Layer microservice.
Run locally with:  uvicorn app.main:app --reload --port 8001
"""

import logging
from fastapi import FastAPI, HTTPException, UploadFile, File

from app.schemas.models import (
    MCQGenerateRequest, MCQGenerateResponse,
    ScenarioGenerateRequest, ScenarioGenerateResponse,
    GapAnalysisRequest, GapAnalysisResponse,
    ExplainGapRequest, ExplainGapResponse,
    ScoreRequest, ScoreResponse, ConceptScore,
    DecayCheckRequest, DecayCheckResponse,
    PredictiveGapRequest, PredictiveGapResponse,
    ProcessUploadResponse,
)
from app.question_gen.mcq_generator import generate_mcqs
from app.question_gen.scenario_generator import generate_scenarios
from app.competency.gap_analyzer import analyze_gaps, explain_gap
from app.competency.scorer import compute_all_scores, ResponseRecord
from app.competency.decay_detector import detect_decay, predict_department_gaps
from app.ingestion.content_parser import process_upload, UnsupportedFileTypeError
from app.llm.groq_client import LLMCallError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_layer.main")

app = FastAPI(title="SkillSense AI Layer", version="0.2.0")


def _handle_ai_errors(fn_name: str, e: Exception):
    if isinstance(e, ValueError):
        logger.error("%s validation failed: %s", fn_name, e)
        raise HTTPException(status_code=502, detail=f"{fn_name} failed: {e}")
    if isinstance(e, LLMCallError):
        logger.error("%s LLM call failed: %s", fn_name, e)
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable")
    logger.exception("%s unexpected error", fn_name)
    raise HTTPException(status_code=500, detail="Internal AI layer error")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-layer", "version": "0.2.0"}


# ---------- Question Generation ----------

@app.post("/generate/mcq", response_model=MCQGenerateResponse)
def generate_mcq_endpoint(payload: MCQGenerateRequest):
    try:
        return generate_mcqs(
            content=payload.content,
            num_questions=payload.num_questions,
            difficulty=payload.difficulty,
            concept=payload.concept,
        )
    except Exception as e:
        _handle_ai_errors("generate_mcq", e)


@app.post("/generate/scenario", response_model=ScenarioGenerateResponse)
def generate_scenario_endpoint(payload: ScenarioGenerateRequest):
    try:
        return generate_scenarios(
            concept=payload.concept,
            content=payload.content,
            num_questions=payload.num_questions,
        )
    except Exception as e:
        _handle_ai_errors("generate_scenario", e)


# ---------- Competency Analysis ----------

@app.post("/analyze/gaps", response_model=GapAnalysisResponse)
def analyze_gaps_endpoint(payload: GapAnalysisRequest):
    try:
        responses = [r.dict() for r in payload.responses]
        return analyze_gaps(responses)
    except Exception as e:
        _handle_ai_errors("analyze_gaps", e)


@app.post("/analyze/explain-gap", response_model=ExplainGapResponse)
def explain_gap_endpoint(payload: ExplainGapRequest):
    try:
        responses = [r.dict() for r in payload.responses]
        return explain_gap(
            concept=payload.concept,
            responses=responses,
            mastery_level=payload.mastery_level,
            score=payload.score,
        )
    except Exception as e:
        _handle_ai_errors("explain_gap", e)


@app.post("/analyze/score", response_model=ScoreResponse)
def score_endpoint(payload: ScoreRequest):
    try:
        records = [
            ResponseRecord(concept=r.concept, correct=r.correct, is_scenario=r.is_scenario)
            for r in payload.responses
        ]
        results = compute_all_scores(records)
        return {
            "scores": [
                ConceptScore(
                    concept=r.concept,
                    score=r.score,
                    mastery_level=r.mastery_level,
                    confidence=r.confidence,
                    sample_size=r.sample_size,
                )
                for r in results.values()
            ]
        }
    except Exception as e:
        _handle_ai_errors("score", e)


@app.post("/analyze/decay", response_model=DecayCheckResponse)
def decay_endpoint(payload: DecayCheckRequest):
    try:
        history = [(item[0], float(item[1])) for item in payload.score_history]
        return detect_decay(concept=payload.concept, score_history=history)
    except Exception as e:
        _handle_ai_errors("decay", e)


@app.post("/analyze/predict-gaps", response_model=PredictiveGapResponse)
def predictive_gaps_endpoint(payload: PredictiveGapRequest):
    try:
        return predict_department_gaps(
            department=payload.department,
            competency_map=payload.competency_map,
            emerging_requirements=payload.emerging_requirements,
        )
    except Exception as e:
        _handle_ai_errors("predict_gaps", e)


# ---------- Content Ingestion ----------

@app.post("/ingest/upload", response_model=ProcessUploadResponse)
async def ingest_upload_endpoint(file: UploadFile = File(...)):
    """
    Accepts a PDF/PPTX/TXT upload, extracts and chunks its text, and
    returns the chunks ready to be passed one-by-one into
    /generate/mcq or /generate/scenario.
    """
    try:
        file_bytes = await file.read()
        chunks = process_upload(file_bytes, file.filename)
        return ProcessUploadResponse(
            filename=file.filename,
            num_chunks=len(chunks),
            chunks=chunks,
        )
    except UnsupportedFileTypeError as e:
        raise HTTPException(status_code=415, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        logger.exception("ingest_upload unexpected error")
        raise HTTPException(status_code=500, detail="Failed to process upload")
