from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from fastapi import APIRouter, Depends
from database import get_db

router = APIRouter()

@router.get("/check-posts")
async def check_tables(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM Posts LIMIT 5;"))
    tables = result.fetchall()
    return {"tables": [row[0] for row in tables]}

@router.get("/check-accounts")
async def check_tables(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM Accounts LIMIT 5;"))
    tables = result.fetchall()
    return {"tables": [row[0] for row in tables]}
