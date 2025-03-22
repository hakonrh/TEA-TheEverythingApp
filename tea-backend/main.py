from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db

from routers import insert_dummy_data, fetch_random, fetch_tables

app = FastAPI()

app.include_router(insert_dummy_data.router, prefix="/data", tags=["Data Management"])
app.include_router(fetch_random.router, prefix="/random", tags=["Random Data"])
app.include_router(fetch_tables.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Twitter Clone API!"}

# Test database connection
@app.get("/ping-db")
async def ping_db(db: AsyncSession = Depends(get_db)):
    try:
        # Just a simple query to check connection
        result = await db.execute(text("SELECT 1"))
        return {"status": "Database Connected", "result": result.scalar()}
    except Exception as e:
        return {"status": "Database Error", "error": str(e)}
