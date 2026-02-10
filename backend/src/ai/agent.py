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
        self.tools_instance = MCPTaskTools()

        self.system_prompt = """You are a helpful task management assistant integrated with a Todo application. You can help users manage their tasks.

When a user wants to add, list, update, complete, or delete tasks, you MUST use the provided tools. Do not just say you did it - actually call the tool.

Always respond in a friendly and helpful manner."""

        # Cohere tool definitions for function calling
        self.tools = [
            {
                "name": "add_task",
                "description": "Create a new task for the user",
                "parameter_definitions": {
                    "title": {
                        "description": "The title of the task",
                        "type": "str",
                        "required": True
                    },
                    "description": {
                        "description": "Optional description of the task",
                        "type": "str",
                        "required": False
                    }
                }
            },
            {
                "name": "list_tasks",
                "description": "List all tasks for the user. Optionally filter by status.",
                "parameter_definitions": {
                    "status": {
                        "description": "Filter by status: 'completed', 'incomplete', or leave empty for all",
                        "type": "str",
                        "required": False
                    }
                }
            },
            {
                "name": "update_task",
                "description": "Update an existing task's title or description",
                "parameter_definitions": {
                    "task_id": {
                        "description": "The ID of the task to update",
                        "type": "str",
                        "required": True
                    },
                    "title": {
                        "description": "New title for the task",
                        "type": "str",
                        "required": False
                    },
                    "description": {
                        "description": "New description for the task",
                        "type": "str",
                        "required": False
                    }
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameter_definitions": {
                    "task_id": {
                        "description": "The ID of the task to complete",
                        "type": "str",
                        "required": True
                    }
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task",
                "parameter_definitions": {
                    "task_id": {
                        "description": "The ID of the task to delete",
                        "type": "str",
                        "required": True
                    }
                }
            }
        ]

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

            # Prepare the request to Cohere with tool definitions
            message = {
                "model": "command-r-08-2024",
                "message": user_message,
                "chat_history": chat_history,
                "preamble": self.system_prompt,
                "tools": self.tools,
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
            ai_response = result.get("text", "")
            tool_calls = result.get("tool_calls", [])
            tool_responses = []

            # Execute tool calls if the model requested them
            if tool_calls:
                for tc in tool_calls:
                    tool_name = tc.get("name", "")
                    tool_args = tc.get("parameters", {})
                    tool_result = self._execute_tool(tool_name, tool_args, session, user)
                    tool_responses.append({
                        "call": {"name": tool_name, "parameters": tool_args},
                        "outputs": [tool_result]
                    })

                # Send tool results back to Cohere for a final response
                followup_message = {
                    "model": "command-r-08-2024",
                    "message": user_message,
                    "chat_history": chat_history,
                    "preamble": self.system_prompt,
                    "tools": self.tools,
                    "tool_results": tool_responses,
                    "temperature": 0.3
                }

                followup_response = requests.post(
                    f"{self.base_url}/chat",
                    headers=headers,
                    json=followup_message
                )

                if followup_response.status_code == 200:
                    followup_result = followup_response.json()
                    ai_response = followup_result.get("text", ai_response or "Done!")

            # If no tool calls and no text, provide a default
            if not ai_response:
                ai_response = "I'm not sure how to help with that."

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
                "confirmation_message": ai_response,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            print("AI Agent Error:", str(e))
            return {
                "message": "Sorry, something went wrong while processing your request.",
                "conversation_id": conversation_id,
                "tool_calls": [],
                "tool_responses": [],
                "confirmation_message": "Sorry, something went wrong while processing your request.",
                "timestamp": datetime.utcnow().isoformat()
            }

    def _execute_tool(self, tool_name: str, args: Dict[str, Any], session: Session, user) -> Dict[str, Any]:
        """Execute a tool call and return the result as a dict for Cohere."""
        try:
            if tool_name == "add_task":
                result = self.tools_instance.add_task(
                    session=session, user=user,
                    title=args.get("title", "Untitled"),
                    description=args.get("description")
                )
            elif tool_name == "list_tasks":
                result = self.tools_instance.list_tasks(
                    session=session, user=user,
                    status=args.get("status")
                )
            elif tool_name == "update_task":
                result = self.tools_instance.update_task(
                    session=session, user=user,
                    task_id=args.get("task_id", ""),
                    title=args.get("title"),
                    description=args.get("description")
                )
            elif tool_name == "complete_task":
                result = self.tools_instance.complete_task(
                    session=session, user=user,
                    task_id=int(args.get("task_id", 0))
                )
            elif tool_name == "delete_task":
                result = self.tools_instance.delete_task(
                    session=session, user=user,
                    task_id=int(args.get("task_id", 0))
                )
            else:
                return {"success": False, "error": f"Unknown tool: {tool_name}"}

            return {"success": result.success, "data": result.data, "error": result.error}
        except Exception as e:
            print(f"Tool execution error ({tool_name}): {e}")
            return {"success": False, "error": str(e)}


# Global instance
agent = AIAgent()