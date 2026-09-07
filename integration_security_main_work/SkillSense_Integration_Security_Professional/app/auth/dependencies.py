from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..security import decode_token
from ..audit.service import record_audit

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload or not payload.get("sub"):
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    try:
        user_id = int(payload["sub"])
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid access token")
    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User account is unavailable")
    return user

def require_roles(*roles):
    def checker(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        if current_user.role not in roles:
            record_audit(db, user=current_user, action="ACCESS_DENIED", resource=request.url.path, status="DENIED", ip_address=request.client.host if request.client else None, details=f"required_roles={','.join(roles)}")
            raise HTTPException(status_code=403, detail="Insufficient permissions for this resource")
        return current_user
    return checker
