from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from app.database.database import get_db
from app.models.user import User


load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


async def get_token_from_form_or_query(request: Request) -> str | None:
    """
    Extract JWT token from form field 'token' or query parameter 'token'.
    This is useful for file uploads where Authorization header may not be sent properly.
    """
    # Try query parameter first
    token = request.query_params.get("token")
    if token:
        return token

    # Try form field (works with multipart/form-data)
    try:
        form = await request.form()
        token = form.get("token")
        if token:
            return str(token)
    except Exception:
        pass

    return None


def _validate_token_and_get_user(token: str, db: Session) -> User:
    """Internal helper: decode JWT token and return the user."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Extract and validate the current user from the JWT token (strict - requires Bearer header)."""
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    return _validate_token_and_get_user(token, db)


async def get_current_user_flexible(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Extract and validate the current user using multiple methods:
    1. Authorization header (Bearer token) via OAuth2PasswordBearer
    2. Form field 'token' (for file uploads)
    3. Query parameter 'token' (for testing/debugging)
    """
    # Method 1: Token from OAuth2 scheme (Authorization header)
    if token:
        return _validate_token_and_get_user(token, db)

    # Method 2: Try form field or query parameter
    fallback_token = await get_token_from_form_or_query(request)
    if fallback_token:
        return _validate_token_and_get_user(fallback_token, db)

    # No token found via any method
    raise HTTPException(
        status_code=401,
        detail="Not authenticated. Provide Authorization header, or 'token' form/query parameter."
    )
