from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models import Conversation, ConversationCreate, Message


class ConversationsService:
    """
    Service class for handling conversation-related operations
    """

    def create_conversation(self, session: Session, conversation_data: ConversationCreate) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation.model_validate(conversation_data)
        conversation.created_at = datetime.utcnow()
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, session: Session, conversation_id: int, user_id: str) -> Optional[Conversation]:
        """Get a specific conversation by ID for a user"""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return session.exec(statement).first()

    def get_user_conversations(self, session: Session, user_id: str, limit: int = 20, offset: int = 0) -> List[Conversation]:
        """Get all conversations for a user with pagination"""
        statement = select(Conversation).where(
            Conversation.user_id == user_id,
            Conversation.is_active == True
        ).order_by(Conversation.updated_at.desc()).offset(offset).limit(limit)
        return session.exec(statement).all()

    def update_conversation_title(self, session: Session, conversation_id: int, user_id: str, title: str) -> Optional[Conversation]:
        """Update conversation title"""
        conversation = self.get_conversation_by_id(session, conversation_id, user_id)
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    def delete_conversation(self, session: Session, conversation_id: int, user_id: str) -> bool:
        """Soft delete a conversation"""
        conversation = self.get_conversation_by_id(session, conversation_id, user_id)
        if conversation:
            conversation.is_active = False
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            return True
        return False

    def get_conversation_messages(self, session: Session, conversation_id: int, user_id: str) -> List[Message]:
        """Get all messages for a specific conversation"""
        statement = select(Message).join(Conversation).where(
            Message.conversation_id == conversation_id,
            Conversation.user_id == user_id
        ).order_by(Message.sequence_number)
        return session.exec(statement).all()

    def add_message_to_conversation(self, session: Session, conversation_id: int, user_id: str, message_content: str,
                                   sender_type: str, role: str, sequence_number: int) -> Optional[Message]:
        """Add a message to a conversation"""
        # Verify user has access to this conversation
        conversation = self.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return None

        from models import Message, MessageCreate
        message_data = MessageCreate(
            conversation_id=conversation_id,
            sender_type=sender_type,
            content=message_content,
            role=role,
            sequence_number=sequence_number
        )

        message = Message.model_validate(message_data)
        session.add(message)
        session.commit()
        session.refresh(message)

        # Update conversation's updated_at timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

        return message

    def get_recent_messages(self, session: Session, conversation_id: int, limit: int = 10) -> List[Message]:
        """Get recent messages from a conversation for context window"""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.desc()).limit(limit)
        messages = session.exec(statement).all()
        # Reverse to get chronological order
        return list(reversed(messages))