from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta
import uuid
import models
from db import SessionLocal
from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
    get_current_user as get_current_user_util
)
from sqlmodel import Session, select


# Create API router for auth endpoints
router = APIRouter(prefix="/api/auth", tags=["authentication"])

# Pydantic models for authentication
class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", response_model=Token)
async def register(user_create: UserCreate):
    """Register a new user"""
    session = None
    try:
        session = SessionLocal()

        # Check if user already exists
        existing_user = session.exec(
            select(models.User).where(models.User.email == user_create.email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = get_password_hash(user_create.password)
        db_user = models.User(
            id=str(uuid.uuid4()),
            email=user_create.email,
            hashed_password=hashed_password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        # Create access token
        token_data = {
            "sub": db_user.id,
            "email": db_user.email,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        access_token = create_access_token(token_data)

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions (like 400 for duplicate email)
        raise
    except Exception as e:
        # Log the actual error for debugging
        print(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )
    finally:
        if session:
            session.close()


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin):
    """Authenticate user and return access token"""
    session = None
    try:
        session = SessionLocal()

        # Find user by email
        db_user = session.exec(
            select(models.User).where(models.User.email == user_login.email)
        ).first()

        if not db_user or not verify_password(user_login.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        token_data = {
            "sub": db_user.id,
            "email": db_user.email,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        access_token = create_access_token(token_data)

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions (like 401 for wrong credentials)
        raise
    except Exception as e:
        # Log the actual error for debugging
        print(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )
    finally:
        if session:
            session.close()


# Endpoint to verify token (optional, for frontend to check if token is valid)
@router.get("/verify")
async def verify(current_user: models.User = Depends(get_current_user_util)):
    """Verify the current user's token"""
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "verified": True
    }