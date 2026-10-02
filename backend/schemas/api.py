from typing import Literal

from models.database import CourseEntryType, UserRole
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Generic model for feedback to the frontend
class Feedback(BaseModel):
    status: str
    message: str


# Sent after login
class TokenOut(BaseModel):
    token: str
    token_type: str = "bearer"


# Received by the register form
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=8)
    role: UserRole = UserRole.STUDENT


# Received by the login form
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    llm_enabled: bool = False
    restriction_status: CourseEntryType = CourseEntryType.OPEN


class CourseJoin(BaseModel):
    course_id: int
    message: str | None = None
