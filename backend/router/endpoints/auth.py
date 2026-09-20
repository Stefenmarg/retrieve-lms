from datetime import datetime, timezone

from core.config import settings
from core.database import get_db
from core.jwt import generate_token, refresh_access_token, validate_token
from core.security import get_current_user, hash_password, verify_password
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from requests.models import Feedback, TokenOut, UserCreate, UserLogin
from schemas.models import User, UserRole
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth")

AllowedRegistrationRoles = [role.value for role in UserRole]


# Private function that sets the server side cookie
def _set_refresh_token_cookie(response, refresh_token):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.app_debug,
        samesite="strict",
        max_age=settings.jwt_refresh_token_expiration_minutes * 60,
        path="/api/v1/auth",
    )


@router.post("/register", response_model=Feedback, status_code=201)
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

    # Write the user to the database, commit the data to the database
    # and commit so no race condition with the unique fields happens
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Email already registered")

    return Feedback(status="ok", message="Account created successfully")


@router.post("/login", response_model=TokenOut)
def Login(payload: UserLogin, response: Response, db: Session = Depends(get_db)):
    # Verify that the user exists and has an active account
    user = (
        db.query(User)
        .filter(User.email == payload.email, User.is_active == True)
        .first()
    )

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    # Get user data that will be part of the token
    claims = dict(user_id=user.id, full_name=user.full_name, role=user.role)

    # Generate the access and refresh tokens with the user data
    access_token = generate_token(
        **claims,
        token_type="access",
    )

    refresh_token = generate_token(
        **claims,
        token_type="refresh",
    )

    _set_refresh_token_cookie(response=response, refresh_token=refresh_token)

    return TokenOut(token=access_token)


# This is a check endpoint that the frontend uses
# to verify token validity
@router.get("/status", response_model=Feedback)
def status(user: User | None = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return Feedback(status="ok", message="Authenticated")


@router.post("/refresh", response_model=TokenOut)
def refresh(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Get the refresh token from the cookie
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(401, "Refresh token missing")

    # Try to extract the data from the refresh token after it gets validated
    try:
        payload = validate_token(refresh_token, token_type="refresh")
    except Exception:
        raise HTTPException(401, "Invalid or expired refresh token")

    if not payload:
        raise HTTPException(401, "Invalid or expired refresh token")

    if settings.app_debug:
        print(payload)

    # Check that the user id is valid
    user_id = int(payload["user_id"])
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(401, "User not found")

    # Get user data that will be part of the token
    claims = dict(user_id=user.id, full_name=user.full_name, role=user.role)

    # Generate the access and refresh tokens with the user data
    access_token = generate_token(**claims, token_type="access")
    new_refresh = generate_token(**claims, token_type="refresh")

    _set_refresh_token_cookie(response=response, refresh_token=new_refresh)
    return TokenOut(token=access_token)


@router.post("/logout", response_model=Feedback)
def logout(
    response: Response,
    user: User | None = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Delete the server cookie with the refresh token
    response.delete_cookie(
        key="refresh_token",
        path="/api/v1/auth",
        httponly=True,
        secure=not settings.app_debug,
        samesite="strict",
    )
    return Feedback(status="ok", message="Logged out successfully")
