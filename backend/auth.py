from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
import models
from db import SessionLocal
from sqlmodel import Session, select
import hashlib
import secrets


# Security configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", os.getenv("SECRET_KEY", "your-secret-key-here"))  # Use BETTER_AUTH_SECRET as primary
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Initialize HTTP Bearer token scheme
security = HTTPBearer()


# Pydantic models for authentication
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str
    email: str


# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    The hashed_password is expected to be in format: salt:hash
    """
    try:
        # Split the stored hash to get salt and hash
        parts = hashed_password.split('$')
        if len(parts) != 2:
            return False

        salt, stored_hash = parts
        # Hash the plain password with the same salt
        computed_hash = hashlib.sha256((plain_password + salt).encode('utf-8')).hexdigest()

        # Compare the computed hash with the stored hash
        return computed_hash == stored_hash
    except Exception as e:
        print(f"Password verification error: {str(e)}")
        return False


def get_password_hash(password: str) -> str:
    """
    Generate a salted hash for the password.
    Returns a string in format: salt$hash
    """
    # Generate a random salt
    salt = secrets.token_hex(32)
    # Hash the password with the salt
    hashed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    # Return salt and hash combined with a separator
    return f"{salt}${hashed}"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        if user_id is None or email is None:
            return None
        token_data = TokenData(user_id=user_id, email=email)
        return token_data
    except JWTError:
        return None


# Dependency to get current user from JWT token
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    token_data = verify_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user exists in the database
    session = None
    try:
        session = SessionLocal()
        user = session.exec(select(models.User).where(models.User.id == token_data.user_id)).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except HTTPException:
        # Re-raise HTTP exceptions (like 401 for invalid credentials)
        raise
    except Exception as e:
        # Log the actual error for debugging
        print(f"Get current user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user: {str(e)}"
        )
    finally:
        if session:
            session.close()


# Additional authentication utilities can be added here