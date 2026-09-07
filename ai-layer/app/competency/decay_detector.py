"""
decay_detector.py
--------------------
Two related "forward/backward looking" features from the vision doc:

1. Competency Decay Detection — is a learner FORGETTING a concept over time?
2. Predictive Skill Gap Detection — which department-level skills are
   likely to become critical gaps soon?

Both use simple statistical checks first (cheap, deterministic) and only
call the LLM to generate a human-readable explanation — we don't want the
LLM deciding the trend itself, since that should be based on real numbers.
"""

import json
import logging
from typing import List, Tuple, Dict

from app.llm.groq_client import call_llm_json
from app.llm.prompts import (
    DECAY_EXPLANATION_SYSTEM_PROMPT,
    DECAY_EXPLANATION_USER_PROMPT_TEMPLATE,
    PREDICTIVE_GAP_SYSTEM_PROMPT,
    PREDICTIVE_GAP_USER_PROMPT_TEMPLATE,
)

logger = logging.getLogger("ai_layer.decay_detector")

# A drop of more than this many points between the earliest and latest
# score (or a sustained downward trend) is treated as decay.
DECAY_THRESHOLD_POINTS = 10


def detect_decay(concept: str, score_history: List[Tuple[str, float]]) -> dict:
    """
    score_history: list of (date_str, score) tuples, oldest first.
    e.g. [("2026-01-15", 82.0), ("2026-03-10", 79.0), ("2026-06-01", 65.0)]

    Returns: {"trend", "urgency", "explanation", "delta"}
    """
    if len(score_history) < 2:
        raise ValueError("Need at least 2 data points to detect decay")

    scores = [s for _, s in score_history]
    delta = round(scores[-1] - scores[0], 1)

    # Deterministic trend classification (not left to the LLM).
    if delta <= -DECAY_THRESHOLD_POINTS:
        computed_trend = "decaying"
    elif delta >= DECAY_THRESHOLD_POINTS:
        computed_trend = "improving"
    else:
        computed_trend = "stable"

    prompt = DECAY_EXPLANATION_USER_PROMPT_TEMPLATE.format(
        concept=concept,
        score_history_json=json.dumps(score_history),
    )
    llm_result = call_llm_json(prompt=prompt, system_msg=DECAY_EXPLANATION_SYSTEM_PROMPT)

    return {
        "concept": concept,
        "trend": computed_trend,  # trust our own math over the LLM's guess
        "urgency": llm_result.get("urgency", "medium"),
        "explanation": llm_result.get("explanation", ""),
        "delta": delta,
    }


def predict_department_gaps(
    department: str,
    competency_map: Dict[str, float],
    emerging_requirements: List[str],
) -> dict:
    """
    competency_map: {concept: average_score_0_to_100}
    emerging_requirements: free-text list, e.g. ["AI Governance", "Cloud migration"]

    Returns: {"predicted_gaps": [{concept, current_score, risk_level, reason}]}
    """
    prompt = PREDICTIVE_GAP_USER_PROMPT_TEMPLATE.format(
        department=department,
        competency_map_json=json.dumps(competency_map, indent=2),
        emerging_requirements=", ".join(emerging_requirements) or "None specified",
    )
    result = call_llm_json(prompt=prompt, system_msg=PREDICTIVE_GAP_SYSTEM_PROMPT)

    if "predicted_gaps" not in result:
        raise ValueError("Predictive gap output missing 'predicted_gaps'")

    return result
