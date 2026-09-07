"""
prompts.py
----------
All prompt templates live here so they're easy to tune without touching
business logic. Keep prompts strict about JSON output shape — the backend
team will parse these responses directly.
"""

MCQ_SYSTEM_PROMPT = (
    "You are an expert assessment designer for India's Official Statistical "
    "System training program. You create fair, unambiguous multiple-choice "
    "questions that test real conceptual understanding, not trivia. "
    "Always respond with valid JSON only — no markdown, no commentary."
)

MCQ_USER_PROMPT_TEMPLATE = """\
Generate {num_questions} multiple-choice question(s) from the learning content below.

Learning content:
\"\"\"
{content}
\"\"\"

Difficulty level: {difficulty}  (one of: beginner, intermediate, advanced)
Target concept (if known): {concept}

Rules:
- Each question must test understanding, not simple recall of a sentence.
- Exactly 4 options per question, only one correct.
- Distractors must be plausible, not obviously wrong.
- Include a one-sentence explanation of why the correct answer is right.
- Tag each question with the concept it tests.

Respond ONLY with JSON in this exact shape:
{{
  "questions": [
    {{
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "correct_index": 0,
      "explanation": "string",
      "concept": "string",
      "difficulty": "beginner|intermediate|advanced"
    }}
  ]
}}
"""

SCENARIO_SYSTEM_PROMPT = (
    "You are an expert assessment designer creating applied, scenario-based "
    "questions that test whether a government official can APPLY a concept "
    "in a realistic work situation, not just recall it. "
    "Always respond with valid JSON only — no markdown, no commentary."
)

SCENARIO_USER_PROMPT_TEMPLATE = """\
Create {num_questions} scenario-based question(s) for the concept below, aimed at
officials working in India's Official Statistical System.

Concept: {concept}
Reference content:
\"\"\"
{content}
\"\"\"

Rules:
- Frame each question as a short realistic workplace scenario (2-4 sentences).
- Ask the official to choose the best course of action or correct interpretation.
- Provide 4 options, only one correct, with an explanation.

Respond ONLY with JSON in this exact shape:
{{
  "questions": [
    {{
      "scenario": "string",
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "correct_index": 0,
      "explanation": "string",
      "concept": "string"
    }}
  ]
}}
"""

GAP_ANALYSIS_SYSTEM_PROMPT = (
    "You are a competency analysis engine. Given a set of assessment "
    "responses mapped to concepts, identify which concepts the learner has "
    "NOT mastered and rank them by priority for relearning. "
    "Always respond with valid JSON only."
)

GAP_ANALYSIS_USER_PROMPT_TEMPLATE = """\
Here are the assessment responses for one learner, each tagged with the
concept it tests and whether the learner answered correctly:

{responses_json}

Task:
1. Group results by concept.
2. Mark a concept as "gap" if the learner got most questions on it wrong.
3. Rank gaps by priority (consider concept prerequisites if given: {prerequisites}).

Respond ONLY with JSON in this exact shape:
{{
  "gaps": [
    {{
      "concept": "string",
      "mastery_level": "none|partial|strong",
      "priority": 1,
      "reason": "string"
    }}
  ]
}}
"""

EXPLAIN_GAP_SYSTEM_PROMPT = (
    "You are an Explainable AI module for a government competency platform. "
    "Your job is to explain WHY a learner's competency score is what it is, "
    "in plain, specific, non-judgmental language. Never just say 'you are "
    "weak' — always point to the specific pattern in their responses. "
    "Always respond with valid JSON only."
)

EXPLAIN_GAP_USER_PROMPT_TEMPLATE = """\
Learner's responses for concept "{concept}":
{responses_json}

Computed mastery level: {mastery_level}
Computed score: {score}

Write a short, specific, human-readable explanation (2-3 sentences) of why
the learner received this mastery level, referencing the actual pattern of
right/wrong answers (e.g. "struggled with scenario-based questions but did
fine on definitions"). Also suggest one concrete next step.

Respond ONLY with JSON in this exact shape:
{{
  "explanation": "string",
  "recommended_next_step": "string"
}}
"""

DECAY_EXPLANATION_SYSTEM_PROMPT = (
    "You are a competency-decay analysis module. Given a time series of "
    "scores for a concept, explain whether the learner's knowledge is "
    "decaying, stable, or improving, and how urgent revision is. "
    "Always respond with valid JSON only."
)

DECAY_EXPLANATION_USER_PROMPT_TEMPLATE = """\
Concept: {concept}
Score history (oldest to newest, as [date, score] pairs):
{score_history_json}

Task:
- Determine the trend: "improving", "stable", or "decaying".
- Estimate urgency of revision: "none", "low", "medium", "high".
- Give a one-sentence, plain-language explanation.

Respond ONLY with JSON in this exact shape:
{{
  "trend": "improving|stable|decaying",
  "urgency": "none|low|medium|high",
  "explanation": "string"
}}
"""

PREDICTIVE_GAP_SYSTEM_PROMPT = (
    "You are a forward-looking skills-planning module for a government "
    "department. Given a department's current competency map and known "
    "emerging requirements, predict which skills are likely to become "
    "critical gaps soon. Always respond with valid JSON only."
)

PREDICTIVE_GAP_USER_PROMPT_TEMPLATE = """\
Department: {department}
Current competency map (concept -> average score 0-100):
{competency_map_json}

Emerging/known upcoming requirements for this department:
{emerging_requirements}

Task:
Identify 1-5 skills likely to become critical gaps within the next few
months, considering both current weak areas and emerging requirements.

Respond ONLY with JSON in this exact shape:
{{
  "predicted_gaps": [
    {{
      "concept": "string",
      "current_score": 0,
      "risk_level": "low|medium|high",
      "reason": "string"
    }}
  ]
}}
"""
