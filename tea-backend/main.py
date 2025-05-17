from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db, get_db_session

from routers import fetch_tables, posts, accounts, search
from user_registration import router as user_router

from fastapi.middleware.cors import CORSMiddleware

from like_batcher import flush_likes
import asyncio

from contextlib import asynccontextmanager
from like_batcher import flush_likes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tea-dofo.onrender.com", "https://tea-cache.onrender.com/", "http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fetch_tables.router)
app.include_router(posts.router)
app.include_router(accounts.router)
app.include_router(search.router, prefix="/search")
app.include_router(user_router, prefix="/user")

@app.get("/")
async def root():
    return {"message": "Welcome to the TEA - The Everything App API!"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background task
    stop_event = asyncio.Event()

    async def flush_loop():
        while not stop_event.is_set():
            async with get_db_session() as db:
                await flush_likes(db)
            await asyncio.sleep(5)

    task = asyncio.create_task(flush_loop())

    yield  # ⬅️ App runs here

    # Shutdown
    stop_event.set()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

# Now initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)
