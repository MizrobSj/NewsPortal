
from socketio import AsyncServer, ASGIApp
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
    
import random


from news import add_news, news

fastapi_app = FastAPI()
sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = ASGIApp(sio, other_asgi_app=fastapi_app)

templates = Jinja2Templates(directory="templates")

# Add CORS middleware to allow cross-origin requests
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Index route to render the main page with news
@fastapi_app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "news": news
    })

# Connect event
@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)

# Disconnect event
@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)


# Endpoint to generate news and emit it to connected clients
@fastapi_app.post("/admin/generate_news")
async def generate_news(auto: bool = False):
    # Generate a random title for the news item
    title = f"News {random.randint(1, 999)}"
    content = "Generated news content."
    item = add_news(title, content)
    # Emit the new news item to all connected clients
    await sio.emit("new_news", item)
    return {"status": "ok", "news": item}


background_task = None

# Starts a background task that generates news every interval_seconds.
# If the task is already running, it will return a message.
@fastapi_app.post("/admin/start_auto_generate")
async def start_auto_generate(interval_seconds: int = 10):

    global background_task
    if background_task is not None and not background_task.done():
        return {"status": "already_running"}
    
    # Define the background task to generate news periodically
    async def worker():
        try:
            while True:
                await generate_news(auto=True)
                await asyncio.sleep(interval_seconds)
        except asyncio.CancelledError:
            pass

    # Start the background task
    background_task = asyncio.create_task(worker())
    return {"status": "started", "interval_seconds": interval_seconds}


# Stops the background task if it is running.
@fastapi_app.post("/admin/stop_auto_generate")
async def stop_auto_generate():
    global background_task
    if background_task is None:
        return {"status": "not_running"}
    
    # If the task is running, cancel it
    background_task.cancel()
    background_task = None
    return {"status": "stopped"}