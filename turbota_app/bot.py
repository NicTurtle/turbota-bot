from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from turbota_app.config import config
from turbota_app.services.gpt import ask_assistant

bot = Bot(token=config.TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def handle_start(message: Message):
    await message.answer("Шо ти, голова?")

@dp.message()
async def handle_message(message: Message):
    response = await ask_assistant(message.from_user.id, message.text)
    await message.answer(response, parse_mode="HTML")

async def start_bot():
    await dp.start_polling(bot)
