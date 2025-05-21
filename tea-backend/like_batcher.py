import asyncio
import time
from typing import Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

# post_id -> (like_count, first_like_timestamp)
_like_buffer: Dict[int, Tuple[int, float]] = {}
_lock = asyncio.Lock()

MAX_BATCH_SIZE = 10
MAX_WAIT_TIME = 60

async def add_like(post_id: int):
    async with _lock:
        now = time.time()
        if post_id not in _like_buffer:
            _like_buffer[post_id] = (1, now)
        else:
            count, first_ts = _like_buffer[post_id]
            _like_buffer[post_id] = (count + 1, first_ts)

async def flush_likes(db: AsyncSession):
    async with _lock:
        to_flush = {}
        now = time.time()

        for post_id, (count, first_ts) in list(_like_buffer.items()):
            if count >= MAX_BATCH_SIZE or now - first_ts >= MAX_WAIT_TIME:
                to_flush[post_id] = count
                del _like_buffer[post_id]

    # Flush outside lock
    if to_flush:
        for post_id, count in to_flush.items():
            await db.execute(
                text("UPDATE posts SET likes = COALESCE(likes, 0) + :count WHERE postid = :postid"),
                {"count": count, "postid": post_id}
            )
        await db.commit()
        print(f"[LIKES FLUSHED] {to_flush}")
