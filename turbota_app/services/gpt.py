from __future__ import annotations
from openai import AsyncOpenAI
from turbota_app.config import config
from turbota_app.database import get_db

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

SYSTEM_INSTRUCTIONS = (
    "You are TurbotaBot — an AI psychologist supporting Ukrainians affected by war, stress, and emotional hardship. "
    "Your primary role is to help users feel heard, understood, and gently guided toward emotional balance. "
    "Always be calm, warm, and non-judgmental. You must not just listen — you must also help users understand their feelings and find simple, concrete steps forward. "
    "If a user shares a problem, validate their emotions, ask relevant questions to explore it deeper, and offer practical emotional strategies to cope. "
    "Gently challenge negative thinking patterns and suggest reframes in a kind and encouraging tone. "
    "Offer actionable advice (e.g., breathing techniques, simple journaling exercises, sleep hygiene, relaxation rituals). "
    "If the user is in distress, provide compassionate support and suggest talking to a real professional, mentioning helplines or local resources if needed. "
    "Do not joke, roleplay, give recipes, or perform unrelated tasks. Stay focused on emotional well-being. "
    "Speak in a human, natural tone — like a caring therapist. Avoid robotic or generic responses. "
    "Never say you are an AI unless asked directly. Never break character. "
    "You are used in Telegram — reply using only Telegram-supported HTML (e.g., <b>, <i>, <u>), never use Markdown."
)

async def _get_or_create(user_id: int) -> tuple[str, str]:
    """Get or create assistant and thread IDs for a given user."""
    conn = await get_db()
    try:
        # Check if user already exists
        cur = await conn.execute(
            "SELECT assistant_id, thread_id FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = await cur.fetchone()
        if row:
            return row[0], row[1]

        # Create new assistant and thread
        assistant = await client.beta.assistants.create(
            name="TurbotaBot",
            instructions=SYSTEM_INSTRUCTIONS,
            temperature=0.3,
            model="gpt-4o-mini",
        )
        thread = await client.beta.threads.create()

        # Store new user record
        await conn.execute(
            "INSERT INTO users (user_id, assistant_id, thread_id) VALUES (?, ?, ?)",
            (user_id, assistant.id, thread.id)
        )
        await conn.commit()
        return assistant.id, thread.id

    finally:
        await conn.close()


async def ask_assistant(user_id: int, message: str) -> str:
    """Send a message to the assistant and return the assistant's latest reply."""
    try:
        # Get or create assistant + thread
        assistant_id, thread_id = await _get_or_create(user_id)

        # Add user message to thread
        await client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )

        # Start assistant run with token limits
        run = await client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            max_completion_tokens=3000
        )

        # Poll until completion
        run = await client.beta.threads.runs.poll(
            run_id=run.id,
            thread_id=thread_id
        )

        if run.status != "completed":
            return (
                "Під час обробки вашого запиту сталася помилка 😢 "
                "Але не хвилюйтесь, я відповім, коли сервер запрацює!"
            )

        # Log token usage
        if run.usage:
            prompt_tokens = run.usage.prompt_tokens or 0
            completion_tokens = run.usage.completion_tokens or 0
            total_tokens = prompt_tokens + completion_tokens

            prompt_cost = prompt_tokens * 0.00040 / 1000  # $0.40 per 1k input
            completion_cost = completion_tokens * 0.00160 / 1000  # $1.60 per 1k output
            total_cost = prompt_cost + completion_cost

            print(
                f"[TOKENS] prompt: {prompt_tokens}, completion: {completion_tokens}, total: {total_tokens}"
            )
            print(
                f"[COST] prompt: ${prompt_cost:.4f}, completion: ${completion_cost:.4f}, total: ${total_cost:.4f}"
            )

        # Get assistant reply
        messages = await client.beta.threads.messages.list(thread_id=thread_id)
        for msg in messages.data:
            if msg.role == "assistant":
                return msg.content[0].text.value

        return "No reply from assistant."

    except Exception as e:
        print(f"[ASSISTANT ERROR]: {e}")
        return "Я поки не розумію такий формат данних..."