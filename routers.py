import asyncio
import json
import time

from fastapi import WebSocket, APIRouter, WebSocketDisconnect

from config import CALC_TIMEOUT

from app import simple_cache, cached_data
from models import FactorialResponse
from utils import compute_factorial, DecimalEncoder

ws_router = APIRouter()

@ws_router.websocket('/ws/factorial')
async def ws_factorial(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            asyncio.create_task(process_message(websocket, message))
    except WebSocketDisconnect:
        await websocket.close()
        
async def process_message(websocket: WebSocket, message: str):
    # Простое кеширование
    if message in cached_data:
        await websocket.send_text(
            simple_cache[message]
        )
    else:
        async def __make_response():
            response = {
                'code': None, 
                'message': message, 
                'body': {}
            }
            
            try:
                data = int(message)
            except ValueError:
                response.update({'code': 400})
                return json.dumps(response)
            
            try:
                factorial = await asyncio.wait_for(
                    asyncio.to_thread(compute_factorial, data),
                    timeout=CALC_TIMEOUT
                )
            except asyncio.TimeoutError:
                response.update(
                    {'code': 408}
                )
                return json.dumps(response)
            
            result = FactorialResponse(
                number=data,
                result=factorial
            )
            response.update(
                {
                    'code': 200,
                    'body': result.dict()
                }
            )
            return json.dumps(response, cls=DecimalEncoder)

        resp = await __make_response()
        
        cached_data.add(message)
        simple_cache[message] = resp
        
        await websocket.send_text(
            resp
        )

