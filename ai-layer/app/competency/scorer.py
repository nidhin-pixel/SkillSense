"""
scorer.py
---------
Evidence-based competency scoring. Combines multiple signals instead of a
single exam score, and reports a confidence level based on sample size —
matching the "Competency Confidence Score" concept from the vision doc.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ResponseRecord:
    concept: str
    correct: bool
    is_scenario: bool = False  # scenario questions weigh more (application)


@dataclass
class CompetencyResult:
    concept: str
    score: float  # 0-100
    mastery_level: str  # none | partial | strong
    confidence: str  # low | medium | high
    sample_size: int


# Scenario-based (applied) questions count more toward the score than
# plain recall MCQs, per the vision doc's "application gap" distinction.
RECALL_WEIGHT = 1.0
SCENARIO_WEIGHT = 1.5

# Minimum number of responses needed to reach each confidence tier.
CONFIDENCE_THRESHOLDS = {"high": 8, "medium": 3}


def compute_concept_score(responses: List[ResponseRecord]) -> CompetencyResult:
    """
    Compute a weighted competency score for a single concept from its
    response history.
    """
    if not responses:
        raise ValueError("Cannot score a concept with zero responses")

    concept = responses[0].concept
    total_weight = 0.0
    earned_weight = 0.0

    for r in responses:
        weight = SCENARIO_WEIGHT if r.is_scenario else RECALL_WEIGHT
        total_weight += weight
        if r.correct:
            earned_weight += weight

    score = round((earned_weight / total_weight) * 100, 1)
    mastery_level = _score_to_mastery(score)
    confidence = _sample_size_to_confidence(len(responses))

    return CompetencyResult(
        concept=concept,
        score=score,
        mastery_level=mastery_level,
        confidence=confidence,
        sample_size=len(responses),
    )


def compute_all_scores(all_responses: List[ResponseRecord]) -> Dict[str, CompetencyResult]:
    """Group responses by concept and score each one."""
    by_concept: Dict[str, List[ResponseRecord]] = {}
    for r in all_responses:
        by_concept.setdefault(r.concept, []).append(r)

    return {
        concept: compute_concept_score(records)
        for concept, records in by_concept.items()
    }


def compute_improvement(previous_score: float, current_score: float) -> Dict[str, float]:
    """Simple improvement-delta helper for the 'Improvement Intelligence' feature."""
    delta = round(current_score - previous_score, 1)
    return {
        "previous_score": previous_score,
        "current_score": current_score,
        "improvement": delta,
        "direction": "up" if delta > 0 else ("down" if delta < 0 else "flat"),
    }


def _score_to_mastery(score: float) -> str:
    if score >= 75:
        return "strong"
    if score >= 40:
        return "partial"
    return "none"


def _sample_size_to_confidence(n: int) -> str:
    if n >= CONFIDENCE_THRESHOLDS["high"]:
        return "high"
    if n >= CONFIDENCE_THRESHOLDS["medium"]:
        return "medium"
    return "low"
