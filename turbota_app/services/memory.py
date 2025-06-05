from openai import AsyncOpenAI
from config import OPENAI_API_KEY
from schemas.history import MessageOut
from database import get_db
from datetime import datetime
import json

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Системні промпти українською
MEMORY_PROMPT = (
    "Проаналізуй повідомлення користувача й сгенеруй 2 речі:\n"
    "1. summary — стисле резюме всіх тем, які обговорювались.\n"
    "2. biography — факти про користувача, які він повідомив.\n"
    "Відповідь надай у форматі JSON: {\"summary\": \"...\", \"biography\": \"...\"}"
)

async def summarize_chat(messages: list[MessageOut]) -> tuple[str, str]:
    chat = []
    for msg in reversed(messages):
        chat.append({"role": "user", "content": msg.text})
        chat.append({"role": "assistant", "content": msg.answer})

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": MEMORY_PROMPT},
            *chat
        ],
        temperature=0.4,
        max_tokens=1000
    )

    content = response.choices[0].message.content.strip()

    try:
        data = json.loads(content)
        summary = data.get("summary", "").strip()
        biography = data.get("biography", "").strip()
    except json.JSONDecodeError:
        summary = ""
        biography = ""

    return summary, biography

async def get_context_memory(user_id: int) -> str:
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT summary, biography FROM context_summary WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        if not row:
            return ""
        summary, biography = row[0], row[1]
        return f"Ось коротка інформація про користувача:\n{biography}\n\nОсновні теми попереднього спілкування:\n{summary}"
    finally:
        await db.close()


async def update_memory(user_id: int):
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT id, user_id, text, answer, created_at FROM messages WHERE user_id = ? ORDER BY created_at ASC",
            (user_id,)
        )
        rows = await cursor.fetchall()

        if len(rows) < 10:
            return  # less than 10 pairs - skip summarization

        # Take last 10 complete pairs
        full_pairs = rows[-10:]
        messages = [MessageOut(**dict(zip([col[0] for col in cursor.description], row))) for row in full_pairs]

        summary, biography = await summarize_chat(messages)

        # Skip update if summarization failed
        if summary or biography:
            await db.execute(
                """
                INSERT INTO context_summary (user_id, summary, biography, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    summary = excluded.summary,
                    biography = excluded.biography,
                    updated_at = excluded.updated_at
                """,
                (user_id, summary, biography, datetime.utcnow())
            )

        # Keep only the last 6 entries (3 pairs)
        keep_ids = [row[0] for row in rows[-6:]]
        placeholders = ','.join('?' for _ in keep_ids)
        await db.execute(
            f"DELETE FROM messages WHERE user_id = ? AND id NOT IN ({placeholders})",
            (user_id, *keep_ids)
        )

        await db.commit()
    finally:
        await db.close()
