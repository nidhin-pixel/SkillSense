"""
AI Layer: question generation.

If GROQ_API_KEY is configured, questions are generated live from the skill's
name/description using an LLM. Otherwise the app falls back to a small
rule-based template bank so the rest of the platform (assessment engine,
scoring, passport) keeps working out of the box during development/demos.

This module intentionally exposes one function, `generate_question`, so the
rest of the app never needs to know whether a question came from the LLM or
the fallback bank.
"""
import json
import random

from app.config import get_settings

settings = get_settings()

_FALLBACK_BANK = {
    "basic": [
        "What is the primary purpose of {skill}?",
        "Which of the following best defines {skill}?",
        "{skill} is most closely related to which of these concepts?",
    ],
    "intermediate": [
        "In practice, which action would improve {skill} outcomes?",
        "Which factor most commonly causes failures related to {skill}?",
        "How does {skill} typically interact with related processes in a government office?",
    ],
    "scenario": [
        "An officer encounters a real-world situation involving {skill}. "
        "What is the most appropriate first response?",
        "During a department audit, a gap in {skill} is discovered. "
        "What should be prioritised next?",
    ],
}


def _fallback_question(skill_name: str, difficulty: str) -> dict:
    templates = _FALLBACK_BANK.get(difficulty, _FALLBACK_BANK["basic"])
    prompt = random.choice(templates).format(skill=skill_name)
    correct = random.choice(["a", "b", "c", "d"])
    options = {
        "a": f"Apply standard {skill_name} best practice",
        "b": f"Ignore the {skill_name} requirement",
        "c": f"Escalate without reviewing {skill_name} guidance",
        "d": f"Postpone the {skill_name} action indefinitely",
    }
    # Make sure the "correct" slot always holds the sound answer.
    options[correct] = f"Apply standard {skill_name} best practice"
    if correct != "a":
        options["a"] = f"Delay action until further {skill_name} training"

    return {
        "prompt": prompt,
        "option_a": options["a"],
        "option_b": options["b"],
        "option_c": options["c"],
        "option_d": options["d"],
        "correct_option": correct,
        "explanation": (
            f"This tests applied understanding of {skill_name} rather than "
            f"rote recall, in line with SkillSense's concept-level assessment model."
        ),
        "is_ai_generated": False,
    }


def _llm_question(skill_name: str, skill_description: str, difficulty: str) -> dict | None:
    if not settings.groq_api_key:
        return None
    try:
        from groq import Groq

        client = Groq(api_key=settings.groq_api_key)
        system = (
            "You are the AI question-generation layer of SkillSense, a "
            "competency assessment platform for Indian government officials. "
            "Generate exactly one multiple-choice question and reply with "
            "ONLY valid JSON, no markdown fences, no preamble."
        )
        user = f"""
Skill: {skill_name}
Skill description: {skill_description or "N/A"}
Difficulty: {difficulty} (basic | intermediate | advanced | scenario)

Return JSON with these exact keys:
prompt, option_a, option_b, option_c, option_d, correct_option (one of "a","b","c","d"), explanation

If difficulty is "scenario", frame the prompt as a realistic workplace situation
for a government official rather than a definition question.
"""
        completion = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.7,
        )
        raw = completion.choices[0].message.content.strip()
        raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(raw)
        data["is_ai_generated"] = True
        return data
    except Exception:
        # Any LLM/network/parsing failure silently falls back so the
        # assessment flow never breaks in front of an officer.
        return None


def generate_question(skill_name: str, skill_description: str, difficulty: str) -> dict:
    return _llm_question(skill_name, skill_description, difficulty) or _fallback_question(
        skill_name, difficulty
    )
