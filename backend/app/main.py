from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.routers import auth, skills, assessment, competency, dashboard

settings = get_settings()

# In a real deployment use Alembic migrations; create_all is fine for the
# hackathon MVP / local development.
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(skills.router)
app.include_router(assessment.router)
app.include_router(competency.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"service": settings.app_name, "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}
