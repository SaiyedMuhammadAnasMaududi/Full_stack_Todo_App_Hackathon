"""
Audit Service - Consumes all task events, persists audit trail.
Runs as a separate microservice with Dapr sidecar.
"""
import os
import uuid
import logging
import httpx
from fastapi import FastAPI
from services.event_processor_base import EventProcessorBase

logger = logging.getLogger(__name__)
app = FastAPI(title="Audit Service")

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"
STATE_STORE = "statestore"


class AuditProcessor(EventProcessorBase):
    def __init__(self):
        super().__init__("audit-service")

    async def handle(self, event: dict):
        audit_entry = {
            "id": str(uuid.uuid4()),
            "event_type": event.get("event_type"),
            "task_id": event.get("task_id"),
            "user_id": event.get("user_id"),
            "timestamp": event.get("timestamp"),
            "snapshot": event.get("task_data", {}),
        }

        # Persist to Dapr state store
        key = f"audit-{audit_entry['id']}"
        url = f"{DAPR_BASE_URL}/v1.0/state/{STATE_STORE}"

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(url, json=[{"key": key, "value": audit_entry}])
                if resp.status_code in (200, 204):
                    logger.info(f"Audit entry saved: {event.get('event_type')} for task {event.get('task_id')}")
                else:
                    logger.warning(f"Failed to save audit entry: {resp.status_code}")
        except Exception as e:
            logger.warning(f"State store unavailable: {e}")


processor = AuditProcessor()


@app.get("/health")
def health():
    return {"status": "healthy", "service": "audit-service"}


@app.get("/dapr/subscribe")
def subscribe():
    return [{"pubsubname": "pubsub-kafka", "topic": "task-events", "route": "/events/tasks"}]


@app.post("/events/tasks")
async def handle_task_event(event: dict):
    await processor.process_event(event.get("data", event))
    return {"status": "SUCCESS"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8003")))
