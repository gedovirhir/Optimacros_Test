from fastapi import WebSocket, APIRouter

ws_router = APIRouter()

@ws_router.websocket('/ws/factorial')
async def ws_factorial(websocket: WebSocket):
    await websocket.accept()
    
