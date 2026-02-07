"""
Base event processor with idempotency via correlation_id deduplication.
"""
import os
import logging
import httpx

logger = logging.getLogger(__name__)

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"
STATE_STORE = "statestore"


class EventProcessorBase:
    """Base class for event consumers with idempotency."""

    def __init__(self, service_name: str):
        self.service_name = service_name

    async def is_duplicate(self, correlation_id: str) -> bool:
        """Check if event was already processed using Dapr state store."""
        key = f"{self.service_name}-{correlation_id}"
        url = f"{DAPR_BASE_URL}/v1.0/state/{STATE_STORE}/{key}"
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(url)
                return resp.status_code == 200 and resp.text != ""
        except Exception:
            return False

    async def mark_processed(self, correlation_id: str):
        """Mark event as processed in Dapr state store."""
        key = f"{self.service_name}-{correlation_id}"
        url = f"{DAPR_BASE_URL}/v1.0/state/{STATE_STORE}"
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                await client.post(url, json=[{"key": key, "value": {"processed": True}}])
        except Exception as e:
            logger.warning(f"Failed to mark event processed: {e}")

    async def process_event(self, event: dict):
        """Process an event with idempotency check."""
        correlation_id = event.get("correlation_id", "")
        if not correlation_id:
            logger.warning("Event missing correlation_id, processing anyway")
            await self.handle(event)
            return

        if await self.is_duplicate(correlation_id):
            logger.info(f"Duplicate event {correlation_id}, skipping")
            return

        await self.handle(event)
        await self.mark_processed(correlation_id)

    async def handle(self, event: dict):
        """Override in subclass to implement event handling logic."""
        raise NotImplementedError
