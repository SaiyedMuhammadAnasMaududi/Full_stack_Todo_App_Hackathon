"""
Recurring Task Service
Handles the creation of recurring tasks based on recurrence rules
"""

from datetime import datetime
from typing import List, Optional
import pytz
from sqlmodel import Session, select
from dateutil import rrule

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models import Task, RecurringTaskTemplate
from utils.datetime_utils import validate_recurrence_rule, utc_now


class RecurrenceService:
    def __init__(self, session: Session):
        self.session = session

    def create_next_instance(self, task: Task) -> Optional[Task]:
        """
        Create the next instance of a recurring task based on the recurrence rule
        """
        if not task.is_recurring or not task.recurrence_rule:
            return None

        # Validate recurrence rule
        if not validate_recurrence_rule(task.recurrence_rule):
            raise ValueError("Invalid recurrence rule")

        # Parse the recurrence rule
        try:
            # Remove 'RRULE:' prefix if present
            rrule_str = task.recurrence_rule
            if rrule_str.upper().startswith('RRULE:'):
                rrule_str = rrule_str[6:]

            # Parse the rule components
            rule_parts = {}
            for part in rrule_str.split(';'):
                if '=' in part:
                    key, value = part.split('=', 1)
                    rule_parts[key] = value

            # Determine the start date for the next occurrence
            start_date = task.due_at if task.due_at else task.created_at

            # Generate the next occurrence using dateutil.rrule
            freq_map = {
                'DAILY': rrule.DAILY,
                'WEEKLY': rrule.WEEKLY,
                'MONTHLY': rrule.MONTHLY,
                'YEARLY': rrule.YEARLY
            }

            freq = rule_parts.get('FREQ', 'DAILY').upper()
            if freq not in freq_map:
                raise ValueError(f"Unsupported frequency: {freq}")

            # Create the rule
            rule = rrule.rrule(
                freq=freq_map[freq],
                dtstart=start_date,
                count=2  # We only need the next occurrence
            )

            # Find the next occurrence after the current due date or creation date
            next_occurrence = None
            for occurrence in rule:
                if occurrence > start_date:
                    next_occurrence = occurrence
                    break

            if not next_occurrence:
                return None

            # Create a new task instance with the next occurrence date
            new_task = Task(
                title=task.title,
                description=task.description,
                user_id=task.user_id,
                priority=task.priority,
                tags=task.tags,
                due_at=next_occurrence,
                reminder_at=task.reminder_at,  # Carry over the same reminder time
                recurrence_rule=task.recurrence_rule,
                is_recurring=task.is_recurring,
                parent_task_id=task.id  # Link to the original task
            )

            # Add to session and commit
            self.session.add(new_task)
            self.session.commit()
            self.session.refresh(new_task)

            return new_task

        except Exception as e:
            # Log error and return None
            print(f"Error creating next recurring task instance: {str(e)}")
            return None

    def process_completed_recurring_task(self, task: Task) -> Optional[Task]:
        """
        Process a completed recurring task and create the next instance if applicable
        """
        if not task.is_recurring:
            return None

        # Set completed_at timestamp
        task.completed_at = utc_now()
        task.completed = True

        # Save the changes
        self.session.add(task)
        self.session.commit()

        # Create next instance
        next_instance = self.create_next_instance(task)

        return next_instance

    def validate_and_parse_rrule(self, rrule_str: str) -> dict:
        """
        Validate and parse recurrence rule string
        """
        if not rrule_str.upper().startswith('RRULE:'):
            rrule_str = f"RRULE:{rrule_str}"

        # Basic validation
        if not validate_recurrence_rule(rrule_str):
            raise ValueError("Invalid recurrence rule format")

        # Parse the rule components
        rrule_str = rrule_str[6:]  # Remove 'RRULE:' prefix
        rule_parts = {}
        for part in rrule_str.split(';'):
            if '=' in part:
                key, value = part.split('=', 1)
                rule_parts[key] = value

        # Validate required components
        if 'FREQ' not in rule_parts:
            raise ValueError("FREQ is required in recurrence rule")

        return rule_parts