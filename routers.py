import asyncio
import json
import time

from fastapi import WebSocket, APIRouter

from app import simple_cache, cached_data
from models import FactorialResponse
from utils import compute_factorial

ws_router = APIRouter()

@ws_router.websocket('/ws/factorial')
async def ws_factorial(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        
        asyncio.create_task(process_message(websocket, message))
        
async def process_message(websocket: WebSocket, message: str):
    try:
        data = int(message)
    except ValueError:
        await websocket.send_text(
            json.dumps({'code': 400, 'message': message, 'body': {}})
        )
        return
    
    # Простое кеширование
    if data in cached_data:
        factorial = simple_cache[data]
    else:
        factorial = await asyncio.to_thread(compute_factorial, data)
        
        cached_data.add(data)
        simple_cache.update({data: factorial})
    
    result = FactorialResponse(
        number=data,
        result=factorial
    )
    
    await websocket.send_text(
        json.dumps({'code': 200, 'message': message, 'body': result.json()})
    )


        
