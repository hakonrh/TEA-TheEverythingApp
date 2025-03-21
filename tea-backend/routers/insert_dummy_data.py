from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from database import get_db

router = APIRouter()

@router.post("/insert-dummy-data")
async def insert_dummy_data(db: AsyncSession = Depends(get_db)):
    try:
        queries = [
            # Insert accounts
            "INSERT INTO Accounts (Email, Username, PasswordHash) VALUES ('alice@example.com', 'Alice', 'hashed_password_1')",
            "INSERT INTO Accounts (Email, Username, PasswordHash) VALUES ('bob@example.com', 'Bob', 'hashed_password_2')",
            "INSERT INTO Accounts (Email, Username, PasswordHash) VALUES ('charlie@example.com', 'Charlie', 'hashed_password_3')",
            "INSERT INTO Accounts (Email, Username, PasswordHash) VALUES ('dave@example.com', 'Dave', 'hashed_password_4')",
            "INSERT INTO Accounts (Email, Username, PasswordHash) VALUES ('eve@example.com', 'Eve', 'hashed_password_5')",
            
            # Insert posts
            "INSERT INTO Posts (AccountID, Content, ParentPostID) VALUES (1, 'Hello world! #welcome', NULL)",
            "INSERT INTO Posts (AccountID, Content, ParentPostID) VALUES (1, 'I love programming! #coding', NULL)",
            "INSERT INTO Posts (AccountID, Content, ParentPostID) VALUES (2, 'Good morning, everyone! #happy', NULL)",
            "INSERT INTO Posts (AccountID, Content, ParentPostID) VALUES (2, 'JavaScript or Python?', NULL)",
            
            # Replies
            "INSERT INTO Posts (AccountID, Content, ParentPostID) VALUES (2, 'Nice post, Alice! #welcome', 1)",
            "INSERT INTO Posts (AccountID, Content, ParentPostID) VALUES (2, 'I love coffee too! ☕', 3)",

            # Sample followers
            "INSERT INTO Followers (FollowerID, FollowingID) VALUES (2, 1)",
            "INSERT INTO Followers (FollowerID, FollowingID) VALUES (3, 1)",
            "INSERT INTO Followers (FollowerID, FollowingID) VALUES (4, 2)",
            "INSERT INTO Followers (FollowerID, FollowingID) VALUES (5, 3)",

            # Sample likes
            "INSERT INTO Likes (AccountID, PostID) VALUES (1, 6)",
            "INSERT INTO Likes (AccountID, PostID) VALUES (2, 1)",
            "INSERT INTO Likes (AccountID, PostID) VALUES (3, 2)",
        ]

        # Execute each query separately
        for query in queries:
            await db.execute(text(query))
        
        await db.commit()
        return {"message": "Dummy data inserted successfully!"}

    except Exception as e:
        await db.rollback()
        return {"error": str(e)}
