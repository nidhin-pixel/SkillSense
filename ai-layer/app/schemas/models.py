"""
schemas/models.py
------------------
Pydantic models for request/response validation across the AI layer's
FastAPI endpoints. Keep these in sync with whatever the backend team
expects to send/receive.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class MCQGenerateRequest(BaseModel):
    content: str = Field(..., description="Raw text content to generate questions from")
    num_questions: int = Field(3, ge=1, le=20)
    difficulty: Literal["beginner", "intermediate", "advanced"] = "intermediate"
    concept: Optional[str] = None


class MCQItem(BaseModel):
    question: str
    options: List[str]
    correct_index: int
    explanation: str
    concept: str
    difficulty: str


class MCQGenerateResponse(BaseModel):
    questions: List[MCQItem]


class ScenarioGenerateRequest(BaseModel):
    concept: str
    content: str
    num_questions: int = Field(2, ge=1, le=10)


class ScenarioItem(BaseModel):
    scenario: str
    question: str
    options: List[str]
    correct_index: int
    explanation: str
    concept: str


class ScenarioGenerateResponse(BaseModel):
    questions: List[ScenarioItem]


class AssessmentResponseItem(BaseModel):
    concept: str
    question_id: str
    correct: bool


class GapAnalysisRequest(BaseModel):
    responses: List[AssessmentResponseItem]
    prerequisites: Optional[dict] = Field(
        default=None,
        description="Optional map of concept -> list of prerequisite concepts",
    )


class GapItem(BaseModel):
    concept: str
    mastery_level: Literal["none", "partial", "strong"]
    priority: int
    reason: str


class GapAnalysisResponse(BaseModel):
    gaps: List[GapItem]


class ExplainGapRequest(BaseModel):
    concept: str
    responses: List[AssessmentResponseItem]
    mastery_level: Literal["none", "partial", "strong"]
    score: float


class ExplainGapResponse(BaseModel):
    explanation: str
    recommended_next_step: str


class ScoreResponseItem(BaseModel):
    concept: str
    correct: bool
    is_scenario: bool = False


class ScoreRequest(BaseModel):
    responses: List[ScoreResponseItem]


class ConceptScore(BaseModel):
    concept: str
    score: float
    mastery_level: str
    confidence: str
    sample_size: int


class ScoreResponse(BaseModel):
    scores: List[ConceptScore]


class DecayCheckRequest(BaseModel):
    concept: str
    score_history: List[List] = Field(
        ..., description="List of [date_str, score] pairs, oldest first"
    )


class DecayCheckResponse(BaseModel):
    concept: str
    trend: Literal["improving", "stable", "decaying"]
    urgency: Literal["none", "low", "medium", "high"]
    explanation: str
    delta: float


class PredictiveGapRequest(BaseModel):
    department: str
    competency_map: dict = Field(..., description="concept -> average score 0-100")
    emerging_requirements: List[str] = Field(default_factory=list)


class PredictedGapItem(BaseModel):
    concept: str
    current_score: float
    risk_level: Literal["low", "medium", "high"]
    reason: str


class PredictiveGapResponse(BaseModel):
    predicted_gaps: List[PredictedGapItem]


class ProcessUploadResponse(BaseModel):
    filename: str
    num_chunks: int
    chunks: List[str]
