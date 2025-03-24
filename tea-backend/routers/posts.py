from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from pydantic import BaseModel
from user_registration import get_current_account
from models import Account
from schemas import CreatePostRequest, EditPostRequest

router = APIRouter()

# Get all posts
@router.get("/posts")
async def get_posts(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT posts.postid, accounts.username, accounts.email, posts.content, posts.createdat 
        FROM posts 
        JOIN accounts ON posts.accountid = accounts.accountid
        ORDER BY posts.createdat DESC;
    """)
    result = await db.execute(query)
    posts = result.fetchall()
    
    return {"posts": [dict(row._mapping) for row in posts]}

# Get current user's posts
@router.get("/myposts")
async def get_user_posts(
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account)
):
    query = text("""
        SELECT postid, content, createdat, lastedited
        FROM posts
        WHERE accountid = :accountid
        ORDER BY createdat DESC;
    """)

    result = await db.execute(query, {"accountid": current_user.accountid})
    posts = result.fetchall()

    return {"posts": [dict(row._mapping) for row in posts]}


# Make a new post
@router.post("/posts")
async def create_post(
    post_data: CreatePostRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account)
):
    if not post_data.content or len(post_data.content) > 240:
        raise HTTPException(status_code=400, detail="Post content must be between 1 and 240 characters.")

    query = text("""
        INSERT INTO posts (accountid, content) 
        VALUES (:accountid, :content) 
        RETURNING postid, createdat;
    """)

    values = {
        "accountid": current_user.accountid,
        "content": post_data.content,
    }

    result = await db.execute(query, values)
    post = result.fetchone()

    if not post:
        raise HTTPException(status_code=500, detail="Failed to create post")

    await db.commit()
    return {"postid": post.postid, "content": post_data.content, "createdat": post.createdat}

# Edit post by id
@router.put("/posts/{post_id}")
async def edit_post(
    post_id: int,
    post_data: EditPostRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account)
):
    if not post_data.new_content or len(post_data.new_content) > 240:
        raise HTTPException(status_code=400, detail="Post content must be between 1 and 240 characters.")

    result = await db.execute(text("SELECT * FROM posts WHERE postid = :postid"), {"postid": post_id})
    post = result.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.accountid != current_user.accountid:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")

    # Update the post
    await db.execute(
        text("UPDATE posts SET content = :content, lastedited = NOW() WHERE postid = :postid"),
        {"content": post_data.new_content, "postid": post_id},
    )
    await db.commit()

    return {"message": "Post updated"}

# Delete post by id
@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    current_user: Account = Depends(get_current_account),
    db: AsyncSession = Depends(get_db)
):
     # Check if post exists and belongs to user
    result = await db.execute(text("SELECT * FROM posts WHERE postid = :postid"), {"postid": post_id})
    post = result.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.accountid != current_user.accountid:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    # Delete the post
    await db.execute(text("DELETE FROM posts WHERE postid = :postid"), {"postid": post_id})
    await db.commit()

    return {"message": "Post deleted"}
