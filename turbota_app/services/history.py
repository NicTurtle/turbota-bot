from database import get_db
from schemas.history import MessageIn
from typing import List
from schemas.history import MessageOut
import aiosqlite

async def save_message(message: MessageIn) -> None:
    db = await get_db()
    try:
        await db.execute(
            """
            INSERT INTO messages (user_id, text, answer)
            VALUES (?, ?, ?)
            """,
            (message.user_id, message.text, message.answer)
        )
        await db.commit()
    finally:
        await db.close()

async def get_last_messages(user_id: int, limit: int = 5) -> List[MessageOut]:
    db = await get_db()
    try:
        cursor = await db.execute(
            """
            SELECT id, user_id, text, answer, created_at
            FROM messages
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit)
        )
        rows = await cursor.fetchall()
        return [MessageOut(**dict(zip([column[0] for column in cursor.description], row))) for row in rows]
    finally:
        await db.close()
