"""
Notification Service - Consumes reminder events, schedules Dapr Jobs for reminders.
Runs as a separate microservice with Dapr sidecar.
"""
import os
import logging
import httpx
from fastapi import FastAPI
from services.event_processor_base import EventProcessorBase

logger = logging.getLogger(__name__)
app = FastAPI(title="Notification Service")

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"


class ReminderProcessor(EventProcessorBase):
    def __init__(self):
        super().__init__("notification-service")

    async def handle(self, event: dict):
        task_data = event.get("task_data", {})
        task_id = event.get("task_id")
        reminder_at = task_data.get("reminder_at")

        if not reminder_at:
            return

        # Schedule a Dapr Job for the reminder
        job_name = f"reminder-{task_id}"
        url = f"{DAPR_BASE_URL}/v1.0-alpha1/jobs/{job_name}"

        job_payload = {
            "schedule": f"@every 0s",  # One-time trigger
            "dueTime": reminder_at,
            "data": {
                "task_id": task_id,
                "user_id": event.get("user_id"),
                "title": task_data.get("title", ""),
            },
        }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(url, json=job_payload)
                if resp.status_code in (200, 204):
                    logger.info(f"Scheduled reminder job for task {task_id} at {reminder_at}")
                else:
                    logger.warning(f"Failed to schedule reminder: {resp.status_code}")
        except Exception as e:
            logger.warning(f"Dapr Jobs API unavailable: {e}")


processor = ReminderProcessor()


@app.get("/health")
def health():
    return {"status": "healthy", "service": "notification-service"}


@app.get("/dapr/subscribe")
def subscribe():
    return [{"pubsubname": "pubsub-kafka", "topic": "reminders", "route": "/events/reminders"}]


@app.post("/events/reminders")
async def handle_reminder_event(event: dict):
    await processor.process_event(event.get("data", event))
    return {"status": "SUCCESS"}


@app.post("/job/reminder")
async def handle_reminder_job(data: dict):
    """Called by Dapr Jobs API when reminder fires."""
    logger.info(f"Reminder fired for task {data.get('task_id')}: {data.get('title')}")
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8001")))
