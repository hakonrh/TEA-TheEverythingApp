from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

router = APIRouter()

@router.post("/insert-dummy-data")
async def insert_dummy_data(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute("""
            -- Insert sample accounts
            INSERT INTO Accounts (Email, Username, PasswordHash) VALUES
            ('alice@example.com', 'Alice', 'hashed_password_1'),
            ('bob@example.com', 'Bob', 'hashed_password_2'),
            ('charlie@example.com', 'Charlie', 'hashed_password_3'),
            ('dave@example.com', 'Dave', 'hashed_password_4'),
            ('eve@example.com', 'Eve', 'hashed_password_5');

            -- Insert posts
            INSERT INTO Posts (AccountID, Content, ParentPostID) VALUES
            (1, 'Hello world! #welcome', NULL),
            (1, 'I love programming! #coding', NULL),
            (1, 'Just had a great coffee ☕', NULL),
            (1, 'Anyone up for a challenge? #fun', NULL),
            (1, 'Learning SQL today!', NULL),

            (2, 'Good morning, everyone! #happy', NULL),
            (2, 'Working on a cool project 🚀', NULL),
            (2, 'Can’t believe it’s already March!', NULL),
            (2, 'Looking for book recommendations 📚 #reading', NULL),
            (2, 'JavaScript or Python?', NULL),

            -- Replies
            (2, 'Nice post, Alice! #welcome', 1),
            (2, 'Coding is life! #coding', 2),
            (2, 'I love coffee too! ☕', 3),
            (2, 'I’m always up for a challenge! 💪', 4),
            (2, 'SQL is super useful!', 5);

            -- Sample followers
            INSERT INTO Followers (FollowerID, FollowingID) VALUES
            (2, 1),
            (3, 1),
            (4, 2),
            (5, 3);

            -- Sample likes
            INSERT INTO Likes (AccountID, PostID) VALUES
            (1, 6),
            (2, 1),
            (3, 2),
            (4, 11),
            (5, 16);
        """)
        await db.commit()
        return {"message": "Dummy data inserted successfully!"}
    except Exception as e:
        await db.rollback()
        return {"error": str(e)}
