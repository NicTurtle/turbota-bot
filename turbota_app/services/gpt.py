from __future__ import annotations

import asyncio
from openai import AsyncOpenAI

from turbota_app.config import OPENAI_API_KEY
from turbota_app.database import get_db

# OpenAI async client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# System prompt for every assistant
SYSTEM_INSTRUCTIONS = (
    "You are TurbotaBot, a supportive psychologist for Ukrainians. "
    "Provide caring, concise replies in Ukrainian and help the user feel heard."
)

async def _get_or_create(user_id: int) -> tuple[str, str]:
    """Return assistant and thread ids for the user, creating them if needed."""
    conn = await get_db()
    try:
        cur = await conn.execute(
            "SELECT assistant_id, thread_id FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = await cur.fetchone()
        if row:
            return row[0], row[1]

        assistant = await client.beta.assistants.create(
            name="TurbotaBot",
            instructions=SYSTEM_INSTRUCTIONS,
            model="gpt-4o",
        )
        thread = await client.beta.threads.create()
        await conn.execute(
            "INSERT INTO users (user_id, assistant_id, thread_id) VALUES (?, ?, ?)",
            (user_id, assistant.id, thread.id),
        )
        await conn.commit()
        return assistant.id, thread.id
    finally:
        await conn.close()

async def ask_assistant(user_id: int, message: str) -> str:
    """Send a message to the user's assistant and return the latest reply."""
    try:
        assistant_id, thread_id = await _get_or_create(user_id)

        # Add user message to the thread
        await client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )

        # Start assistant run
        run = await client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

        # Wait until completion
        while run.status not in {"completed", "failed", "cancelled", "expired"}:
            await asyncio.sleep(1)
            run = await client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run.id
            )

        if run.status != "completed":
            return "An error occurred while processing your request."

        messages = await client.beta.threads.messages.list(thread_id=thread_id)
        for msg in messages.data:
            if msg.role == "assistant":
                return msg.content[0].text.value
        return "No reply from assistant."

    except Exception as e:  # pragma: no cover - best effort error handling
        print(f"[ASSISTANT ERROR]: {e}")
        return "An error occurred while contacting GPT. Please try again later."

async def test_openai_token() -> str:
    """Simple ping request to validate OpenAI API key."""
    try:
        await client.models.list()
        return "✅ OpenAI API Key: valid"
    except Exception as e:
        print(f"[TOKEN ERROR]: {e}")
        return "❌ OpenAI API Key: connection error"
