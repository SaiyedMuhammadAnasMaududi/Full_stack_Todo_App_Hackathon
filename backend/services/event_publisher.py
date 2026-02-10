"""
Event Publisher - Publishes task events to Kafka via Dapr PubSub.
All task operations (create, update, delete, complete) are published as events.
"""
import os
import uuid
import logging
import httpx
from datetime import datetime

logger = logging.getLogger(__name__)

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"
PUBSUB_NAME = "pubsub-kafka"


async def publish_event(topic: str, event_type: str, task_id: str, user_id: str, task_data: dict):
    """Publish a task event to Kafka via Dapr PubSub."""
    event = {
        "event_type": event_type,
        "task_id": task_id,
        "user_id": user_id,
        "task_data": task_data,
        "timestamp": datetime.utcnow().isoformat(),
        "correlation_id": str(uuid.uuid4()),
    }

    url = f"{DAPR_BASE_URL}/v1.0/publish/{PUBSUB_NAME}/{topic}"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json=event)
            if response.status_code in (200, 204):
                logger.info(f"Published {event_type} to {topic} for task {task_id}")
            else:
                logger.warning(f"Failed to publish event: {response.status_code} {response.text}")
    except Exception as e:
        logger.warning(f"Dapr PubSub unavailable, skipping event publish: {e}")


async def publish_task_created(task_id: str, user_id: str, task_data: dict):
    await publish_event("task-events", "task.created", task_id, user_id, task_data)
    if task_data.get("reminder_at"):
        await publish_event("reminders", "task.reminder_scheduled", task_id, user_id, task_data)
    await publish_event("task-updates", "task.created", task_id, user_id, task_data)


async def publish_task_updated(task_id: str, user_id: str, task_data: dict):
    await publish_event("task-events", "task.updated", task_id, user_id, task_data)
    await publish_event("task-updates", "task.updated", task_id, user_id, task_data)


async def publish_task_completed(task_id: str, user_id: str, task_data: dict):
    await publish_event("task-events", "task.completed", task_id, user_id, task_data)
    await publish_event("task-updates", "task.completed", task_id, user_id, task_data)


async def publish_task_deleted(task_id: str, user_id: str, task_data: dict):
    await publish_event("task-events", "task.deleted", task_id, user_id, task_data)
    await publish_event("task-updates", "task.deleted", task_id, user_id, task_data)
