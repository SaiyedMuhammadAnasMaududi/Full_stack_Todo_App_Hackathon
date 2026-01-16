from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import json

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from db import get_session
from auth import get_current_user, TokenData
from models import Conversation, ConversationCreate, Message, MessageCreate
from src.services.conversations import ConversationsService
from src.services.auth import validate_user_id_match
from src.ai.agent import AIAgent, agent

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: Dict[str, Any]


class ToolResponse(BaseModel):
    tool_call_id: str
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    message: str
    conversation_id: int
    tool_calls: Optional[list] = []
    tool_responses: Optional[list] = []
    confirmation_message: str
    timestamp: str


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def send_message_to_chatbot(
    user_id: str,
    request: ChatRequest,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Send a message to the AI chatbot and receive a response with potential tool calls
    """
    # Validate that the user_id in the token matches the user_id in the request
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in request"
        )

    # Initialize conversation service
    conversation_service = ConversationsService()

    # If no conversation_id is provided, create a new conversation
    conversation_id = request.conversation_id
    if not conversation_id:
        # Create a new conversation
        conversation_data = ConversationCreate(
            user_id=user_id,
            title=request.message[:50] + "..." if len(request.message) > 50 else request.message  # Use first part of message as title
        )

        new_conversation = conversation_service.create_conversation(session, conversation_data)
        conversation_id = new_conversation.id

    # Verify that the conversation belongs to the user
    conversation = conversation_service.get_conversation_by_id(session, conversation_id, user_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or does not belong to user"
        )

    # Add user's message to the conversation
    # Get the current message count to determine the sequence number
    existing_messages = conversation_service.get_conversation_messages(session, conversation_id, user_id)
    sequence_number = len(existing_messages) + 1

    user_message = conversation_service.add_message_to_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=user_id,
        message_content=request.message,
        sender_type="user",
        role="user",
        sequence_number=sequence_number
    )

    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add user message to conversation"
        )

    # Process the message with the AI agent
    try:
        response = agent.process_message(
            user_message=request.message,
            conversation_id=conversation_id,
            user_id=user_id,
            session=session,
            user=current_user
        )

        # Update the conversation's updated_at timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

        return ChatResponse(
            message=response["message"],
            conversation_id=response["conversation_id"],
            tool_calls=response["tool_calls"],
            tool_responses=response["tool_responses"],
            confirmation_message=response["confirmation_message"],
            timestamp=response["timestamp"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message with AI agent: {str(e)}"
        )


@router.get("/{user_id}/conversations")
async def get_user_conversations(
    user_id: str,
    limit: int = 20,
    offset: int = 0,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get user's conversation history
    """
    # Validate that the user_id in the token matches the user_id in the request
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in request"
        )

    # Initialize conversation service
    conversation_service = ConversationsService()

    # Get user conversations
    conversations = conversation_service.get_user_conversations(session, user_id, limit, offset)

    # Calculate total count
    from sqlmodel import select
    total_count_query = select(Conversation).where(
        Conversation.user_id == user_id,
        Conversation.is_active == True
    )
    total_count = len(session.exec(total_count_query).all())

    # Prepare response with message counts
    conversation_list = []
    for conv in conversations:
        # Get message count for this conversation
        messages = conversation_service.get_conversation_messages(session, conv.id, user_id)
        message_count = len(messages)

        conversation_list.append({
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat(),
            "message_count": message_count
        })

    return {
        "conversations": conversation_list,
        "total_count": total_count,
        "limit": limit,
        "offset": offset
    }


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation(
    user_id: str,
    conversation_id: int,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific conversation
    """
    # Validate that the user_id in the token matches the user_id in the request
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in request"
        )

    # Initialize conversation service
    conversation_service = ConversationsService()

    # Get the conversation
    conversation = conversation_service.get_conversation_by_id(session, conversation_id, user_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or does not belong to user"
        )

    # Get messages for this conversation
    messages = conversation_service.get_conversation_messages(session, conversation_id, user_id)

    # Format messages
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "id": msg.id,
            "sender_type": msg.sender_type,
            "content": msg.content,
            "role": msg.role,
            "timestamp": msg.timestamp.isoformat(),
            "sequence_number": msg.sequence_number,
            "tool_calls": msg.tool_calls,
            "tool_responses": msg.tool_responses
        })

    return {
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at.isoformat(),
        "updated_at": conversation.updated_at.isoformat(),
        "messages": formatted_messages,
        "participants": ["user", "assistant"]
    }