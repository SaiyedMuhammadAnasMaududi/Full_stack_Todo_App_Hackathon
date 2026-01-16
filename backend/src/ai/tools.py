import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from typing import Dict, Any, List
from pydantic import BaseModel
from sqlmodel import Session
from models import Message, Conversation
from db import get_session
from auth import get_current_user
from fastapi import Depends
import json
from datetime import datetime


class ToolResult(BaseModel):
    """Standardized result format for all MCP tools"""
    success: bool
    data: Any = None
    error: Dict[str, str] = None
    timestamp: str = str(datetime.utcnow().isoformat())


class TaskData(BaseModel):
    """Task data structure for operations"""
    id: int = None
    title: str
    description: str = None
    completed: bool = False
    user_id: str
    created_at: str = None
    updated_at: str = None


class MCPTaskTools:
    """
    MCP Tools for task operations following the specification:
    - add_task
    - list_tasks
    - update_task
    - complete_task
    - delete_task
    """

    def __init__(self):
        # Session and user will be passed to each method individually
        self.session = None
        self.user = None

    def add_task(self, session: Session, user, title: str, description: str = None) -> ToolResult:
        """
        Create a new task for the authenticated user
        Args:
            session: Database session
            user: Authenticated user
            title: Title of the task
            description: Optional description of the task
        Returns:
            ToolResult with success status and created task data
        """
        try:
            # Import the existing Task model from the main models file
            from ..models import Task

            # Create new task instance
            new_task = Task(
                title=title,
                description=description,
                completed=False,
                user_id=user.id  # Use the authenticated user's ID
            )

            # Add to session and commit
            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            # Return success result with task data
            task_data = TaskData(
                id=new_task.id,
                title=new_task.title,
                description=new_task.description,
                completed=new_task.completed,
                user_id=new_task.user_id,
                created_at=str(new_task.created_at),
                updated_at=str(new_task.updated_at)
            )

            return ToolResult(success=True, data=task_data.model_dump())

        except Exception as e:
            # Return error result
            return ToolResult(
                success=False,
                error={
                    "type": "create_error",
                    "message": f"Failed to create task: {str(e)}"
                }
            )

    def list_tasks(self, session: Session, user, status: str = None) -> ToolResult:
        """
        Retrieve tasks for the authenticated user
        Args:
            session: Database session
            user: Authenticated user
            status: Optional status filter ('completed', 'incomplete', or None for all)
        Returns:
            ToolResult with success status and list of tasks
        """
        try:
            from ..models import Task
            from sqlmodel import select

            # Build query based on status filter
            query = select(Task).where(Task.user_id == user.id)

            if status == "completed":
                query = query.where(Task.completed == True)
            elif status == "incomplete":
                query = query.where(Task.completed == False)

            # Execute query
            tasks = session.exec(query).all()

            # Convert to TaskData format
            task_list = []
            for task in tasks:
                task_data = TaskData(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    user_id=task.user_id,
                    created_at=str(task.created_at),
                    updated_at=str(task.updated_at)
                )
                task_list.append(task_data.model_dump())

            return ToolResult(success=True, data=task_list)

        except Exception as e:
            return ToolResult(
                success=False,
                error={
                    "type": "query_error",
                    "message": f"Failed to list tasks: {str(e)}"
                }
            )

    def update_task(self, session: Session, user, task_id: int, title: str = None, description: str = None) -> ToolResult:
        """
        Update specified fields of an existing task
        Args:
            session: Database session
            user: Authenticated user
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
        Returns:
            ToolResult with success status and updated task data
        """
        try:
            from ..models import Task
            from sqlmodel import select

            # Find the task for the authenticated user
            task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user.id)
            ).first()

            if not task:
                return ToolResult(
                    success=False,
                    error={
                        "type": "not_found",
                        "message": f"Task with ID {task_id} not found or doesn't belong to user"
                    }
                )

            # Update fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description

            # Update timestamp
            task.updated_at = datetime.utcnow()

            # Commit changes
            session.add(task)
            session.commit()
            session.refresh(task)

            # Return updated task data
            task_data = TaskData(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                user_id=task.user_id,
                created_at=str(task.created_at),
                updated_at=str(task.updated_at)
            )

            return ToolResult(success=True, data=task_data.model_dump())

        except Exception as e:
            return ToolResult(
                success=False,
                error={
                    "type": "update_error",
                    "message": f"Failed to update task: {str(e)}"
                }
            )

    def complete_task(self, session: Session, user, task_id: int) -> ToolResult:
        """
        Mark a task as completed
        Args:
            session: Database session
            user: Authenticated user
            task_id: ID of the task to mark as complete
        Returns:
            ToolResult with success status and updated task data
        """
        try:
            from ..models import Task
            from sqlmodel import select

            # Find the task for the authenticated user
            task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user.id)
            ).first()

            if not task:
                return ToolResult(
                    success=False,
                    error={
                        "type": "not_found",
                        "message": f"Task with ID {task_id} not found or doesn't belong to user"
                    }
                )

            # Mark as completed
            task.completed = True
            task.updated_at = datetime.utcnow()

            # Commit changes
            session.add(task)
            session.commit()
            session.refresh(task)

            # Return updated task data
            task_data = TaskData(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                user_id=task.user_id,
                created_at=str(task.created_at),
                updated_at=str(task.updated_at)
            )

            return ToolResult(success=True, data=task_data.model_dump())

        except Exception as e:
            return ToolResult(
                success=False,
                error={
                    "type": "update_error",
                    "message": f"Failed to complete task: {str(e)}"
                }
            )

    def delete_task(self, session: Session, user, task_id: int) -> ToolResult:
        """
        Delete an existing task
        Args:
            session: Database session
            user: Authenticated user
            task_id: ID of the task to delete
        Returns:
            ToolResult with success status and deletion confirmation
        """
        try:
            from ..models import Task
            from sqlmodel import select

            # Find the task for the authenticated user
            task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user.id)
            ).first()

            if not task:
                return ToolResult(
                    success=False,
                    error={
                        "type": "not_found",
                        "message": f"Task with ID {task_id} not found or doesn't belong to user"
                    }
                )

            # Delete the task
            session.delete(task)
            session.commit()

            # Return success result
            return ToolResult(
                success=True,
                data={"message": f"Task with ID {task_id} deleted successfully"}
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error={
                    "type": "delete_error",
                    "message": f"Failed to delete task: {str(e)}"
                }
            )


# Create global instance for use in other modules
mcptools = MCPTaskTools()