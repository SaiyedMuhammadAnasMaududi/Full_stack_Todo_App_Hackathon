"""
Audit Service
Handles the logging of task-related actions for accountability and debugging
"""

from datetime import datetime
from typing import Optional
import json
from sqlmodel import Session

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models import TaskAudit, Task
from utils.datetime_utils import utc_now


class AuditService:
    def __init__(self, session: Session):
        self.session = session

    def log_task_action(
        self,
        task_id: str,
        user_id: str,
        action: str,
        details: Optional[dict] = None
    ) -> TaskAudit:
        """
        Log a task-related action to the audit trail
        """
        # Create audit record
        audit_record = TaskAudit(
            task_id=task_id,
            user_id=user_id,
            action=action,
            timestamp=utc_now(),
            details=json.dumps(details) if details else None
        )

        # Add to session and commit
        self.session.add(audit_record)
        self.session.commit()
        self.session.refresh(audit_record)

        return audit_record

    def log_task_create(self, task: Task) -> TaskAudit:
        """Log the creation of a task"""
        details = {
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "tags": task.tags,
            "due_at": task.due_at.isoformat() if task.due_at else None,
            "reminder_at": task.reminder_at.isoformat() if task.reminder_at else None,
            "is_recurring": task.is_recurring,
            "recurrence_rule": task.recurrence_rule
        }

        return self.log_task_action(
            task_id=task.id,
            user_id=task.user_id,
            action="create",
            details=details
        )

    def log_task_update(self, task: Task, updated_fields: list) -> TaskAudit:
        """Log the update of a task"""
        details = {
            "updated_fields": updated_fields,
            "title": task.title,
            "completed": task.completed,
            "priority": task.priority,
            "tags": task.tags,
            "due_at": task.due_at.isoformat() if task.due_at else None,
            "reminder_at": task.reminder_at.isoformat() if task.reminder_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }

        return self.log_task_action(
            task_id=task.id,
            user_id=task.user_id,
            action="update",
            details=details
        )

    def log_task_complete(self, task: Task) -> TaskAudit:
        """Log the completion of a task"""
        details = {
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }

        return self.log_task_action(
            task_id=task.id,
            user_id=task.user_id,
            action="complete",
            details=details
        )

    def log_task_delete(self, task: Task) -> TaskAudit:
        """Log the deletion of a task"""
        details = {
            "title": task.title,
            "was_completed": task.completed
        }

        return self.log_task_action(
            task_id=task.id,
            user_id=task.user_id,
            action="delete",
            details=details
        )

    def get_task_history(self, task_id: str) -> list:
        """Retrieve the audit history for a specific task"""
        statement = select(TaskAudit).where(TaskAudit.task_id == task_id).order_by(TaskAudit.timestamp.desc())
        audit_records = self.session.exec(statement).all()
        return audit_records

    def get_user_task_history(self, user_id: str, limit: int = 50) -> list:
        """Retrieve audit history for all tasks of a specific user"""
        statement = select(TaskAudit).where(TaskAudit.user_id == user_id).order_by(TaskAudit.timestamp.desc()).limit(limit)
        audit_records = self.session.exec(statement).all()
        return audit_records