from datetime import timezone
from typing import Optional

from core.database import SessionLocal
from core.jwt import validate_token
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from schemas.models import User

# We are putting auto error false in order to not automatically
# return Unaithorised on every request sent. Public endpoints need
# to be accessible without a bearer
security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> User | None:

    # Means user has not logged in / has empty cookies
    if credentials is None:
        return None

    # Get the token and the values it contains
    token = credentials.credentials
    payload = validate_token(token, token_type="access")

    # No / Invalid token thus user is not logged
    if payload is None:
        return None

    # Fetch user from database to check if account is active
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == int(payload["user_id"])).first()

        if user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        return user
    finally:
        db.close()


def require_role(required_role: str):
    def dependency(
        user: User | None = Depends(get_current_user),
        credentials: HTTPAuthorizationCredentials | None = Depends(security),
    ) -> User:
        # Check if token was provided at all
        # if not: they should login
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if user exists and token is valid
        # if not: they should refresh the token
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Wildcard so any authenticated user is allowed
        # to access that endpoint
        if required_role.lower() == "*":
            return user

        # Check if it is the role needed
        # if not: let them know with a message
        if user.role.lower() != required_role.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient role permissions",
            )

        return user

    return dependency


hash_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return hash_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return hash_context.verify(password, hashed)


# Automatic generation of a variable length password
def generate_password(length=12) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
