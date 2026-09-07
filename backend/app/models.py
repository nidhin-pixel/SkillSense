import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
)
from sqlalchemy.orm import relationship

from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class UserRole(str, enum.Enum):
    officer = "officer"
    admin = "admin"


class Difficulty(str, enum.Enum):
    basic = "basic"
    intermediate = "intermediate"
    advanced = "advanced"
    scenario = "scenario"


class ConfidenceLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(180), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.officer, nullable=False)
    department = Column(String(120), default="General Administration")
    designation = Column(String(120), default="Officer")
    created_at = Column(DateTime, default=utcnow)

    competency_records = relationship("CompetencyRecord", back_populates="user")
    sessions = relationship("AssessmentSession", back_populates="user")


class Skill(Base):
    """A node in the Skill Knowledge Graph. parent_id lets skills nest,
    e.g. Cybersecurity -> Incident Response -> Detection."""

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, default="")
    parent_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    is_critical = Column(Boolean, default=False)

    parent = relationship("Skill", remote_side=[id], backref="children")
    questions = relationship("Question", back_populates="skill")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    prompt = Column(Text, nullable=False)
    option_a = Column(String(300), nullable=False)
    option_b = Column(String(300), nullable=False)
    option_c = Column(String(300), nullable=False)
    option_d = Column(String(300), nullable=False)
    correct_option = Column(String(1), nullable=False)  # 'a' | 'b' | 'c' | 'd'
    difficulty = Column(Enum(Difficulty), default=Difficulty.basic)
    explanation = Column(Text, default="")
    is_ai_generated = Column(Boolean, default=False)

    skill = relationship("Skill", back_populates="questions")


class AssessmentSession(Base):
    """One adaptive assessment attempt by an officer, optionally scoped to a skill."""

    __tablename__ = "assessment_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    started_at = Column(DateTime, default=utcnow)
    completed_at = Column(DateTime, nullable=True)
    current_difficulty = Column(Enum(Difficulty), default=Difficulty.basic)
    score_percent = Column(Float, nullable=True)
    estimated_level = Column(String(30), nullable=True)  # Beginner..Expert

    user = relationship("User", back_populates="sessions")
    responses = relationship("AssessmentResponse", back_populates="session")


class AssessmentResponse(Base):
    __tablename__ = "assessment_responses"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_option = Column(String(1), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime, default=utcnow)

    session = relationship("AssessmentSession", back_populates="responses")
    question = relationship("Question")


class CompetencyRecord(Base):
    """The living Competency Passport entry: one row per user per skill,
    continuously updated rather than a one-time score."""

    __tablename__ = "competency_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    level_percent = Column(Float, default=0.0)
    previous_level_percent = Column(Float, default=0.0)
    confidence = Column(Enum(ConfidenceLevel), default=ConfidenceLevel.low)
    assessments_count = Column(Integer, default=0)
    last_assessed_at = Column(DateTime, default=utcnow)

    user = relationship("User", back_populates="competency_records")
    skill = relationship("Skill")
