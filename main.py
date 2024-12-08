from fastapi import FastAPI
from fastapi.websockets import WebSocket
from typing import List

app = FastAPI()

active_connections: List[WebSocket] = []

async def broadcast_message(message: str):
    for connection in active_connections:
        await connection.send_text(message)

@app.websocket("/ws/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await broadcast_message(data)
    except Exception:
        active_connections.remove(websocket)
