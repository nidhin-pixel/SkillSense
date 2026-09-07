from sqlalchemy.orm import Session
from ..models import AuditLog, User

def record_audit(db: Session, *, user: User | None, action: str, resource: str, status: str = "SUCCESS", ip_address: str | None = None, details: str | None = None):
    db.add(AuditLog(user_id=user.id if user else None, action=action, resource=resource, status=status, ip_address=ip_address, details=details))
    db.commit()
