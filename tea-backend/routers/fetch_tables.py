from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from fastapi import APIRouter, Depends
from database import get_db

router = APIRouter()

@router.get("/check-tables")
async def check_tables(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
    tables = result.fetchall()
    return {"tables": [row[0] for row in tables]}
