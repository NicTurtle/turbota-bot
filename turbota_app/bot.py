from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart

from config import TELEGRAM_TOKEN
from services.gpt import ask_gpt
from services.history import get_last_messages, save_message
from services.memory import update_memory, get_context_memory
from schemas.history import MessageIn

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(
        "Привіт! Я TurbotaBot 🤖\n"
        "Я тут, щоб підтримати тебе. Напиши що-небудь — і я постараюся допомогти ❤️"
    )

@dp.message(lambda m: m.text)
async def handle_message(message: Message):
    user_id = message.from_user.id
    user_input = message.text

    # 1. Load conversation history
    history = await get_last_messages(user_id=user_id, limit=50)

    # 2. Get GPT response
    gpt_answer = await ask_gpt(user_input, history, user_id)

    # 3. Save the pair
    await save_message(MessageIn(
        user_id=user_id,
        text=user_input,
        answer=gpt_answer
    ))

    # 4. Update memory when we have at least 10 pairs
    if len(history) + 1 >= 10:
        await update_memory(user_id)

    # 5. Send reply
    await message.answer(gpt_answer)

    # DEBUG: show stored memory
    memory_text = await get_context_memory(user_id)
    print(f"\n===== [DEBUG for {user_id}] =====")
    print(f"[HISTORY LEN] {len(history)}")
    print(f"[CONTEXT MEMORY]\n{memory_text}\n")


async def start_bot():
    await dp.start_polling(bot)

