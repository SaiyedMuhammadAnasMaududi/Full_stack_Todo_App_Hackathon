from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
import os
from sqlmodel import Session
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from auth import verify_token, get_current_user, TokenData  # Import from existing auth module


def validate_user_id_match(token_data: TokenData = Depends(get_current_user), user_id: str = None) -> bool:
    """
    Validate that the user_id in the request matches the user_id in the token
    """
    if user_id and token_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in request"
        )
    return True


def get_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> str:
    """
    Extract bearer token from authorization header
    """
    return credentials.credentials