"""
WebSocket Sync Service - Consumes task-updates, broadcasts to connected clients.
Runs as a separate microservice with Dapr sidecar.
"""
import os
import logging
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List

logger = logging.getLogger(__name__)
app = FastAPI(title="WebSocket Sync Service")

# Track connected clients by user_id
connections: Dict[str, List[WebSocket]] = {}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "websocket-service"}


@app.get("/dapr/subscribe")
def subscribe():
    return [{"pubsubname": "pubsub-kafka", "topic": "task-updates", "route": "/events/updates"}]


@app.post("/events/updates")
async def handle_update_event(event: dict):
    """Broadcast task updates to connected WebSocket clients."""
    data = event.get("data", event)
    user_id = data.get("user_id", "")

    if user_id in connections:
        message = json.dumps(data)
        disconnected = []
        for ws in connections[user_id]:
            try:
                await ws.send_text(message)
            except Exception:
                disconnected.append(ws)
        for ws in disconnected:
            connections[user_id].remove(ws)

    return {"status": "SUCCESS"}


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()

    if user_id not in connections:
        connections[user_id] = []
    connections[user_id].append(websocket)

    logger.info(f"WebSocket connected for user {user_id}")

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections[user_id].remove(websocket)
        logger.info(f"WebSocket disconnected for user {user_id}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8004")))
