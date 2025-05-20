from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db, SessionLocal

from routers import fetch_tables, posts, accounts, search, logs_route
from user_registration import router as user_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from like_batcher import flush_likes

import asyncio
from contextlib import asynccontextmanager

from typing import List
import time
from contextvars import ContextVar
from datetime import datetime
from log_state import logs, db_counter
import pytz

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = round((time.time() - start_time) * 1000, 2)
    method = request.method
    path = request.url.path

    # Capture request info and DB access count
    logs.append({
        "timestamp": datetime.now(pytz.utc).isoformat() + "Z",
        "method": method,
        "path": path,
        "duration_ms": duration,
        "db_accesses": db_counter.get()
    })

    return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    stop_event = asyncio.Event()

    async def flush_loop():
        while not stop_event.is_set():
            async with SessionLocal() as db:
                await flush_likes(db)
            await asyncio.sleep(5)

    task = asyncio.create_task(flush_loop())

    # This is where the app runs
    yield  

    stop_event.set()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tea-dofo.onrender.com",
        "https://tea-cache.onrender.com/",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fetch_tables.router)
app.include_router(posts.router)
app.include_router(accounts.router)
app.include_router(search.router, prefix="/search")
app.include_router(user_router, prefix="/user")
app.include_router(logs_route.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the TEA - The Everything App API!"}
