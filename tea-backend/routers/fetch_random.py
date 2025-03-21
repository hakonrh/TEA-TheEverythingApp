import random
from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import Post, Account, Follower, Like

router = APIRouter()

@router.get("/random-post")
async def get_random_post(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    return random.choice(posts) if posts else {"message": "No posts available"}

@router.get("/random-account")
async def get_random_account(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Account))
    accounts = result.scalars().all()
    return random.choice(accounts) if accounts else {"message": "No accounts available"}

@router.get("/random-follower")
async def get_random_follower(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Follower))
    followers = result.scalars().all()
    return random.choice(followers) if followers else {"message": "No followers available"}

@router.get("/random-like")
async def get_random_like(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Like))
    likes = result.scalars().all()
    return random.choice(likes) if likes else {"message": "No likes available"}
