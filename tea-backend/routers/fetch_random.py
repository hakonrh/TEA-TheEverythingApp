import random
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from database import get_db

router = APIRouter()

async def fetch_all_as_dicts(result):
    """Helper function to convert raw SQLAlchemy result to list of dictionaries"""
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]  # Convert Row objects to dictionaries

@router.get("/random-post")
async def get_random_post(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM posts;"))
    posts = result.fetchall()
    return random.choice(posts) if posts else {"message": "No posts available"}

@router.get("/random-account")
async def get_random_account(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM accounts;"))
    accounts = result.fetchall()
    return random.choice(accounts) if accounts else {"message": "No accounts available"}

@router.get("/random-follower")
async def get_random_follower(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM followers;"))
    followers = result.fetchall()
    return random.choice(followers) if followers else {"message": "No followers available"}

@router.get("/random-like")
async def get_random_like(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM likes;"))
    likes = result.fetchall()
    return random.choice(likes) if likes else {"message": "No likes available"}
