from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    department: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class LearningProgressRequest(BaseModel):
    course_id: str
    progress_percent: int = Field(ge=0, le=100)
    status: str = Field(default="IN_PROGRESS", max_length=30)
