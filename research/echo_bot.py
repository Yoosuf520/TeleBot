import asyncio
from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

dp = Dispatcher()


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello! I'm a bot created by Yoosuf.")

@dp.message()
async def echo_handler(message: Message):
    await message.answer(message.text)

# Run the bot
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
          