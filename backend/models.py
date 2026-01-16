from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, CheckConstraint
from typing import Optional, Literal
from pydantic import Json
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


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationship with messages
    messages: list["Message"] = Relationship(back_populates="conversation", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id")
    sender_type: str = Field(sa_column=Column(String, CheckConstraint("sender_type IN ('user', 'assistant')")))
    content: str = Field(max_length=10000)
    role: str = Field(sa_column=Column(String, CheckConstraint("role IN ('user', 'assistant', 'tool_call', 'tool_response')")))
    tool_calls: Optional[str] = Field(default=None)  # JSON string
    tool_responses: Optional[str] = Field(default=None)  # JSON string
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sequence_number: int

    # Relationship with conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class ConversationBase(SQLModel):
    user_id: str = Field(index=True)
    title: Optional[str] = Field(default=None, max_length=200)
    is_active: bool = Field(default=True)


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    message_count: int


class MessageBase(SQLModel):
    conversation_id: int = Field(foreign_key="conversation.id")
    sender_type: Literal['user', 'assistant']
    content: str = Field(max_length=10000)
    role: Literal['user', 'assistant', 'tool_call', 'tool_response']
    tool_calls: Optional[Json] = None
    tool_responses: Optional[Json] = None
    sequence_number: int


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    timestamp: datetime

