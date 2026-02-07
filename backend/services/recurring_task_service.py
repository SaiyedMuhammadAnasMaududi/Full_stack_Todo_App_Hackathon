"""
Recurring Task Service - Consumes task.completed events, creates next recurring instance.
Runs as a separate microservice with Dapr sidecar.
"""
import os
import logging
import httpx
from fastapi import FastAPI
from services.event_processor_base import EventProcessorBase

logger = logging.getLogger(__name__)
app = FastAPI(title="Recurring Task Service")

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"


class RecurringTaskProcessor(EventProcessorBase):
    def __init__(self):
        super().__init__("recurring-service")

    async def handle(self, event: dict):
        if event.get("event_type") != "task.completed":
            return

        task_data = event.get("task_data", {})
        if not task_data.get("is_recurring") or not task_data.get("recurrence_rule"):
            return

        # Create next task instance via Dapr Service Invocation
        new_task = {
            "title": task_data.get("title"),
            "description": task_data.get("description"),
            "priority": task_data.get("priority", "medium"),
            "tags": task_data.get("tags"),
            "recurrence_rule": task_data.get("recurrence_rule"),
            "is_recurring": True,
            "parent_task_id": event.get("task_id"),
            "user_id": event.get("user_id"),
        }

        url = f"{DAPR_BASE_URL}/v1.0/invoke/todo-backend/method/api/{event.get('user_id')}/tasks"

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(url, json=new_task)
                if resp.status_code in (200, 201):
                    logger.info(f"Created next recurring task for parent {event.get('task_id')}")
                else:
                    logger.warning(f"Failed to create recurring task: {resp.status_code}")
        except Exception as e:
            logger.warning(f"Service invocation failed: {e}")


processor = RecurringTaskProcessor()


@app.get("/health")
def health():
    return {"status": "healthy", "service": "recurring-service"}


@app.get("/dapr/subscribe")
def subscribe():
    return [{"pubsubname": "pubsub-kafka", "topic": "task-events", "route": "/events/tasks"}]


@app.post("/events/tasks")
async def handle_task_event(event: dict):
    await processor.process_event(event.get("data", event))
    return {"status": "SUCCESS"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8002")))
