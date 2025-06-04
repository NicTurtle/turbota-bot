from openai import AsyncOpenAI
from schemas.history import MessageOut
from config import OPENAI_API_KEY
from services.memory import get_context_memory
import json

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "Ти — емпатичний психолог на імʼя TurbotaBot. "
    "Твоя мета — підтримувати українців у важкі часи. "
    "Відповідай тепло, коротко і по суті."
)

async def ask_gpt(prompt: str, history: list[MessageOut], user_id: int) -> str:
    # 1. Системне повідомлення + контекст памʼяті
    context_memory = await get_context_memory(user_id)
    system_prompt = SYSTEM_PROMPT
    if context_memory.strip():
        system_prompt += "\n\n" + context_memory.strip()

    messages = [{"role": "system", "content": system_prompt}]

    # 2. Додаємо історію повідомлень
    for msg in reversed(history):
        messages.append({"role": "user", "content": msg.text})
        messages.append({"role": "assistant", "content": msg.answer})

    # 3. Поточне повідомлення користувача
    messages.append({"role": "user", "content": prompt})

    # 4. Виклик OpenAI
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
        max_tokens=100
    )

    print(f"[TOKENS] prompt: {response.usage.prompt_tokens}, completion: {response.usage.completion_tokens}")
    return response.choices[0].message.content.strip()
