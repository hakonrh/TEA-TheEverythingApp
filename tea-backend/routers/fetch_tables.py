from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from fastapi import APIRouter, Depends
from database import get_db

router = APIRouter()

@router.get("/tables")
async def check_tables(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT 
            table_name, 
            column_name, 
            data_type 
        FROM information_schema.columns 
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)
    result = await db.execute(query)
    tables_info = result.fetchall()

    # Organizing data into a structured dictionary format
    tables_dict = {}
    for row in tables_info:
        table_name = row.table_name
        if table_name not in tables_dict:
            tables_dict[table_name] = []
        tables_dict[table_name].append({"column_name": row.column_name, "data_type": row.data_type})

    return {"tables": tables_dict}