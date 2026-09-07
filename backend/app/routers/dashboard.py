from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.deps import require_admin

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/admin", response_model=schemas.AdminDashboardOut)
def admin_dashboard(db: Session = Depends(get_db), _admin: models.User = Depends(require_admin)):
    total_officers = db.query(models.User).filter(models.User.role == models.UserRole.officer).count()
    total_assessments = db.query(models.AssessmentSession).filter(
        models.AssessmentSession.completed_at.isnot(None)
    ).count()

    records = db.query(models.CompetencyRecord).all()
    buckets: dict[str, list[float]] = defaultdict(list)
    critical_by_skill: dict[str, bool] = {}
    for r in records:
        buckets[r.skill.name].append(r.level_percent)
        critical_by_skill[r.skill.name] = r.skill.is_critical

    department_averages = [
        schemas.DepartmentSkillAverage(
            skill_name=name,
            average_level=round(sum(levels) / len(levels), 1),
            officer_count=len(levels),
        )
        for name, levels in buckets.items()
    ]
    department_averages.sort(key=lambda d: d.average_level)

    critical_gaps = [
        d.skill_name for d in department_averages
        if d.average_level < 50 and critical_by_skill.get(d.skill_name)
    ]

    return schemas.AdminDashboardOut(
        total_officers=total_officers,
        total_assessments=total_assessments,
        department_averages=department_averages,
        critical_gaps=critical_gaps,
    )
