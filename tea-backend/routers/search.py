from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from fastapi import APIRouter, Depends, HTTPException
from database import get_db

router = APIRouter()

@router.get("/posts")
async def search_posts(
    q: str,
    db: AsyncSession = Depends(get_db)
):
    if not q:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    search_term = f"%{q}%"

    query = text("""
        SELECT posts.postid, accounts.username, accounts.email, posts.content, posts.createdat 
        FROM posts 
        JOIN accounts ON posts.accountid = accounts.accountid
        WHERE posts.content ILIKE :search
        ORDER BY posts.createdat DESC
    """)

    result = await db.execute(query, {"search": search_term})
    posts = [dict(row._mapping) for row in result.fetchall()]

    return {"posts": posts}


@router.get("/accounts")
async def search_accounts(
    q: str,
    db: AsyncSession = Depends(get_db)
):
    if not q:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    search_term = f"%{q}%"

    query = text("""
        SELECT accountid, username, email
        FROM accounts
        WHERE username ILIKE :search OR email ILIKE :search
    """)

    result = await db.execute(query, {"search": search_term})
    accounts = [dict(row._mapping) for row in result.fetchall()]

    return {"accounts": accounts}


@router.get("/hashtags")
async def search_hashtags(
    q: str,
    db: AsyncSession = Depends(get_db)
):
    if not q:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    hashtag_term = f"%#{q}%" 
    
    query = text("""
        SELECT posts.postid, accounts.username, posts.content, posts.createdat
        FROM posts
        JOIN accounts ON posts.accountid = accounts.accountid
        WHERE posts.content ILIKE :hashtag
        ORDER BY posts.createdat DESC;
    """)

    result = await db.execute(query, {"hashtag": hashtag_term})
    hashtags = [dict(row._mapping) for row in result.fetchall()]

    return {"hashtags": hashtags}
