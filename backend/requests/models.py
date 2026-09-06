from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class TokenOut(BaseModel):
    token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=8)
    role: Literal["teacher", "student", "admin"] = "student"
