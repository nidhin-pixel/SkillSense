"""
AI Layer: competency scoring and gap analysis.

Implements a simplified Item-Response-Theory-style adaptive step function
(difficulty rises on correct answers, falls on incorrect ones) plus the
evidence-based competency scoring and decay/confidence model described in
the SkillSense concept doc.
"""
from datetime import datetime, timezone

DIFFICULTY_ORDER = ["basic", "intermediate", "advanced", "scenario"]

DIFFICULTY_WEIGHT = {
    "basic": 1.0,
    "intermediate": 1.5,
    "advanced": 2.0,
    "scenario": 2.5,
}

LEVEL_BANDS = [
    (0, 20, "Beginner"),
    (20, 45, "Basic"),
    (45, 70, "Intermediate"),
    (70, 90, "Advanced"),
    (90, 101, "Expert"),
]


def next_difficulty(current_difficulty: str, was_correct: bool) -> str:
    idx = DIFFICULTY_ORDER.index(current_difficulty)
    if was_correct:
        idx = min(idx + 1, len(DIFFICULTY_ORDER) - 1)
    else:
        idx = max(idx - 1, 0)
    return DIFFICULTY_ORDER[idx]


def score_session(responses: list[dict]) -> dict:
    """responses: [{"difficulty": "basic", "is_correct": bool}, ...]"""
    if not responses:
        return {"score_percent": 0.0, "estimated_level": "Beginner"}

    earned = sum(DIFFICULTY_WEIGHT[r["difficulty"]] for r in responses if r["is_correct"])
    possible = sum(DIFFICULTY_WEIGHT[r["difficulty"]] for r in responses)
    score_percent = round((earned / possible) * 100, 1) if possible else 0.0

    level = next(
        label for low, high, label in LEVEL_BANDS if low <= score_percent < high
    )
    return {"score_percent": score_percent, "estimated_level": level}


def confidence_for(assessments_count: int) -> str:
    if assessments_count >= 5:
        return "high"
    if assessments_count >= 2:
        return "medium"
    return "low"


def update_competency_record(
    previous_level: float,
    previous_assessments: int,
    new_session_score: float,
) -> dict:
    """
    Blend the new session score into the running competency level rather than
    overwriting it — recent evidence matters more, but a single bad day
    doesn't erase a track record (and vice versa).
    """
    if previous_assessments == 0:
        blended = new_session_score
    else:
        # Weighted toward the newest evidence (60/40) so the record stays
        # responsive to real, current capability.
        blended = round(previous_level * 0.4 + new_session_score * 0.6, 1)

    trend = "stable"
    if blended > previous_level + 2:
        trend = "improving"
    elif blended < previous_level - 2:
        trend = "declining"

    return {
        "level_percent": blended,
        "previous_level_percent": previous_level,
        "assessments_count": previous_assessments + 1,
        "confidence": confidence_for(previous_assessments + 1),
        "trend": trend,
        "last_assessed_at": datetime.now(timezone.utc),
    }


def gap_severity(level_percent: float, is_critical_skill: bool) -> str:
    if level_percent < 40:
        return "critical" if is_critical_skill else "moderate"
    if level_percent < 60:
        return "moderate"
    return "none"
