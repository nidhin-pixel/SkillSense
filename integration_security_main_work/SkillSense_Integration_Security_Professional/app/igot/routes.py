from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import LearningProgressRequest
from ..auth.dependencies import get_current_user
from ..audit.service import record_audit
from .adapter import IGOTAdapter

router = APIRouter(prefix="/api/igot", tags=["iGOT Integration (Demo Adapter)"])
adapter = IGOTAdapter()

@router.get("/courses", summary="Fetch recommended learning catalogue")
def courses(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record_audit(db, user=user, action="IGOT_COURSES_FETCH", resource="/api/igot/courses", ip_address=request.client.host if request.client else None)
    return {"integration_mode": "DEMO_ADAPTER", "source": "iGOT Karmayogi (mock data)", "courses": adapter.list_courses()}

@router.get("/competencies/{user_id}", summary="Read competency data through the adapter")
def competencies(user_id: int, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.id != user_id and user.role not in ("department_admin", "super_admin"):
        record_audit(db, user=user, action="IGOT_COMPETENCY_ACCESS", resource=f"/api/igot/competencies/{user_id}", status="DENIED", ip_address=request.client.host if request.client else None)
        raise HTTPException(status_code=403, detail="You can only access your own competency data")
    record_audit(db, user=user, action="IGOT_COMPETENCY_ACCESS", resource=f"/api/igot/competencies/{user_id}", ip_address=request.client.host if request.client else None)
    return {"integration_mode": "DEMO_ADAPTER", "source": "iGOT Karmayogi (mock data)", **adapter.get_competencies(user_id)}

@router.post("/learning-progress", summary="Send learning progress to the adapter")
def learning_progress(payload: LearningProgressRequest, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = adapter.accept_learning_progress(payload.model_dump())
    record_audit(db, user=user, action="IGOT_PROGRESS_PUSH", resource="/api/igot/learning-progress", ip_address=request.client.host if request.client else None, details=f"course_id={payload.course_id};progress={payload.progress_percent}")
    return {"integration_mode": "DEMO_ADAPTER", **result}
