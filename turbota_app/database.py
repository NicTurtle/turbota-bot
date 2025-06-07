import os
import aiosqlite

DB_PATH = os.getenv("PSYCHO_DB", "/tmp/psychologist.db")  # ✅ теперь контролируемо

async def init_db() -> None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # ✅ создаст /tmp если надо
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                assistant_id TEXT,
                thread_id TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await db.commit()

async def get_db() -> aiosqlite.Connection:
    conn = await aiosqlite.connect(DB_PATH)
    conn.row_factory = aiosqlite.Row
#todo remove
    print(f"[DB INIT] using {DB_PATH}")

    return conn
