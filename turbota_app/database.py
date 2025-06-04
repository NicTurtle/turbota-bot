import aiosqlite

async def get_db():
    return await aiosqlite.connect("data/turbota.db")

async def init_db():
    db = await get_db()
    try:
        await db.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            is_premium BOOLEAN DEFAULT 0,
            joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")
        await db.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text TEXT,
            answer TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")
        await db.execute("""CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            paid_at DATETIME,
            status TEXT
        )""")
        await db.execute("""
            CREATE TABLE IF NOT EXISTS context_summary (
                user_id INTEGER PRIMARY KEY,
                summary TEXT,
                biography TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
    finally:
        await db.close()
