from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from fastapi import APIRouter, Depends
from database import get_db
from pydantic import BaseModel

from cache_db import get_or_set_cache

router = APIRouter()

@router.get("/accountposts")
async def get_accounts(db: AsyncSession = Depends(get_db)):
    async def fetch():
        query = text("""SELECT accounts.username, accounts.email,
                        COUNT(posts.postid) AS num_posts, 
                        json_agg(json_build_object('postid', posts.postid, 'content', posts.content, 'createdat', posts.createdat)) AS posts
                        FROM accounts LEFT JOIN posts ON accounts.accountid = posts.accountid
                        GROUP BY accounts.username, accounts.email""")
        result = await db.execute(query)
        return [dict(row._mapping) for row in result.fetchall()]

    accounts = await get_or_set_cache("accountposts:all", fetch)
    return {"accounts": accounts}


@router.get("/accounts")
async def get_accounts(db: AsyncSession = Depends(get_db)):
    async def fetch():
        query = text("""SELECT accounts.accountid, accounts.username, accounts.email,
                        COUNT(posts.postid) AS num_posts FROM accounts 
                        LEFT JOIN posts ON accounts.accountid = posts.accountid 
                        GROUP BY accounts.accountid, accounts.username, accounts.email""")
        result = await db.execute(query)
        return [dict(row._mapping) for row in result.fetchall()]
    
    accounts = await get_or_set_cache("accounts:all", fetch)
    return {"accounts": accounts}
