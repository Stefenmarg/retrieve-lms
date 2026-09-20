from typing import Literal

from pydantic import BaseModel, EmailStr, Field


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
    role: Literal["teacher", "student", "admin"] = "student"


# Received by the login form
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
