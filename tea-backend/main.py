from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db

from routers import insert_dummy_data, fetch_tables, user_registration

app = FastAPI()

app.include_router(insert_dummy_data.router, prefix="/data")
app.include_router(fetch_tables.router)
app.include_router(user_registration, prefix="/user")

@app.get("/")
async def root():
    return {"message": "Welcome to the TEA - The Everything App API!"}

