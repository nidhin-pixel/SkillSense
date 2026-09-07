from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..database import get_db
from ..models import User
from ..schemas import LoginRequest, TokenResponse, UserResponse
from ..security import verify_password, create_access_token
from ..audit.service import record_audit
from .dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse, summary="Authenticate a user")
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    ip = request.client.host if request.client else None
    if not user or not user.is_active or not verify_password(data.password, user.password_hash):
        record_audit(db, user=user, action="LOGIN_FAILED", resource="/api/auth/login", status="FAILED", ip_address=ip, details=f"email={data.email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    record_audit(db, user=user, action="LOGIN_SUCCESS", resource="/api/auth/login", ip_address=ip)
    return {"access_token": create_access_token(user.id, user.role), "token_type": "bearer", "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60}

@router.get("/me", response_model=UserResponse, summary="Return the authenticated user's profile")
def me(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record_audit(db, user=current_user, action="PROFILE_VIEW", resource="/api/auth/me", ip_address=request.client.host if request.client else None)
    return current_user
