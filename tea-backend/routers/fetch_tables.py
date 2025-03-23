from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from pydantic import BaseModel

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

@router.get("/posts")
async def get_posts(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT accounts.username, posts.content, posts.createdat 
        FROM posts 
        JOIN accounts ON posts.accountid = accounts.accountid
        ORDER BY posts.createdat DESC;
    """)
    result = await db.execute(query)
    posts = result.fetchall()
    return {"posts": [dict(row._mapping) for row in posts]}

@router.get("/accountposts")
async def get_accounts(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT accounts.username, 
               COUNT(posts.postid) AS num_posts, 
               json_agg(json_build_object(
                   'postid', posts.postid, 
                   'content', posts.content, 
                   'createdat', posts.createdat
               )) AS posts
        FROM accounts
        LEFT JOIN posts ON accounts.accountid = posts.accountid
        GROUP BY accounts.username;
    """)
    result = await db.execute(query)
    accounts = result.fetchall()
    return {"accounts": [dict(row._mapping) for row in accounts]}

@router.get("/accounts")
async def get_accounts(db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT accounts.username, 
               COUNT(posts.postid) AS num_posts
        FROM accounts
        LEFT JOIN posts ON accounts.accountid = posts.accountid
        GROUP BY accounts.username;
    """)
    result = await db.execute(query)
    accounts = result.fetchall()
    return {"accounts": [dict(row._mapping) for row in accounts]}

class CreatePostRequest(BaseModel):
    accountid: int
    content: str

@router.post("/posts")
async def create_post(
    post_data: CreatePostRequest,
    db: AsyncSession = Depends(get_db)
):
    if not post_data.content or len(post_data.content) > 240:
        raise HTTPException(status_code=400, detail="Post content must be between 1 and 240 characters.")

    query = text("""
        INSERT INTO posts (accountid, content) 
        VALUES (:accountid, :content) 
        RETURNING postid, createdat;
    """)
    result = await db.execute(query, {"accountid": post_data.accountid, "content": post_data.content})
    post = result.fetchone()
    await db.commit()

    return {"postid": post.postid, "accountid": post_data.accountid, "content": post_data.content, "createdat": post.createdat}

class EditPostRequest(BaseModel):
    accountid: int
    new_content: str

@router.put("/posts/{post_id}")
async def edit_post(
    post_id: int,
    post_data: EditPostRequest,
    db: AsyncSession = Depends(get_db)
):
    if not post_data.new_content or len(post_data.new_content) > 240:
        raise HTTPException(status_code=400, detail="Post content must be between 1 and 240 characters.")

    # Check if the post exists and belongs to the user
    check_query = text("SELECT accountid FROM posts WHERE postid = :postid;")
    result = await db.execute(check_query, {"postid": post_id})
    post = result.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    if post.accountid != post_data.accountid:
        raise HTTPException(status_code=403, detail="You can only edit your own posts.")

    # Update the post
    update_query = text("""
        UPDATE posts 
        SET content = :new_content, lastedited = NOW() 
        WHERE postid = :postid
        RETURNING postid, createdat, lastedited;
    """)
    updated_result = await db.execute(update_query, {"postid": post_id, "new_content": post_data.new_content})
    updated_post = updated_result.fetchone()
    await db.commit()

    return {"postid": updated_post.postid, "content": post_data.new_content, "lastedited": updated_post.lastedited}

class DeletePostRequest(BaseModel):
    accountid: int

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    post_data: DeletePostRequest,
    db: AsyncSession = Depends(get_db)
):
    # Check if the post exists and belongs to the user
    check_query = text("SELECT accountid FROM posts WHERE postid = :postid;")
    result = await db.execute(check_query, {"postid": post_id})
    post = result.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    if post.accountid != post_data.accountid:
        raise HTTPException(status_code=403, detail="You can only delete your own posts.")

    # Delete the post
    delete_query = text("DELETE FROM posts WHERE postid = :postid;")
    await db.execute(delete_query, {"postid": post_id})
    await db.commit()

    return {"message": "Post deleted successfully."}
