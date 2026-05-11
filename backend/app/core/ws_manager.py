from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        # doc_id → list of websockets
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, doc_id: int, websocket: WebSocket):
        await websocket.accept()

        if doc_id not in self.active_connections:
            self.active_connections[doc_id] = []

        self.active_connections[doc_id].append(websocket)

    def disconnect(self, doc_id: int, websocket: WebSocket):
        if doc_id in self.active_connections:
            self.active_connections[doc_id].remove(websocket)

            if not self.active_connections[doc_id]:
                del self.active_connections[doc_id]

    async def broadcast(self, doc_id: int, message: dict):
        if doc_id in self.active_connections:
            for ws in self.active_connections[doc_id]:
                await ws.send_json(message)


manager = ConnectionManager()