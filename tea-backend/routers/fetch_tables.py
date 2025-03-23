from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from fastapi import APIRouter, Depends
from database import get_db

router = APIRouter()

@router.get("/check-posts")
async def check_tables(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM posts LIMIT 5;"))
    tables = result.fetchall()
    return {"posts": [dict(row._mapping) for row in tables]}

@router.get("/check-accounts")
async def check_tables(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM accounts LIMIT 5;"))
    tables = result.fetchall()
    return {"accounts": [dict(row._mapping) for row in tables]}  

@router.get("/check-tables")
async def check_tables(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
    tables = result.fetchall()
    return {"tables": [dict(row._mapping) for row in tables]}
