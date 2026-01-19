from typing import Dict, Any
import os
import json
from datetime import datetime
from sqlmodel import Session
import requests
from dotenv import load_dotenv
from .tools import MCPTaskTools, ToolResult
from src.services.conversations import ConversationsService

# Load environment variables from .env file
load_dotenv()


class AIAgent:
    """
    AI Agent using Cohere API directly for task management
    """

    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY is missing in environment variables")

        self.base_url = "https://api.cohere.ai/v1"

        self.system_prompt = """You are a helpful task management assistant integrated with a Todo application. You can help users manage their tasks.

Your capabilities include:
- Add tasks with 'add_task' function
- List tasks with 'list_tasks' function
- Update tasks with 'update_task' function
- Complete tasks with 'complete_task' function
- Delete tasks with 'delete_task' function

When a user wants to perform a task operation, call the appropriate function.
Always respond in a friendly and helpful manner."""

    def process_message(
        self,
        user_message: str,
        conversation_id: int,
        user_id: str,
        session: Session,
        user
    ) -> Dict[str, Any]:

        try:
            # Get conversation service and history
            conversation_service = ConversationsService()
            recent_messages = conversation_service.get_recent_messages(
                session, conversation_id, limit=5
            )

            # Format messages for the API
            chat_history = []

            # Add conversation history (skip the system prompt since we'll include it differently)
            for msg in recent_messages:
                role = "USER" if msg.sender_type == "user" else "CHATBOT"
                chat_history.append({
                    "role": role,
                    "message": msg.content
                })

            # Prepare the request to Cohere
            message = {
                "model": "command-r-08-2024",  # Updated to use currently available model
                "message": user_message,
                "chat_history": chat_history,
                "preamble": self.system_prompt,
                "connectors": [],  # Removed connectors to avoid potential issues
                "temperature": 0.3
            }

            # Call Cohere API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                f"{self.base_url}/chat",
                headers=headers,
                json=message
            )

            if response.status_code != 200:
                print(f"Cohere API Error: {response.status_code} - {response.text}")
                return {
                    "message": "Sorry, I'm having trouble connecting to the AI service right now.",
                    "conversation_id": conversation_id,
                    "timestamp": datetime.utcnow().isoformat()
                }

            result = response.json()
            ai_response = result.get("text", result.get("response", "I'm not sure how to help with that."))

            # Extract tool calls if present
            tool_calls = result.get("tool_calls", [])
            tool_responses = result.get("tool_results", []) or result.get("toolResponses", [])

            # Add the assistant's response to the conversation
            conversation_service.add_message_to_conversation(
                session=session,
                conversation_id=conversation_id,
                user_id=user_id,
                message_content=ai_response,
                sender_type="assistant",
                role="assistant",
                sequence_number=len(recent_messages) + 1
            )

            return {
                "message": ai_response,
                "conversation_id": conversation_id,
                "tool_calls": tool_calls,
                "tool_responses": tool_responses,
                "confirmation_message": "",
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            print("AI Agent Error:", str(e))
            return {
                "message": "Sorry, something went wrong while processing your request.",
                "conversation_id": conversation_id,
                "tool_calls": [],
                "tool_responses": [],
                "confirmation_message": "",
                "timestamp": datetime.utcnow().isoformat()
            }


# Global instance
agent = AIAgent()