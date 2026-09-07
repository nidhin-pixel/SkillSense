from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.deps import get_current_user
from app.ai.competency_engine import gap_severity

router = APIRouter(prefix="/competency", tags=["competency"])


def _build_competency_out(record: models.CompetencyRecord) -> schemas.CompetencyOut:
    trend = "stable"
    if record.level_percent > record.previous_level_percent + 2:
        trend = "improving"
    elif record.level_percent < record.previous_level_percent - 2:
        trend = "declining"

    return schemas.CompetencyOut(
        skill_id=record.skill_id,
        skill_name=record.skill.name,
        level_percent=record.level_percent,
        previous_level_percent=record.previous_level_percent,
        confidence=record.confidence.value if hasattr(record.confidence, "value") else record.confidence,
        assessments_count=record.assessments_count,
        last_assessed_at=record.last_assessed_at,
        trend=trend,
        gap_severity=gap_severity(record.level_percent, record.skill.is_critical),
    )


@router.get("/passport", response_model=schemas.PassportOut)
def get_passport(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    records = (
        db.query(models.CompetencyRecord)
        .filter(models.CompetencyRecord.user_id == user.id)
        .all()
    )
    competencies = [_build_competency_out(r) for r in records]

    overall = round(sum(c.level_percent for c in competencies) / len(competencies), 1) if competencies else 0.0
    strongest = max(competencies, key=lambda c: c.level_percent).skill_name if competencies else None
    weakest = min(competencies, key=lambda c: c.level_percent).skill_name if competencies else None
    recommended = [c.skill_name for c in sorted(competencies, key=lambda c: c.level_percent)[:2]]

    return schemas.PassportOut(
        user=schemas.UserOut.model_validate(user),
        generated_at=datetime.now(timezone.utc),
        competencies=competencies,
        overall_score=overall,
        strongest_skill=strongest,
        weakest_skill=weakest,
        recommended_focus=recommended,
    )
