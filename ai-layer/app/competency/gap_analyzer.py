"""
gap_analyzer.py
-----------------
Concept-level competency gap detection. Uses the LLM to interpret patterns
in a learner's responses and the knowledge graph to prioritize gaps by
prerequisite chains (e.g. "Incident Analysis is weak because Network
Attacks — its prerequisite — is also weak").
"""

import json
import logging
from typing import List, Dict

from app.llm.groq_client import call_llm_json
from app.llm.prompts import (
    GAP_ANALYSIS_SYSTEM_PROMPT,
    GAP_ANALYSIS_USER_PROMPT_TEMPLATE,
    EXPLAIN_GAP_SYSTEM_PROMPT,
    EXPLAIN_GAP_USER_PROMPT_TEMPLATE,
)
from app.competency import knowledge_graph as kg

logger = logging.getLogger("ai_layer.gap_analyzer")


def analyze_gaps(responses: List[Dict]) -> dict:
    """
    responses: list of {"concept": str, "question_id": str, "correct": bool}

    Returns: {"gaps": [{concept, mastery_level, priority, reason}, ...]}
    """
    if not responses:
        raise ValueError("No responses provided for gap analysis")

    concepts = list({r["concept"] for r in responses})
    prerequisites = kg.build_prerequisite_map(concepts)

    prompt = GAP_ANALYSIS_USER_PROMPT_TEMPLATE.format(
        responses_json=json.dumps(responses, indent=2),
        prerequisites=json.dumps(prerequisites),
    )
    result = call_llm_json(prompt=prompt, system_msg=GAP_ANALYSIS_SYSTEM_PROMPT)
    _validate_gap_output(result)
    return result


def explain_gap(concept: str, responses: List[Dict], mastery_level: str, score: float) -> dict:
    """
    Explainable AI: produce a human-readable reason for a computed mastery
    level, plus a concrete next step. This is what turns "you are weak"
    into a specific, trustworthy explanation.
    """
    prompt = EXPLAIN_GAP_USER_PROMPT_TEMPLATE.format(
        concept=concept,
        responses_json=json.dumps(responses, indent=2),
        mastery_level=mastery_level,
        score=score,
    )
    result = call_llm_json(prompt=prompt, system_msg=EXPLAIN_GAP_SYSTEM_PROMPT)

    if "explanation" not in result or "recommended_next_step" not in result:
        raise ValueError("Explanation output missing required fields")

    return result


def _validate_gap_output(result: dict) -> None:
    if "gaps" not in result or not isinstance(result["gaps"], list):
        raise ValueError("LLM output missing 'gaps' list")

    for i, g in enumerate(result["gaps"]):
        missing = [k for k in ("concept", "mastery_level", "priority", "reason") if k not in g]
        if missing:
            raise ValueError(f"Gap item {i} missing fields: {missing}")
        if g["mastery_level"] not in ("none", "partial", "strong"):
            raise ValueError(f"Gap item {i} has invalid mastery_level: {g['mastery_level']}")
