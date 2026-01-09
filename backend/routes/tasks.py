from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel
from slowapi import _rate_limit_exceeded_handler
import models
from db import SessionLocal
from auth import get_current_user
from sqlmodel import Session, select
from cachetools import TTLCache
import threading

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


class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

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


class TaskToggleComplete(BaseModel):
    completed: bool


@router.get("/tasks", response_model=List[models.Task])
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

        # Cache the results
        with cache_lock:
            tasks_list_cache[user_id] = tasks

        return tasks
    finally:
        session.close()


@router.post("/tasks", response_model=models.Task, status_code=status.HTTP_201_CREATED)
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
        db_task = models.Task(
            title=task_create.title,
            description=task_create.description,
            user_id=user_id,
            completed=task_create.completed
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Invalidate the user's tasks list cache
        with cache_lock:
            tasks_list_cache.pop(user_id, None)

        return db_task
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )
    finally:
        session.close()


@router.get("/tasks/{task_id}", response_model=models.Task)
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

        # Cache the result
        with cache_lock:
            task_cache[cache_key] = db_task

        return db_task
    finally:
        session.close()


@router.put("/tasks/{task_id}", response_model=models.Task)
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

        return db_task
    except HTTPException:
        raise  # Re-raise HTTP exceptions (like 404)
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

        session.delete(db_task)
        session.commit()

        # Invalidate caches for this task and user's task list
        cache_key = f"{user_id}:{task_id}"
        with cache_lock:
            task_cache.pop(cache_key, None)
            tasks_list_cache.pop(user_id, None)

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


@router.patch("/tasks/{task_id}/complete", response_model=models.Task)
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

        # Update completion status
        db_task.completed = task_toggle.completed
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Invalidate caches for this task and user's task list
        cache_key = f"{user_id}:{task_id}"
        with cache_lock:
            task_cache.pop(cache_key, None)
            tasks_list_cache.pop(user_id, None)

        return db_task
    except HTTPException:
        raise  # Re-raise HTTP exceptions (like 404)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task completion: {str(e)}"
        )
    finally:
        session.close()