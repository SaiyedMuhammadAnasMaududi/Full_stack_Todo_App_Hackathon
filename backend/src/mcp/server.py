from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.shared.exceptions import McpError
import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime
from ..ai.tools import MCPTaskTools, ToolResult
from db import get_session
from auth import get_current_user
from fastapi import Depends
from models import Task, User


# Initialize MCP server
server = Server("todo-chatbot-mcp")


@server.tools.register
def add_task(title: str, description: str = None, priority: str = "medium", tags: List[str] = None, due_at: str = None, reminder_at: str = None, recurrence_rule: str = None, is_recurring: bool = False) -> Dict[str, Any]:
    """
    Create a new task for the authenticated user with advanced features
    """
    try:
        # Get session and user from context - this would be injected by the MCP framework
        # For now, using a mock implementation that demonstrates the structure
        from ...models import Task
        from ...db import SessionLocal

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return the parameters that would be processed
            import uuid
            task_id = str(uuid.uuid4())

            # Convert tags to JSON string for storage
            tags_json = json.dumps(tags) if tags else None

            # Create task representation
            task_data = {
                "id": task_id,
                "title": title,
                "description": description,
                "completed": False,
                "user_id": "mock_user_id",  # Would come from MCP context
                "priority": priority,
                "tags": tags_json,
                "due_at": due_at,
                "reminder_at": reminder_at,
                "recurrence_rule": recurrence_rule,
                "is_recurring": is_recurring,
                "created_at": str(datetime.utcnow()),
                "updated_at": str(datetime.utcnow())
            }

            return {
                "success": True,
                "data": task_data,
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "create_error",
                "message": f"Failed to create task: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


@server.tools.register
def list_tasks(status: str = None, priority: str = None) -> Dict[str, Any]:
    """
    List tasks for the authenticated user with optional filters
    """
    try:
        # Get session and user from context - this would be injected by the MCP framework
        from ...models import Task
        from ...db import SessionLocal
        from sqlmodel import select

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return mock data that demonstrates the structure
            mock_tasks = [
                {
                    "id": "task1",
                    "title": "Sample Task",
                    "description": "This is a sample task",
                    "completed": False,
                    "user_id": "mock_user_id",
                    "priority": "medium",
                    "tags": json.dumps(["work", "important"]),
                    "due_at": "2023-12-31T10:00:00Z",
                    "reminder_at": "2023-12-30T09:00:00Z",
                    "recurrence_rule": None,
                    "is_recurring": False,
                    "created_at": str(datetime.utcnow()),
                    "updated_at": str(datetime.utcnow())
                }
            ]

            # Apply filters if provided
            if status == "completed":
                mock_tasks = [t for t in mock_tasks if t["completed"]]
            elif status == "incomplete":
                mock_tasks = [t for t in mock_tasks if not t["completed"]]

            if priority:
                mock_tasks = [t for t in mock_tasks if t["priority"] == priority]

            return {
                "success": True,
                "data": mock_tasks,
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "query_error",
                "message": f"Failed to list tasks: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


@server.tools.register
def update_task(task_id: str, title: str = None, description: str = None, priority: str = None, tags: List[str] = None, due_at: str = None, reminder_at: str = None, recurrence_rule: str = None, is_recurring: bool = None) -> Dict[str, Any]:
    """
    Update an existing task with advanced features
    """
    try:
        # Get session and user from context - this would be injected by the MCP framework
        from ...models import Task
        from ...db import SessionLocal
        from sqlmodel import select

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return mock data that demonstrates the structure
            updated_task = {
                "id": task_id,
                "title": title,
                "description": description,
                "completed": False,  # Would be retrieved from DB
                "user_id": "mock_user_id",  # Would come from MCP context
                "priority": priority,
                "tags": json.dumps(tags) if tags is not None else None,
                "due_at": due_at,
                "reminder_at": reminder_at,
                "recurrence_rule": recurrence_rule,
                "is_recurring": is_recurring if is_recurring is not None else False,
                "created_at": str(datetime.utcnow()),
                "updated_at": str(datetime.utcnow())
            }

            return {
                "success": True,
                "data": updated_task,
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "update_error",
                "message": f"Failed to update task: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


@server.tools.register
def complete_task(task_id: str) -> Dict[str, Any]:
    """
    Mark a task as complete
    """
    try:
        # Get session and user from context - this would be injected by the MCP framework
        from ...models import Task
        from ...db import SessionLocal
        from sqlmodel import select

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return mock data that demonstrates the structure
            completed_task = {
                "id": task_id,
                "title": "Updated Task Title",  # Would be retrieved from DB
                "description": "Updated Task Description",  # Would be retrieved from DB
                "completed": True,
                "user_id": "mock_user_id",  # Would come from MCP context
                "priority": "medium",  # Would be retrieved from DB
                "tags": json.dumps(["work"]),  # Would be retrieved from DB
                "due_at": "2023-12-31T10:00:00Z",  # Would be retrieved from DB
                "reminder_at": "2023-12-30T09:00:00Z",  # Would be retrieved from DB
                "recurrence_rule": None,  # Would be retrieved from DB
                "is_recurring": False,  # Would be retrieved from DB
                "created_at": str(datetime.utcnow()),
                "updated_at": str(datetime.utcnow()),
                "completed_at": str(datetime.utcnow())
            }

            return {
                "success": True,
                "data": completed_task,
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "update_error",
                "message": f"Failed to complete task: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


@server.tools.register
def delete_task(task_id: str) -> Dict[str, Any]:
    """
    Delete a task
    """
    try:
        # Get session and user from context - this would be injected by the MCP framework
        from ...models import Task
        from ...db import SessionLocal
        from sqlmodel import select

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return a confirmation that the task would be deleted
            return {
                "success": True,
                "data": {"message": f"Task with ID {task_id} would be deleted in a real implementation"},
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "delete_error",
                "message": f"Failed to delete task: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


# New MCP tools for Advanced Features
@server.tools.register
def set_priority(task_id: str, priority: str) -> Dict[str, Any]:
    """
    Set the priority of a task (low, medium, high)
    """
    try:
        if priority not in ["low", "medium", "high"]:
            return {
                "success": False,
                "error": {
                    "type": "validation_error",
                    "message": "Priority must be one of: low, medium, high"
                },
                "timestamp": str(datetime.utcnow().isoformat())
            }

        # Get session and user from context - this would be injected by the MCP framework
        from ...models import Task
        from ...db import SessionLocal
        from sqlmodel import select

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return mock data that demonstrates the structure
            updated_task = {
                "id": task_id,
                "title": "Sample Task",  # Would be retrieved from DB
                "description": "Sample description",  # Would be retrieved from DB
                "completed": False,  # Would be retrieved from DB
                "user_id": "mock_user_id",  # Would come from MCP context
                "priority": priority,
                "tags": json.dumps(["work"]),  # Would be retrieved from DB
                "due_at": "2023-12-31T10:00:00Z",  # Would be retrieved from DB
                "reminder_at": "2023-12-30T09:00:00Z",  # Would be retrieved from DB
                "recurrence_rule": None,  # Would be retrieved from DB
                "is_recurring": False,  # Would be retrieved from DB
                "created_at": str(datetime.utcnow()),
                "updated_at": str(datetime.utcnow())
            }

            return {
                "success": True,
                "data": updated_task,
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "update_error",
                "message": f"Failed to set priority: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


@server.tools.register
def add_tags(task_id: str, tags: List[str]) -> Dict[str, Any]:
    """
    Add tags to a task (replaces existing tags)
    """
    try:
        if not isinstance(tags, list):
            return {
                "success": False,
                "error": {
                    "type": "validation_error",
                    "message": "Tags must be a list of strings"
                },
                "timestamp": str(datetime.utcnow().isoformat())
            }

        for tag in tags:
            if not isinstance(tag, str) or len(tag.strip()) == 0:
                return {
                    "success": False,
                    "error": {
                        "type": "validation_error",
                        "message": "Tags must be non-empty strings"
                    },
                    "timestamp": str(datetime.utcnow().isoformat())
                }

        # Get session and user from context - this would be injected by the MCP framework
        from ...models import Task
        from ...db import SessionLocal
        from sqlmodel import select

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return mock data that demonstrates the structure
            updated_task = {
                "id": task_id,
                "title": "Sample Task",  # Would be retrieved from DB
                "description": "Sample description",  # Would be retrieved from DB
                "completed": False,  # Would be retrieved from DB
                "user_id": "mock_user_id",  # Would come from MCP context
                "priority": "medium",  # Would be retrieved from DB
                "tags": json.dumps(tags),
                "due_at": "2023-12-31T10:00:00Z",  # Would be retrieved from DB
                "reminder_at": "2023-12-30T09:00:00Z",  # Would be retrieved from DB
                "recurrence_rule": None,  # Would be retrieved from DB
                "is_recurring": False,  # Would be retrieved from DB
                "created_at": str(datetime.utcnow()),
                "updated_at": str(datetime.utcnow())
            }

            return {
                "success": True,
                "data": updated_task,
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "update_error",
                "message": f"Failed to add tags: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


@server.tools.register
def search_tasks(query: str, limit: int = 20) -> Dict[str, Any]:
    """
    Search tasks by content across title, description, and tags
    """
    try:
        if not query or len(query.strip()) == 0:
            return {
                "success": False,
                "error": {
                    "type": "validation_error",
                    "message": "Query cannot be empty"
                },
                "timestamp": str(datetime.utcnow().isoformat())
            }

        # Get session and user from context - this would be injected by the MCP framework
        from ...models import Task
        from ...db import SessionLocal
        from sqlmodel import select

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return mock data that demonstrates the structure
            mock_tasks = [
                {
                    "id": "task1",
                    "title": f"Sample task matching '{query}'",
                    "description": f"This is a sample task description matching '{query}'",
                    "completed": False,
                    "user_id": "mock_user_id",
                    "priority": "medium",
                    "tags": json.dumps(["work", "important"]),
                    "due_at": "2023-12-31T10:00:00Z",
                    "reminder_at": "2023-12-30T09:00:00Z",
                    "recurrence_rule": None,
                    "is_recurring": False,
                    "created_at": str(datetime.utcnow()),
                    "updated_at": str(datetime.utcnow())
                }
            ]

            return {
                "success": True,
                "data": mock_tasks[:limit],
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "search_error",
                "message": f"Failed to search tasks: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


@server.tools.register
def filter_tasks(priority: str = None, completed: bool = None, due_after: str = None, due_before: str = None, tags: List[str] = None, limit: int = 20) -> Dict[str, Any]:
    """
    Filter tasks by various criteria
    """
    try:
        if priority and priority not in ["low", "medium", "high"]:
            return {
                "success": False,
                "error": {
                    "type": "validation_error",
                    "message": "Priority must be one of: low, medium, high"
                },
                "timestamp": str(datetime.utcnow().isoformat())
            }

        if tags and not isinstance(tags, list):
            return {
                "success": False,
                "error": {
                    "type": "validation_error",
                    "message": "Tags must be a list of strings"
                },
                "timestamp": str(datetime.utcnow().isoformat())
            }

        # Get session and user from context - this would be injected by the MCP framework
        from ...models import Task
        from ...db import SessionLocal
        from sqlmodel import select

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return mock data that demonstrates the structure
            mock_tasks = [
                {
                    "id": "task1",
                    "title": "Filtered Sample Task",
                    "description": "This is a sample task after filtering",
                    "completed": completed if completed is not None else False,
                    "user_id": "mock_user_id",
                    "priority": priority if priority else "medium",
                    "tags": json.dumps(tags) if tags else json.dumps(["work"]),
                    "due_at": "2023-12-31T10:00:00Z",
                    "reminder_at": "2023-12-30T09:00:00Z",
                    "recurrence_rule": None,
                    "is_recurring": False,
                    "created_at": str(datetime.utcnow()),
                    "updated_at": str(datetime.utcnow())
                }
            ]

            return {
                "success": True,
                "data": mock_tasks[:limit],
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "filter_error",
                "message": f"Failed to filter tasks: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


@server.tools.register
def sort_tasks(sort_field: str = "created_at", sort_order: str = "asc", limit: int = 20) -> Dict[str, Any]:
    """
    Sort tasks by various criteria
    """
    try:
        allowed_fields = ["title", "priority", "due_at", "created_at"]
        if sort_field not in allowed_fields:
            return {
                "success": False,
                "error": {
                    "type": "validation_error",
                    "message": f"sort_field must be one of: {', '.join(allowed_fields)}"
                },
                "timestamp": str(datetime.utcnow().isoformat())
            }

        if sort_order not in ["asc", "desc"]:
            return {
                "success": False,
                "error": {
                    "type": "validation_error",
                    "message": "sort_order must be either 'asc' or 'desc'"
                },
                "timestamp": str(datetime.utcnow().isoformat())
            }

        # Get session and user from context - this would be injected by the MCP framework
        from ...models import Task
        from ...db import SessionLocal
        from sqlmodel import select

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return mock data that demonstrates the structure
            mock_tasks = [
                {
                    "id": "task1",
                    "title": "Sorted Sample Task",
                    "description": "This is a sample task after sorting",
                    "completed": False,
                    "user_id": "mock_user_id",
                    "priority": "medium",
                    "tags": json.dumps(["work"]),
                    "due_at": "2023-12-31T10:00:00Z",
                    "reminder_at": "2023-12-30T09:00:00Z",
                    "recurrence_rule": None,
                    "is_recurring": False,
                    "created_at": str(datetime.utcnow()),
                    "updated_at": str(datetime.utcnow())
                }
            ]

            return {
                "success": True,
                "data": mock_tasks[:limit],
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "sort_error",
                "message": f"Failed to sort tasks: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


@server.tools.register
def set_due_date(task_id: str, due_date: str) -> Dict[str, Any]:
    """
    Set the due date for a task
    """
    try:
        from datetime import datetime
        # Validate date format
        parsed_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))

        # Get session and user from context - this would be injected by the MCP framework
        from ...models import Task
        from ...db import SessionLocal
        from sqlmodel import select

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return mock data that demonstrates the structure
            updated_task = {
                "id": task_id,
                "title": "Sample Task",  # Would be retrieved from DB
                "description": "Sample description",  # Would be retrieved from DB
                "completed": False,  # Would be retrieved from DB
                "user_id": "mock_user_id",  # Would come from MCP context
                "priority": "medium",  # Would be retrieved from DB
                "tags": json.dumps(["work"]),  # Would be retrieved from DB
                "due_at": due_date,
                "reminder_at": "2023-12-30T09:00:00Z",  # Would be retrieved from DB
                "recurrence_rule": None,  # Would be retrieved from DB
                "is_recurring": False,  # Would be retrieved from DB
                "created_at": str(datetime.utcnow()),
                "updated_at": str(datetime.utcnow())
            }

            return {
                "success": True,
                "data": updated_task,
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except ValueError:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "update_error",
                "message": f"Failed to set due date: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


@server.tools.register
def set_reminder(task_id: str, reminder_time: str) -> Dict[str, Any]:
    """
    Set a reminder for a task
    """
    try:
        from datetime import datetime
        # Validate date format
        parsed_date = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))

        # Get session and user from context - this would be injected by the MCP framework
        from ...models import Task
        from ...db import SessionLocal
        from sqlmodel import select

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return mock data that demonstrates the structure
            updated_task = {
                "id": task_id,
                "title": "Sample Task",  # Would be retrieved from DB
                "description": "Sample description",  # Would be retrieved from DB
                "completed": False,  # Would be retrieved from DB
                "user_id": "mock_user_id",  # Would come from MCP context
                "priority": "medium",  # Would be retrieved from DB
                "tags": json.dumps(["work"]),  # Would be retrieved from DB
                "due_at": "2023-12-31T10:00:00Z",  # Would be retrieved from DB
                "reminder_at": reminder_time,
                "recurrence_rule": None,  # Would be retrieved from DB
                "is_recurring": False,  # Would be retrieved from DB
                "created_at": str(datetime.utcnow()),
                "updated_at": str(datetime.utcnow())
            }

            return {
                "success": True,
                "data": updated_task,
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except ValueError:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "update_error",
                "message": f"Failed to set reminder: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


@server.tools.register
def set_recurrence(task_id: str, recurrence_rule: str) -> Dict[str, Any]:
    """
    Set a recurrence rule for a task
    """
    try:
        # Basic validation - checking if it looks like an RRULE
        if not recurrence_rule.startswith("RRULE:"):
            return {
                "success": False,
                "error": {
                    "type": "validation_error",
                    "message": "Recurrence rule must start with 'RRULE:'"
                },
                "timestamp": str(datetime.utcnow().isoformat())
            }

        # Get session and user from context - this would be injected by the MCP framework
        from ...models import Task
        from ...db import SessionLocal
        from sqlmodel import select

        with SessionLocal() as session:
            # In a real implementation, user would come from the MCP context
            # For now, we'll return mock data that demonstrates the structure
            updated_task = {
                "id": task_id,
                "title": "Sample Task",  # Would be retrieved from DB
                "description": "Sample description",  # Would be retrieved from DB
                "completed": False,  # Would be retrieved from DB
                "user_id": "mock_user_id",  # Would come from MCP context
                "priority": "medium",  # Would be retrieved from DB
                "tags": json.dumps(["work"]),  # Would be retrieved from DB
                "due_at": "2023-12-31T10:00:00Z",  # Would be retrieved from DB
                "reminder_at": "2023-12-30T09:00:00Z",  # Would be retrieved from DB
                "recurrence_rule": recurrence_rule,
                "is_recurring": True,
                "created_at": str(datetime.utcnow()),
                "updated_at": str(datetime.utcnow())
            }

            return {
                "success": True,
                "data": updated_task,
                "timestamp": str(datetime.utcnow().isoformat())
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "update_error",
                "message": f"Failed to set recurrence: {str(e)}"
            },
            "timestamp": str(datetime.utcnow().isoformat())
        }


# Health check for the MCP server
@server.profiles.register
def get_server_info():
    return {
        "name": "Todo Chatbot MCP Server",
        "version": "1.0.0",
        "description": "MCP server for Todo chatbot task operations with advanced features",
        "capabilities": [
            "add_task", "list_tasks", "update_task", "complete_task", "delete_task",
            "set_priority", "add_tags", "search_tasks", "filter_tasks", "sort_tasks",
            "set_due_date", "set_reminder", "set_recurrence"
        ]
    }


# Startup event handler
@server.lifecycle.startup
async def startup_event():
    print("MCP Server for Todo Chatbot started successfully")
    print("Registered tools:", [tool.name for tool in server.tools])


# Shutdown event handler
@server.lifecycle.shutdown
async def shutdown_event():
    print("MCP Server for Todo Chatbot shutting down")


# This would be called when running the server
def run_server():
    """
    Run the MCP server
    """
    import uvicorn
    from mcp.transport.stdio import stdio_server

    async def main():
        async with stdio_server(server) as shutdown:
            await shutdown

    asyncio.run(main())


if __name__ == "__main__":
    run_server()