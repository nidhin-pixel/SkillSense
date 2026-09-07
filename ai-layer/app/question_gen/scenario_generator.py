"""
scenario_generator.py
-----------------------
Generates realistic, applied scenario-based questions (as opposed to plain
recall MCQs). These test whether an official can actually apply a concept.
"""

import logging
from app.llm.groq_client import call_llm_json
from app.llm.prompts import SCENARIO_SYSTEM_PROMPT, SCENARIO_USER_PROMPT_TEMPLATE

logger = logging.getLogger("ai_layer.scenario_generator")


def generate_scenarios(concept: str, content: str, num_questions: int = 2) -> dict:
    """
    Generate scenario-based questions for a given concept.

    Returns:
        {"questions": [{scenario, question, options, correct_index,
                        explanation, concept}, ...]}
    """
    prompt = SCENARIO_USER_PROMPT_TEMPLATE.format(
        num_questions=num_questions,
        concept=concept,
        content=content.strip()[:6000],
    )
    result = call_llm_json(prompt=prompt, system_msg=SCENARIO_SYSTEM_PROMPT)
    _validate_scenario_output(result)
    return result


def _validate_scenario_output(result: dict) -> None:
    if "questions" not in result or not isinstance(result["questions"], list):
        raise ValueError("LLM output missing 'questions' list")
    if len(result["questions"]) == 0:
        raise ValueError("LLM returned zero scenario questions")

    for i, q in enumerate(result["questions"]):
        missing = [
            key
            for key in ("scenario", "question", "options", "correct_index", "explanation", "concept")
            if key not in q
        ]
        if missing:
            raise ValueError(f"Scenario question {i} missing fields: {missing}")
        if len(q["options"]) != 4:
            raise ValueError(f"Scenario question {i} does not have exactly 4 options")
        if not (0 <= q["correct_index"] <= 3):
            raise ValueError(f"Scenario question {i} has invalid correct_index")
