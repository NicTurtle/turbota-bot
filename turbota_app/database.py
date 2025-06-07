import aiosqlite

DB_PATH = "tmp/psychologist.db"

async def init_db() -> None:
    """Initialize database and ensure users table exists."""
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
    """Return an aiosqlite connection."""
    conn = await aiosqlite.connect(DB_PATH)
    conn.row_factory = aiosqlite.Row
    return conn
