from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import Index

# Define SQLModel base class
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    # Define composite indexes
    __table_args__ = (
        Index("idx_user_completed_created", "user_id", "completed", "created_at"),
        Index("idx_user_completed", "user_id", "completed"),
        Index("idx_completed_created", "completed", "created_at"),
    )

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None, index=True)
    completed: bool = Field(default=False, index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationship to user
    user: User = Relationship(back_populates="tasks")