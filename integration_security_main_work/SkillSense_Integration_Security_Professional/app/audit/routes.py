from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AuditLog, User
from ..auth.dependencies import require_roles
from .service import record_audit

router = APIRouter(prefix="/api/audit", tags=["Audit"])

@router.get("", summary="View security audit events")
def list_audit_logs(request: Request, current_user: User = Depends(require_roles("super_admin")), db: Session = Depends(get_db)):
    record_audit(db, user=current_user, action="AUDIT_LOG_VIEW", resource="/api/audit", ip_address=request.client.host if request.client else None)
    rows = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(200).all()
    return [{"id": r.id, "user_id": r.user_id, "action": r.action, "resource": r.resource, "status": r.status, "ip_address": r.ip_address, "timestamp": r.timestamp.isoformat(), "details": r.details} for r in rows]
