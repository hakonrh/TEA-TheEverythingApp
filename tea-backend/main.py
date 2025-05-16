from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db

from routers import fetch_tables, posts, accounts, search
from user_registration import router as user_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tea-dofo.onrender.com", "http://localhost:3000", "http://localhost:8000"],
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
