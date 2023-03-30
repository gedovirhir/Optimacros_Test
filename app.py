from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from static import index_html

app = FastAPI()
simple_cache = {}
cached_data = set()

@app.get('/')
async def get_main_page():
    return HTMLResponse(index_html)