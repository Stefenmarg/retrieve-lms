import uuid
from datetime import datetime, timedelta, timezone

import jwt
from core.config import settings
from core.database import SessionLocal
from schemas.models import User


def generate_token(
    user_id: int, username: str, role: str, token_type: str = "access"
) -> str:
    token_type = token_type.lower()
    # Set token expiration time based on the token type
    expire_minutes = (
        settings.jwt_access_token_expiration_minutes
        if token_type == "access"
        else settings.jwt_refresh_token_expiration_minutes
    )
    now = datetime.now(tz=timezone.utc)
    # Insert the payload data as well as other token information
    payload = {
        "sub": str(user_id),
        "exp": now + timedelta(minutes=expire_minutes),
        "iat": now,
        "jti": str(uuid.uuid4()),
        "type": token_type,
        # Custom properties
        "username": username,
        "role": role,
    }
    # return the new tokens
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def validate_token(token: str, token_type: str | None = None) -> dict | None:
    try:
        # Extract token payload with the secret and the algorithm
        token_payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        # Check that the token type expected matches the token given
        if token_type and token_payload.get("type") != token_type.lower():
            # Token type mismatch, returns none to signify error
            return None

        db = SessionLocal()
        try:
            user_record = (
                db.query(User).filter(User.id == int(token_payload["sub"])).first()
            )
            if user_record is None:
                # User no longer exists, returns none
                return None

            if user_record.last_logout:
                last_logout_ts = user_record.last_logout.replace(
                    tzinfo=timezone.utc
                ).timestamp()
                if token_payload["iat"] < last_logout_ts:
                    return None
        finally:
            db.close()
        return token_payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def refresh_access_token(refresh_token: str) -> str | None:
    # Get payload if token is valid
    payload = validate_token(refresh_token, token_type="refresh")
    # Return None if it is invalid
    if not payload:
        return None
    # Else generate new access token and return it
    return generate_token(
        user_id=int(payload["sub"]),
        username=payload["username"],
        role=payload["role"],
        token_type="access",
    )
