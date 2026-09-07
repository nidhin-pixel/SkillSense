from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .config import APP_NAME, CORS_ORIGINS
from .database import Base, engine, SessionLocal, get_db
from .models import User
from .security import hash_password
from .auth.routes import router as auth_router
from .auth.dependencies import get_current_user, require_roles
from .audit.routes import router as audit_router
from .igot.routes import router as igot_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_demo_users()
    yield

app = FastAPI(
    title=f"{APP_NAME} — Integration & Security API",
    version="2.0.0",
    description="Hackathon reference implementation for secure authentication, RBAC, auditability and an iGOT integration boundary.",
    lifespan=lifespan,
)
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type"])

def seed_demo_users():
    db = SessionLocal()
    try:
        demo = [
            ("official@example.com", "Demo Official", "official", "Education"),
            ("department@example.com", "Demo Department Admin", "department_admin", "Education"),
            ("admin@example.com", "Demo Super Admin", "super_admin", "NCIDE"),
        ]
        for email, name, role, dept in demo:
            if not db.query(User).filter(User.email == email).first():
                db.add(User(email=email, full_name=name, role=role, department=dept, password_hash=hash_password("Demo@12345")))
        db.commit()
    finally:
        db.close()

app.include_router(auth_router)
app.include_router(audit_router)
app.include_router(igot_router)

@app.get("/", tags=["System"])
def root():
    return {"application": APP_NAME, "module": "Integration & Security", "status": "operational", "api_version": "2.0.0"}

@app.get("/api/official/dashboard", tags=["RBAC"])
def official_dashboard(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome {current_user.full_name}", "role": current_user.role, "access_scope": "official"}

@app.get("/api/admin/users", tags=["RBAC"])
def department_users(current_user: User = Depends(require_roles("department_admin", "super_admin")), db: Session = Depends(get_db)):
    return [{"id": u.id, "email": u.email, "name": u.full_name, "role": u.role, "department": u.department, "active": bool(u.is_active)} for u in db.query(User).order_by(User.id).all()]

@app.get("/api/admin/system", tags=["RBAC"])
def system_admin(current_user: User = Depends(require_roles("super_admin"))):
    return {"message": "Super-admin access granted", "role": current_user.role, "scope": "system"}
