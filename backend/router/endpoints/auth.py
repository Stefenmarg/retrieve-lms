from core.config import settings
from core.database import get_db
from core.jwt import generate_token, refresh_access_token, validate_token
from core.security import hash_password
from fastapi import APIRouter, Depends, HTTPException, Response
from requests.models import TokenOut, UserCreate
from schemas.models import User, UserRole
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth")

AllowedRegistrationRoles = [role.value for role in UserRole]


@router.post("/register", response_model=TokenOut)
def Register(payload: UserCreate, response: Response, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Email already registered")

    if payload.role not in AllowedRegistrationRoles:
        raise HTTPException(400, "Invalid role")

    new_user = User(
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = generate_token(
        user_id=new_user.id,
        username=new_user.full_name,
        role=new_user.role,
        token="access",
    )

    refresh_token = generate_token(
        user_id=new_user.id,
        username=new_user.full_name,
        role=new_user.role,
        token="refresh",
    )

    response.set_cookie(
        key="retrieve_refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=settings.jwt_refresh_token_expiration_minutes*60,
        path="/api/v1/auth"
    )


    return TokenOut(token=access_token)
