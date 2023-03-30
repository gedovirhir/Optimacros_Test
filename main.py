import uvicorn

from config import WEB_PORT, WEB_HOST
from app import app

from routers import ws_router

app.include_router(ws_router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        port=WEB_PORT
    )