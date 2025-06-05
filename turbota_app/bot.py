from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from config import TELEGRAM_TOKEN, OPENAI_API_KEY
from services.gpt import ask_assistant, test_openai_token

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def handle_start(message: Message):
    status = []
    if TELEGRAM_TOKEN:
        status.append("✅ Telegram Token: set")
    else:
        status.append("❌ Telegram Token: missing")

    if OPENAI_API_KEY:
        result = await test_openai_token()
        status.append(result)
    else:
        status.append("❌ OpenAI API Key: missing")

    msg = "\n".join(["🤖 TurbotaBot is ready:"] + status)
    await message.answer(msg)

@dp.message()
async def handle_message(message: Message):
    response = await ask_assistant(message.from_user.id, message.text)
    await message.answer(response)

async def start_bot():
    await dp.start_polling(bot)
