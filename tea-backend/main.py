from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db

app = FastAPI()

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
