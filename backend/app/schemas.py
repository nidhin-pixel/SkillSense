from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- Auth ----------

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    department: str = "General Administration"
    designation: str = "Officer"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: EmailStr
    role: str
    department: str
    designation: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Skills ----------

class SkillOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    parent_id: int | None
    is_critical: bool


# ---------- Questions ----------

class QuestionPublic(BaseModel):
    """Question shape sent to the client while an assessment is in progress —
    never includes the correct answer."""
    id: int
    skill_id: int
    skill_name: str
    prompt: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty: str


class SessionQuestionOut(BaseModel):
    session_id: int
    question: QuestionPublic


class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: str


class AnswerResult(BaseModel):
    is_correct: bool
    correct_option: str
    explanation: str
    next_question: QuestionPublic | None
    session_complete: bool


# ---------- Assessment sessions ----------

class SessionStart(BaseModel):
    skill_id: int


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    skill_id: int | None
    started_at: datetime
    completed_at: datetime | None
    current_difficulty: str
    score_percent: float | None
    estimated_level: str | None


# ---------- Competency ----------

class CompetencyOut(BaseModel):
    skill_id: int
    skill_name: str
    level_percent: float
    previous_level_percent: float
    confidence: str
    assessments_count: int
    last_assessed_at: datetime
    trend: str  # "improving" | "declining" | "stable"
    gap_severity: str  # "none" | "moderate" | "critical"


class PassportOut(BaseModel):
    user: UserOut
    generated_at: datetime
    competencies: list[CompetencyOut]
    overall_score: float
    strongest_skill: str | None
    weakest_skill: str | None
    recommended_focus: list[str]


# ---------- Dashboard / org ----------

class DepartmentSkillAverage(BaseModel):
    skill_name: str
    average_level: float
    officer_count: int


class AdminDashboardOut(BaseModel):
    total_officers: int
    total_assessments: int
    department_averages: list[DepartmentSkillAverage]
    critical_gaps: list[str]
