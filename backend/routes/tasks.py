from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from slowapi import _rate_limit_exceeded_handler
import models
from db import SessionLocal
from auth import get_current_user
from services.recurrence import RecurrenceService
from services.audit import AuditService
from services.event_publisher import publish_task_created, publish_task_updated, publish_task_completed, publish_task_deleted
from utils.datetime_utils import utc_now, is_future_datetime, validate_recurrence_rule
from sqlmodel import Session, select
from cachetools import TTLCache
import threading
import json
from datetime import datetime

# The limiter will be assigned from main.py


# Create caches for frequently accessed data
# Cache for individual tasks (key: user_id:task_id, ttl: 5 minutes)
task_cache = TTLCache(maxsize=1000, ttl=300)

# Cache for user's task list (key: user_id, ttl: 2 minutes)
tasks_list_cache = TTLCache(maxsize=100, ttl=120)

# Thread lock for cache operations
cache_lock = threading.Lock()


# Create API router for task endpoints
router = APIRouter(prefix="/api/{user_id}", tags=["tasks"])


from pydantic import validator

# Pydantic models for request/response
class TaskCreate(BaseModel):
    title: str
    description: str = None
    completed: bool = False
    priority: str = "medium"  # low, medium, high
    tags: Optional[list] = None  # Array of tag strings
    due_at: Optional[datetime] = None
    reminder_at: Optional[datetime] = None
    recurrence_rule: Optional[str] = None
    is_recurring: bool = False

    @validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(v) > 255:
            raise ValueError('Title must be less than 255 characters')
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be less than 1000 characters')
        return v

    @validator('priority')
    def validate_priority(cls, v):
        if v and v not in ['low', 'medium', 'high']:
            raise ValueError('Priority must be one of: low, medium, high')
        return v

    @validator('due_at', 'reminder_at')
    def validate_future_datetime(cls, v):
        if v and not is_future_datetime(v):
            raise ValueError('Date/time must be in the future')
        return v

    @validator('recurrence_rule')
    def validate_recurrence_rule_format(cls, v):
        if v and not validate_recurrence_rule(v):
            raise ValueError('Invalid recurrence rule format')
        return v

    @validator('tags')
    def validate_tags(cls, v):
        if v is not None:
            if not isinstance(v, list):
                raise ValueError('Tags must be a list of strings')
            for tag in v:
                if not isinstance(tag, str) or len(tag.strip()) == 0:
                    raise ValueError('Tags must be non-empty strings')
                if len(tag) > 50:
                    raise ValueError('Tags must be less than 50 characters')
        return v


class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None
    priority: str = None
    tags: Optional[list] = None
    due_at: Optional[datetime] = None
    reminder_at: Optional[datetime] = None
    recurrence_rule: Optional[str] = None
    is_recurring: bool = None

    @validator('title')
    def validate_title(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Title cannot be empty')
            if len(v) > 255:
                raise ValueError('Title must be less than 255 characters')
            return v.strip()
        return v

    @validator('description')
    def validate_description(cls, v):
        if v is not None and len(v) > 1000:
            raise ValueError('Description must be less than 1000 characters')
        return v

    @validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in ['low', 'medium', 'high']:
            raise ValueError('Priority must be one of: low, medium, high')
        return v

    @validator('due_at', 'reminder_at')
    def validate_future_datetime(cls, v):
        if v is not None and not is_future_datetime(v):
            raise ValueError('Date/time must be in the future')
        return v

    @validator('recurrence_rule')
    def validate_recurrence_rule_format(cls, v):
        if v is not None and not validate_recurrence_rule(v):
            raise ValueError('Invalid recurrence rule format')
        return v

    @validator('tags')
    def validate_tags(cls, v):
        if v is not None:
            if not isinstance(v, list):
                raise ValueError('Tags must be a list of strings')
            for tag in v:
                if not isinstance(tag, str) or len(tag.strip()) == 0:
                    raise ValueError('Tags must be non-empty strings')
                if len(tag) > 50:
                    raise ValueError('Tags must be less than 50 characters')
        return v


class TaskSearch(BaseModel):
    query: str  # Search query string
    limit: int = 20  # Number of results to return
    offset: int = 0  # Offset for pagination


class TaskFilter(BaseModel):
    priority: Optional[str] = None  # low, medium, high
    completed: Optional[bool] = None
    due_after: Optional[datetime] = None
    due_before: Optional[datetime] = None
    tags: Optional[list] = None  # Array of tag strings to filter by
    limit: int = 20
    offset: int = 0


class TaskSort(BaseModel):
    sort_field: str = "created_at"  # Field to sort by
    sort_order: str = "asc"  # asc or desc
    limit: int = 20
    offset: int = 0


class TaskToggleComplete(BaseModel):
    completed: bool


def serialize_task(t):
    return {
        "id": t.id, "title": t.title, "description": t.description,
        "completed": t.completed, "user_id": t.user_id,
        "created_at": str(t.created_at), "updated_at": str(t.updated_at),
        "priority": t.priority, "tags": t.tags,
        "due_at": str(t.due_at) if t.due_at else None,
        "reminder_at": str(t.reminder_at) if t.reminder_at else None,
        "recurrence_rule": t.recurrence_rule, "is_recurring": t.is_recurring,
        "parent_task_id": t.parent_task_id,
        "completed_at": str(t.completed_at) if t.completed_at else None,
    }


@router.get("/tasks")
async def get_tasks(user_id: str, current_user: models.User = Depends(get_current_user)):
    """
    Retrieve all tasks belonging to the authenticated user
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    # Check cache first
    with cache_lock:
        cached_tasks = tasks_list_cache.get(user_id)

    if cached_tasks is not None:
        return cached_tasks

    # Fetch from database
    session = SessionLocal()
    try:
        tasks = session.exec(
            select(models.Task).where(models.Task.user_id == user_id)
        ).all()
        result = [serialize_task(t) for t in tasks]

        # Cache the results
        with cache_lock:
            tasks_list_cache[user_id] = result

        return result
    finally:
        session.close()


@router.post("/tasks/search", )
async def search_tasks(
    user_id: str,
    search_request: TaskSearch,
    current_user: models.User = Depends(get_current_user)
):
    """
    Search tasks by content across title, description, and tags
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    session = SessionLocal()
    try:
        # Build search query
        query = select(models.Task).where(models.Task.user_id == user_id)

        # Apply search filters based on query string
        if search_request.query:
            query = query.where(
                (models.Task.title.contains(search_request.query)) |
                (models.Task.description.contains(search_request.query))
            )

        # Apply pagination
        query = query.offset(search_request.offset).limit(search_request.limit)

        tasks = session.exec(query).all()
        return [serialize_task(t) for t in tasks]
    finally:
        session.close()


@router.post("/tasks/filter")
async def filter_tasks(
    user_id: str,
    filter_request: TaskFilter,
    current_user: models.User = Depends(get_current_user)
):
    """
    Filter tasks by various criteria
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    session = SessionLocal()
    try:
        # Build filter query
        query = select(models.Task).where(models.Task.user_id == user_id)

        # Apply filters
        if filter_request.priority:
            query = query.where(models.Task.priority == filter_request.priority)
        if filter_request.completed is not None:
            query = query.where(models.Task.completed == filter_request.completed)
        if filter_request.due_after:
            query = query.where(models.Task.due_at >= filter_request.due_after)
        if filter_request.due_before:
            query = query.where(models.Task.due_at <= filter_request.due_before)
        if filter_request.tags:
            # Search in the JSON string of tags (for simplicity)
            for tag in filter_request.tags:
                query = query.where(models.Task.tags.contains(tag))

        # Apply pagination
        query = query.offset(filter_request.offset).limit(filter_request.limit)

        tasks = session.exec(query).all()
        return [serialize_task(t) for t in tasks]
    finally:
        session.close()


@router.post("/tasks/sort")
async def sort_tasks(
    user_id: str,
    sort_request: TaskSort,
    current_user: models.User = Depends(get_current_user)
):
    """
    Sort tasks by various criteria
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    session = SessionLocal()
    try:
        # Build sort query
        query = select(models.Task).where(models.Task.user_id == user_id)

        # Apply sorting
        if sort_request.sort_order.lower() == "desc":
            if sort_request.sort_field == "title":
                query = query.order_by(models.Task.title.desc())
            elif sort_request.sort_field == "priority":
                query = query.order_by(models.Task.priority.desc())
            elif sort_request.sort_field == "due_at":
                query = query.order_by(models.Task.due_at.desc())
            elif sort_request.sort_field == "created_at":
                query = query.order_by(models.Task.created_at.desc())
            else:  # default to created_at
                query = query.order_by(models.Task.created_at.desc())
        else:  # ascending order
            if sort_request.sort_field == "title":
                query = query.order_by(models.Task.title.asc())
            elif sort_request.sort_field == "priority":
                query = query.order_by(models.Task.priority.asc())
            elif sort_request.sort_field == "due_at":
                query = query.order_by(models.Task.due_at.asc())
            elif sort_request.sort_field == "created_at":
                query = query.order_by(models.Task.created_at.asc())
            else:  # default to created_at
                query = query.order_by(models.Task.created_at.asc())

        # Apply pagination
        query = query.offset(sort_request.offset).limit(sort_request.limit)

        tasks = session.exec(query).all()
        return [serialize_task(t) for t in tasks]
    finally:
        session.close()


@router.patch("/tasks/{task_id}/update")
async def update_task_extended(
    user_id: str,
    task_id: str,
    task_update: TaskUpdate,
    current_user: models.User = Depends(get_current_user)
):
    """
    Extended update endpoint that supports all new fields
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    session = SessionLocal()
    try:
        db_task = session.exec(
            select(models.Task).where(
                models.Task.id == task_id,
                models.Task.user_id == user_id
            )
        ).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update task fields based on provided values
        update_data = task_update.dict(exclude_unset=True) if hasattr(task_update, 'dict') else task_update.model_dump(exclude_unset=True)

        if "title" in update_data and update_data["title"] is not None:
            db_task.title = update_data["title"]
        if "description" in update_data and update_data["description"] is not None:
            db_task.description = update_data["description"]
        if "completed" in update_data and update_data["completed"] is not None:
            db_task.completed = update_data["completed"]
        if "priority" in update_data and update_data["priority"] is not None:
            db_task.priority = update_data["priority"]
        if "tags" in update_data and update_data["tags"] is not None:
            db_task.tags = json.dumps(update_data["tags"]) if update_data["tags"] else None
        if "due_at" in update_data:
            db_task.due_at = update_data["due_at"]
        if "reminder_at" in update_data:
            db_task.reminder_at = update_data["reminder_at"]
        if "recurrence_rule" in update_data:
            db_task.recurrence_rule = update_data["recurrence_rule"]
        if "is_recurring" in update_data and update_data["is_recurring"] is not None:
            db_task.is_recurring = update_data["is_recurring"]

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Log the update in the audit trail (non-blocking)
        try:
            audit_service = AuditService(session)
            audit_service.log_task_update(db_task, list(update_data.keys()))
        except Exception:
            pass

        # Invalidate caches
        cache_key = f"{user_id}:{task_id}"
        with cache_lock:
            task_cache.pop(cache_key, None)
            tasks_list_cache.pop(user_id, None)

        return {
            "id": db_task.id, "title": db_task.title, "description": db_task.description,
            "completed": db_task.completed, "user_id": db_task.user_id,
            "created_at": str(db_task.created_at), "updated_at": str(db_task.updated_at),
            "priority": db_task.priority, "tags": db_task.tags,
            "due_at": str(db_task.due_at) if db_task.due_at else None,
            "reminder_at": str(db_task.reminder_at) if db_task.reminder_at else None,
            "recurrence_rule": db_task.recurrence_rule, "is_recurring": db_task.is_recurring,
            "parent_task_id": db_task.parent_task_id,
            "completed_at": str(db_task.completed_at) if db_task.completed_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}"
        )
    finally:
        session.close()


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_create: TaskCreate,
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new task for the authenticated user
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    session = SessionLocal()
    try:
        # Prepare tags as JSON string
        tags_json = json.dumps(task_create.tags) if task_create.tags else None

        db_task = models.Task(
            title=task_create.title,
            description=task_create.description,
            user_id=user_id,
            completed=task_create.completed,
            priority=task_create.priority,
            tags=tags_json,
            due_at=task_create.due_at,
            reminder_at=task_create.reminder_at,
            recurrence_rule=task_create.recurrence_rule,
            is_recurring=task_create.is_recurring
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Log the creation in the audit trail (non-blocking)
        try:
            audit_service = AuditService(session)
            audit_service.log_task_create(db_task)
        except Exception:
            pass  # Don't fail task creation if audit logging fails

        # Invalidate the user's tasks list cache
        with cache_lock:
            tasks_list_cache.pop(user_id, None)

        task_dict = {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "user_id": db_task.user_id,
            "created_at": str(db_task.created_at),
            "updated_at": str(db_task.updated_at),
            "priority": db_task.priority,
            "tags": db_task.tags,
            "due_at": str(db_task.due_at) if db_task.due_at else None,
            "reminder_at": str(db_task.reminder_at) if db_task.reminder_at else None,
            "recurrence_rule": db_task.recurrence_rule,
            "is_recurring": db_task.is_recurring,
            "parent_task_id": db_task.parent_task_id,
            "completed_at": str(db_task.completed_at) if db_task.completed_at else None
        }

        # Publish event to Kafka via Dapr (non-blocking)
        try:
            await publish_task_created(db_task.id, user_id, task_dict)
        except Exception:
            pass

        return task_dict
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )
    finally:
        session.close()


@router.get("/tasks/{task_id}")
async def get_task(
    user_id: str,
    task_id: str,
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve details of a specific task
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    # Check cache first
    cache_key = f"{user_id}:{task_id}"
    with cache_lock:
        cached_task = task_cache.get(cache_key)

    if cached_task is not None:
        return cached_task

    # Fetch from database
    session = SessionLocal()
    try:
        db_task = session.exec(
            select(models.Task).where(
                models.Task.id == task_id,
                models.Task.user_id == user_id
            )
        ).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        result = serialize_task(db_task)
        # Cache the result
        with cache_lock:
            task_cache[cache_key] = result

        return result
    finally:
        session.close()


@router.put("/tasks/{task_id}")
async def update_task(
    user_id: str,
    task_id: str,
    task_update: TaskUpdate,
    current_user: models.User = Depends(get_current_user)
):
    """
    Update properties of an existing task
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    session = SessionLocal()
    try:
        db_task = session.exec(
            select(models.Task).where(
                models.Task.id == task_id,
                models.Task.user_id == user_id
            )
        ).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update task fields
        if task_update.title is not None:
            db_task.title = task_update.title
        if task_update.description is not None:
            db_task.description = task_update.description
        if task_update.completed is not None:
            db_task.completed = task_update.completed

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Invalidate caches for this task and user's task list
        cache_key = f"{user_id}:{task_id}"
        with cache_lock:
            task_cache.pop(cache_key, None)
            tasks_list_cache.pop(user_id, None)

        result = serialize_task(db_task)

        # Publish event to Kafka via Dapr (non-blocking)
        try:
            await publish_task_updated(task_id, user_id, result)
        except Exception:
            pass

        return result
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}"
        )
    finally:
        session.close()


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: str,
    current_user: models.User = Depends(get_current_user)
):
    """
    Delete a specific task
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session = SessionLocal()
    try:
        db_task = session.exec(
            select(models.Task).where(
                models.Task.id == task_id,
                models.Task.user_id == user_id
            )
        ).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        task_data = serialize_task(db_task)
        session.delete(db_task)
        session.commit()

        # Invalidate caches for this task and user's task list
        cache_key = f"{user_id}:{task_id}"
        with cache_lock:
            task_cache.pop(cache_key, None)
            tasks_list_cache.pop(user_id, None)

        # Publish delete event (non-blocking)
        try:
            await publish_task_deleted(task_id, user_id, task_data)
        except Exception:
            pass

        return
    except HTTPException:
        raise  # Re-raise HTTP exceptions (like 404)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task: {str(e)}"
        )
    finally:
        session.close()


@router.patch("/tasks/{task_id}/complete")
async def toggle_task_completion(
    user_id: str,
    task_id: str,
    task_toggle: TaskToggleComplete,
    current_user: models.User = Depends(get_current_user)
):
    """
    Toggle or set the completion status of a task
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    session = SessionLocal()
    try:
        db_task = session.exec(
            select(models.Task).where(
                models.Task.id == task_id,
                models.Task.user_id == user_id
            )
        ).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update completion status and set completed_at timestamp
        db_task.completed = task_toggle.completed
        if task_toggle.completed:
            db_task.completed_at = utc_now()
        else:
            db_task.completed_at = None

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Log the completion in the audit trail (non-blocking)
        try:
            audit_service = AuditService(session)
            if task_toggle.completed:
                audit_service.log_task_complete(db_task)
            if db_task.is_recurring and task_toggle.completed:
                recurrence_service = RecurrenceService(session)
                recurrence_service.process_completed_recurring_task(db_task)
        except Exception:
            pass

        # Invalidate caches
        cache_key = f"{user_id}:{task_id}"
        with cache_lock:
            task_cache.pop(cache_key, None)
            tasks_list_cache.pop(user_id, None)

        result = serialize_task(db_task)

        # Publish completion event (non-blocking)
        try:
            await publish_task_completed(task_id, user_id, result)
        except Exception:
            pass

        return result
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task completion: {str(e)}"
        )
    finally:
        session.close()