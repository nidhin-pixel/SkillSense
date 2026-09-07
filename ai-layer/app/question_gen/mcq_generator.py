"""
mcq_generator.py
-----------------
Generates multiple-choice questions from uploaded learning content using
the Groq LLM. Output is validated before being returned to the caller.
"""

import logging
from typing import Optional

from app.llm.groq_client import call_llm_json
from app.llm.prompts import MCQ_SYSTEM_PROMPT, MCQ_USER_PROMPT_TEMPLATE

logger = logging.getLogger("ai_layer.mcq_generator")


def generate_mcqs(
    content: str,
    num_questions: int = 3,
    difficulty: str = "intermediate",
    concept: Optional[str] = None,
) -> dict:
    """
    Generate MCQs from a chunk of learning content.

    Returns a dict shaped like:
        {"questions": [{question, options, correct_index, explanation,
                        concept, difficulty}, ...]}

    Raises:
        ValueError: if the LLM output fails validation.
    """
    prompt = MCQ_USER_PROMPT_TEMPLATE.format(
        num_questions=num_questions,
        content=content.strip()[:6000],  # guard against oversized inputs
        difficulty=difficulty,
        concept=concept or "not specified — infer from content",
    )

    result = call_llm_json(prompt=prompt, system_msg=MCQ_SYSTEM_PROMPT)
    _validate_mcq_output(result, expected_count=num_questions)
    return result


def _validate_mcq_output(result: dict, expected_count: int) -> None:
    """
    Basic sanity checks on the LLM's JSON output before it goes anywhere near
    the frontend. Raises ValueError on any structural problem.
    """
    if "questions" not in result or not isinstance(result["questions"], list):
        raise ValueError("LLM output missing 'questions' list")

    if len(result["questions"]) == 0:
        raise ValueError("LLM returned zero questions")

    for i, q in enumerate(result["questions"]):
        missing = [
            key
            for key in ("question", "options", "correct_index", "explanation", "concept")
            if key not in q
        ]
        if missing:
            raise ValueError(f"Question {i} missing fields: {missing}")

        if len(q["options"]) != 4:
            raise ValueError(f"Question {i} does not have exactly 4 options")

        if len(set(q["options"])) != 4:
            raise ValueError(f"Question {i} has duplicate options")

        if not (0 <= q["correct_index"] <= 3):
            raise ValueError(f"Question {i} has invalid correct_index")

    if len(result["questions"]) < expected_count:
        logger.warning(
            "Requested %d questions but only got %d — LLM may have truncated.",
            expected_count,
            len(result["questions"]),
        )
