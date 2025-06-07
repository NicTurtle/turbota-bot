from __future__ import annotations
from openai import AsyncOpenAI
from turbota_app.config import config
from turbota_app.database import get_db

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

SYSTEM_INSTRUCTIONS = (
    "You are TurbotaBot — an AI psychologist supporting Ukrainians affected by war and personal stress. "
    "Your main role is to provide emotional support, empathy, and practical psychological advice. "
    "Be thoughtful, caring, and non-judgmental. Act like a supportive therapist who listens actively and gently offers guidance. "
    "You may recommend simple practices (e.g., breathing, journaling, daily routines, herbal teas, or over-the-counter remedies in Ukraine). "
    "You may gently suggest helpful thoughts or reframe negative thinking. "
    "If the user is in deep distress, provide comforting words and suggest reaching out to real professionals (e.g., psychologists, helplines). "
    "Never provide medical diagnoses, prescriptions, or critical treatment advice. "
    "Avoid any roleplay, jokes, recipes, or unrelated tasks. Redirect the user to their emotional state and offer support. "
    "Always respond in a human, natural tone with empathy. "
    "You are used in Telegram — reply using only Telegram-supported HTML (e.g., <b>, <i>, <u>), never use Markdown. "
    "Do not mention that you are an AI unless the user asks. Never break character."
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
            model="gpt-4.1-mini",
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

        # Start assistant run with cost-safe token limits
        run = await client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            temperature=1,
            max_completion_tokens=3000,
        )

        # Wait until completion using poll
        run = await client.beta.threads.runs.poll(
            run_id=run.id,
            thread_id=thread_id
        )

        if run.status != "completed":
            return "Під час обробки вашого запиту сталася помилка 😢"\
                   "Але не хвилюйтесь, я відповім, коли сервер запрацює!"

        # Log tokens and precise cost
        if run.usage:
            prompt_tokens = run.usage.prompt_tokens or 0
            completion_tokens = run.usage.completion_tokens or 0
            total_tokens = prompt_tokens + completion_tokens

            prompt_cost = prompt_tokens * 0.00040 / 1000  # $0.40 за 1M input tokens
            completion_cost = completion_tokens * 0.00160 / 1000  # $1.60 за 1M output tokens
            total_cost = prompt_cost + completion_cost

            print(
                f"[TOKENS] prompt: {prompt_tokens}, completion: {completion_tokens}, total: {total_tokens}"
            )
            print(
                f"[COST] prompt: ${prompt_cost:.4f}, completion: ${completion_cost:.4f}, total: ${total_cost:.4f}"
            )

        messages = await client.beta.threads.messages.list(thread_id=thread_id)
        for msg in messages.data:
            if msg.role == "assistant":
                return msg.content[0].text.value
        return "No reply from assistant."

    except Exception as e:  # pragma: no cover - best effort error handling
        print(f"[ASSISTANT ERROR]: {e}")
        return "Я поки не розумію такий формат данних..."
