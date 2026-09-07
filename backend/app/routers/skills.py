from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.deps import get_current_user

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=list[schemas.SkillOut])
def list_skills(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(models.Skill).all()
